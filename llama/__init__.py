from llama_cpp.llama_grammar import LlamaGrammar
from llama_cpp.llama import Llama
import httpx

from downloader import download_file

json_grammar = LlamaGrammar.from_string(
    httpx.get(
        "https://raw.githubusercontent.com/ggerganov/llama.cpp/master/grammars/json_arr.gbnf"
    ).text
)

download_file(
    "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q5_K_M.gguf",
    "models/mistral-7b.gguf",
)

llm = Llama("./models/mistral-7b.gguf")
print("LOADED")
