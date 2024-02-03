from openai import OpenAI
import streamlit as st
import random
import time

def load_view():
    st.title("Sarcastic Financial Guru")
    
    api_key = st.secrets["julep"]["api_key"]
    base_url = st.secrets["julep"]["url"]

    client = OpenAI(
        api_key = api_key,
        base_url = base_url
    )  

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "name": "situation",
                "content": "You are a Sarcastic Financial Guru. You answer with a sarcastic and witty personality that provides financial advice and education. It could use humor to demystify complex financial concepts and offer practical tips in a relatable way."
            }
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Sarcastic Financial Guru"):
        st.session_state.messages.append({"role": "user", "name": "David", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="julep-ai/samantha-1-turbo",
                messages=[
                    {"role": m["role"], "name": m["name"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.7,
                max_tokens=200,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["<","<|"],
            )
            # response = st.write_stream(response)
            st.markdown(response.choices[0].message.content)  
        st.session_state.messages.append({"role": "assistant", "name": "Julia", "content": response.choices[0].message.content})


load_view()