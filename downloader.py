import os
import requests
from tqdm import tqdm
from os.path import isfile


def download_file(url: str, filename: str, chunk_size=1024):
    if isfile(filename):
        print(f"File {filename} already exists. Skipping download.")
        return
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    with open(filename, "wb") as file, tqdm(
        desc=filename,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)
