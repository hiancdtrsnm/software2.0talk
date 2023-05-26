from dotenv import load_dotenv, find_dotenv
import os
import openai
import streamlit as st
from io import BytesIO
import pandas as pd

_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.getenv("OPENAI_API_KEY")


@st.cache()
# @st.cache_data()
def get_completion(
    prompt, model="gpt-3.5-turbo", temperature=0
):  # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


@st.cache()
# @st.cache_data()
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    #     print(str(response.choices[0].message))
    return response.choices[0].message["content"]


@st.cache()
# @st.cache_data()
def load_dataset(file):
    csv_bytes = file.read()
    sep = "," if csv_bytes.count(b",") > csv_bytes.count(b";") else ";"
    in_memory_csv = BytesIO(csv_bytes)
    df = pd.read_csv(in_memory_csv, sep=sep)
    return df
