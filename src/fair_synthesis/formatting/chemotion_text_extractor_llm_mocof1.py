import json
from pathlib import Path

from jsonschema import ValidationError, validate
from openai import OpenAI


schema_path = Path(__file__).parent / \
    "chemotion_text_extractor_llm_mocof1_experiment_diff.schema.json"
with open(schema_path, "r", encoding="utf-8") as f:
    experiment_diff_schema = json.load(f)


def extract_experiment_diff(
        plain_text_description: str | None,
        plain_text_observation: str | None) -> dict:
    client = OpenAI()

    instructions_path = Path(__file__).parent / \
        "chemotion_text_extractor_llm_mocof1_instructions.txt"
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = f.read()

    messages_content = (
        "Extract structured information from Chemotion free text fields. "
        "Return only JSON following the ChemotionExperimentDiff schema.\n\n"
        + instructions
    )

    user_content = json.dumps({
        "plain_text_description": plain_text_description or "",
        "plain_text_observation": plain_text_observation or "",
    })

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": messages_content},
            {"role": "user", "content": user_content},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ChemotionExperimentDiff",
                "schema": experiment_diff_schema,
            },
        },
    )

    diff = response.choices[0].message.content
    print("received Chemotion diff: ", diff)
    diff_as_object = json.loads(diff)

    try:
        validate(instance=diff_as_object, schema=experiment_diff_schema)
    except ValidationError as e:
        print("Model returned invalid Chemotion diff: ", e.message)

    return diff_as_object


def apply_diff(item: dict, diff: dict) -> dict:
    for key, value in diff.items():
        if value is None:
            continue
        if isinstance(value, list) and not value:
            continue
        item[key] = value
    return item


def process_free_text_fields(data: list[dict]) -> None:
    for i, item in enumerate(data, start=1):
        try:
            print("Processing Chemotion experiment with index ", i)
            diff = extract_experiment_diff(
                item.get("plain_text_description"),
                item.get("plain_text_observation"),
            )
            apply_diff(item, diff)
        except Exception as e:
            print(f"Error processing Chemotion item. Cause: {e}")


def process_data_use_case_specific(data: list[dict]) -> None:
    process_free_text_fields(data)
