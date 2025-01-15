import streamlit as st

#Page Setup
home_page = st.Page(
    page="./Views/Home.py",
    title="Home",
    # icon=":./material/account_circle:",
    default=True,
)

st.page
contact_page = st.Page(
    page="./Views/Contact.py",
    title="Contact Us",
    # icon=":./material/thumb_up:",
)
search_page = st.Page(
    page="./Views/Search.py",
    title="Search History",
)
event_page = st.Page(
    page="./Views/Event.py",
    title="Event Extractor",
)


# ---- Navigation Setups [Without Sections] ------
pg = st.navigation(pages=[home_page,contact_page,search_page,event_page])

#Logo

st.sidebar.text("Made By DUZ💖")


# ---- Run Navigation ----
pg.run()






