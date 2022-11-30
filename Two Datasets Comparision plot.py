#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[ ]:


import numpy as np
import pandas as pd
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from matplotlib import pyplot
import seaborn as sns
from tabulate import tabulate


# ### Downloading the required libraries like stop words etc.,

# In[ ]:


nltk.download("vader_lexicon", quiet=True)
nltk.download("stopwords")
import PIL
from PIL import Image 


# ### Collecting data from YouTube

# In[ ]:


connectionURL = 'mongodb://abhist:abhist@ac-9o2aihs-shard-00-00.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-01.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-02.iyatkxl.mongodb.net:27017/?ssl=true&replicaSet=atlas-7rmkeo-shard-0&authSource=admin&retryWrites=true&w=majority'
utubedata = pd.DataFrame()
client = MongoClient(connectionURL)
dbs = client['5nyc'];
collection = dbs['youtube']
utubedata = utubedata.append(pd.DataFrame(list(collection.find())))


# ### Collecting data from Reddit

# In[ ]:


redditdata = pd.DataFrame()
collection = dbs['reddit']
redditdata = redditdata.append(pd.DataFrame(list(collection.find())))


# ### Definition for Score calculation and categorizing either comment is Negative or Neutral or Positive

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
# 
# *   Removing extra White Space
# *   Replacing newlines with single space
# *   Removing Tags and Hyper Links
# *   Removing Punctuations, Emoticons and Special Characters
# *   Converting to Lowercase
# *   Removing Numbers
# *   Removing Hashtags
# *   Removing Stopwords
# 

# In[ ]:


def cleaningYouTube(dataframe: pd.DataFrame) -> pd.DataFrame:
    # logger.info("Cleaning data for analysis...")

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

# In[ ]:


def analyzing(dataframe: pd.DataFrame) -> pd.DataFrame:
    
    # logger.info("Performing sentiment analysis on comments...")

    analyzer = SentimentIntensityAnalyzer()

    dataframe["Sentiment Score"] = dataframe["Cleaned Comment Text"].apply(
        lambda comment: scoreCalculation(analyzer, comment)
    )

    dataframe["Sentiment"] = dataframe["Sentiment Score"].apply(
        lambda score: scoreCategorization(score)
    )
    

    return dataframe


# ### Cleaning Reddit Data, and following the same steps same as YouTube data

# In[ ]:


def cleaningReddit(dataframe: pd.DataFrame) -> pd.DataFrame:
    # logger.info("Cleaning data for analysis...")

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


# ### Graph and Table which represents the following:
# * In the below plot we have various categories for example a base categories are ['YouTube', 'Reddit'] are plotted on x-axis. 
# * The y-axis contains the 'Sentiment Scores' analyzed in the above defintions
# * The plot is categorized based on 'Sentiment' category
# * The aggregation function we used is 'count' which represents the comparision between YouTube and Reddit data that which data set contains how many Positive, Negative or Neutral comments.
# 
# 
# * Finally, we have tabulated the graph result in table format using pivot table.

# In[ ]:


if __name__ == '__main__':
  df = pd.DataFrame(utubedata, columns=["CommentText", "VideoID"])
  df['type'] = 'YouTube'
  cleaned = cleaningYouTube(df)
  results = analyzing(cleaned)
  utuberesults = results[['type', 'Sentiment Score', 'Sentiment']].copy()

  df = pd.DataFrame(redditdata, columns=["selftext", "subreddit"])
  df['type'] = 'Reddit'
  cleaned = cleaningReddit(df)
  results = analyzing(cleaned)
  redditresults =  results[['type', 'Sentiment Score', 'Sentiment']].copy()

  results_df = pd.DataFrame()
  results_df = results_df.append(utuberesults)
  results_df = results_df.append(redditresults)
  
  # fig, ax = pyplot.subplots(figsize=(20,10))
  sns.catplot(data=results_df, x="type", y="Sentiment Score", hue = "Sentiment", height=10)

  table = pd.pivot_table(results_df, values='Sentiment Score', index=['type'],

                    columns=['Sentiment'], aggfunc='count')

  print(tabulate(table, headers='keys', tablefmt='fancy_grid'))

