import requests
import json

API_KEY = "uAhrq0GwelKK5F0tyonojc9w"
SECRET_KEY = "vpHMPK25EAbp2Pac5SA8O9TkD2rCVi1U"
MESSAGES = []

def get_access_token():
    """
    使用 API Key,Secret Key 获取access_token
    """
    #url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[应用API Key]&client_secret=[应用Secret Key]"
    
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)
    return response.json().get("access_token")

def chat(user_input):
    """
    发送用户输入至AI并接收回复,同时更新全局MESSAGES列表
    """
    global MESSAGES
    MESSAGES.append({"role": "user", "content": user_input})
    
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/yi_34b_chat?access_token=" + get_access_token()
    payload = json.dumps({"messages": MESSAGES})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    response_data = response.json()
    
    # 添加AI回复到MESSAGES列表
    MESSAGES.append({"role": "assistant", "content": response_data["result"]})
    
    return response_data["result"]

def main_loop():
    print("Welcome to the chat! Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        assistant_reply = chat(user_input)
        print(f"Assistant: {assistant_reply}")

if __name__ == '__main__':
    main_loop()