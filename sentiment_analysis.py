import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from database import insert_data, connect

CLIENT_ID = "kkToVl9TgRgfXcB6e_mOAA"
CLEINT_SECRET = "zMIwVRhzPe32E336yGyBpUvVQmhCow"
USER_AGENT = "sentiment_analysis:v1.0 (by /u/eathumanspetcats)"

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLEINT_SECRET,
    user_agent=USER_AGENT
)

def fetch_and_store_posts(username, limit=100):
    try:
        user = reddit.redditor(username)
        posts = [submission.title for submission in user.submissions.new(limit=limit)]
        comments = [comment.body for comment in user.comments.new(limit=limit)]
        all_data = posts + comments

        for text in all_data:
            insert_data(username, text)

        # debugging print(f"Fetched and stored {len(all_data)} posts/comments from u/{username}")
        return all_data 
    except Exception as e:
        print(f"Error: {e}")
        return [] 


def analyze_and_update_sentiment(username):
    try:
        conn, cursor = connect()
        query = "SELECT id, text FROM sentiment_data WHERE username = %s"
        cursor.execute(query, (username,))
        rows = cursor.fetchall()

        analyzer = SentimentIntensityAnalyzer()
        sentiments = []
        for row in rows:
            text_id, text = row
            sentiment = analyzer.polarity_scores(text)
            if sentiment['compound'] >= 0.05:
                sentiment_label = "Positive"
            elif sentiment['compound'] <= -0.05:
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"
                

            update_query = "UPDATE sentiment_data SET sentiment = %s WHERE id = %s"
            cursor.execute(update_query, (sentiment_label, text_id))
            conn.commit()
            sentiments.append(sentiment_label)

        # debugginggggg print(f"Updated sentiment for u/{username}")
        #return sentiments
    except Exception as e:
        print(f"Error: {e}")
        return []