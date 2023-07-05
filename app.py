import io
import os
import re
from tempfile import NamedTemporaryFile

import replicate
import streamlit as st
from PIL import Image
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You're a chef and an helpful assistant who suggests delicious recipes that includes foods which are "
    "nutritionally beneficial, easy & not time consuming, healthy yet economical."
)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


st.title('Chef:green[GPT] :cook:')


with st.sidebar:
    st.title("Add grocery items")

    uploaded_files = st.file_uploader(
        label="Upload image of each item",
        key="files_upload",
        accept_multiple_files=True,
    )

    cook = st.button("Let AI cook!")

    if cook:
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.getvalue()
            image = Image.open(io.BytesIO(bytes_data))
            st.image(image, width=100)

            with NamedTemporaryFile(suffix=".jpg") as temp_file:
                image.save(temp_file.name)
                output = replicate.run(
                    MODEL_NAME,
                    input={"image": open(temp_file.name, "rb")},
                )
                pattern = r"Caption:\s(.*)"
                match = re.search(pattern, output).group(1)

                if "groceries" not in st.session_state:
                    st.session_state["groceries"] = ""
                st.session_state["groceries"] += f"{match},"


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="system", content=SYSTEM_PROMPT),
        ChatMessage(role="assistant", content="How can I help you?"),
    ]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(
            openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler]
        )
        response = llm(st.session_state.messages)
        st.session_state.messages.append(
            ChatMessage(role="assistant", content=response.content)
        )

if "groceries" in st.session_state and st.session_state["groceries"]:
    st.session_state.messages.append(
        ChatMessage(
            role="user",
            content=f"Using these items: `{st.session_state['groceries']}` "
            f"generate a recipe.",
        )
    )
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(
            openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler]
        )
        response = llm(st.session_state.messages)
        st.session_state.messages.append(
            ChatMessage(role="assistant", content=response.content)
        )
        st.session_state["groceries"] = ""
