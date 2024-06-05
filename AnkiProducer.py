import gradio as gr
from FuncOrg import pdf2anki
    
# gradio: upload files
# https://blog.csdn.net/qq_51116518/article/details/132628392
def main():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                pdf_upload = gr.File(label="上傳PDF檔案")
                question_textbox = gr.Textbox(label="Ask questions", placeholder="請輸入您的問題，若有多個問題請以換行分割問句", interactive=True)
            with gr.Column():
                api_textbox = gr.Textbox(label="API key", placeholder="請輸入gemini的API key", type="password", interactive=True)
                deck_name = gr.Textbox(label="Deck name", placeholder="請輸入生成後的Deck名字", interactive=True)
                submit_button = gr.Button("Submit")
                output_file = gr.File(label="下載apkg檔案")

        submit_button.click(pdf2anki, inputs=[question_textbox, api_textbox, pdf_upload, deck_name], outputs=output_file)

    demo.launch(share=True, debug=True)

if __name__=='__main__':
    main()