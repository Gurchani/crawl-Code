
def getNames():
    namesList = []
    howMany = int(input('how many leaders'))
    for i in range(0, howMany):
        namesList.append(input('Leader Twitter Handle:'))
    return namesList
