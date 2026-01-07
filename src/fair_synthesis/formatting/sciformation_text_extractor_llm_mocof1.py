import json
from pathlib import Path
from openai import OpenAI
from jsonschema import validate, ValidationError

from .sciformation_text_extractor_mocof1 import fix_inchi_code_for_do, use_more_detailed_reagent_roles

# Load schema from file
schema_path = Path(__file__).parent / "sciformation_text_extractor_llm_mocof1_experiment_diff.schema.json"
with open(schema_path, "r", encoding="utf-8") as f:
    experiment_diff_schema = json.load(f)


def extract_experiment_diff(realization_text: str):
    """
    Send realization text to the OpenAI model and get a JSON diff
    following the ExperimentDiff schema. The result is validated
    against the schema before returning.
    """
    # Initialize client (requires OPENAI_API_KEY in env)
    client = OpenAI()

    # Read further instructions from llm_instructions.txt
    instructions_path = Path(__file__).parent / "llm_instructions.txt"
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = f.read()

    messages_content = "You are given the realization text of an experiment. Extract structured information from it according to the ExperimentDiff schema. Only include properties that apply. Further instructions:\n"+ instructions

    # print("sending experiment to LLM: ", current_experiment)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",   # or gpt-4.1
        messages=[
            {
                "role": "system",
                "content": messages_content
            },
            {
                "role": "user",
                "content": realization_text
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ExperimentDiff",
                "schema": experiment_diff_schema
            }
        }
    )

    diff = response.choices[0].message.content
    print("received diff: ", diff)
    diff_as_object = json.loads(diff)

    # Validate against schema
    try:
        validate(instance=diff_as_object, schema=experiment_diff_schema)
    except ValidationError as e:
        print("Model returned invalid diff: ", e.message)

    return diff_as_object


def apply_diff(item: dict, diff: dict) -> dict:
    """
    Recursively apply the diff dictionary onto the original item dictionary.
    Dicts are merged key by key.
    Lists are merged element by element (assuming identical order).
    Modifies item in place.
    """

    def merge(target, patch):
        for k, v in patch.items():
            if isinstance(v, dict) and isinstance(target.get(k), dict):
                # merge nested dicts
                merge(target[k], v)

            elif isinstance(v, list) and isinstance(target.get(k), list):
                # merge lists element by element
                target_list = target[k]
                for i, patch_item in enumerate(v):
                    if i < len(target_list):
                        if isinstance(patch_item, dict) and isinstance(target_list[i], dict):
                            merge(target_list[i], patch_item)
                        else:
                            target_list[i] = patch_item
                    else:
                        # append new items if diff has more
                        target_list.append(patch_item)

            else:
                # replace scalars or new keys
                target[k] = v
        return target

    return merge(item, diff)


def process_realization_text(data: list):
    max_process_count = 100000 # put a low value here only for testing purposes
    i = 0
    """Loop through experiment array and apply diffs."""
    for item in data:
        i += 1
        if i > max_process_count:
            print(f"Reached max process count of {max_process_count}, stopping.")
            break
        if "realizationText" in item and isinstance(item["realizationText"], str):
            try:
                print("Processing experiment with index ", i)
                diff = extract_experiment_diff(item["realizationText"])
                apply_diff(item, diff)
            except Exception as e:
                print(f"Error processing item. Cause: {e}")



def process_data_use_case_specific(data):
    fix_inchi_code_for_do(data)
    use_more_detailed_reagent_roles(data)
    return process_realization_text(data)
