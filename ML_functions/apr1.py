import numpy as np
import pandas as pd

df=pd.read_csv('ratings.csv')

movie_titles = pd.read_csv("movies.csv")

df=pd.merge(df,movie_titles,on='movieId')

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')

df=df[df['rating']>=3]
df=df.sort_values('userId')


moviemat = df.pivot_table(index='userId',columns='movieId',values='title',aggfunc='first')


# Data Preprocessing
transactions = []
for i in range(609):
    temp=[]
    for j in range(500):
        if(str(moviemat.values[i,j])!='nan'):
            temp.append(str(moviemat.values[i,j]))
    transactions.append(temp)

    
# Training Apriori on the dataset
from apyori import apriori
rules = apriori(transactions, min_support = 0.1, min_confidence = 0.5, min_lift = 3, min_length = 2)
    
results = list(rules)

res=pd.DataFrame(results)

res=res['items']
temp=[list(x) for x in res]
print(res)
