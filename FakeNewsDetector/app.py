import streamlit as st
import feedparser
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk

# Download stopwords if not already downloaded
try:
    stopwords_set = set(stopwords.words('english'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    stopwords_set = set(stopwords.words('english'))

# Define the stemming function (same as used during training)
port_stem = PorterStemmer()

def stemming(content):
    # Ensure content is a string and handle potential NaN
    if not isinstance(content, str):
        content = str(content)
    content = re.sub('[^a-zA-Z]', ' ', content).lower()
    words = content.split()
    stemmed = [port_stem.stem(word) for word in words if word not in stopwords_set]
    return ' '.join(stemmed)

# Define the function to preprocess and predict for new data
def predict_fake_news(title, text):
    """
    Predicts if a news article is fake or real using the trained model.

    Args:
        title (str): The title of the news article.
        text (str): The text of the news article.

    Returns:
        str: The predicted label ('Fake' or 'Real').
    """
    # Combine title and text and preprocess (stemming)
    combined_text = str(title) + " " + str(text) # Ensure they are strings
    stemmed_text = stemming(combined_text)

    # Vectorize the preprocessed text
    vectorized_text = loaded_vectorizer.transform([stemmed_text])

    # Predict the label using the loaded model
    prediction = loaded_model.predict(vectorized_text)

    return 'Real' if prediction[0] == 1 else 'Fake'

# --- Streamlit App Layout ---

st.set_page_config(page_title="Fake News Detector", layout="wide")

st.title("📰 Fake News Detector from RSS Feed and Text Input")

st.write("Analyze news articles for authenticity using a trained Logistic Regression model.")

# Load the saved model and vectorizer
# Use st.cache_resource to cache the model loading
@st.cache_resource
def load_resources():
    try:
        loaded_model = joblib.load('fake_news_model.pkl')
        loaded_vectorizer = joblib.load('vectorizer.pkl')
        return loaded_model, loaded_vectorizer
    except FileNotFoundError:
        st.error("Model files not found. Please make sure 'fake_news_model.pkl' and 'vectorizer.pkl' are in the same directory.")
        return None, None

loaded_model, loaded_vectorizer = load_resources()

if loaded_model and loaded_vectorizer:

    # --- RSS Feed Analysis Section ---
    st.header("Analyze RSS Feed")
    rss_url = st.text_input("Enter RSS Feed URL:", "https://feeds.bbci.co.uk/news/rss.xml")

    if st.button("Analyze Feed"):
        if rss_url:
            with st.spinner("Analyzing feed..."):
                try:
                    feed = feedparser.parse(rss_url)

                    if feed.entries:
                        st.subheader("Analysis Results:")
                        for entry in feed.entries:
                            title = entry.title
                            text = entry.summary if hasattr(entry, 'summary') else (entry.description if hasattr(entry, 'description') else '')

                            predicted_label = predict_fake_news(title, text)

                            with st.expander(f"**Title:** {title}"):
                                st.write(f"**Predicted Label:** {predicted_label}")
                                if text:
                                    st.write("**Article Snippet:**")
                                    st.write(text[:500] + "...")
                                else:
                                     st.write("**No article text available.**")
                            st.markdown("---")
                    else:
                        st.warning("No entries found in the RSS feed.")
                except Exception as e:
                    st.error(f"Error fetching or processing the RSS feed: {e}")
        else:
            st.warning("Please enter an RSS Feed URL.")

    st.markdown("---") # Separator

    # --- Manual Text Input Section ---
    st.header("Analyze Custom Text")
    manual_title = st.text_input("Enter News Title:")
    manual_text = st.text_area("Enter News Content:")

    if st.button("Analyze Text"):
        if manual_title or manual_text:
            with st.spinner("Analyzing text..."):
                predicted_label_manual = predict_fake_news(manual_title, manual_text)
                st.subheader("Analysis Result:")
                st.write(f"**Predicted Label:** {predicted_label_manual}")
        else:
            st.warning("Please enter a title or content to analyze.")