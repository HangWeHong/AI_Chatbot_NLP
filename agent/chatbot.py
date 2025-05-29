import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


def chat_with_bot(input):
    url = "https://ibotservice.alipayplus.com/almpapi/v1/message/chat"

    payload = json.dumps({
    "stream": False,
    "botId": os.getenv("BOT_ID"),
    "bizUserId": "xxxx",
    "token": os.getenv("API_KEY"),
    "chatContent": {
        "text": input,
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

if __name__ == "__main__":
    
    user_input = input("Enter your message: ")
    chat_with_bot(user_input)
    