import gradio as gr
import google.generativeai as genai

# functions made by myself
from Contents import Topics
from Chunks import Questions
from AnkiExport import Convert

# ====================================================== #

# gemini出題
def geminiQA(pdf_path: str, model: None) :
    contents, topics = Topics(pdf_path, model)
    csv_name = Questions(pdf_path, contents, topics, model)
    return csv_name

# 使用者出題
# def userQA():

# 整合題目
def pdf2anki(api: str, pdf: None, apkg_name: str) -> str:
    pdf_path = pdf.name
    model = input_API(api)
    csv_name = geminiQA(pdf_path, model)
    apkg_path = Convert(csv_name, apkg_name)
    return apkg_path

# ====================================================== #

def input_API(api):
    genai.configure(api_key=api)
    model = genai.GenerativeModel('gemini-pro')
    try:
        model.generate_content(
        "test",
        )
        print("Set Gemini API sucessfully!!")
        return model
    except:
        print("There seems to be something wrong with your Gemini API. Please follow our demonstration in the slide to get a correct one.")
        return None
    
# gradio: upload files
# https://blog.csdn.net/qq_51116518/article/details/132628392
def main():
    with gr.Blocks() as demo:
        with gr.Row():
            pdf_upload = gr.File(label="上傳PDF檔案")
            with gr.Column():
                api_textbox = gr.Textbox(label="API key", placeholder="請輸入gemini的API key", type="password", interactive=True)
                deck_name = gr.Textbox(label="Deck name", placeholder="請輸入生成後的Deck名字", interactive=True)
                submit_button = gr.Button("Submit")
                output_file = gr.File(label="下載apkg檔案")

        submit_button.click(pdf2anki, inputs=[api_textbox, pdf_upload, deck_name], outputs=output_file)

    demo.launch(debug=True)

if __name__=='__main__':
    main()