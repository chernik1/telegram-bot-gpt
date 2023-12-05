import aspose.words as aw
import re

def is_form_new_docx(path: str, promt: str):

    doc = aw.Document(fr'{path}')
    doc.save("Output.pdf")