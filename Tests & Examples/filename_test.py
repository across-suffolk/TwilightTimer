import os

fullName = os.path.basename(__file__)
justName = os.path.splitext(fullName)[0] + ".txt"

print (justName)

#Works:
#theName = os.path.basename(__file__)
#print(os.path.splitext(theName)[0])


