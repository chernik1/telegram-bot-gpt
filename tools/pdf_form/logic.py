from .reader import reader
import re
import os

def is_form_new_pdf(path: str, promt: str) -> list:
    full_path = os.path.abspath(path)
    text_pdf = reader(full_path)

    promt_for_ai = text_pdf.strip()

    if len(promt_for_ai) > 3000:
        split_3000_symbols = [promt_for_ai[i:i+3000] for i in range(0, len(promt_for_ai), 3000)]
        return split_3000_symbols

    return [promt_for_ai]

