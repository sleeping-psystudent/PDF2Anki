import fitz
import google.generativeai as genai
import numpy as np

# 內容萃取＋標題判斷
# https://blog.csdn.net/star1210644725/article/details/136318768
def extractContents(filepath):
    doc = fitz.open(filepath)
    topics = []
    re_contents = []
 
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        page_contents = []

        # extract font sizes
        page_number = page_num + 1
        sizes = []
        for block in blocks:
            text_parts = []
            size = 0
            try:
                for line in block["lines"]:
                    for span in line["spans"]:
                         sizes.append(span["size"])
                         text_parts.append(span["text"])
                         size = span["size"]
            except KeyError:
                continue
            text = "".join(text_parts)
            page_contents.append({
                "text": text,
                "size": size,
                "pnum": page_number
            })

        # find median
        sizes_arr = np.array(sizes)
        med = np.median(sizes_arr)

        # topic filter
        for content in page_contents:
            text = content["text"]
            # 找出大小大於中位數的字體、過濾掉可能是文字塊、圖片、公式的語料
            if content["size"] > med and not is_body_text(text) and not is_image(text) and not is_formula(text):
                topics.append(content)
                re_contents.append(content)
            # 找出大小大於等於於中位數的字體、過濾掉可能是圖片的語料
            elif content["size"] == med and not is_image(text):
                re_contents.append(content)
    return re_contents, topics
 
def is_body_text(text):
    return len(text) > 100 or text.endswith(".") or text.endswith("?") or text.endswith("!")
 
def is_image(text):
    return text.startswith("Image:") or text.startswith("Figure:")
 
def is_formula(text):
    return text.startswith("Formula:") or text.startswith("Equation:")

# gemini再次確認是否為標題
def reCheck(text, model):
    input = f"""please check whether "{text}" is a topic, and answer "yes" or "no" only
    """
    reply = model.generate_content(
    input,
    generation_config=genai.types.GenerationConfig(temperature=0),
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE",},
        ]
    )
    if "yes" in reply.text:
        return True
    else:
        return False

# === Topic Main === #

def Topics(filepath, model):
    re_topics = []
    contents, topics = extractContents(filepath)
    for element in topics:
        if reCheck(element['text'], model):
            re_topics.append(element)
        else:
            continue
    return contents, re_topics