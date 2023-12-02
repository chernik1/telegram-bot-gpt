import aspose.words as aw
import re

doc = aw.Document(r"G:\telegram-bot-gpt\tools\docx_form\Input.docx")
doc.save("Output.pdf")