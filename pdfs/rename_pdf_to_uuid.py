#!/usr/bin/env python3

from pathlib import Path
import uuid

def change_pdf_name_to_UUID(directory:str=".",recursive:bool=False):
    path = Path(directory)
    if not path.is_dir():
        raise NotADirectoryError(directory)
    exts = {".pdf"}
    if not recursive:
        for p in path.iterdir():
            if p.is_file() and p.suffix.lower() in exts:
                ext = p.suffix
                new_name = str(uuid.uuid4()).replace("-","") + ext
                p.rename(new_name)
    else:
        for p in path.rgob("*"):
            if p.is_file() and p.suffix.lower() in exts:
                ext = p.suffix
                new_name = str(uuid.uuid4()).replace("-","") + ext
                p.rename(new_name)

def main():
    change_pdf_name_to_UUID()

if __name__ == "__main__":
    main()

