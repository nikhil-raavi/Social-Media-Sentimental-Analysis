#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[1]:


import pandas as pd
import numpy as np
from pymongo import MongoClient
import matplotlib.pyplot as plt


# ### MongoDB Client connection URLs

# In[2]:


connections = [
    'mongodb://abhist:abhist@ac-reqvybb-shard-00-00.06uvlcs.mongodb.net:27017,ac-reqvybb-shard-00-01.06uvlcs.mongodb.net:27017,ac-reqvybb-shard-00-02.06uvlcs.mongodb.net:27017/?ssl=true&replicaSet=atlas-oirygx-shard-0&authSource=admin&retryWrites=true&w=majority',
    'mongodb://abhist:abhist@ac-azdsz9t-shard-00-00.xxg837d.mongodb.net:27017,ac-azdsz9t-shard-00-01.xxg837d.mongodb.net:27017,ac-azdsz9t-shard-00-02.xxg837d.mongodb.net:27017/?ssl=true&replicaSet=atlas-5z4ubv-shard-0&authSource=admin&retryWrites=true&w=majority',
    'mongodb://abhist:abhist@ac-onyjlcw-shard-00-00.n7ldiv0.mongodb.net:27017,ac-onyjlcw-shard-00-01.n7ldiv0.mongodb.net:27017,ac-onyjlcw-shard-00-02.n7ldiv0.mongodb.net:27017/?ssl=true&replicaSet=atlas-njxi3v-shard-0&authSource=admin&retryWrites=true&w=majority'
]


# ### Collecting and Filtering Twitter Data

# In[3]:


final_data = pd.DataFrame()
for connection in connections:
  client = MongoClient(connection)
  dbs = client['5nyc'];
  collectionList = dbs.list_collection_names()
  collection = dbs[collectionList[0]]
  final_data = final_data.append(pd.DataFrame(list(collection.find())))
print(len(final_data))


# In[4]:


final_data['CreatedOn'] = final_data['CreatedOn'].dt.date


# In[11]:


filtereddf = pd.DataFrame()
for index,tweet in final_data.iterrows():
  if("video games" in tweet.Tweet_Text.lower() or "online games" in tweet.Tweet_Text.lower() or "pokemon" in tweet.Tweet_Text.lower() or "pokémon" in tweet.Tweet_Text.lower() or "dota" in tweet.Tweet_Text.lower() or "leagueoflegends" in tweet.Tweet_Text.lower() or "league of legends" in tweet.Tweet_Text.lower()):
    filtereddf = filtereddf.append(tweet, ignore_index = True)


# In[12]:


groupedfiltereddf = filtereddf.groupby(['CreatedOn'])['_id'].agg('count').to_frame('FilteredCount').reset_index()


# ### Collecting Reddit Data

# In[6]:


connectionURL = "mongodb://abhist:abhist@ac-9o2aihs-shard-00-00.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-01.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-02.iyatkxl.mongodb.net:27017/?ssl=true&replicaSet=atlas-7rmkeo-shard-0&authSource=admin&retryWrites=true&w=majority"


# In[7]:


redditdata = pd.DataFrame()
client = MongoClient(connectionURL)
dbs = client['5nyc'];
collection = dbs['reddit']
redditdata = redditdata.append(pd.DataFrame(list(collection.find())))


# ### Collecting YouTube Data

# In[8]:


youtubedata = pd.DataFrame()
collection = dbs['youtube']
youtubedata = youtubedata.append(pd.DataFrame(list(collection.find())))


# In[13]:


data = np.array([['Twitter', len(filtereddf)], ['Reddit', len(redditdata)], ['YouTube', len(youtubedata)]])
datasets = pd.DataFrame(data, columns=['Platform', 'DataCount'])


# ### Comparing the Three Data sets:

# ###### I am using Bar plot to represent the count of the documents in Twitter, Reddit and YouTube collections by fetching the data from MongoDB database.

# In[14]:


datasets['DataCount'] = datasets['DataCount'].astype('int')
ax = datasets.plot(x='Platform', y='DataCount', kind='bar', title='All 3 Datasets Plot (Comparing the Data Count)', figsize=(20, 10))
ax.set_xlabel('Platform')
ax.set_ylabel('Total Collections')

