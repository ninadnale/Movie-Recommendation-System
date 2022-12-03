#import sys
#output = "Hi %s, Welcome !!!" % (sys.argv[1])
#print(output)

#from django.test import TestCase

# Create your tests here.

import pandas as pd
import numpy as np
import sys

import matplotlib.pyplot as plt

#import plotly.plotly as py
#import plotly.graph_objs as go

movie = pd.read_csv('/home/ninad/workspace/movie_rcm/hello_world/movies.csv')
movie.set_index('movieId',inplace=True)

rating = pd.read_csv('/home/ninad/workspace/movie_rcm/hello_world/ratings.csv')
rating.set_index('movieId',inplace=True)

link = pd.read_csv('/home/ninad/workspace/movie_rcm/hello_world/links.csv',usecols = range(2))
link.set_index('movieId', inplace=True)

movie_ratings = pd.merge(movie,rating,on='movieId')

movie_ratings = pd.merge(movie_ratings,link,on='movieId')

overall_ratings = movie_ratings.groupby('movieId', as_index=True).rating.mean()
overall_ratings = overall_ratings.to_frame();

for_suggestion = movie_ratings.drop(labels=None, axis=0, index=None, columns={'userId','rating','timestamp'}, level=None, inplace=False, errors='raise')

userRatings = movie_ratings.pivot_table(index={'userId'}, columns={'title'}, values='rating')

corrMatrix = userRatings.corr(method='pearson', min_periods=50)

#userID = input("Enter user ID : ")
userID = int(sys.argv[1])
#userID=11

myRatings = userRatings.loc[userID].dropna()

to_be_dropped = myRatings.index

simCandidates = pd.Series()

for i in range(0, len(myRatings.index)):
    #print("Adding sims for "+myRatings.index[i]+"...")
    #Retrieve similar movies to one that user rated 
    sims = corrMatrix[myRatings.index[i]].dropna()
    #In above line dropna is used 'cause we don't want to take movies with NaN values
    #Now scale its similarity by how well user rated this movie
    sims = sims.map(lambda x:x * myRatings[i])
    #Add the score to the list of similarity candidates
    simCandidates = simCandidates.append(sims)
    
#Our RESULTS so far...
#print("\n\nsorting...\n")
print("The movies suggested for you are ...\n")
simCandidates.sort_values(inplace=True, ascending=False)

#print(simCandidates[:10])
#simCandidates
#print(simCandidates[-10:])

simCandidates = simCandidates.groupby(simCandidates.index).sum()
simCandidates.sort_values(inplace=True, ascending=False)
suggested = pd.DataFrame({'title':simCandidates.index, 'rating':simCandidates.values})

suggested.set_index('title', inplace=True)
suggested = pd.merge(suggested,for_suggestion,on='title')
suggested.set_index('title',inplace=False)
suggested = suggested.drop_duplicates()
suggested = suggested.rename(columns={'rating':'similarity_factor'})
suggested.set_index('imdbId',inplace=True)


suggested = suggested.head(15)
#sug_html = suggested.to_html()
suggested.to_csv('/home/ninad/workspace/movie_rcm/hello_world/output.csv')

