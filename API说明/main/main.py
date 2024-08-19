import requests
import json
import threading
import re

API_KEY = "uAhrq0GwelKK5F0tyonojc9w"
SECRET_KEY = "vpHMPK25EAbp2Pac5SA8O9TkD2rCVi1U"

ANSWER = []
PROBLEM = {}

QUESTION_PATH = "F:\\python\\text\\workspace\\网页自动化\\qusetions.txt" # 问题文件，每个问题只能是一行
ORIGINAL_PATH = "F:\\python\\text\\workspace\\网页自动化\\answer.txt" # 原始数据
ANALYZED_PATH = "F:\\python\\text\\workspace\\网页自动化\\Answer2.txt" # 分析后的答案数据


def prepare_data():
    """准备问题数据"""
    question = []
    
    with open(QUESTION_PATH, 'r', encoding='utf-8') as f:
        qest = f.readlines()
        question.extend(qest)
    return question



def save_data(answer_data='',original_data=''):
    if answer_data != "":
        with open(ANALYZED_PATH,'a',encoding='utf-8') as f:
            f.write(answer_data)
    if original_data != "":  
        with open(ORIGINAL_PATH,'a',encoding='utf-8') as f:
            f.write(original_data)
            f.write('\n')



def analysis_data():
    """
    处理返回的答案数据
    """
    with open("F:\\python\\text\\workspace\\网页自动化\\answer.txt", "r", encoding="utf-8") as f:
        for line in f:
            # print(line)
            code = re.search(r'编号.*?:(.*?),', line).group(1).replace('\\"', '')
            answer = re.search(r'答案.*?:(.*?),', line).group(1).replace('\\"', '')
            print(code)
            print(answer)
            print("*" * 20)
            save_data(answer_data=f"code:{code},answer:{answer}\n")
        
        
        
def clear_data(clear_original_data=True,clear_analyzed_data=True):
    if clear_analyzed_data:
        with open(ANALYZED_PATH,'w',encoding='utf-8') as f:
            f.write("")
            print("The analyzed data has been cleared!!!")


    if clear_original_data:
        with open(ORIGINAL_PATH,'w',encoding='utf-8') as f:
            f.write("")
            print("The analyzed data has been cleared!!!")



def get_access_token():
    """获取access_token"""
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")



def send_request(question):
    """发送单个问题的请求"""
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-8k-preview?access_token={get_access_token()}"
    
    msg = {
        "messages": [
            {
                "role": "user",
                "content": "请你按照问题的编号，答案，解析的格式来回答，例如：'编号:1,答案:A,解析:**'."
            },
            {
                "role": "assistant",
                "content": "好的，我会按照 编号: 3,答案: 正确,解析: "
            },
            {
                "role": "user", 
                "content": question
            }
        
        ],
        "response_format": "json_object",
        "system" : "你是一个正在考试的学生,将会回答多选题，单选题，填空等问题" ,#人物设置
        # "stream": True #流式输出
    }
    payload = json.dumps(msg)
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        #保存返回的数据
        save_data(original_data=response.text)

    
    except Exception as e:
        print(f"Error requesting for question: {question}, Error: {e}")


def put_messages_concurrently(questions):
    """并发发送所有问题的请求"""
    threads = []
    for question in questions:
        thread = threading.Thread(target=send_request, args=(question,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def main():
    #是否清空答案数据
    clear_data()
    questions = prepare_data()
    put_messages_concurrently(questions)
    analysis_data()
    


if __name__ == '__main__':
    main()