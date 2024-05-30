import google.generativeai as genai
import time
import csv

# 標出章節標題
def containTopic(string, topics):
    return any(element['text'] in string for element in topics)

# gemini出題
def teacher(text, model):
    input = f"""You are now a university professor preparing for the final exam and are planning to create question-and-answer format questions. Based on the following article, please create at least three question-and-answer pairs related to the title. The output format must separate the question and answer with a '|', and each new question-answer pair must be on a new line. No need to label 'Question' and 'Answer'.
    Here is an example:
    What is gender panics? | Moments where people react to a challenge to the gender binary by frantically asserting its naturalness.
    Who are transgender women? | People who were assigned male at birth but identify as female.
    
    {text}
    """
    QA = model.generate_content(
    input,
    generation_config=genai.types.GenerationConfig(temperature=0),
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE",},
        ]
    )
    return QA.text

# === Question Main === #

def Questions(filepath, contents, topics, model):
    tests = []
    text = ""
    for element in contents:
        sentence = element['text']
        if containTopic(sentence, topics):
            if text != "":
                questions = teacher(text, model)
                tests += questions.split("\n")
            text = sentence+"\n\n"
        else:
            text += sentence    
    tests = list(filter(None, tests))

    # 處理生成的問答
    re_tests = []
    for element in tests:
        temp = element.split("|")
        re_tests.append(temp)
    
    # 轉為csv檔
    file_name = filepath.split('.')
    file_name = file_name[0]+'.csv'
    with open(file_name, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Answer"])
        writer.writerows(re_tests)
    
    return file_name