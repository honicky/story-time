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
one or more drawings or paintings
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

Use only about 3 sentences for each character.
"""


def generate_detailed_setting_prompt():
    return """Ok, now from each of the sub-settings in your description,
construct a single sentence image prompt for an image generating model.

Place each setting inside of <setting></setting> tags.

Also create a sinlge sentence image prompt for the overall setting
and put it in between <cover-setting></cover-setting> tags."""


def generate_character_image_prompt():
    return """Ok, now take each of these characters you have generated above, and create a concise
visual description that I can use to do one or more drawings or paintings.  Make sure
to include visual details such as the color of the character's hair, eyes, skin, as well
as details about the character's clothing and any accessories they may have, including style.

It is very important that you place each character description inside of <character-description></character-description> tags
so that I can extract the visual description from the text.

Also, it is important that the description is concise and does not contain any extra text.  Use key words
instead of full sentences.  You should use 15 words.
"""



def generate_story_skeleton_prompt(story):
    subsettings_str = generate_subsettings_str(story)
    characters_str = generate_characters_str(story)

    return f"""
Here is the setting of the story:
{story['setting']['setting_text']}

Here are the characters of the story:
{characters_str}

This story is a {story['outline']['StoryStructure']['type']} story
with a {story['outline']['Tone']['type']} tone. 

A {story['outline']['StoryStructure']['type']} type story can be described as
{story['outline']['StoryStructure']['description']}. Please take inspiration from
stories like {story['outline']['StoryStructure']['example']}.

The setting on the cover image of the story is:
{story['setting']['cover_setting']}

Here is a list of the sub-settings of the story:
{subsettings_str}

Using these this information as inspiration, write a story skeleton in which the characters
take actions in each sub-setting.  The skeleton should indicate using what happens in the
story using one sentence per scene.  The skeleton should read like a very short story.

For each sub-setting, write a sentence that describes what happens in a scene in the story in that sub-setting,
and who is in the scene.  Each scene should be proceeded by a number indicating the subsetting of the scene.
For example

1. The foobar went to the closet to get a broom, but the broom was not there, and it wondered where it could be.
2. The foobar and the baz checked in the kitchen, bit was not there either.

Do not provide any other structure to the story skeleton, besides the numbered list. 
"""


def generate_characters_str(story):
    return generate_numbered_list_str(story["characters"]["descriptions"])

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

def generate_scene_image_prompt(story):
    subsettings_prompts = generate_subsettings_str(story)
    characters_prompt_str = generate_numbered_list_str(story["characters"]["prompts"])
    scene_descriptions = generate_scene_descriptions(story)

    return f"""Here are the setting image promtps for the story:
{subsettings_prompts}

Here are the characters image prompts for the story:
{characters_prompt_str}

Here are the scene descriptions:
{scene_descriptions}

For each of these scene descriptions, generate a prompt I can use to generate an image for the scene.
The prompt should be a single sentence that describes the scene. Use combine the text of the charater prompts
and with the setting prompts and scene descriptions to create a single sentence prompt for each scene.

It is important that the description is concise and does not contain any extra text.  Use key words
instead of full sentences.  You should use around 30 words.  The prompt focus on the main visual elements
of the scene, and add detail for each character in the scene across all of the prompts.
"""

def generate_scene_descriptions(story):
    return "\n".join(
        f"""{i+1}. {scene}"""
        for i, scene in enumerate(story["scenes"])
    )