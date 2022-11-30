#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[1]:


import pandas as pd
from pymongo import MongoClient
from tabulate import tabulate


# ### Fetching YouTube data from MongoDB

# In[2]:


connectionURL = 'mongodb://abhist:abhist@ac-9o2aihs-shard-00-00.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-01.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-02.iyatkxl.mongodb.net:27017/?ssl=true&replicaSet=atlas-7rmkeo-shard-0&authSource=admin&retryWrites=true&w=majority'
utubedata = pd.DataFrame()
client = MongoClient(connectionURL)
dbs = client['5nyc'];
collection = dbs['youtube']
utubedata = utubedata.append(pd.DataFrame(list(collection.find())))


# ### Creating Pivot table on YouTube data and grouping them by different video sources. Displaying the Total Number of Comment Threads, Likes and Replies.

# In[3]:


pivot = pd.pivot_table(
    data = utubedata,
    index = 'VideoID',
    aggfunc = 'sum'
)


# In[4]:


print(tabulate(pivot, headers = 'keys', tablefmt='fancy_grid'))


# ## From above table we have grouped the data by 'VideoID' column and extracting the summary of Comment Threads, Likes and Replies for each Comment Thread.
# * As we can see VideoID "jHk45HIGUtE" has 712 comment threads, 28494 likes and 1060 total replies.
# * For VideoID "rXTIWlbRtts" has 1 comment threads, 0 likes and 0 total replies
# * For VideoID "zInThheL0L8" has 6 comment threads, 9 likes and 13 total replies 
