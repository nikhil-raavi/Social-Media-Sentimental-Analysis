#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[1]:


import pandas as pd
from datetime import datetime
from pymongo import MongoClient
import matplotlib.pyplot as plt


# ### Fetching Reddit Data from MongoDB

# In[2]:


connectionURL = 'mongodb://abhist:abhist@ac-9o2aihs-shard-00-00.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-01.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-02.iyatkxl.mongodb.net:27017/?ssl=true&replicaSet=atlas-7rmkeo-shard-0&authSource=admin&retryWrites=true&w=majority'
redditdata = pd.DataFrame()
client = MongoClient(connectionURL)
dbs = client['5nyc'];
collection = dbs['reddit']
redditdata = redditdata.append(pd.DataFrame(list(collection.find())))


# #### Our Reddit contains Subreddits like r/pokemon, r/leagueoflegends and r/politics. 
# #### This File is for plotting hourly data for r/politics subreddits. So, below code filters the r/politics posts comments 

# In[3]:


politics = pd.DataFrame()
for index, reddit in redditdata.iterrows():
  if reddit.subreddit == 'politics':
    politics = politics.append(reddit)


# ### Converting the 'Created time' column to 'mm/dd/yyyy HH:MM:SS' format.

# In[4]:


redditdata['Created time'] = redditdata['Created time'].astype(int)


# In[5]:


from pandas.core.common import temp_setattr
politics['date'] = None
politics['date1'] = None
for index, row in politics.iterrows():
  temp = datetime.utcfromtimestamp(row['Created time'])
  politics.loc[index, 'date'] = temp

politics['date'] = pd.to_datetime(politics['date'])
# for index, row in politics.iterrows():
politics['date1'] = politics['date'].dt.strftime('%m/%d/%Y %H:00:00')

# redditdata['date'] = datetime.utcfromtimestamp(redditdata['Created time'])


# In[6]:


politicsgroupeddf = politics.groupby(['date1'])['_id'].agg('count').to_frame('count').reset_index()


# ## Below code plots bar chart displaying hourly count of 'r/politics' subreddit posts.

# In[8]:


politicsgroupeddf['count'] = politicsgroupeddf['count'].astype('int')
politicsgroupeddf.plot(x = 'date1', y = 'count', kind = 'bar', color='green')
plt.rcParams["figure.figsize"] = [25,15]
plt.xlabel('Sub-Reddit Collected On')
plt.ylabel('Frequency of posts')
plt.title('r/politics collected on hourly basis')
plt.show()

