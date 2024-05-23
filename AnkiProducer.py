import gradio as gr
import anki
from anki.exporting import AnkiPackageExporter

# functions made by myself
from Contents import Topics

# GOOGLE_API_KEY = ""
# model = None
# page_contents = []
# topics = []

# ====================================================== #

# 取得文字塊

def Chunks():

# gemini出題

# 使用者出題

# ====================================================== #

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