import fitz
import numpy as np
import gradio as gr
import google.generativeai as genai
import PyPDF2
import anki
from anki.exporting import AnkiPackageExporter

filepath = ""
magasin = None
GOOGLE_API_KEY = ""
model = None

# ====================================================== #

# 標題判斷
# https://blog.csdn.net/star1210644725/article/details/136318768
def Titles(filepath):
    doc = fitz.open(filepath)
    titles = []
 
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        # extract font sizes
        page_number = page_num + 1
        page_titles = []
        sizes = []
        for block in blocks:
            try:
                for line in block["lines"]:
                    for span in line["spans"]:
                        sizes.append(span["size"])
            except KeyError:
                continue

        # find median
        sizes_arr = np.array(sizes)
        med = np.median(sizes_arr)

        # find titles
        for block in blocks:
            text_parts = []
            size = 0
            try:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_parts.append(span["text"])
                        size = span["size"]
            except KeyError:
                continue

            text = "".join(text_parts)
            # 如果這行的字體大小比中位數大，便可以猜測這行是標題
            # （預期文字塊的字體大小為中位數）
            if size > med and not is_body_text(text) and not is_image(text) and not is_formula(text):
                page_titles.append((text.strip(), page_number))
        titles += page_titles
 
    return titles
 
def is_body_text(text):
    return len(text) > 100 or text.endswith(".") or text.endswith("?") or text.endswith("!")
 
def is_image(text):
    return text.startswith("Image:") or text.startswith("Figure:")
 
def is_formula(text):
    return text.startswith("Formula:") or text.startswith("Equation:")

# gemini再次確認是否為標題
def reCheck(text):
    input = f"""please ignore the "Title" part, check whether "{text}" is a topic, and answer "yes" or "no" only
    """
    reply = model.generate_content(
    input,
    generation_config=genai.types.GenerationConfig(temperature=0)
    )
    if "yes" in reply:
        return True
    elif "no" in reply:
        return False
    return "Error"

# ====================================================== #

# 取得文字塊

def Chunk():

# gemini出題

# anki: csv轉anki
# https://superuser.com/questions/698902/can-i-create-an-anki-deck-from-a-csv-file


# ====================================================== #

# gradio: upload files
# https://blog.csdn.net/qq_51116518/article/details/132628392

def main():
    with gr.Blocks() as demo:
        with gr.Column():

    demo.launch(debug=True)

if __name__=='__main__':
    main()