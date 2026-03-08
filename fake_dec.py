import streamlit as st
import pickle
import pandas as pd
import tldextract

# Load trained model
model = pickle.load(open("url_model.pkl", "rb"))

# Feature extraction function
def extract_features(url):

    features = {}

    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")

    ext = tldextract.extract(url)

    if ext.subdomain:
        features["num_subdomains"] = len(ext.subdomain.split("."))
    else:
        features["num_subdomains"] = 0

    features["https"] = 1 if url.startswith("https") else 0

    return pd.DataFrame([features])


# Streamlit UI
st.title("🔍 Fake Website Detector")

st.write("Enter a URL to check if it is Fake or Official.")

url = st.text_input("Enter Website URL")

if st.button("Check Website"):

    if url == "":
        st.warning("Please enter a URL")

    else:
        features = extract_features(url)

        prediction = model.predict(features)

        if prediction[0] == 1:
            st.success("✅ This looks like an Official Website")
        else:
            st.error("⚠️ This may be a Fake / Scam Website")
