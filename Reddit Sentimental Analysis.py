#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[ ]:


import pandas as pd
import json
import pymongo
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns


# ### Fetching Reddit data from MongoDB database 

# In[ ]:


connectionURL = 'mongodb://abhist:abhist@ac-9o2aihs-shard-00-00.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-01.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-02.iyatkxl.mongodb.net:27017/?ssl=true&replicaSet=atlas-7rmkeo-shard-0&authSource=admin&retryWrites=true&w=majority'
redditdata = pd.DataFrame()
client = MongoClient(connectionURL)
dbs = client['5nyc'];
collection = dbs['reddit']
redditdata = redditdata.append(pd.DataFrame(list(collection.find())))


# ### Downloading the stopwords.

# In[ ]:


nltk.download("vader_lexicon", quiet=True)
nltk.download("stopwords")


# ### Definitions for Score calculation and categorizing either comment is Negative or Neutral or Positive

# In[ ]:


def scoreCalculation(analyzer: SentimentIntensityAnalyzer, text: str) -> float:
  scores = analyzer.polarity_scores(text)
  return scores["compound"]

def scoreCategorization(score) -> str:   
  sentiment = ""
  if score <= -0.5:
      sentiment = "Negative"
  elif -0.5 < score <= 0.5:
      sentiment = "Neutral"
  else:
      sentiment = "Positive"
  
  return sentiment


# ### Cleaning the Data by removing the following:
# 
# *    Removing extra White Space
# *    Replacing newlines with single space
# *    Removing Tags and Hyper Links
# *    Removing Punctuations, Emoticons and Special Characters
# *    Converting to Lowercase
# *    Removing Numbers
# *    Removing Hashtags
# *    Removing Stopwords
# 

# In[ ]:


def cleaningReddit(dataframe: pd.DataFrame) -> pd.DataFrame:
  dataframe["Cleaned Comment Text"] = (
      dataframe["selftext"]
      .str.strip()
      .str.replace("\n", " ")
      .str.replace(r"(?:\@|http?\://|https?\://|www)\S+", "", regex=True)
      .str.replace(r"[^\w\s]+", "", regex=True)
      .str.lower()
      .str.replace(r"\d+", "", regex=True)
      .str.replace(r"#\S+", " ", regex=True)
  )

  stop_words = stopwords.words("english")
  dataframe["Cleaned Comment Text"] = dataframe["Cleaned Comment Text"].apply(
      lambda comment: " ".join([word for word in comment.split() if word not in stop_words])
  )
  
  return dataframe


# ### Analyzing the Reddit and YouTube Data

# In[ ]:


def analyzing(dataframe: pd.DataFrame) -> pd.DataFrame:
  analyzer = SentimentIntensityAnalyzer()
  dataframe["Sentiment Score"] = dataframe["Cleaned Comment Text"].apply(
      lambda comment: scoreCalculation(analyzer, comment)
  )
  dataframe["Sentiment"] = dataframe["Sentiment Score"].apply(
      lambda score: scoreCategorization(score)
  )
  return dataframe


# In[ ]:


def main():
  df = pd.DataFrame(redditdata, columns=["selftext", "subreddit"])
  cleaned_df = cleaningReddit(df)
  results_df = analyzing(cleaned_df)

  plt.figure(figsize=(17, 10))
  sns.countplot(data=results_df, x='subreddit', hue = "Sentiment")
  # sns.catplot(data=results_df, x="VideoID", y="Sentiment Score", hue = "Sentiment",  kind = "swarm",  height=10)


# ### Plotting all subreddits posts after performing sentimental analysis, which shows the r/politics contains more neutral comments, while other subreddits contains mixed sentimentals. 

# In[ ]:


if __name__ == '__main__':
    main()

