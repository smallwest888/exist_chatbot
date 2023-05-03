#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import time
import openai

def generate_response(user_input):
    # 用您的OpenAI API密钥进行身份验证
    openai.api_key = "sk-"

    # 设置GPT-3模型的相关参数
    model_engine = "gpt-3.5-turbo"

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "Antwort auf Deutsch, Sie vertreten die Hochschule Emden/Leer, Halten Sie Ihre Antworten so kurz wie möglich, Ihr Name ist IPRO-ChatBot"},
            {"role": "user", "content": user_input},
        ],
    )

    # 提取并返回生成的文本
    return response.choices[0].message.content.strip()



st.title("IPRO-Demo")

# 创建一个输入框，用于接收用户输入
user_input = st.text_input("Frage Hier：")

if st.button("Send"):
    # 模拟ChatBot正在生成回答
    with st.spinner("Waiting..."):
        time.sleep(2)

    # 调用generate_response函数生成回答
    response = generate_response(user_input)

    # 显示回答
    st.write(response)
