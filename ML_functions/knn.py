import pandas as pd
import numpy as np
from scipy import spatial
import operator
import sys

# Get ratings people give to movies
r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('/home/ninad/workspace/movie_rcm/hello_world/u.data', sep='\t', names=r_cols, usecols=range(3))

# Divide film ratings into total size and average
movieProperties = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})

# Normalize rating sizes of movies
movieNumRatings = pd.DataFrame(movieProperties['rating']['size'])
movieNormalizedNumRatings = movieNumRatings.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))

# Get film data
movieDict = {}
with open('/home/ninad/workspace/movie_rcm/hello_world/u.item', mode='r', encoding="ISO-8859-1") as f:
    temp = ''
    for line in f:
        fields = line.rstrip('\n').split('|')
        movieID = int(fields[0])
        name = fields[1]
        genres = fields[5:25]
        genres = list(map(int, genres))
        movieDict[movieID] = (name, genres, movieNormalizedNumRatings.loc[movieID].get('size'),
                              movieProperties.loc[movieID].rating.get('mean'))
# Function to calculate distances between movies
def ComputeDistance(a, b):
    genresA = a[1]			#name of that movie user entered
    genresB = b[1]			#name of every movie in for loop
    genreDistance = spatial.distance.cosine(genresA, genresB)
    popularityA = a[2]
    popularityB = b[2]
    popularityDistance = abs(popularityA - popularityB)
    return genreDistance + popularityDistance


# Get the neighbor K of the given film
def getNeighbors(movieID, K):
    distances = []
    for movie in movieDict:
        if (movie != movieID):
            dist = ComputeDistance(movieDict[movieID], movieDict[movie])
            #print(movieDict[movieID], movieDict[movie])
            distances.append((movie, dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(K):
        neighbors.append(distances[x][0])
    return neighbors

movies = []

K = 10
avgRating = 0

mvs = pd.read_csv('/home/ninad/workspace/movie_rcm/hello_world/movies.csv')

mv_name = sys.argv[1]#input("Enter movie name : ")#
mvs.set_index('movieId', inplace=True)
movieID = mvs.index[mvs['title'].str.contains(mv_name)].tolist()
movie_id = movieID[0]
#movie_id = int(3)#int(sys.argv[1])

neighbors = getNeighbors(movie_id, K)
#print("5 Neighbors:")
for neighbor in neighbors:
    avgRating += movieDict[neighbor][3]
    #print(movieDict[neighbor][0] + " " + str(movieDict[neighbor][3]))
    movies.append([movieDict[neighbor][0],str(movieDict[neighbor][3])])


movies_df = pd.DataFrame(movies, columns=['Movie_Name','Avg_Rating'])
print(movies_df)
movies_df.to_csv("output_knn.csv")

#print(sys.argv[1])
