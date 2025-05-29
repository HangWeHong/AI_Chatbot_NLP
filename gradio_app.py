import gradio as gr
from agent.chatbot import chat_with_bot

iface = gr.ChatInterface(
    fn=chat_with_bot,
    title="🟦 TouchNGo - Touch 'n Go FAQ Chatbot",
    description="💬 Ask any question about Touch 'n Go eWallet, tolls, payments, and more!",
    theme=gr.themes.Soft(),
    # chatbot=gr.Chatbot(type='messages')
)

iface.launch()
