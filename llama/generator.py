from json import loads
from schemas import ModelGenerationPrompt
from llama import llm, json_grammar


def generate_json_response(generation_prompt: ModelGenerationPrompt):
    model_schema = generation_prompt.object_type.model_json_schema()["properties"]
    json_schema = {
        object_field: model_schema[object_field]["type"]
        for object_field in model_schema
    }
    prompt = f"JSON schema: {json_schema}\n"

    prompt += f"Example object: {generation_prompt.example.model_dump()}\n"
    prompt += "Generate a JSON "
    prompt += (
        f"list of {generation_prompt.count} " if generation_prompt.count > 1 else "of "
    )
    prompt += f"{generation_prompt.object_description}:"

    response = llm(
        prompt,
        grammar=json_grammar,
        max_tokens=-1,
    )

    return loads(response["choices"][0]["text"])
