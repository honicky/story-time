def setting_prompt(
    setting_type,
    setting_description,
    setting_example,
    tone_type,
    tone_description,
    tone_example,
    specific_setting_type=None,
    specific_setting_description=None,
):
    prompt = f"""
Describe a detailed setting for a children's story that takes place in a {setting_type}.
Consider the following description as inspiration:
{setting_description}.
For example, '{setting_example}'.

The setting should be appropriate for a {tone_type} tone. 
Consider the following description as inspiration:
{tone_description}.
For example, '{tone_example}'.
"""

    #     if cultural_setting is not None:
    #         prompt += f"""
    # Also, infuse elements of {cultural_setting['type']} into the setting.
    # Consider aspects such as {cultural_setting['description']}.
    # """

    if specific_setting_type is not None:
        prompt += f"""
To be more specific, think of places like a {specific_setting_type}.
For example, you can include elements like {specific_setting_description}.
"""

    prompt += """
Please provide a detailed visual description of this setting that I can use to do
one or more drawings or paintings. This description should be about one paragraph long.
"""

    return prompt


def generate_character_prompt_for_gpt(
    character_type, character_description, character_example
):
    return f"""Ok, now help me create an engaging {character_type} character for the story
A character of this type can be described as {character_description}
An example of this type of character is {character_example}

Generate a name for this character:

Describe the personality of this character:

Provide a detailed visual description of this character suitable for an image model.
Include the color of the character's hair, eyes, skin, and any other relevant details.
Describe the character's clothing and any accessories they may have, including style, and color of each item.

Consider the setting of the story when describing each character.

Use only about 3 sentences to describe the character.
"""


def generate_setting_prompt_for_sdxl(setting_description):
    return f"""Use the following setting description to create an image prompt for a text-to-image model:

{setting_description}

The output should be about ten words that captures the most important visual elements of the setting, including
objects, colors, textures and mood.  Do not include description of characters in the setting.
"""

def generate_character_prompt_for_sdxl(character_description):
    return f"""Use the following character description to create an image prompt for a text-to-image model:

{character_description}

The output should be about ten words that captures the most important visual elements of the character, including species if not human,
gender, skin, hair, eyes, clothing, accessories, stature.  Make sure to include gender and species.  Really include species if not human,
and gender or an innocent puppy will die. 
Do not include description of the setting.
"""


def generate_story_prompt(story):

    return f"""
Here is the setting of the story:
{story['setting']['setting_text']}

Here is the main character for the story:
{story['character']['description']}

This story is a {story['outline']['StoryStructure']['type']} story
with a {story['outline']['Tone']['type']} tone. 

A {story['outline']['StoryStructure']['type']} type story can be described as
{story['outline']['StoryStructure']['description']}. Please take inspiration from
stories like {story['outline']['StoryStructure']['example']}.

The setting for the story is:
{story['setting']['setting_text']}

Please generate a story based on this information. The story should be about
5-10 paragraphs long.  Each paragraph should only be 1-2 simple sentences,
appropriate for a 3 year old child to follow easily.
"""

def generate_paragraph_image_prompt(setting_text, character_description, story_paragraph_text):
    return f"""
    Generate an image prompt for a text-to-image model based on the following information:

    Setting: {setting_text}

    Main Character: {character_description}

    Action paragraph: {story_paragraph_text}

    The output should only describe what the main character is doing in the action paragraph. It should be about 10 words long.
    Always included exactly the following details about the main character:
    1. Species (if not human)
    2. Gender (if human)
    Do not include anyextra detail about the setting or character except for what is explicitly mentioned
    in the Action paragraph.
    """


def generate_numbered_list_str(items):
    return "\n".join(
        f"""{i+1}. {item}"""
        for i, item in enumerate(items)
    )

def generate_subsettings_str(story):
    return generate_numbered_list_str(story["setting"]["setting_prompts"])


def parse_story_skeleton_prompt():
    return """Ok, now take the story skeleton you have generated above, and parse out the components
from the scene.

For each scene, render XML that contains the following tags:
<scene></scene> - this tag should wrap the entire scene
<setting-id></setting-id> - this tag should contain the id of the setting of the scene
<setting-name></setting-name> - this tag should contain the name of the setting of the scene
<setting-description></setting-description> - this tag should contain the description of the setting
<character-ids></character-ids> - this tag should contain a comma separated list of the ids of the characters in the scene 
<other-people></other-people> - this tag should contain a description of the other people in the scene
<text></text> - scene text

Be sure to use XML as described above, and to wrap each scene in <scene></scene> tags.
"""
