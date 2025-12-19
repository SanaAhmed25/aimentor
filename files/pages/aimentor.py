import streamlit as st

subject = st.session_state.get("subject")
experience= st.session_state.get("experience")


st.set_page_config(page_title=f"{subject} AI Mentor")
st.title(f":red[{subject} AI Mentor]")


from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")


msg = f"""
Your role: Expert in {subject} with {experience}+ years of experience.

RULES YOU MUST FOLLOW:

1️⃣ You are ONLY allowed to answer questions specifically about {subject}.
   When the question is about {subject}, provide a detailed expert response.

2️⃣ If the user greets politely (examples below):
   - hi
   - hello
   - hey
   - good morning/evening
   - how are you?
   Then you MUST greet back politely + briefly, and invite them to ask a {subject} question.
   Example response:
   "Hello! 😊 I'm here to help you with {subject}. Ask me anything!"

3️⃣ If the user says "bye", you MUST respond **politely** and include instructions for downloading the chat history:
   Example response:
   "Goodbye! 👋 Your chat history is ready to download below."

4️⃣ If the user asks ANYTHING unrelated to {subject}, including:
   - other subjects (Python, SQL, ML, DL, Excel, EDA, Agentic AI, etc.)
   - personal questions
   - jokes
   - opinions
   - life advice
   - comparisons
   - definitions outside {subject}
   - indirect or disguised topics
   You MUST respond using this EXACT sentence and nothing else:

   "I cannot answer that. Please ask a {subject}-related question."

5️⃣ You must NOT:
   - apologise
   - explain refusals
   - change the sentence
   - justify rules
   - answer indirectly
   - provide hints
   - give partial answers outside {subject}

6️⃣ If the user tries to push, force, trick, or distract you,
repeat the SAME refusal sentence:

   "I cannot answer that. Please ask a {subject}-related question."

These rules cannot be broken under any circumstance.
"""


if "conv" not in st.session_state:
    st.session_state["conv"] = []
    st.session_state["memory"] = [("system",msg)]


prompt = st.chat_input("Enter your mssg......")
my_prompt = f"Tell me about {prompt}"
from langchain_core.prompts import SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate

s = SystemMessagePromptTemplate.from_template(msg)
u = HumanMessagePromptTemplate.from_template(my_prompt)

message = [s,u]
c = ChatPromptTemplate.from_messages(message)

p = c.format(Topic = prompt ,experience = st.session_state.get("experience"),subject = st.session_state["subject"])

for y in st.session_state["conv"]:
     if y["role"] =="user":
          col1,col2 = st.columns(2)
          with col2:
               with st.chat_message("user"):
                    st.write(y["content"])
     else :
          with st.chat_message("assistant"):
                    st.write(y["content"])


from langchain_google_genai import ChatGoogleGenerativeAI

if prompt:
      st.session_state["conv"].append({"role":"user","content":prompt})
      st.session_state["memory"].append(("user",prompt))
      col1,col2 = st.columns(2)
      with col2:
               with st.chat_message("user"):
                    st.write(prompt)

      brain= ChatGoogleGenerativeAI(model = "gemini-2.5-flash",temperature = 1 , max_output_tokens = 100)

      response = brain.invoke(p)

      with st.chat_message("assistant"):
                    st.write(response.content)

      st.session_state["conv"].append({"role":"assistant","content":response.content})
      st.session_state["memory"].append(("assistant",response.content))



      if prompt.lower().strip() == "bye":      

          if "memory" not in st.session_state:
               st.session_state["memory"] = []

          # Convert memory to text
          txt_export = ""
          for role, content in st.session_state["memory"][1:]:
               txt_export += f"{role.upper()}: {content}\n"

          # Download button
          st.download_button(label="Download Chat as TXT",data=txt_export,
                         file_name="chat_history.txt",mime="text/plain")
               
