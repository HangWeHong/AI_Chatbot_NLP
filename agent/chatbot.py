import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


def chat_with_bot(input, history):
    url = "https://ibotservice.alipayplus.com/almpapi/v1/message/chat"
    payload = json.dumps({
    "stream": False,
    "botId": os.getenv("BOT_ID"),
    "bizUserId": "xxxx",
    "token": os.getenv("API_KEY"),
    "chatContent": {
        "text": collect_history(history) + input ,
        "contentType": "TEXT"
    }
    })
    headers = {
    'content-type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_json = response.json()
    try:
        return response_json['data']['messageList'][0]['content'][0]['text']
    except:
        return "Sorry, something went wrong with the bot response."

def collect_history(history):
    if history is None or len(history) == 0:
        return ""
    history_text = "## History Conversation:\n"
    for item in history:
        if item['role'] == 'user':
            history_text += f"User: {item['content']}\n"
        elif item['role'] == 'assistant':
            history_text += f"Assistant: {item['content']}\n"
        
    return history_text.strip()

if __name__ == "__main__":
    
    user_input = input("Enter your message: ")
    chat_with_bot(user_input)
    