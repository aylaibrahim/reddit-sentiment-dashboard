import streamlit as st
from collections import Counter
from sentiment_analysis import fetch_and_store_posts, analyze_and_update_sentiment
from database import fetch_sentiment_data
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

def preprocess_text(texts):
    preprocessed_texts = []
    for text in texts:
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        text = text.lower()
        preprocessed_texts.append(text)
    return preprocessed_texts

st.title("Reddit Sentiment Analysis")
username = st.text_input("Enter Reddit Username (u/username):")

if username:
    user_data = fetch_and_store_posts(username)

    if user_data:
        analyze_and_update_sentiment(username)

        sentiments = fetch_sentiment_data(username)

        preprocessed_data = preprocess_text(user_data)

        st.write(f"Fetched and analyzed {len(sentiments)} posts and comments combined from u/{username}")

        st.subheader("Sentiment Distribution")
        
        sentiment_counts = Counter(sentiments)
        labels = list(sentiment_counts.keys())
        sizes = list(sentiment_counts.values())

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['pink', 'lavenderblush', 'thistle'])
        st.pyplot(fig)

        st.subheader("Word Cloud")
        all_text = " ".join(preprocessed_data)
        
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap="PuRd_r").generate(all_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
    else:
        st.error("No data fetched. Please check the Reddit username and try again.")