#!/usr/bin/env python
# coding: utf-8

# In[57]:


import pandas as pd
data=pd.read_csv('C:\\Users\\Jack Wang\\Desktop\\ml-latest-small\\movies.csv')


# In[58]:


data


# In[59]:


data['Action']=''
data['Adventure']=''
data['Animation']=''
data['Children']=''
data['Comedy']=''
data['Crime']=''
data['Documentary']=''
data['Drama']=''
data['Fantasy']=''
data['Film-Noir']=''
data['Horror']=''
data['Musical']=''
data['Mystery']=''
data['Romance']=''
data['Sci-Fi']=''
data['Thriller']=''
data['War']=''
data['Western']=''


# In[60]:


for i in range (0,9742):
    for j in range (3,21):
        if data.iloc[i,2].find(list(data)[j])== -1:
            data.iloc[i,j]=0
        else:
            data.iloc[i,j]=1


# In[61]:


data

