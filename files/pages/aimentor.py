import streamlit as st
from dotenv import load_dotenv
import os
from langchain_core.prompts import (SystemMessagePromptTemplate,HumanMessagePromptTemplate,
                                    ChatPromptTemplate)
from langchain_google_genai import ChatGoogleGenerativeAI


subject = st.session_state.get("subject")
experience = st.session_state.get("experience")

st.set_page_config(page_title=f"{subject} AI Mentor")
st.title(f":red[{subject} AI Mentor]")

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")


msg = f"""
Your role: Expert in {subject} with {experience}+ years of experience.

RULES YOU MUST FOLLOW:

1️⃣ You are ONLY allowed to answer questions specifically about {subject}.
   When the question is about {subject}, provide a detailed expert response.

2️⃣ If the user greets politely:
   - hi
   - hello
   - hey
   - good morning/evening
   - how are you?
   Then greet back politely + briefly and invite them to ask a {subject} question.

3️⃣ If the user says "bye", answer politely + say chat download is ready.

4️⃣ If user asks anything outside {subject}, reply ONLY:
   "I cannot answer that. Please ask a {subject}-related question."

5️⃣ Never apologise, explain rules, give hints or partial answers.
"""


if "conv" not in st.session_state:
    st.session_state["conv"] = []
    st.session_state["memory"] = [("system", msg)]

prompt = st.chat_input("Enter your message...")


s = SystemMessagePromptTemplate.from_template(msg)
u = HumanMessagePromptTemplate.from_template("{query}")

message = [s, u]
c = ChatPromptTemplate.from_messages(message)

for y in st.session_state["conv"]:
    if y["role"] == "user":
        col1,col2 = st.columns(2) 
        with col2:
            with st.chat_message("user"):
                  st.write(y["content"])
    else:
        with st.chat_message("assistant"):
            st.write(y["content"])

if prompt:

    st.session_state["conv"].append({"role": "user", "content": prompt})
    st.session_state["memory"].append(("user", prompt))
    col1,col2 = st.columns(2) 
    with col2:
         with st.chat_message("user"):
            st.write(prompt)

    # FORMAT PROMPT
    p = c.format(query=prompt,subject=subject,experience=experience)

    brain = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",temperature=1,max_output_tokens=100)

    response = brain.invoke(p)

    with st.chat_message("assistant"):
        st.write(response.content)

    st.session_state["conv"].append({"role": "assistant", "content": response.content})
    st.session_state["memory"].append(("assistant", response.content))

    if prompt.lower().strip() == "bye":

        txt_export = ""
        for role, content in st.session_state["memory"][1:]:
            txt_export += f"{role.upper()}: {content}\n"

        st.download_button(
            label="Download Chat as TXT",
            data=txt_export,
            file_name="chat_history.txt",
            mime="text/plain"
        )
