import requests
import json
import concurrent.futures
import os
import re

API_KEY = "uAhrq0GwelKK5F0tyonojc9w"
SECRET_KEY = "vpHMPK25EAbp2Pac5SA8O9TkD2rCVi1U"


QUESTION_PATH = "F:\\python\\text\\workspace\\网页自动化\\qusetions.txt"  # 问题文件，每个问题只能是一行
ORIGINAL_PATH = "F:\\python\\text\\workspace\\网页自动化\\original_answer.txt"  # 原始数据
ANALYZED_PATH = "F:\\python\\text\\workspace\\网页自动化\\Answer.txt"  # 分析后的答案数据


TEMP_PATH = ANALYZED_PATH + ".tmp"

def get_questions():
    """该函数用于特定的乡村振兴选课网页#将问题从1.json中提取出来
    """
    f = open('F:\\python\\text\\workspace\\网页自动化\\1.json','r',encoding='utf-8')
    text = f.read()
    parsed_data = json.loads(text)
    txt = parsed_data['rows']['newTopics']
    with open('F:\python\\text\workspace\网页自动化\qusetions.txt','w',encoding='utf-8') as f:
                f.write("")         
    for i in range(len(txt)):
        title = txt[i]['topic_name']
        option = txt[i]['topic_config']
        if txt[i]['topics_handle_simple_state'] == '未完成' :
            content = f'{i+1}.'+title + option + '\n'
            with open('F:\python\\text\workspace\网页自动化\qusetions.txt','a',encoding='utf-8') as f:
                f.write(content)


def prepare_data():
    """准备问题数据"""
    with open(QUESTION_PATH, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


def save_data(answer_data='', original_data=''):
    with open(ANALYZED_PATH, 'a', encoding='utf-8') as f:
        f.write(answer_data)
    with open(ORIGINAL_PATH, 'a', encoding='utf-8') as f:
        f.write(original_data + '\n')


def sort_answer():
    """排序答案"""
    with open(ANALYZED_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # 改进 key 函数，确保提取干净的数字
    lines.sort(key=lambda x: int(re.sub(r'^"\d+"$', lambda m: m.group().strip('"'), x.split(':')[1].split(',')[0].strip())))
    with open(TEMP_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    # 替换原始文件
    os.replace(TEMP_PATH, ANALYZED_PATH)



def analysis_data():
    """
    处理返回的答案数据
    """
    with open(ORIGINAL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            code_match = re.search(r'编号.*?:(.*?),', line)
            answer_match = re.search(r'答案.*?:(.*?),', line)
            if code_match and answer_match:
                code = code_match.group(1).replace('\\', '')  # 移除转义字符
                answer = answer_match.group(1).replace('\\', '')  # 移除转义字符
                answer_data = f"code:{code},answer:{answer}\n"
                print(answer_data,end='')
                save_data(answer_data = answer_data)
                
    sort_answer()



def clear_data(clear_original_data=True, clear_analyzed_data=True):
    if clear_analyzed_data:
        with open(ANALYZED_PATH, 'w', encoding='utf-8') as f:
            f.write("")
            print("The analyzed data has been cleared!!!")

    if clear_original_data:
        with open(ORIGINAL_PATH, 'w', encoding='utf-8') as f:
            f.write("")
            print("The original data has been cleared!!!")


def get_access_token():
    """获取access_token"""
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers)
    return response.json().get("access_token")


def send_request(question):
    """发送单个问题的请求"""
    #https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/yi_34b_chat?access_token=
    #https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-8k-preview?access_token=
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-8k-preview?access_token={get_access_token()}"

    msg = {
        "messages": [
            {
                "role": "user",
                "content": "下面你将回答单选题,请你按照问题的编号，答案，解析的格式来回答，例如：'编号:1,答案:A,解析:**'."
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
        "system": "你是一个正在考试的学生,将会回答选择题（默认都为单选题），填空等问题"  # 人物设置
    }
    payload = json.dumps(msg)
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        save_data(original_data=response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error requesting for question: {question}, Error: {e}")


def put_messages_concurrently(questions):
    """并发发送所有问题的请求"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(send_request, questions)


def main(clear_data_first=True):
    # get_questions() 
    if clear_data_first: # 清空数据
        clear_data()
    questions = prepare_data()
    put_messages_concurrently(questions)
    analysis_data()


if __name__ == '__main__':
    main()