'''In this problem, the goal was to find what posts were getting the most up votes. So, I needed to filter results by top quantiles and then analyze entity names along with the
connotation names were used in and create data frames to output results. I also wanted to add a search and look feature in which a user can input an entity name and find all resulting titles involving that entity'''


import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()



   
data = pd.read_csv (r'/Users/chaitanya_andalkovil/Desktop/Python/Eluvio_DS_Challenge.csv')   #Reading in csv file into initial data
votes = pd.DataFrame(data, columns= ['up_votes'])       #Creating a dataset only factoring in up_votes for a filter that occupies less space
stats = np.percentile(votes.up_votes, 98.5)             #Looking at the 98.5 quantile to filter top 1.5 percent of up_voted posts
df = pd.DataFrame(data, columns = ['up_votes', 'title'])
filter_df = df['up_votes'] > stats            #Filter of boolean values
df_top = df[filter_df]                      #Applying the filter to a new dataframe


words = set(stopwords.words('english'))


df_top['title'] = df_top['title'].apply(lambda title: ' '.join([word for word in title.split() if word not in (words)]))  #Removing stopwords in Title column of dataframe




tokens = nlp(''.join(str(df_top.title.tolist())))       #Converting strings into tokens we can use to iterate through to determine entity
items = [title.text for title in tokens.ents]
Counter(items).most_common(30)

name_list = []
for ent in tokens.ents:             #Iterate through tokens for persons
    if ent.label_ == 'PERSON':
        name_list.append(ent.text)
        
name_counts = Counter(name_list).most_common(30)
df_names = pd.DataFrame(name_counts, columns =['Names', 'count'])

org_list = []
for ent in tokens.ents:             #Iterate through tokens for country/race entities
    if ent.label_ == 'NORP':
        org_list.append(ent.text)
        
org_counts = Counter(org_list).most_common(30)
df_org = pd.DataFrame(org_counts, columns =['Country/Race', 'count'])





for index, row in df_top.iterrows():                                        #iterate through df_top for each row title to analyze sentiment by assigning score values
    score = SentimentIntensityAnalyzer().polarity_scores(row['title'])
    neg = score['neg']
    pos = score['pos']
    if neg > pos:
        row['Sent'] = 'Negative'
    elif pos > neg:
        row['Sent'] = 'Positive'
    else:
        row['sent'] = 'Neutral'

print('***Emotion Analysis DataFrame with top 1.5% of up_voted posts***')       
print(df_top, end = '\n')
print('***Top 30 Entity Names***')
print(df_names, end = '\n')
print('***Top 30 Country/Race Entities***')
print(df_org, end = '\n')

list_names = df_names['Names'].to_list()
list_org = df_org['Country/Race'].to_list()
print(list_names)    
print('If you would like to see all results for certain entity, please enter entity name:')             #Filters df_top to show Entity titles input from user by creating lists with entity_names to iterate over
Entity = input()
df_top_temp = df_top
start = len(Entity)
if Entity not in list_names or list_org:
    print('Entity not found')
else:
    df_top['indexes']= data["title"].str.find(Entity, start)

    print(df_top[df_top['indexes'] > -1])





                  
    

