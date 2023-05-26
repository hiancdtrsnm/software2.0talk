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

st.markdown("# Software 2.0")


t = Tweet("https://twitter.com/karpathy/status/893576281375219712").component()

st.markdown("""
## Ventajas de Software 2.0

1. Manejo de tareas complejas
2. Personalización y adaptabilidad
3. Escalabilidad
"""
)

st.markdown("""
# Referencias
[Karphaty Talk](https://www.youtube.com/watch?v=y57wwucbXR8&ab_channel=Databricks)

[Karphaty post](https://karpathy.medium.com/software-2-0-a64152b37c35)

[Karpathy twitter post](https://twitter.com/karpathy/status/893576281375219712?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E893576281375219712%7Ctwgr%5E87872290581e626c006868e0984164c93c746d61%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fkarpathy.ai%2Ftweets.html)


[Deeplearning.ai](https://learn.deeplearning.ai/?_gl=1*1lzr5jb*_ga*MTU4MDcxMTk3MC4xNjgyNjIwMTYz*_ga_PZF1GBS1R1*MTY4NTA2NzExNC40LjEuMTY4NTA2NzEyNy40Ny4wLjA.)
""")