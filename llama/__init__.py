from os import getenv
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
    "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q5_K_M.gguf",
    "models/mistral-7b.gguf",
)

llm = Llama(
    "./models/mistral-7b.gguf", n_gpu_layers=50, n_threads=int(getenv("N_THREADS", 4))
)
print("LOADED")
