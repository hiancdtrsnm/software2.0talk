import streamlit as st
from common import get_completion, get_completion_from_messages, load_dataset
import os
from dotenv import load_dotenv, find_dotenv
import openai
import random
import requests
import streamlit.components.v1 as components

_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.getenv("OPENAI_API_KEY")


class Tweet(object):
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = "https://publish.twitter.com/oembed?url={}".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=600)


def generate_example(input_text, prompt, key=None):
    left, right = st.columns(2)

    with left:
        input_text = st.text_area(
            "Input Text", value=input_text, key=f"{key}-input-text", height=375
        )

    with right:
        prompt = st.text_area(
            "Prompt",
            value=prompt,
            key=f"{key}-prompt",
            height=375,
        )

    prompt = prompt.format(text=input_text)

    if st.button("Ejecutar", key=key):
        response = get_completion(prompt)
        super_response = response.replace("\n", "\n\n")
        st.success(super_response)

        return response

    return ""


st.title("Desarrollando con ChatGPT: Optimizando Prompts y Abrazando el Software 2.0 🚀")

st.image(open("images/qr.png", "rb").read(), width=500)

st.markdown("### 👋 Hian Cañizares - @hiancdtrsnm")