"""
#CODE FOR 1ST GRAPH
year_specific0 = movie[movie['title'].str.contains('1990')]
period = ['1991','1992','1993','1994']

for ys in period:
    cy = movie[movie['title'].str.contains(ys)]
    year_specific0 = year_specific0.append(cy)
        
#year_specific0

hrr0 = year_specific0[year_specific0['genres'].str.contains('Horror')]
act0 = year_specific0[year_specific0['genres'].str.contains('Action')]
adv0 = year_specific0[year_specific0['genres'].str.contains('Adventure')]
drm0 = year_specific0[year_specific0['genres'].str.contains('Drama')]
com0 = year_specific0[year_specific0['genres'].str.contains('Comedy')]
chl0 = year_specific0[year_specific0['genres'].str.contains('Children')]
rom0 = year_specific0[year_specific0['genres'].str.contains('Romance')]
scf0 = year_specific0[year_specific0['genres'].str.contains('Sci-Fi')]

year_specific1 = movie[movie['title'].str.contains('1996')]
period = ['1997','1998','1999','2000']

for ys in period:
    cy = movie[movie['title'].str.contains(ys)]
    year_specific1 = year_specific1.append(cy)
        
#year_specific1

hrr1 = year_specific1[year_specific1['genres'].str.contains('Horror')]
act1 = year_specific1[year_specific1['genres'].str.contains('Action')]
adv1 = year_specific1[year_specific1['genres'].str.contains('Adventure')]
drm1 = year_specific1[year_specific1['genres'].str.contains('Drama')]
com1 = year_specific1[year_specific1['genres'].str.contains('Comedy')]
chl1 = year_specific1[year_specific1['genres'].str.contains('Children')]
rom1 = year_specific1[year_specific1['genres'].str.contains('Romance')]
scf1 = year_specific1[year_specific1['genres'].str.contains('Sci-Fi')]

year_specific2 = movie[movie['title'].str.contains('2001')]
period = ['2002','2003','2004','2005']

for ys in period:
    cy = movie[movie['title'].str.contains(ys)]
    year_specific2 = year_specific2.append(cy)
        
#year_specific2

hrr2 = year_specific2[year_specific2['genres'].str.contains('Horror')]
act2 = year_specific2[year_specific2['genres'].str.contains('Action')]
adv2 = year_specific2[year_specific2['genres'].str.contains('Adventure')]
drm2 = year_specific2[year_specific2['genres'].str.contains('Drama')]
com2 = year_specific2[year_specific2['genres'].str.contains('Comedy')]
chl2 = year_specific2[year_specific2['genres'].str.contains('Children')]
rom2 = year_specific2[year_specific2['genres'].str.contains('Romance')]
scf2 = year_specific2[year_specific2['genres'].str.contains('Sci-Fi')]

year_specific3 = movie[movie['title'].str.contains('2006')]
period = ['2007','2008','2009','2010']

for ys in period:
    cy = movie[movie['title'].str.contains(ys)]
    year_specific3 = year_specific3.append(cy)
        
#year_specific3

hrr3 = year_specific3[year_specific3['genres'].str.contains('Horror')]
act3 = year_specific3[year_specific3['genres'].str.contains('Action')]
adv3 = year_specific3[year_specific3['genres'].str.contains('Adventure')]
drm3 = year_specific3[year_specific3['genres'].str.contains('Drama')]
com3 = year_specific3[year_specific3['genres'].str.contains('Comedy')]
chl3 = year_specific3[year_specific3['genres'].str.contains('Children')]
rom3 = year_specific3[year_specific3['genres'].str.contains('Romance')]
scf3 = year_specific3[year_specific3['genres'].str.contains('Sci-Fi')]

year_specific4 = movie[movie['title'].str.contains('2011')]
period = ['2012','2013','2014','2015','2016']

for ys in period:
    cy = movie[movie['title'].str.contains(ys)]
    year_specific4 = year_specific4.append(cy)
        
#year_specific4

hrr4 = year_specific4[year_specific4['genres'].str.contains('Horror')]
act4 = year_specific4[year_specific4['genres'].str.contains('Action')]
adv4 = year_specific4[year_specific4['genres'].str.contains('Adventure')]
drm4 = year_specific4[year_specific4['genres'].str.contains('Drama')]
com4 = year_specific4[year_specific4['genres'].str.contains('Comedy')]
chl4 = year_specific4[year_specific4['genres'].str.contains('Children')]
rom4 = year_specific4[year_specific4['genres'].str.contains('Romance')]
scf4 = year_specific4[year_specific4['genres'].str.contains('Sci-Fi')]

d1 = {'Year_Span':['1990 to 1995','1996 to 2000','2001 to 2005','2006 to 2010','2011 to 2016'],'Horror':[len(hrr0),len(hrr1),len(hrr2),len(hrr3),len(hrr4)],'Action':[len(act0),len(act1),len(act2),len(act3),len(act4)],'Adventure':[len(adv0),len(adv1),len(adv2),len(adv3),len(adv4)],'Drama':[len(drm0),len(drm1),len(drm2),len(drm3),len(drm4)],'Comedy':[len(com0),len(com1),len(com2),len(com3),len(com4)],'Children':[len(chl0),len(chl1),len(chl2),len(chl3),len(chl4)],'Romance':[len(rom0),len(rom1),len(rom2),len(rom3),len(rom4)],'Sci-Fi':[len(scf0),len(scf1),len(scf2),len(scf3),len(scf4)]}

dfyrs = pd.DataFrame(data=d1)

mygraph = dfyrs.plot(kind='bar',stacked=True, legend=True, figsize=(10,6))
mygraph.set_xlabel("Time_Span (in yrs)")
mygraph.set_ylabel("Total Movies Produced")
mygraph.legend(loc='center left', bbox_to_anchor=(1,0.5))
mygraph.set_xticklabels(['1990-95','1996-00','2001-05','2006-10','2011-16'], rotation=45)
mygraph.set_title(" Analysis of Film Production over 1990 to 2016 ")

fig1 = mygraph.get_figure()
fig1.savefig("/home/ninad/workspace/movie_rcm/media/graph1.png")

#BELOW IS CODE FOR SECOND GRAPH

ageuser = pd.read_csv("/home/ninad/workspace/movie_rcm/hello_world/ageusers.csv", usecols=range(0,3))
ageuser.set_index('movieId')
ageuser.dropna()
ageuser = pd.merge(ageuser,link,on='movieId')
ageuser = pd.merge(ageuser,movie,on='movieId')
ageuser = ageuser.set_index('movieId')
#ageuser

agebelow20 = ageuser[ageuser.age<=20]

hrr_age0 = agebelow20[agebelow20['genres'].str.contains('Horror')]
act_age0 = agebelow20[agebelow20['genres'].str.contains('Action')]
adv_age0 = agebelow20[agebelow20['genres'].str.contains('Adventure')]
drm_age0 = agebelow20[agebelow20['genres'].str.contains('Drama')]
com_age0 = agebelow20[agebelow20['genres'].str.contains('Comedy')]
chl_age0 = agebelow20[agebelow20['genres'].str.contains('Children')]
rom_age0 = agebelow20[agebelow20['genres'].str.contains('Romance')]
scf_age0 = agebelow20[agebelow20['genres'].str.contains('Sci-Fi')]

age21to30 = ageuser[ageuser.age==21]
period = [22,23,24,25,26,27,28,29,30]

for a in period:
    ca = ageuser[ageuser.age==a]
    age21to30 = age21to30.append(ca)

hrr_age1 = age21to30[age21to30['genres'].str.contains('Horror')]
act_age1 = age21to30[age21to30['genres'].str.contains('Action')]
adv_age1 = age21to30[age21to30['genres'].str.contains('Adventure')]
drm_age1 = age21to30[age21to30['genres'].str.contains('Drama')]
com_age1 = age21to30[age21to30['genres'].str.contains('Comedy')]
chl_age1 = age21to30[age21to30['genres'].str.contains('Children')]
rom_age1 = age21to30[age21to30['genres'].str.contains('Romance')]
scf_age1 = age21to30[age21to30['genres'].str.contains('Sci-Fi')]

age31to40 = ageuser[ageuser.age==31]
period = [32,33,34,35,36,37,38,39,40]

for a in period:
    ca = ageuser[ageuser.age==a]
    age31to40 = age31to40.append(ca)

hrr_age2 = age31to40[age31to40['genres'].str.contains('Horror')]
act_age2 = age31to40[age31to40['genres'].str.contains('Action')]
adv_age2 = age31to40[age31to40['genres'].str.contains('Adventure')]
drm_age2 = age31to40[age31to40['genres'].str.contains('Drama')]
com_age2 = age31to40[age31to40['genres'].str.contains('Comedy')]
chl_age2 = age31to40[age31to40['genres'].str.contains('Children')]
rom_age2 = age31to40[age31to40['genres'].str.contains('Romance')]
scf_age2 = age31to40[age31to40['genres'].str.contains('Sci-Fi')]

age41to50 = ageuser[ageuser.age==41]
period = [42,43,44,45,46,47,48,49,50]

for a in period:
    ca = ageuser[ageuser.age==a]
    age41to50 = age41to50.append(ca)

hrr_age3 = age41to50[age41to50['genres'].str.contains('Horror')]
act_age3 = age41to50[age41to50['genres'].str.contains('Action')]
adv_age3 = age41to50[age41to50['genres'].str.contains('Adventure')]
drm_age3 = age41to50[age41to50['genres'].str.contains('Drama')]
com_age3 = age41to50[age41to50['genres'].str.contains('Comedy')]
chl_age3 = age41to50[age41to50['genres'].str.contains('Children')]
rom_age3 = age41to50[age41to50['genres'].str.contains('Romance')]
scf_age3 = age41to50[age41to50['genres'].str.contains('Sci-Fi')]

ageabove50 = ageuser[ageuser.age>=50]

hrr_age4 = ageabove50[ageabove50['genres'].str.contains('Horror')]
act_age4 = ageabove50[ageabove50['genres'].str.contains('Action')]
adv_age4 = ageabove50[ageabove50['genres'].str.contains('Adventure')]
drm_age4 = ageabove50[ageabove50['genres'].str.contains('Drama')]
com_age4 = ageabove50[ageabove50['genres'].str.contains('Comedy')]
chl_age4 = ageabove50[ageabove50['genres'].str.contains('Children')]
rom_age4 = ageabove50[ageabove50['genres'].str.contains('Romance')]
scf_age4 = ageabove50[ageabove50['genres'].str.contains('Sci-Fi')]

d2 = {'age_groups':['agebelow20','age21to30','age31to40','age41to50','ageabove50'],'Horror':[len(hrr_age0),len(hrr_age1),len(hrr_age2),len(hrr_age3),len(hrr_age4)],'Action':[len(act_age0),len(act_age1),len(act_age2),len(act_age3),len(act_age4)],'Adventure':[len(adv_age0),len(adv_age1),len(adv_age2),len(adv_age3),len(adv_age4)],'Drama':[len(drm_age0),len(drm_age1),len(drm_age2),len(drm_age3),len(drm_age4)],'Comedy':[len(com_age0),len(com_age1),len(com_age2),len(com_age3),len(com_age4)],'Children':[len(chl_age0),len(chl_age1),len(chl_age2),len(chl_age3),len(chl_age4)],'Romance':[len(rom_age0),len(rom_age1),len(rom_age2),len(rom_age3),len(rom_age4)],'Sci-Fi':[len(scf_age0),len(scf_age1),len(scf_age2),len(scf_age3),len(scf_age4)]}

dfags = pd.DataFrame(data=d2)
dfags

scndgraph = dfags.plot(kind='bar',stacked=True, legend=True, figsize=(10,6))
scndgraph.set_xlabel("Age Groups")
scndgraph.set_ylabel("No of Movies")
scndgraph.legend(loc='center left', bbox_to_anchor=(1,0.5))
scndgraph.set_xticklabels(['Below20','21to30','31to40','41to50','Above50'], rotation=0)
scndgraph.set_title(" Agewise Analysis of Films Watched ")

fig2 = scndgraph.get_figure()
fig2.savefig("/home/ninad/workspace/movie_rcm/media/graph2.png")
"""
