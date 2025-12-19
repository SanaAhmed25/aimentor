import streamlit as st
st.set_page_config(page_title="AI Mentor")

st.title(":red[AI Mentor]")

st.header("Select which subject mentor you need : ")


options = ["Python","EDA","Excel","SQL","Machine Leraning","Deep Learning","AgenticAI"]

subject = st.pills("Subjects : ", options, selection_mode="single")
st.divider(width="stretch")

st.header("How many years of mentor's experience you need : ")
col1,col2 = st.columns(2)
with col1:
    experience = st.number_input("",value=1,step = 1)
st.divider(width="stretch")

if subject :
    st.session_state["subject"] = subject
    st.session_state["experience"] = experience
    if st.button("Submit"):
        st.switch_page("pages/aimentor.py")
