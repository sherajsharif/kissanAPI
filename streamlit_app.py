import streamlit as st
import requests

# Set your Flask API URL
API_URL = "http://localhost:5000/ask"

st.set_page_config(page_title="\U0001F33E Kissan AI", page_icon="\U0001F33F")
st.title("\U0001F33E Kissan AI")
# st.markdown("**Namaste! Main Kissan AI hoon, Rishiswar Industry Private Limited dwara viksit ek prasangik kisaan sahayak. Main aapki kisaan sambandhit sawalon ka jawab dena pasand karta hoon. Kya aap kisi vishesh kisaan sambandhit sawal puchna chahte hain?**")

query = st.text_input("\U0001F4DD Enter your query:")

if st.button("Ask"):
    if not query.strip():
        st.warning("\u26A0\uFE0F Please enter a valid question.")
    else:
        st.info("\u23F3 Generating response...")
        try:
            response = requests.post(API_URL, json={"query": query}, timeout=65)
            data = response.json()
            if "response" in data:
                st.success("\u2705 Response received:")
                st.markdown(data["response"])
            else:
                st.error(f"\u274C {data.get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"\u274C Error: {e}") 