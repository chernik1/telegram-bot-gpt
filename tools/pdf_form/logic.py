from reader import reader

def is_form_new_pdf(path: str, promt: str) -> bool:

    text_pdf = reader(path)

    promt_for_ai = text_pdf