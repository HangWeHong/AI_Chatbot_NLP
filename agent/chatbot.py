import requests
import json
from dotenv import load_dotenv
import os
from knowledge_base.vector_db import vector_db 


load_dotenv()


def chat_with_bot(input, history):
    url = "https://ibotservice.alipayplus.com/almpapi/v1/message/chat"
    payload = json.dumps({
    "stream": False,
    "botId": os.getenv("BOT_ID"),
    "bizUserId": "xxxx",
    "token": os.getenv("API_KEY"),
    "chatContent": {
        "text": assemble_question(input, history),
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
    
def assemble_question(input, history):
    question = collect_history(history) +"## User Question\n" + input + "\n\n" + recall_knowledge_base(input)
    print(f"Question to Bot:\n{question}")
    return question

def collect_history(history):
    if history is None or len(history) == 0:
        return ""
    history_text = "## History Conversation:\n"
    for item in history:
        if item['role'] == 'user':
            history_text += f"User: {item['content']}\n"
        elif item['role'] == 'assistant':
            history_text += f"Assistant: {item['content']}\n"
    history_text += "\n\n"
    return history_text

def recall_knowledge_base(input):
    cate_vdb = vector_db(vdb_name="cate_vdb_4")

    results = cate_vdb.query(
        query_texts=[input],
        n_results=5,
    )
    knowledge_text = "## Knowledge Base\n"
    for index, item in enumerate(results["documents"][0]):
        knowledge_text += (f"Knowledge {index + 1}:\n")
        cate_info = json.loads(item)
        knowledge_text+=f"Question: {cate_info['Question']}\n"
        knowledge_text+=f"Answer: {cate_info['Answer']}\n"
        knowledge_text += "-" * 40 + "\n"
    
    return knowledge_text.strip()
        

