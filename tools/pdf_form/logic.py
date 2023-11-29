from reader import reader

def is_form_new_pdf(path: str, promt: str) -> bool:

    text_pdf = reader(path)

    promt_for_ai = text_pdf
    print(promt_for_ai)

is_form_new_pdf(r'G:\telegram-bot-gpt\tools\pdf_form\6_биосфера_высший_уровень_орг_ции_жизни_Жильцова.pdf', 1)