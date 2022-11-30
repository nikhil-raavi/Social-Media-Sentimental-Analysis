#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[1]:


import pandas as pd
import json
import pymongo
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns


# ### Fetching YouTube data from MongoDB database

# In[3]:


connectionURL = 'mongodb://abhist:abhist@ac-9o2aihs-shard-00-00.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-01.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-02.iyatkxl.mongodb.net:27017/?ssl=true&replicaSet=atlas-7rmkeo-shard-0&authSource=admin&retryWrites=true&w=majority'
utubedata = pd.DataFrame()
client = MongoClient(connectionURL)
dbs = client['5nyc'];
collection = dbs['youtube']
utubedata = utubedata.append(pd.DataFrame(list(collection.find())))


# ### Downloading the stopwords.

# In[4]:


nltk.download("vader_lexicon", quiet=True)
nltk.download("stopwords")


# ### Definitions for Score calculation and categorizing either comment is Negative or Neutral or Positive

# In[10]:


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

# In[6]:


def cleaning(dataframe: pd.DataFrame) -> pd.DataFrame:
  dataframe["Cleaned Comment Text"] = (
      dataframe["CommentText"]
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

# In[7]:


def analyzing(dataframe: pd.DataFrame) -> pd.DataFrame:
  analyzer = SentimentIntensityAnalyzer()

  dataframe["Sentiment Score"] = dataframe["Cleaned Comment Text"].apply(
      lambda comment: scoreCalculation(analyzer, comment)
  )

  dataframe["Sentiment"] = dataframe["Sentiment Score"].apply(
      lambda score: scoreCategorization(score)
  )
  return dataframe


# In[8]:


def main():
  df = pd.DataFrame(utubedata, columns=["CommentText", "VideoID"])
  cleaned_df = cleaning(df)
  results_df = analyzing(cleaned_df)

  sns.catplot(data=results_df, x="VideoID", y="Sentiment Score", hue = "Sentiment",  kind = "swarm",  height=10)


# ### Plotting the different sentiments calculated for different video's. Video links are extracted from Twitter tweets.

# In[12]:


if __name__ == '__main__':
    main()

