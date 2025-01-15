import streamlit as st
import Pipeline as pl
st.title("Event Extractor")

Url = st.text_input("Enter the Url")
result=[]


if st.button("Extract Event"):
    result= pl.event_extract(Url, 4)
    for x in result:
        st.write(x)

