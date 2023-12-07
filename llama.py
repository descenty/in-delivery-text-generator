from json import dumps, loads
from llama_cpp.llama_grammar import LlamaGrammar
from llama_cpp.llama import Llama
import httpx

grammar_text = httpx.get(
    "https://raw.githubusercontent.com/ggerganov/llama.cpp/master/grammars/json_arr.gbnf"
).text
grammar = LlamaGrammar.from_string(grammar_text)

llm = Llama("./mistral-path")

response = llm(
    'JSON list of 5 subcategories for category "milk" (json schema: {"slug": string, "title": string}, e.g. {"slug": "fruits-vegetables", "title": "Fruits and Vegetables"}): ',
    grammar=grammar,
    max_tokens=-1,
)

print(dumps(loads(response["choices"][0]["text"]), indent=4))
