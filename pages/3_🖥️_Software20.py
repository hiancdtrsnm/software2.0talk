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




st.markdown("# Software 2.0")


t = Tweet("https://twitter.com/karpathy/status/893576281375219712").component()

st.markdown("""
## Ventajas de Software 2.0

1. Manejo de tareas complejas
2. Personalización y adaptabilidad
3. Escalabilidad
4. Mejora Continua
"""
)

st.markdown("""
## Ideas para aplicar Software 2.0

1. Asistente de inteligencia artificial

2. Tutor interactivo

3. Generador de contenido

4. Atención al cliente y soporte técnico

5. Herramienta de productividad

6. Análisis de sentimiento y moderación de contenido
""")
