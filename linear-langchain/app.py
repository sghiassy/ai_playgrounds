from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import requests
import os
# import streamlit as st


load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
print(f"HUGGINGFACEHUB_API_TOKEN {HUGGINGFACEHUB_API_TOKEN}")

t = "espnet/kan-bayashi_ljspeech_vits"


# img2text
def img2text(url):
    image_to_text = pipeline(
        "image-to-text", model="Salesforce/blip-image-captioning-large"
    )

    text = image_to_text(url)[0]["generated_text"]

    print(text)

    return text


# llm
def generate_story(scenario):
    template = """
    You are a story teller;
    You can generate a short story based on a simple narrative, the story should be no more than 50 words;

    CONTEXT: {scenario}
    STORY:
    """
    prompt = PromptTemplate(template=template, input_variables=["scenario"])

    story_llm = LLMChain(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1),
        prompt=prompt,
        verbose=True,
    )

    story = story_llm.predict(scenario=scenario)

    print(story)
    return story


# text to speech
def text2speech(message):
    API_URL = (
        "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    )
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    payloads = {"inputs": message}
    response = requests.post(API_URL, headers=headers, json=payloads)
    with open("audio.flac", "wb") as file:
        file.write(response.content)


scenario = img2text("image.png")
# scenario = "a group of people jumping in the air with their hands in the air"
story = generate_story(scenario)
# story = "A spontaneous burst of joy swept through the crowd as they soared into the sky, united by freedom and exhilaration."

text2speech(story)
