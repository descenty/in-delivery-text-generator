from json import loads
from re import match
from schemas import ModelGenerationPrompt
from llama import llm, json_grammar


def generate_json_response(generation_prompt: ModelGenerationPrompt):
    model_schema = generation_prompt.object_type.model_json_schema()["properties"]
    json_schema = {
        object_field: model_schema[object_field]["type"]
        for object_field in model_schema
    }
    prompt = (
        f"JSON schema for generation (generate only with this schema): {json_schema}\n"
    )
    prompt += f"Example of object: {generation_prompt.example.model_dump()}\n"
    if generation_prompt.additional_prompt:
        prompt += f"Additional information: {generation_prompt.additional_prompt}\n"
    prompt += f"Generate a JSON list of {generation_prompt.count} {generation_prompt.object_description}"
    print(prompt)

    while True:
        try:
            response = llm(
                prompt, grammar=json_grammar, max_tokens=-1, stop=["]\n"], stream=True
            )
            result = ""

            count = 0
            for output in response:
                result += output["choices"][0]["text"]
                print(result)
                if count % 15 == 0:
                    # if it's just generating array of numbers or empty space
                    if any(
                        match(regexp, result)
                        for regexp in [r"\[\n\s*-*\d.+", r"\n\n\n\n\n"]
                    ):
                        raise
                    count = 0
                count += 1

            json_response: list[dict] = loads(result)
            [
                generation_prompt.object_type.model_validate(dict_object)
                for dict_object in json_response
            ]
            if len(json_response) != generation_prompt.count:
                print("Wrong count, retrying")
                continue
            break
        except Exception:
            print("Failed to generate JSON, retrying")
    return json_response
