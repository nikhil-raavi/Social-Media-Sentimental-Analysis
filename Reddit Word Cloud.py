#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from pymongo import MongoClient


# ### Fetching Reddit data from MongoDb database

# In[2]:


connectionURL = 'mongodb://abhist:abhist@ac-9o2aihs-shard-00-00.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-01.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-02.iyatkxl.mongodb.net:27017/?ssl=true&replicaSet=atlas-7rmkeo-shard-0&authSource=admin&retryWrites=true&w=majority'
redditData = pd.DataFrame()
client = MongoClient(connectionURL)
dbs = client['5nyc'];
collection = dbs['reddit']
redditData = redditData.append(pd.DataFrame(list(collection.find())))


# ### Combining all the data to one single string and storing them in lowercase

# In[3]:


finalText = " ".join(record.selftext.lower() for index, record in redditData.iterrows())


# In[4]:


finalText


# ### Building word cloud from the subreddit comments.

# In[5]:


word_cloud = WordCloud(collocations = False, background_color = 'white').generate(finalText)


# In[6]:


plt.figure(figsize = (18, 7), facecolor = None)
plt.imshow(word_cloud)
plt.axis("off")
plt.show()

