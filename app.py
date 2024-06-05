import gradio as gr
import google.generativeai as genai
from typing import List, Tuple

GOOGLE_API_KEY = "AIzaSyC_YXmg7dCWwNIuc04BGM-wWP08rd2VAME"
model = None

# load gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

infile = open('文學作品讀法下（一）.md', "r", encoding="utf-8")
lines =infile.readlines()
outfile = open('文學作品讀法下（一）.txt', "w", encoding="utf-8")


def toanki(note):
    format="""
    question\tanswer

    For example:
    poetry\t(1) patterned arrangement of language (2) generate rhyrthm (3) express and evoke specific emotions of feelings (4) a concentrated way/intensity
    """
    input = f"Please create Anki cards using the following notes and format. Do not mark the chapter names, and there is no need to write 'question' or 'answer'.\n\nnotes:\n{note}\nformat:\n{format}"
    info = model.generate_content(
        input,
        generation_config=genai.types.GenerationConfig(temperature=0),
        safety_settings=[
          {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE",},
          ]
    )
    return info.text

switch=0 # 用以決定擷取範圍
text=""

for line in lines:
    if switch==0:
        if line.startswith(":::warning"):
            switch=1 # 開始擷取筆記
    elif switch==1:
        if line.startswith(":::"):
            switch=0 # 結束擷取
            card=toanki(text)
            print(card)
            outfile.write(card.strip()+'\n')
            text="" #清空重複利用
        else:
            text+=(line+'\n')


infile.close()
outfile.close()

"""
# update global api
def input_API(api):
    global GOOGLE_API_KEY
    global model

    GOOGLE_API_KEY = api
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    try:
        model.generate_content(
        "test",
        )
        print("Set Gemini API sucessfully!!")
    except:
        print("There seems to be something wrong with your Gemini API. Please follow our demonstration in the slide to get a correct one.")

if __name__=='__main__':
    main()

"""