import os
import chainlit as cl
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from chainlit.input_widget import Select, Switch, Slider

load_dotenv()
api_key = os.getenv("SUTRA_API_KEY")

LANGUAGES = [
    "English", "Hindi", "Gujarati", "Bengali", "Tamil", "Telugu", "Kannada", "Malayalam",
    "Punjabi", "Marathi", "Urdu", "Assamese", "Odia", "Sanskrit", "Korean", "Japanese",
    "Arabic", "French", "German", "Spanish", "Portuguese", "Russian", "Chinese",
    "Vietnamese", "Thai", "Indonesian", "Turkish", "Polish", "Ukrainian", "Dutch",
    "Italian", "Greek", "Hebrew", "Persian", "Swedish", "Norwegian", "Danish",
    "Finnish", "Czech", "Hungarian", "Romanian", "Bulgarian", "Croatian", "Serbian",
    "Slovak", "Slovenian", "Estonian", "Latvian", "Lithuanian", "Malay", "Tagalog", "Swahili"
]

@cl.on_chat_start
async def start():
    await cl.ChatSettings(
        [
            Select(id="language", label="🌐 Language", values=LANGUAGES, initial_index=0),
            Switch(id="streaming", label="💬 Stream Response", initial=True),
            Slider(id="temperature", label="🔥 Temperature", initial=0.7, min=0, max=1, step=0.1),
        ]
    ).send()

    await cl.Message("👋 Welcome! Please start chatting in your selected language.").send()


@cl.on_message
async def handle_message(msg: cl.Message):
    settings = cl.user_session.get("chat_settings")
    language = settings.get("language", "English")
    streaming = settings.get("streaming", True)
    temperature = settings.get("temperature", 0.7)

    system_prompt = f"You are a helpful assistant. Respond strictly in {language}."

    model = ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=temperature,
        streaming=streaming
    )

    response = cl.Message(content="")

    async for chunk in model.astream([
        SystemMessage(content=system_prompt),
        HumanMessage(content=msg.content)
    ]):
        await response.stream_token(chunk.content)

    await response.send()
