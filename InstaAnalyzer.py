#!/usr/bin/env python
# coding: utf-8

# In[105]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

import os
import wget
import requests
import json
import random

import pandas as pd
import datetime

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


# In[113]:


class InstaAnalyzer:
    
    def __init__(self, influencer):
        self.driver = None
        self.username = 'mahsa.esk77'
        self.password = 'Ghadi385'
        self.query_hash = "cda12de4f7fd3719c0569ce03589f4c4"
        #self.links = {}
        self.mentions = []
        self.influencer = influencer
        self.filename = '{}.csv'.format(influencer)
    
    def open_chrome(self):
        self.driver = webdriver.Chrome('chromedriver.exe')
    
    def log_on_instagram(self):
        
        self.driver.get("http://www.instagram.com")
        
        try:
            cookies_alert = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept All")]'))).click()
        except:
            pass
        
        #find input boxes
        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        #enter username and password
        username.clear()
        username.send_keys(self.username)
        password.clear()
        password.send_keys(self.password)
        
        time.sleep(random.randint(5,10))
        #login
        button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

        try:
            save_info_alert = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
        except:
            pass
        try:
             turn_on_notif_alert = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
        except:
            pass
    
    def get_userid(self):
        self.driver.get("http://www.instagram.com/{}".format(self.influencer))
        userid = self.driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.id")
        return userid
    
    def get_json(self, userid):
        graphql_query_url = (
            'https://www.instagram.com/graphql/query/?query_hash={}'
            '&variables={{"reel_ids":{},"tag_names":[],"location_ids":[],'
            '"highlight_reel_ids":[],"precomposed_overlay":false,"show_story_viewer_list":true,'
            '"story_viewer_fetch_count":50,"story_viewer_cursor":"",'
            '"stories_video_dash_manifest":false}}'.format(self.query_hash, str([int(userid)])))
        
        self.driver.get(graphql_query_url)
        jsonfile = json.loads(self.driver.find_element_by_tag_name('body').text)
        
        return jsonfile

    def get_mentions_from_stories(self, json):
        stories = []
        for m in json['data']['reels_media']:
            user = m['user']['username']
            stories = m['items']

        
        for story in stories:
            if 'tappable_objects' not in story:
                continue
            for tappable_obj in story['tappable_objects']:
                if 'username' in tappable_obj:
                    if tappable_obj['username'] not in self.mentions:
                        self.mentions.append(tappable_obj['username'])
                        #self.links[self.influencer] = mentions
        
    def get_number_of_followers(self, i):
        if self.mentions:
            self.driver.get("http://www.instagram.com/{}".format(self.mentions[i]))
            followersElem = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
            followers = followersElem.get_attribute("title");
            return followers
        
    def get_mentions(self):
        return self.mentions
    
    def save_page(self, pageNames, times, followers):
        times = [dt.strftime(TIME_FORMAT) for dt in times]
        pd.DataFrame(data = {'PageName':pageNames, 'Time':times, 'Followers':followers}).to_csv(self.filename)

    def read_page(self):
        if not os.path.isfile(self.filename):
            return [], [], []
        df = pd.read_csv(self.filename, index_col=0)
        times = [datetime.datetime.strptime(t, TIME_FORMAT) for t in df['Time']]
        return df['Page Name'].tolist(), times, df['Followers'].tolist()
    
    def read_values(self):
        values= []
        with open(self.filename, 'r') as filehandle:
            for line in filehandle:
                if len(line) < 2:
                    continue
                v = line[:-1]
                values.append(v)
        return values
    
#     def write_time(self):
#         with open(self.filename, 'w') as filehandle:
#             dt = datetime.datetime.now()
#             filehandle.write(dt.strftime(TIME_FORMAT))


    def run(self):
        
        self.open_chrome()
        self.log_on_instagram() 
        userid = self.get_userid()
        time.sleep(random.randint(5,10))
        jsonfile = self.get_json(userid)
        self.get_mentions_from_stories(jsonfile)
        follower_count = self.get_number_of_followers(0)
        
        for i, mention in enumerate(self.mentions):
            follower_count = self.get_number_of_followers(i)
            print(follower_count)


# In[114]:


instaAnalyzer = InstaAnalyzer('taranehtj')


# In[115]:


instaAnalyzer.run()


# In[ ]:




