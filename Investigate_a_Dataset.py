#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigating The Movie Database 
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### The data Overview: TMDB movies
#  This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue.
# Certain columns, like ‘cast’ and ‘genres’, contain multiple values separated by pipe (|) characters.
# There are some odd characters in the ‘cast’ column. Don’t worry about cleaning them. You can leave them as is.
# The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.
# 
# ### Questions i'll answer in this project:
#  **1-** Dose the movies budget have any kind of impact or relationship with the popularity?
#  
#  **2-** How it look the release year distrbution?
#  
#  
#  **3-** What is the the most popular genres ?
#  
#  **4-** What is the most popular movies with heighest votes in 2015 ?

# In[1]:


#  import all of the packages i plan to use.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib
matplotlib.style.use('ggplot')

get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wragling

# In[2]:


# import data that i'll anayze
tmdb=pd.read_csv('tmdb-movies.csv')
tmdb.head()


# In[3]:


tmdb.info()


# **colmuns have missing values:** imdb_id , cast , homepage , director , tagline , keywords , overview , runtime ,  genres , production_companies

# In[4]:


# describe the numaric variables
tmdb.describe()


# In[5]:


# describe the object variables
tmdb.describe(include='O')


# In[6]:


tmdb.shape


# ### Data Cleaning

#  **columns i'll not need in my analysis is:**
#  
#  id, imdb_id, cast, homepage, tagline, keywords, overview, production_companies, release_date
# 
#  and it's look like there's alot of zeros in budget_adj and revenue_adj which is not make sence. However, i don't need these columns for my analysis so i'll drop it too.
#  
# also, i'll try to deal with the column 'genres' because it have multiple values in the same row.
#  

# In[7]:


# drop columns we don't need
tmdb.drop(['id','imdb_id','cast','homepage','tagline','keywords','overview','production_companies','release_date',
           'budget_adj','revenue_adj'], 
        axis=1, inplace=True)


# In[8]:


# checking if they have been deleted or not
tmdb.head(1)


# In[9]:


# droping the missing valuse in my dataset
tmdb.dropna(inplace= True)


# In[10]:


tmdb.info()


# Now we removed all the missing values!

# In[11]:


# checking if there's any duplicate columns
tmdb.duplicated().sum()


# In[12]:


# removing the duplicate columns
tmdb.drop_duplicates(inplace=True)


# In[13]:


# removing rows with zeros values
tmdb= tmdb[(tmdb!= 0).all(axis=1)]


# In[17]:


tmdb.describe()


# Now we are sure we erased all the zero values.

# In[14]:


# delete the multiple values in genres by "|"
tmdb['genres'] = tmdb['genres'].apply(lambda x: x.split('|')[0])


# i tried to split it to multiple rows but it didn't worked so i decide to choose the first value only and delete the rest after the "|".

# In[48]:


tmdb.shape


# In[49]:


tmdb.head()


#  >now the genres column looks better after deleting the multiple values in row

# In[50]:


# making sure we don't have null values before we start exploratory
tmdb.isnull().sum()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
#  Now it's time to analyze my data and answer my questions after cleaning it.
# 
# ### Research Question 1 : Dose the movies budget have any kind of impact or relationship with the popularity?

# In[15]:


tmdb.plot(x='budget', y='popularity',title="the relationship between movies budget and the popularity",
          kind='scatter', figsize=(16,9));


# > the graph result shows budget are strongly correlated with popularity.

# ### Research Question 2 : How it look the release year distrbution?

# In[16]:


tmdb.release_year.hist();
plt.title("Release year distrbution")
plt.xlabel("Release year")
plt.ylabel("amount of movies")


# the release year look strongly left-skeewd distrbution. which is mean releasing movies is increasing in the last years.

# ### Research Question 3 : What is the the most popular genres ?

# In[53]:


tmdb.genres.unique()


# In[102]:


gen_pop =tmdb.groupby('genres').mean()['popularity']
indices = np.arange(len(gen_pop))
fig = plt.figure(figsize=(19,11))
# create labels
labels = ['Action', 'Adventure', 'Western', 'Science Fiction', 'Drama',
       'Family', 'Comedy', 'Crime', 'Romance', 'War', 'Thriller',
       'Fantasy', 'History', 'Mystery', 'Animation', 'Horror', 'Music',
       'Documentary', 'TV Movie']
# Create bars and labels
plt.bar(indices, gen_pop, color='purple', alpha=0.5, tick_label=labels)

# Add title and axis names
plt.title('The popularity by genres', size=17)
plt.xlabel('genres',size=15)
plt.ylabel('popularity',size=15);

# Show graphic
plt.show()


# it show's that animation and adventure are the popular genres and then become the rest.

# ### Research Question 4 : What is the most popular movies with high votes in 2015 ?

# In[55]:


x= tmdb.query('release_year > 2014 and vote_average > 7.5')


# In[84]:


x.plot("original_title", "popularity",kind="bar", title="The most popular movies with high votes in 2015", color="purple",
       alpha=0.5, figsize=(10,5));


# the graph shows The martian, inside out and Ex Machina was the three top of movies in 2015 with more than 7.5 vote average.

# <a id='conclusions'></a>
# ## Conclusions
# 
# **Results:**
# > first result i find budget are strongly correlated with popularity.
# 
# > next i've been thinking How it look the release year distrbution? then i found the release year is increasing in the last years in releasing movies and that pretty fun we need more great movies.
# 
# > i think most of us when we saw this data asked the same question "What is the the most popular genres?" and here's my findings it show's that animation and adventure are the popular genres and then become the rest.
# 
# > then i find The martian, inside out and Ex Machina was the three top of movies in 2015 with more than 7.5 vote average.
# 
# **Limitations:**
# > i found alot of missing data in some colmuns and zeros values which is effected my analysis and reduced the rows in my dataset from 10866 row to only 3853 row from cleaning.
# 
# > i find it tough to split genres column because it have multiple values in some rows, i tried to split every value after the "|" in row but it did't work with me so i decide to delete all values after the first "|".

# In[18]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




