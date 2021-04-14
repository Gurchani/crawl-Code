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

def interSectionLevel(setList):
    intersections = 0
    interSectList = range(0, len(setList))
    combos = itertools.combinations(interSectList, 2)
    for i, j in combos:
        intersections = intersections + len(setList[i].intersection(setList[j]))
    return intersections

def findTheBestCombo(df, parties, partyRTFriendsDF, reTweeterLen, targetPercentage):
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
            tempSetist = []
            for k in j:
                #print(k)
                tempSetist.append(rtDFDictionary.get(k))
                tempList.extend(rtDFDictionary.get(k))
                cost = cost + df[df['id'] == k ]['crawlCost'].values[0]
            if len(tempSetist) > 1:
                intersections = interSectionLevel(tempSetist)
            else:
                intersections = reTweeterLen * 10 # to discourse single values
            covered = list(set(tempList))
            costCoverDic[ref] = [j, covered]
            if (cost != None) and (len(covered) > 0):
                costCoverAnalysis.append([ref, cost, len(covered), intersections])
    ccDF = pd.DataFrame(costCoverAnalysis, columns=['ref', 'cost', 'coveredLen', 'instersections'])
    ccDF['cov/cos'] = (ccDF['coveredLen']/reTweeterLen) * (1/ccDF['cost']) * (1/ccDF['instersections'])
    tempDF = ccDF.sort_values(by='cov/cos', ascending=False)
    #tempDF = tempDF[tempDF['coveredLen'] > reTweeterLen * targetPercentage]
    #valScore = ccDF.sort_values(by='cov/cos', ascending=False).head(1)['ref'].values[0]
    tg = targetPercentage
    while True:
        for i in range(0, tempDF.shape[0]):
            valScore = tempDF['ref'].iloc[i]
            if tempDF['coveredLen'].iloc[i]/reTweeterLen > tg:
                print('The best set is: ')
                bestOne = costCoverDic.get(valScore)
                print(bestOne[0])
                print(len(bestOne[1]))
                return bestOne[0]
        tg = tg * 0.95







