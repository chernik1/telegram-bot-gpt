import aspose.slides as slides
import re

def is_form_new_ppt(path: str, promt: str) -> list:

    # Load presentation
    pres = slides.Presentation(fr'{path}')

    # Convert PPTX to PDF
    pres.save("pptx-to-pdf.pdf", slides.export.SaveFormat.PDF)