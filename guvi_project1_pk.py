

#installing SNSCRAPE library
#pip install snscrape #to be done in CMD
import streamlit as st


  

#importing required modules
import pandas as pd
import snscrape.modules.twitter as sntwitter
import datetime

#scraping the required data
def twitter_scrape(query,limit):
  scraper = sntwitter.TwitterSearchScraper(query)
  tweets=[]
  for i, tweet in enumerate(scraper.get_items()): #date, id, url, tweet content, user,reply count, retweet count,language, source, like count
    data = [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.replyCount
          ,tweet.retweetCount,tweet.lang, tweet.source,tweet.likeCount]
    tweets.append(data)
    if i == limit:
      break
  df = pd.DataFrame(tweets, columns=['date and time','id','content','user','reply','retweetcount','language','source','likecount'])
  return df

 #uploading dataframe to MongoDB 
def mongo_up(df):
  from pymongo import MongoClient #importing the MongoClient
  py = MongoClient(#enter your MongoDB url)
  p1 = py["Projects_GUVI"] #Creating a database
  project_collect = p1["Twitter_data"] #creating a collection
  project_collect.insert_many(df.to_dict('records')) #inserting the scraped values in the collection
  
#streamlit function
def streamlit():
  st.title("Twitter data scrapping")
  st.header("This is twitter scraper by Prathamesh.") 
  text = st.text_input("Text")
  htag = st.text_input("#Hashtag", placeholder = "Enter the hashtag", disabled = False, label_visibility='visible')
  uname = st.text_input("username", placeholder = "Enter the username", disabled = False, label_visibility='visible')
  startdt = st.date_input("Start date")
  enddt = st.date_input("End date")
  query = f"{text} (#{htag}) (from:{uname}) since:{startdt} until:{enddt}"
  limit=st.number_input("Max number of tweets", disabled = False, label_visibility = 'visible')
  limit = int(limit)
  data = twitter_scrape(query,limit)
  st.dataframe(data=data)
  if st.button("Upload"):
     mongo_up(data)
  st.download_button("Download CSV", data = data.to_csv(), file_name="CSV_data")
  st.download_button("Download json", data = data.to_json(), file_name="json_data")  
    
#calling the main function of streamlit    
maincall = streamlit()

