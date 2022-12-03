
###1. Load data 
import pandas as pd
all_ratings = pd.read_csv("u.data",delimiter="\t", header=None, names = ["UserID", "MovieID", "Rating", "Datetime"])
#print(all_ratings.head())
 
###2.Observe data
import pandas as pd 
#def rstr(df):
    #print('\n''Structure of Data:''\n','\n''Rows X Columns: ',df.shape,'\n''\n''Features and value:''\n',df.apply(lambda x:[x.unique()]))
#rstr(all_ratings)
 
###3.Preprocess data (add necessary features)
all_ratings["Favorable"] = all_ratings["Rating"] > 3
two_ratings=all_ratings[all_ratings['UserID'].isin(range(200))]
two_ratings["Datetime"] = pd.to_datetime(two_ratings['Datetime'], unit='s')
favorable_ratings = two_ratings[two_ratings["Favorable"]]
favorable_reviews_by_users = dict((k, frozenset(v.values)) 
    for k, v in favorable_ratings.groupby("UserID")["MovieID"])
num_favorable_by_movie = two_ratings[["MovieID", "Favorable"]].groupby("MovieID").sum()
#print(num_favorable_by_movie.sort_values(by="Favorable", ascending=False).head())
 
###4. Split the data(skipped)
###5. Build the Apriori model
###5.1 Build the frequent viewd and favorable movies
frequent_itemsets = {}
min_num_req=50
frequent_itemsets[1]=dict((frozenset((movie_id,)),row["Favorable"])
    for movie_id, row in num_favorable_by_movie.iterrows()
    if row["Favorable"] > min_num_req)
#print("There are {} movies with more than {} favorable reviews".format(len(frequent_itemsets[1]), min_num_req))
 
from collections import defaultdict
def find_frequent_itemsets(favorable_reviews_by_users, k_1_itemsets, min_num_req):
    counts = defaultdict(int)
    for user, reviews in favorable_reviews_by_users.items():
        for itemset in k_1_itemsets:
            if itemset.issubset(reviews):
                for other_reviewed_movie in reviews - itemset:
                    current_superset = itemset | frozenset((other_reviewed_movie,))
                    counts[current_superset] += 1
    return dict([(itemset, frequency) for itemset, frequency in counts.items() if frequency >= min_num_req])
 
for k in range(2, 20):
    # Generate candidates of length k, using the frequent itemsets of length k-1
    # Only store the frequent itemsets
    cur_frequent_itemsets = find_frequent_itemsets(favorable_reviews_by_users, frequent_itemsets[k-1],min_num_req)
    if len(cur_frequent_itemsets)==0:
        #print("Did not find any frequent itemsets of length {}".format(k))
        break
    else:
        #print("I found {} frequent itemsets of length {}".format(len(cur_frequent_itemsets), k))
        frequent_itemsets[k] = cur_frequent_itemsets
del frequent_itemsets[1]   

###5.2 Build association rules. We can make an association rule from a frequent itemset by 
###taking one of the movies in the itemset and denoting it as the conclusion. The other 
###movies in the itemset will be the premise. This will form rules of the following form: 
###if a reviewer recommends all of the movies in the premise, they will also recommend the 
###conclusion movie.
candidate_rules = []
for itemset_length, itemset_counts in frequent_itemsets.items():
    for itemset in itemset_counts.keys():
        for conclusion in itemset:
            premise = itemset - set((conclusion,))
            candidate_rules.append((premise, conclusion))
#print("There are {} candidate rules".format(len(candidate_rules)))
#print(candidate_rules[:4])
 
###6. Validate 
correct_counts = defaultdict(int)
incorrect_counts = defaultdict(int)
for user, reviews in favorable_reviews_by_users.items():
    for candidate_rule in candidate_rules:
        premise, conclusion = candidate_rule
        if premise.issubset(reviews):
            if conclusion in reviews:
                correct_counts[candidate_rule] += 1
            else:
                incorrect_counts[candidate_rule] += 1
rule_confidence = {candidate_rule: correct_counts[candidate_rule] 
/ float(correct_counts[candidate_rule] + incorrect_counts[candidate_rule])
              for candidate_rule in candidate_rules}
rule_confidence = {rule: confidence for rule, confidence in rule_confidence.items() 
if confidence > 0.8}
#print(len(rule_confidence))
 
from operator import itemgetter
sorted_confidence = sorted(rule_confidence.items(), key=itemgetter(1), reverse=True)
for index in range(3):
    #print("Rule #{0}".format(index + 1))
    (premise, conclusion) = sorted_confidence[index][0]
    #print("Rule: If a person recommends {0} they will also recommend {1}".format(premise, conclusion))
    #print(" - Confidence: {0:.3f}\n".format(rule_confidence[(premise, conclusion)]))
 
###We can build the direct rules to see the recommendation details of the movies
def get_movie_name(movie_id):
    title_object = movie_name_data[movie_name_data["MovieID"] == movie_id]["Title"]
    title = title_object.values[0]
    return title
movie_name_data = pd.read_csv("u.item", delimiter="|", header=None, encoding = "mac-roman")
movie_name_data.columns = ["MovieID", "Title", "Release Date", "Video Release", "IMDB", "", "Action", "Adventure","Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir","Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
#print(movie_name_data.head())
##SKIPPED
 
for index in range(3):
    #print("Rule #{0}".format(index + 1))
    (premise, conclusion) = sorted_confidence[index][0]
    premise_names = ", ".join(get_movie_name(idx) for idx in premise)
    conclusion_name = get_movie_name(conclusion)
    #print("Rule: If a person recommends {0} they will also recommend {1}".format(premise_names, conclusion_name))
    #print(" - Confidence: {0:.3f}\n".format(rule_confidence[(premise, conclusion)]))
 
###7 Test and Evaluate the rules
###7.1 Load test data
test_dataset = all_ratings[~all_ratings['UserID'].isin(range(200))]
test_favorable = test_dataset[test_dataset["Favorable"]]
test_favorable_by_users = dict((k, frozenset(v.values)) 
    for k, v in test_favorable.groupby("UserID")["MovieID"])
 
###7.2 Count the correct instances where the premise leads to the conclusion
correct_counts=defaultdict(int)
incorrect_counts=defaultdict(int)
for user, reviews in test_favorable_by_users.items():
    for candidate_rule in candidate_rules:
        premise,conclusion=candidate_rule
        if premise.issubset(reviews):
            if conclusion in reviews:
                correct_counts[candidate_rule]+=1
            else:
                incorrect_counts[candidate_rule]+=1
test_confidence = {candidate_rule:(correct_counts[candidate_rule] /float(correct_counts[candidate_rule] + incorrect_counts[candidate_rule]))
for candidate_rule in rule_confidence}
#print(len(test_confidence))
 
for index in range(3):
    print("Rule #{0}".format(index + 1))
    (premise, conclusion) = sorted_confidence[index][0]
    premise_names = ", ".join(get_movie_name(idx) for idx in premise)
    conclusion_name = get_movie_name(conclusion)
    print("Rule: If a person recommends {0} they will also recommend {1}"
        .format(premise_names, conclusion_name))
    print(" - Train Confidence: {0:.3f}".format(rule_confidence.get((premise, conclusion), -1)))
    print(" - Test Confidence: {0:.3f}\n".format(test_confidence.get((premise, conclusion), -1)))






