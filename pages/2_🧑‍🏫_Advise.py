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




st.markdown(
    """
## Principio 1: Escribe de forma clara y con instrucciones lo más específicas posible.
"""
)

st.markdown(
    """\
### Tacticas 1: Usa delimitadores claros para indicar diferentes partes de la conversación.
* Los delimitadores pueden ser cosas como ```, \"\"\", <>, <tag> </tag>, :
"""
)

generate_example(
    """\
You should express what you want a model to do by \
providing instructions that are as clear and \
specific as you can possibly make them. \
This will guide the model towards the desired output, \
and reduce the chances of receiving irrelevant \
or incorrect responses. Don't confuse writing a \
clear prompt with writing a short prompt. \
In many cases, longer prompts provide more clarity \
and context for the model, which can lead to \
more detailed and relevant outputs.
""",
    """\
Summarize the text delimited by triple backticks \
into a single sentence.
```{text}```
""",
    "tatic1-1",
)


st.markdown(
    """\
### Tacticas 2: Pide una respuesta estructurada.
* JSON, XML, HTML, CSV, etc.
"""
)

generate_example(
    "",
    """\
Generate a list of three made-up book titles along \
with their authors and genres.
Provide them in JSON format with the following keys:
book_id, title, author, genre.
""",
    "tatic1-2",
)

st.markdown(
    """\
### Tacticas 3: Pregunta si se satisfacen las condiciones necesarias."""
)

generate_example(
    """\
Making a cup of tea is easy! First, you need to get some \
water boiling. While that's happening, \
grab a cup and put a tea bag in it. Once the water is \
hot enough, just pour it over the tea bag. \
Let it sit for a bit so the tea can steep. After a \
few minutes, take out the tea bag. If you \
like, you can add some sugar or milk to taste. \
And that's it! You've got yourself a delicious \
cup of tea to enjoy.
""",
    """\
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \
then simply write \"No steps provided.\"

\"\"\"{text}\"\"\"
""",
    "tatic1-3",
)

st.markdown(
    """\
### Tacticas 4: "Few-shot" prompting"""
)

generate_example(
    "Teach me about resilience.",
    """\
Your task is to answer in a consistent style.

: Teach me about patience.

: The river that carves the deepest \
valley flows from a modest spring; the \
grandest symphony originates from a single note; \
the most intricate tapestry begins with a solitary thread.\

: {text}
""",
    "tatic1-4",
)

st.markdown(
    """\
## Principio 2: Dale tiempo al modelo a pensar."""
)

st.markdown(
    """\
### Tacticas 1: Define los pasos que se requieren para completar la tarea."""
)

variants = [
    """\
Perform the following actions:
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following \
keys: french_summary, num_names.

Separate your answers with line breaks.

Text:
```{text}```
""",
    """\
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the 
  following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Text: <{text}>
""",
]

prompt_variant = st.number_input(
    "Prompt Variant",
    min_value=0,
    max_value=len(variants) - 1,
    value=0,
    step=1,
    key=f"tatic2-1-prompt-variant",
)

generate_example(
    """\
In a charming village, siblings Jack and Jill set out on \
a quest to fetch water from a hilltop \
well. As they climbed, singing joyfully, misfortune \
struck—Jack tripped on a stone and tumbled \
down the hill, with Jill following suit. \
Though slightly battered, the pair returned home to \
comforting embraces. Despite the mishap, \
their adventurous spirits remained undimmed, and they \
continued exploring with delight.
""",
    variants[prompt_variant],
    "tatic2-1",
)

st.markdown(
    """\
### Tacticas 2: Pide que el modelo genere su propia solucion antes de sacar conclusiones."""
)

variants = [
    """\
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need \
 help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations 
as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
""",
    """\
Your task is to determine if the student's solution \
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
```
question here
```
Student's solution:
```
student's solution here
```
Actual solution:
```
steps to work out the solution and your solution here
```
Is the student's solution the same as actual solution \
just calculated:
```
yes or no
```
Student grade:
```
correct or incorrect
```

Question:
```
I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:
""",
]

prompt_variant = st.number_input(
    "Prompt Variant",
    min_value=0,
    max_value=len(variants) - 1,
    value=0,
    step=1,
    key="tatic2-2-prompt-variant",
)

generate_example("", variants[prompt_variant], "tatic2-2")
