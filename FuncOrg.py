import google.generativeai as genai
import time
from Contents import Topics
from Chunks import Questions
from Knowledge import Ask
from AnkiExport import Convert

contents = []
topics = []
count = 0

# gemini出題
def geminiQA(pdf_path: str, model: None) :
    global contents, topics
    if not contents:
        contents, topics = Topics(pdf_path, model)
    csv_name = Questions(pdf_path, contents, topics, model)
    return csv_name

# 使用者出題
def userQA(pdf_path: str, question:str, model: None, api: str):
    global contents, topics
    if not contents:
        contents, topics = Topics(pdf_path, model)
    csv_name = Ask(pdf_path, question, contents, api)
    return csv_name

# 整合題目
def pdf2anki(question: None, api: str, pdf: None, apkg_name: str) -> str:
    global count
    pdf_path = pdf.name
    model = input_API(api)
    if count == 0:
        csv_name = geminiQA(pdf_path, model)
        count += 1
    if question != "":
        csv_name = userQA(pdf_path, question, model, api)
    apkg_path = Convert(csv_name, apkg_name)
    return apkg_path

def input_API(api):
    genai.configure(api_key=api)
    model = genai.GenerativeModel('gemini-pro')
    while(True):
        try:
            model.generate_content(
            "test",
            )
            print("Set Gemini API sucessfully!!")
            return model
        except:
            print("There seems to be something wrong with your Gemini API.")
            time.sleep(5)