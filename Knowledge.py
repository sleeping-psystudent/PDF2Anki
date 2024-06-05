from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import csv
import google.generativeai as genai
import time

retriever = None

def Retrieve(contents, api):
    text = ""
    for element in contents:
        text += element['text']
    doc =  Document(page_content = text, metadata={"source": "local"})

    # Split the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    text_chunks = text_splitter.split_documents([doc])

    # Get the embeddings engine ready
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key = api)

    # Set the vectorstore
    vectorstoreDB = Chroma(embedding_function = gemini_embeddings,
                            persist_directory = './Chroma_DATABASE')
    vectorstoreDB.add_documents(text_chunks)

    # Define retriever
    retriever = vectorstoreDB.as_retriever(search_kwargs={"k": 3})
    return retriever

def Chain(question, contents, api):
    global retriever
    if not retriever:
        retriever = Retrieve(contents, api)
    # Define the prompt
    template = """Please answer the following question based on the context provided:

    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Set the LLM chain
    model = ChatGoogleGenerativeAI(
        model='gemini-pro',
        google_api_key = api,
        safety_settings = {
            genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH    
            }
        )
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    while(True):
        try:
            return chain.invoke(question)
        except:
            time.sleep(1)

# 切割問題
def Cut(text):
    return text.split("\n")

# === Question Main === #

def Ask(filepath, questions, contents, api):
    answers = []
    re_questions = Cut(questions)
    for question in re_questions:
        answers.append(Chain(question, contents, api))
    print(re_questions)
    print(answers)

    # 轉為csv檔
    file_name = filepath.split('.')
    file_name = file_name[0]+'.csv'
    with open(file_name, 'a', newline="") as f:
        writer = csv.writer(f)
        for i in range(len(re_questions)):
            writer.writerow([re_questions[i], answers[i]])

    return file_name