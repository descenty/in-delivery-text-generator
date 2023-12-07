from llama_cpp.llama_grammar import LlamaGrammar
from llama_cpp.llama import Llama
import httpx

json_grammar = LlamaGrammar.from_string(
    httpx.get(
        "https://raw.githubusercontent.com/ggerganov/llama.cpp/master/grammars/json_arr.gbnf"
    ).text
)

llm = Llama("./models/mistral-7b-instruct-v0.1.Q6_K.gguf")
