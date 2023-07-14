#!/usr/bin/env python
# coding: utf-8

import os
import streamlit as st
import time
import openai
import pandas as pd
import numpy as np
from openai.embeddings_utils import cosine_similarity
from streamlit_chat import message
import PyPDF2

def get_pdf_content(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    num_pages = len(pdf_reader.pages)
    text_content = ""
    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        text_content += page_obj.extract_text()
    pdf_file_obj.close()
    return text_content

def generate_response(user_input):
    # OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # GPT-3 and other parameter
    model_engine = "gpt-4"
    qa_template = """
   `````Answer in German, you represent the Hochschule Emden/Leer, Keep your answers as short as possible, Your name is IPRO-ChatBot
        If you don't know the answer, just say you don't know. Do NOT try to make up an answer.
        If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
        Use as much detail as possible when responding.
        If a link is found, it must be displayed in the following format: [Link Description](URL)
        All answers can only be based on existing documents
    
        context: {context}
        =========
        question: {question}
        ======
        """

    # load PDF content
    pdf_content = get_pdf_content("Liste_Fragen_IuP KSpethmann.pdf")

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": qa_template.format(context=pdf_content, question=user_input) },
            {"role": "user", "content": user_input},
        ],
    )

    # get response
    return response.choices[0].message.content.strip()

st.title("IPRO-Demo")

# Load the dataframe and embeddings
df_try = pd.read_csv('output.csv')
all_embeddings = np.load('output.npy', allow_pickle=True)
df_try['ada_v2_embedding'] = all_embeddings

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def custom_message(message, is_user):
    if is_user:
        st.write(f"User: {message}")
    else:
        st.markdown(f"Bot: {message}", unsafe_allow_html=True)

# input frame
user_input = st.text_input("Frage Hier：")

if st.button("Send"):
    # with a waiting icon
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # GPT needs some time to response
    with st.spinner("Waiting..."):
        time.sleep(2)

    # get generate_response
    response = generate_response(user_input)

    # Add user input and response to chat history
    st.session_state['chat_history'].append((user_input, response))

    # show the chat history
    # show the chat history
    for user_msg, bot_msg in st.session_state['chat_history']:
        custom_message(user_msg, is_user=True)
        custom_message(bot_msg, is_user=False)

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state['chat_history'] = []
