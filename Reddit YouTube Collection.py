#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
from pymongo import MongoClient
from googleapiclient.discovery import build


# In[2]:


connectionURL = 'mongodb://abhist:abhist@ac-9o2aihs-shard-00-00.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-01.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-02.iyatkxl.mongodb.net:27017/?ssl=true&replicaSet=atlas-7rmkeo-shard-0&authSource=admin&retryWrites=true&w=majority'


# In[3]:


final_data = pd.DataFrame()
client = MongoClient(connectionURL)
dbs = client['5nyc'];
collection = dbs['reddit']
final_data = final_data.append(pd.DataFrame(list(collection.find())))
print(len(final_data))


# In[4]:


final_data.head()


# In[5]:


youtubeLinks = []
for index,item in final_data.iterrows():
  if "https://www.youtube.com/watch?v=" in item["selftext"]:
    youtubeLinks.append(item)

print(len(youtubeLinks))


# In[11]:


video_ids = []
for link in youtubeLinks:
  video_ids.append(link.selftext.split("https://www.youtube.com/watch?v=")[1][0:11])

video_ids



# In[18]:


youtube = build('youtube','v3',
                  developerKey="AIzaSyD6pmqJgnj5gKT7XMDRIqcJi-9_C0qNZlw")

for id in video_ids:
  # retrieve youtube video results
  video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=id
  ).execute()

  # print(json.dumps(video_response, indent=2))

  NoneValue = None
  youtubeComments_df = pd.DataFrame()
  for comment in video_response['items']:
    record = pd.DataFrame({
        # If it is a main comment, then store 1 i.e., CommentThread. Else store 0 i.e., reply to the comment.
        'IsCommentThread': 1 if comment["kind"] == "youtube#commentThread" else 0,
        'CommentID': comment["id"],
        'VideoID': comment["snippet"]["videoId"],
        'CommentText': comment["snippet"]['topLevelComment']["snippet"]['textOriginal'],
        'AuthorName': comment["snippet"]['topLevelComment']['snippet']['authorDisplayName'],
        'LikeCount': comment["snippet"]['topLevelComment']['snippet']['likeCount'],
        'PostedAt': comment['snippet']['topLevelComment']['snippet']['publishedAt'],
        'UpdatedAt': comment['snippet']['topLevelComment']['snippet']['updatedAt'],
        'TotalReplies': comment['snippet']['totalReplyCount'],
        'ParentCommentID': NoneValue
        }, index=[9])
    youtubeComments_df = youtubeComments_df.append(record);

    if comment['snippet']['totalReplyCount'] > 0:
      for reply in comment['replies']['comments']:
        record = pd.DataFrame({
            # If it is a main comment, then store 1 i.e., CommentThread. Else store 0 i.e., reply to the comment.
            'IsCommentThread': 0 if reply["kind"] == "youtube#comment" else 0,
            'CommentID': reply["id"],
            'VideoID': reply["snippet"]["videoId"],
            'CommentText': reply["snippet"]['textOriginal'],
            'AuthorName': reply["snippet"]['authorDisplayName'],
            'LikeCount': reply["snippet"]['likeCount'],
            'PostedAt': reply['snippet']['publishedAt'],
            'UpdatedAt': reply['snippet']['updatedAt'],
            'TotalReplies': 0,
            'ParentCommentID': reply['snippet']['parentId']
            }, index=[9])
        youtubeComments_df = youtubeComments_df.append(record);
  
  if('nextPageToken' in video_response):
    nextToken = video_response["nextPageToken"]
    while video_response:
      video_response = youtube.commentThreads().list(
              part = 'snippet,replies',
              videoId = id,
              pageToken = nextToken
          ).execute()

      for comment in video_response['items']:
        record = pd.DataFrame({
            # If it is a main comment, then store 1 i.e., CommentThread. Else store 0 i.e., reply to the comment.
            'IsCommentThread': 1 if comment["kind"] == "youtube#commentThread" else 0,
            'CommentID': comment["id"],
            'VideoID': comment["snippet"]["videoId"],
            'CommentText': comment["snippet"]['topLevelComment']["snippet"]['textOriginal'],
            'AuthorName': comment["snippet"]['topLevelComment']['snippet']['authorDisplayName'],
            'LikeCount': comment["snippet"]['topLevelComment']['snippet']['likeCount'],
            'PostedAt': comment['snippet']['topLevelComment']['snippet']['publishedAt'],
            'UpdatedAt': comment['snippet']['topLevelComment']['snippet']['updatedAt'],
            'TotalReplies': comment['snippet']['totalReplyCount'],
            'ParentCommentID': NoneValue
            }, index=[9])
        youtubeComments_df = youtubeComments_df.append(record);

        if comment['snippet']['totalReplyCount'] > 0 and 'replies' in comment:
          for reply in comment['replies']['comments']:
            record = pd.DataFrame({
                # If it is a main comment, then store 1 i.e., CommentThread. Else store 0 i.e., reply to the comment.
                'IsCommentThread': 0 if reply["kind"] == "youtube#comment" else 1,
                'CommentID': reply["id"],
                'VideoID': reply["snippet"]["videoId"],
                'CommentText': reply["snippet"]['textOriginal'],
                'AuthorName': reply["snippet"]['authorDisplayName'],
                'LikeCount': reply["snippet"]['likeCount'],
                'PostedAt': reply['snippet']['publishedAt'],
                'UpdatedAt': reply['snippet']['updatedAt'],
                'TotalReplies': 0,
                'ParentCommentID': reply['snippet']['parentId']
                }, index=[9]);
            youtubeComments_df = youtubeComments_df.append(record);

      if 'nextPageToken' in video_response:
        nextToken = video_response["nextPageToken"]
      else:
        break;
      # print(json.dumps(video_response, indent=2))
      # print("ABHIST: ")
  print(len(youtubeComments_df))
  
  # Santosh Personal MongoDB URL
  mongoDB_URL = "mongodb://abhist:abhist@ac-9o2aihs-shard-00-00.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-01.iyatkxl.mongodb.net:27017,ac-9o2aihs-shard-00-02.iyatkxl.mongodb.net:27017/?ssl=true&replicaSet=atlas-7rmkeo-shard-0&authSource=admin&retryWrites=true&w=majority"
  client = MongoClient(mongoDB_URL);

  db = client['5nyc']
  collection = db['youtube']
  for index, comment in youtubeComments_df.iterrows():
    key = comment.to_dict();
    value = { "$set": comment.to_dict() }

    collection.update_many(key, value, upsert=True)

print('Pushed YouTube Comments to MongoDB')

