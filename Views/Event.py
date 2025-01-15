import streamlit as st
import Pipeline as pl
st.title("Event Extractor")

Url = st.text_input("Enter the Url", value="", max_chars=100)
result=[]

st.markdown(
    """
    <style>
    #stMainBlockContainer {
        background-color: #f0f4f0;  # Set your desired background color
    }
    </style>
    """,
    unsafe_allow_html=True
)


if st.button("Extract Event"):
    result= pl.event_extract(Url, 4)
    for x in result:
        st.write(x)

