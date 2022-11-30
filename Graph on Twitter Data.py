#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[1]:


import pandas as pd
import numpy as np
from pymongo import MongoClient
import matplotlib.pyplot as plt


# ### Storing all the Mongo client connections

# In[2]:


connections = [
    'mongodb://abhist:abhist@ac-reqvybb-shard-00-00.06uvlcs.mongodb.net:27017,ac-reqvybb-shard-00-01.06uvlcs.mongodb.net:27017,ac-reqvybb-shard-00-02.06uvlcs.mongodb.net:27017/?ssl=true&replicaSet=atlas-oirygx-shard-0&authSource=admin&retryWrites=true&w=majority',
    'mongodb://abhist:abhist@ac-azdsz9t-shard-00-00.xxg837d.mongodb.net:27017,ac-azdsz9t-shard-00-01.xxg837d.mongodb.net:27017,ac-azdsz9t-shard-00-02.xxg837d.mongodb.net:27017/?ssl=true&replicaSet=atlas-5z4ubv-shard-0&authSource=admin&retryWrites=true&w=majority',
    'mongodb://abhist:abhist@ac-onyjlcw-shard-00-00.n7ldiv0.mongodb.net:27017,ac-onyjlcw-shard-00-01.n7ldiv0.mongodb.net:27017,ac-onyjlcw-shard-00-02.n7ldiv0.mongodb.net:27017/?ssl=true&replicaSet=atlas-njxi3v-shard-0&authSource=admin&retryWrites=true&w=majority'
]


# ### Fetching all the Twitter data from MongoDB clients

# In[3]:


final_data = pd.DataFrame()
for connection in connections:
  client = MongoClient(connection)
  dbs = client['5nyc'];
  collectionList = dbs.list_collection_names()
  collection = dbs[collectionList[0]]
  final_data = final_data.append(pd.DataFrame(list(collection.find())))


# ### Converting the date string to date format

# In[4]:


final_data['CreatedOn'] = final_data['CreatedOn'].dt.date


# ### Grouping the data by date tweet was created.

# In[5]:


groupeddf = final_data.groupby(['CreatedOn'])['_id'].agg('count').to_frame('count').reset_index()


# ### Plot describes the total tweets per day was collected from Twitter API

# In[7]:


groupeddf['count'] = groupeddf['count'].astype('int')
groupeddf.plot(x = 'CreatedOn', y = 'count', kind = 'bar', color='green')
plt.rcParams["figure.figsize"] = [20,10]
plt.xlabel('Tweet Collected On')
plt.ylabel('Frequency of Tweets')
plt.title('Tweets Collected per day')
plt.show()


# ## Filtering Data (i.e, video games or online games or pokemon or pokémon or dota or league of legends) from the whole 1% sample streaming data 

# In[8]:


filtereddf = pd.DataFrame()
for index,tweet in final_data.iterrows():
  if("video games" in tweet.Tweet_Text.lower() or "online games" in tweet.Tweet_Text.lower() or "pokemon" in tweet.Tweet_Text.lower() or "pokémon" in tweet.Tweet_Text.lower() or "dota" in tweet.Tweet_Text.lower() or "leagueoflegends" in tweet.Tweet_Text.lower() or "league of legends" in tweet.Tweet_Text.lower()):
    filtereddf = filtereddf.append(tweet, ignore_index = True)


# ### Grouping the tweet documents based on the date it was created.

# In[9]:


groupedfiltereddf = filtereddf.groupby(['CreatedOn'])['_id'].agg('count').to_frame('FilteredCount').reset_index()


# ### Plot for filtered Twitter data (i.e. pokemon, dota, league of legends or video games). It is different from above graph, because above plot represents 1% sample stream twitter data. 

# In[10]:


ax = groupeddf.plot(x='CreatedOn', y='count', kind='bar', title='Tweets Collected per Day', figsize=(20, 10))
ax.set_xlabel('Tweet Collcted On')
ax.set_ylabel('Frequency of Tweets')


# ## Comparing the Actual 1% streaming twitter data versus filtered twitter data

# In[11]:


groupeddf['FilteredCount'] = groupedfiltereddf['FilteredCount']


# In[12]:


ax = groupeddf.plot(x='CreatedOn', y=['count', 'FilteredCount'], kind='bar', title='1% Sample Data vs Online Video Games', figsize=(20, 10))
ax.set_xlabel('Tweet Collcted On')
ax.set_ylabel('Frequency of Tweets')

