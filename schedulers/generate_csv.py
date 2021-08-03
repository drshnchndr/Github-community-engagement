import pymongo
import requests
import json
import numpy as np
import pandas as pd
import time
import datetime
from bson.json_util import dumps, loads

# d1 = datetime.datetime.strptime("2021-05-01", '%Y-%m-%d')
# d2 = datetime.datetime.today()
# difference = d2-d1
# print(difference.days)
# dti = pd.date_range("2021-05-01", periods=difference.days+1, freq="D")
# print(dti[-1])

def generateIssuesCSV():

    mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    repodb = mongo_client["repo_collector"]
    collection = repodb["repo_issuesV1.1"]

    cursor = collection.find({})
    # print(type(cursor))
    mongo_client.close()
    list_cur = list(cursor)
    df = pd.DataFrame(list_cur)
    # print(df.head(5))
    # print(list(df.columns))

    issues_df = df[['id','html_url', 'title', 'body', 'state', 'labels', 'user', 'comments', 'created_at', 'updated_at', 'closed_at', 'org_id', 'repo_id']]
    print(issues_df.columns)

    issues_df['label'] = df['labels'].apply(lambda values: [v['name'] for v in values])
    del issues_df['labels']

    
    # issues_df['created_by'] = issues_df['user'].apply(lambda x: x['login'])
    # issues_df['user_type'] = issues_df['user'].apply(lambda x: x['type'])
    issues_df['user_id']=issues_df['user'].str['id']
    issues_df['created_by']=issues_df['user'].str['login']
    issues_df['user_type']=issues_df['user'].str['type']

    del issues_df['user']
    # print(issues_df.columns)
    issues_df.to_csv('Issues.csv', index=False)

def generateIssueCommentCSV():

    mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    repodb = mongo_client["repo_collector"]
    collection = repodb["repo_commentsV1.1"]

    cursor = collection.find({})
    # print(type(cursor))
    mongo_client.close()
    list_cur = list(cursor)
    df = pd.DataFrame(list_cur)
    # print(df.head(5))
    # print(list(df.columns))

    comments_df = df[['id','issue_id', 'author_association', 'body', 'user', 'created_at', 'org_id', 'repo_id']]
    print(comments_df.columns)

    comments_df['created_by']=comments_df['user'].str['login']
    comments_df['user_id']=comments_df['user'].str['id']

    del comments_df['user']
    print(comments_df.columns)
    comments_df.to_csv('IssueComments.csv', index=False)

def generateEventsCSV():

    mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    repodb = mongo_client["repo_collector"]
    collection = repodb["repo_eventsV1.1"]

    cursor = collection.find({})
    # print(type(cursor))
    mongo_client.close()
    list_cur = list(cursor)
    df = pd.DataFrame(list_cur)
    # print(df.head(5))
    # print(list(df.columns))

    events_df = df[['id','issue_id', 'event', 'actor', 'created_at', 'org_id', 'repo_id']]
    print(events_df.columns)

    events_df['created_by']=events_df['actor'].str['login']
    events_df['user_type']=events_df['actor'].str['type']
    del events_df['actor']
    print(events_df.columns)

    events_df.to_csv('Events.csv', index=False)

def generateReleasesCSV():

    mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    repodb = mongo_client["repo_collector"]
    collection = repodb["repo_releases"]

    cursor = collection.find({})
    # print(type(cursor))
    mongo_client.close()
    list_cur = list(cursor)
    df = pd.DataFrame(list_cur)
    # print(df.head(5))
    # print(list(df.columns))

    releases_df = df[['id','name', 'tag_name', 'created_at','published_at', 'org_id', 'repo_id', 'body']]
    
    print(releases_df.columns)

    releases_df.to_csv('Releases.csv', index=False)

def generateRepoUsersCSV():

    mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    repodb = mongo_client["repo_collector"]
    collection = repodb["repo_users"]

    contributor_user_cursor = collection.find({'isContributor':1, 'type':'User'})
    contributor_ann_cursor = collection.find({'isContributor':1, 'type':'Anonymous'})
    member_cursor = collection.find({'isMember':1})
    # print(type(cursor))
    mongo_client.close()
    list_contributors_ann = list(contributor_ann_cursor)
    df = pd.DataFrame(list_contributors_ann)
    # print(df.head(5))
    # print(list(df.columns))
    contributors_ann_df = df[['name', 'type','org_id', 'repo_id','isContributor', 'contributions']]

    list_contributors_user = list(contributor_user_cursor)
    df = pd.DataFrame(list_contributors_user)

    contributors_user_df = df[['login', 'type','org_id', 'repo_id','isContributor', 'contributions']]
    contributors_user_df.columns = ['name', 'type','org_id', 'repo_id','isContributor', 'contributions']
    
    contributors_df = contributors_ann_df.append(contributors_user_df, sort=False)

    list_members = list(member_cursor)
    df = pd.DataFrame(list_members)

    members_df = df[['login', 'type','org_id', 'repo_id', 'isContributor']]
    members_df.columns = ['name', 'type','org_id', 'repo_id','isContributor']
    users_df = members_df.append(contributors_df, sort=False)
    
    print(users_df.columns)

    users_df.to_csv('Users.csv', index=False)

def generatePullsCSV():

    mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    repodb = mongo_client["repo_collector"]
    collection = repodb["repo_pulls"]

    cursor = collection.find({})
    # print(type(cursor))
    mongo_client.close()
    list_cur = list(cursor)
    df = pd.DataFrame(list_cur)
    # print(df.head(5))
    # print(list(df.columns))

    pulls_df = df[['id','title', 'user', 'state', 'created_at','closed_at','merged_at', 'org_id', 'repo_id']]

    pulls_df['created_by']=pulls_df['user'].str['login']
    pulls_df['user_type']=pulls_df['user'].str['type']
    del pulls_df['user']
    
    print(pulls_df.columns)

    pulls_df.to_csv('Pulls.csv', index=False)

# generateIssuesCSV()
# generateIssueCommentCSV()
generateRepoUsersCSV()
# generateEventsCSV()
# generateReleasesCSV()
# generatePullsCSV()