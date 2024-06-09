import google.generativeai as genai
import time
from Contents import Topics
from Chunks import Questions
from Knowledge import Ask
from AnkiExport import Convert

class PDFtoAnki:
    def __init__(self):
        self.contents = []
        self.topics = []
        self.count = 0

    def geminiQA(self, pdf_path: str, model: None):
        if not self.contents:
            self.contents, self.topics = Topics(pdf_path, model)
        csv_name = Questions(pdf_path, self.contents, self.topics, model)
        return csv_name

    def userQA(self, pdf_path: str, question: str, model: None, api: str):
        if not self.contents:
            self.contents, self.topics = Topics(pdf_path, model)
        csv_name = Ask(pdf_path, question, self.contents, api)
        return csv_name

    def pdf2anki(self, question: str, api: str, pdf, apkg_name: str) -> str:
        pdf_path = pdf.name
        model = self.input_API(api)
        if self.count == 0:
            csv_name = self.geminiQA(pdf_path, model)
            self.count += 1
        if question:
            csv_name = self.userQA(pdf_path, question, model, api)
        apkg_path = Convert(csv_name, apkg_name)
        return apkg_path

    def input_API(self, api):
        genai.configure(api_key=api)
        model = genai.GenerativeModel('gemini-pro')
        while True:
            try:
                model.generate_content("test")
                print("Set Gemini API successfully!!")
                return model
            except:
                print("There seems to be something wrong with your Gemini API.")
                time.sleep(5)