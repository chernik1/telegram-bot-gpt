import aspose.slides as slides
import re

# Load presentation
pres = slides.Presentation(r"G:\telegram-bot-gpt\tools\ppt_form\ЛК-2  Ч-1 ИЗМЕР. ТЕОРИЯ.ptx.pptx")

# Convert PPTX to PDF
pres.save("pptx-to-pdf.pdf", slides.export.SaveFormat.PDF)