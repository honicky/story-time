from dotenv import load_dotenv
import os
import json
import random

load_dotenv()

from story_config import story_config
from lib.util import current_time_ms
from lib import image_prompt
from lib import llm_prompt
from lib import object_store_client
from lib import mongo_client
import prompt_templates

import wandb
from wandb.sdk.data_types.trace_tree import Trace

run = wandb.init(project="story-time")

root_span = Trace(
    name="StoryGenAgent",
    kind="agent",
    start_time_ms=current_time_ms(),
    metadata={"version": "0.3"},
)


def generate_story_outline():
    start_time = current_time_ms()
    story_outline = {
        "StoryStructure": random.choice(story_config["StoryStructure"]),
        "Setting": random.choice(story_config["Setting"]),
        "Character": random.choice(story_config["Characters"]),
        "Style": random.choice(story_config["Style"]),
        "Tone": random.choice(story_config['Tone']),
        "CulturalSetting": "None",
        "EverydayPublicPlace": "None",
    }

    if story_outline["Setting"]["type"] == "Everyday Public Place":
        story_outline["EverydayPublicPlace"] = random.choice(story_config["EverydayPublicPlaces"])

    end_time = current_time_ms()
    story_outline_span = Trace(
        name="GenerateStoryOutline",
        kind="tool",
        status_code="success",
        outputs=story_outline,
        start_time_ms=start_time,
        end_time_ms=end_time,
    )
    root_span.add_child(story_outline_span)
    root_span.add_inputs_and_outputs(inputs={}, outputs=story_outline)
    root_span._span.end_time_ms = end_time

    return story_outline


def generate_setting_prompt(story_outline):
    selected_setting = story_outline["Setting"]
    specific_setting = story_outline["EverydayPublicPlace"]

    return prompt_templates.setting_prompt(
        selected_setting["type"],
        selected_setting["description"],
        selected_setting["example"],
        story_outline["Tone"]["type"],
        story_outline["Tone"]["description"],
        story_outline["Tone"]["example"],
        specific_setting["type"] if specific_setting != "None" else None,
        specific_setting["example"] if specific_setting != "None" else None,
    )


def extract_paragraphs_from_story(story_text):
    start_time = current_time_ms()

    paragraphs = [
        paragraph.strip()
        for paragraph in story_text.split("\n")
        if paragraph.strip() != ""
    ]

    paragraph_extractor_span = Trace(
        name="ExtractParagraphsFromStory",
        kind="tool",
        status_code="success",
        outputs={"paragraphs": paragraphs},
        start_time_ms=start_time,
        end_time_ms=current_time_ms(),
    )
    root_span.add_child(paragraph_extractor_span)
    root_span.add_inputs_and_outputs(
        inputs={"story_text": story_text}, outputs={"paragraphs": paragraphs}
    )
    root_span._span.end_time_ms = paragraph_extractor_span._span.end_time_ms
    return paragraphs


def store_story_in_s3(story_descriptor, run_name):
    bucket_id = "botos-generated-images"
    user_id = "dev-test-user"
    story_descriptor_key = f"{user_id}/story_prompt_v2/{run_name}.json"
    client = object_store_client.Boto3Client()
    client.upload_object(story_descriptor, bucket_id, story_descriptor_key)
    return story_descriptor_key


def store_story_in_mongo(story_descriptor):
    mongo = mongo_client.StoryMongoDB()
    story_id = None
    try:
        story_id = mongo.insert_story(story_descriptor)
    finally:
        mongo.close_connection()
    return story_id


try:
    openai_api_token = os.environ.get("OPENAI_API_TOKEN")
    image_client = image_prompt.DalleClient(openai_api_token)

    def generate_image(prompt):
        print(f"Generating image for prompt: {prompt} ...", end="", flush=True)
        start_time = current_time_ms()
        try:
            image_urls = image_client.generate_image(prompt)
            status = "success"
            print("Done")
            print(f"Image: {image_urls}")
        except Exception as e:
            print(f"Error generating image: {e}")
            status = "error"
            image_urls = []

        generate_image_span = Trace(
            name="GenerateImage",
            kind="tool",
            status_code=status,
            inputs={"prompt": prompt},
            outputs={"url": image_urls},
            start_time_ms=start_time,
            end_time_ms=current_time_ms(),
        )
        root_span.add_child(generate_image_span)
        root_span.add_inputs_and_outputs(
            inputs={"prompt": prompt}, outputs={"image_urls": image_urls}
        )
        root_span._span.end_time_ms = generate_image_span._span.end_time_ms

        return image_urls

    # Generate the story outline
    story_outline = generate_story_outline()
    story = {"outline": story_outline}

    # Generate the setting prompt based on the outline
    setting_prompt = generate_setting_prompt(story_outline)

    print("Generating story setting... ", end="", flush=True)

    llm = llm_prompt.GTP4LLM(openai_api_token)

    story_setting = llm.generate_text(setting_prompt, root_span)
    story["setting"] = {"setting_text": story_setting}
    print("Done")

    character_prompt_str = prompt_templates.generate_character_prompt_for_gpt(
        story_outline["Character"]["type"],
        story_outline["Character"]["description"],
        story_outline["Character"]["example"],
    )

    print("Generating the main character... ", end="", flush=True)
    character_description = llm.generate_text(character_prompt_str, root_span)
    print("Done")

    story["character"] = {"description": character_description}

    story_prompt = prompt_templates.generate_story_prompt(story)

    llm.reset_history()
    print("Generating the story... ", end="", flush=True)
    story["story_text"] = llm.generate_text(story_prompt, root_span)
    print("Done")

    llm.reset_history()
    print("Generating the setting image prompt... ", end="", flush=True)
    story["setting"]["image_prompt"] = llm.generate_text(
        prompt_templates.generate_setting_image_prompt(story["setting"]["setting_text"]),
        root_span,
        model_name="gpt-4o-mini",
    )
    print("Done")

    llm.reset_history()
    print("Generating the character image prompt... ", end="", flush=True)
    story["character"]["image_prompt"] = llm.generate_text(
        prompt_templates.generate_character_image_prompt(story["character"]["description"]),
        root_span,
        model_name="gpt-4o-mini",
    )
    print("Done")

    paragraphs = extract_paragraphs_from_story(story["story_text"])

    paragraph_image_prompts = [
        llm.generate_text(
            prompt_templates.generate_paragraph_image_prompt(
                story["setting"]["setting_text"],
                story["character"]["description"],
                paragraph,
            ),
            root_span,
        ) if llm.reset_history() is None else ""
        for paragraph in paragraphs
    ]

    image_prompts = [
        f"{paragraph_image_prompt}, {story['character']['image_prompt']}, {story['setting']['image_prompt']}, "
        f"children's book illustration style"
        for paragraph_image_prompt in paragraph_image_prompts
    ]

    story["pages"] = [
        {
            "paragraph": [paragraph],
            "paragraph_image_prompt": [paragraph_image_prompt],
            "image_prompt": [image_prompt_str],
            "image_urls": generate_image(image_prompt_str),
        }
        for paragraph, paragraph_image_prompt, image_prompt_str in zip(
            paragraphs, paragraph_image_prompts, image_prompts
        )
    ]

    story["run_name"] = run.name
    story["version"] = "v3.0.0"
    story_id = store_story_in_mongo(story)

    print(f"Story id: {story_id}")

finally:
    root_span._span.end_time_ms = current_time_ms()
    root_span.log(name="story-time")
