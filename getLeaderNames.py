
def getNames():
    namesList = []
    partyList = []
    howMany = int(input('how many leaders'))
    for i in range(0, howMany):
        namesList.append(input('Leader Twitter Handle:'))
        partyList.append(input('His/her party name:'))
    return (namesList, partyList)

import pandas as pd
def getLeaderPartyDF(namesList, partyList):
    return pd.DataFrame(zip(namesList, partyList), columns= ['leader', 'party'])



