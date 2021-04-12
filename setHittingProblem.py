#This file will take a dataframe of friends of retweeters and try to determine
#the best possible combination of seed that cover the most users and has the lowest cost

#Approch
## order them by crawl-cost
import itertools
from IPython.display import display
import pandas as pd


def getCombos(df):
    combos = []
    friendsCombo = list(df['id'].unique())
    for i in range(len(friendsCombo)):
        combos.append(itertools.combinations(friendsCombo, i))
    return combos
def rtDFDic(df, friendsDb):
    dicOfSets = {}
    for i in df['id'].unique():
        dicOfSets[i] = set(friendsDb[friendsDb['friend'] == i]['retweeterId'])
    return dicOfSets

def findTheBestCombo(df, parties, partyRTFriendsDF):
    rtDFDictionary = rtDFDic(df, partyRTFriendsDF)
    combos = getCombos(df)
    costCoverAnalysis = []
    costCoverDic = {}
    ref = 0
    for i in combos:
        print('At Combo level')
        for j in i:
            cost = 0
            ref = ref + 1
            tempList = []
            for k in j:
                #print(k)
                tempList.extend(rtDFDictionary.get(k))
                cost = cost + df[df['id'] == k ]['crawlCost'].values[0]
            covered = list(set(tempList))
            costCoverDic[ref] = [j, covered]
            if (cost != None) and (len(covered) > 0):
                costCoverAnalysis.append([ref, cost, len(covered)])
    ccDF = pd.DataFrame(costCoverAnalysis, columns=['ref', 'cost', 'coveredLen'])
    ccDF['cov/cos'] = ccDF['coveredLen']/ccDF['cost']
    print(ccDF.sort_values(by='cov/cos', ascending=False))
    valScore = ccDF.sort_values(by='cov/cos', ascending=False).head(1)['ref'].values[0]
    print('The best set is: ')
    bestOne = costCoverDic.get(valScore)
    print(bestOne[0])
    print(len(bestOne[1]))


