#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools # it is a module in python that is used to iterate over data structures that can be stepped over 
                    #using for-loop

#   The below function generates the first candidate set using the dataset
def candidateSet1(itemSet):
    product_Dictionary = {}
    returnSet = []
    for data in itemSet: # read transaction line by line
        for product in data:
            if product not in product_Dictionary: # if the product is not  in the dictionary
               product_Dictionary[product] = 1 # Add the product with count 1
            else:
                 product_Dictionary[product] = product_Dictionary[product] + 1 # Increment the product count by 1 
    for key in product_Dictionary:
        temp_Array = []
        temp_Array.append(key)
        returnSet.append(temp_Array)# adding the product name to the list
        returnSet.append(product_Dictionary[key]) # Number of times that product have occurred in transaction
        temp_Array = []
    return returnSet


# In[2]:


#   The following function creates Frequent item sets by taking candidate sets as input
#   and also calls candidateSetsCk by feeding the output of the
#   current function as the input of the other function
def frequentItemSetLk(CandidateList, countOfTransactions, minSupport, itemSet, topFrequentArray):
    frequent_Items_Array = []
    for x in range(len(CandidateList)):
        if x%2 != 0: #  only odd places of the list
            support = (CandidateList[x] * 1.0 / countOfTransactions) * 100 # formula for calculating the support value
            if support >= minSupport:
                frequent_Items_Array.append(CandidateList[x-1])# Product name will display on even place
                frequent_Items_Array.append(CandidateList[x])# Product name count(number of times it occurs) will display on odd place

    for k in frequent_Items_Array:
        topFrequentArray.append(k)

    if len(frequent_Items_Array) == 2 or len(frequent_Items_Array) == 0:
        
        returnArray = topFrequentArray
        return returnArray

    else:
        candidateSetsCk(itemSet,frequent_Items_Array, countOfTransactions, minSupport)


# In[3]:


#   The below function creates Candidate sets by taking frequent sets as the input
#   At last, the function calls frequentItemSetLk by feeding the output of the
#   current function as the input of the other function
def candidateSetsCk(itemSet,frequent_Items_Array, countOfTransactions, minSupport):
    singleElements = []
    array_After_Combinations = []
    candidate_Set_Array = []
    for x in range(len(frequent_Items_Array)): # list with no. occurrence of the each items
        if x%2 == 0:
            singleElements.append(frequent_Items_Array[x]) # List of name of the items
    for item in singleElements:
        tempCombinationArray = []
        k = singleElements.index(item)
        for x in range(k + 1, len(singleElements)): # Creating combinations with every product
            for j in item:
                if j not in tempCombinationArray:
                    tempCombinationArray.append(j)
            for m in singleElements[x]:
                if m not in tempCombinationArray:
                    tempCombinationArray.append(m)
            array_After_Combinations.append(tempCombinationArray)
            tempCombinationArray = []
    sortedCombinationArray = []
    uniqueCombinationArray = []
    for x in array_After_Combinations:
        sortedCombinationArray.append(sorted(x))
    for x in sortedCombinationArray:
        if x not in uniqueCombinationArray:
            uniqueCombinationArray.append(x)
    array_After_Combinations = uniqueCombinationArray
    for item in array_After_Combinations:
        count = 0
        for transaction in itemSet: # itemSet is the dataset
            if set(item).issubset(set(transaction)): # Check if there is any transaction for the combination
                count = count + 1
        if count != 0:
            candidate_Set_Array.append(item)# Name of the combination
            candidate_Set_Array.append(count) # Number of transaction for the combination
    frequentItemSetLk(candidate_Set_Array, countOfTransactions, minSupport, itemSet, topFrequentArray)


# In[4]:


#   This function takes all the frequent sets as the input and generates all possible Association Rules
def findingPossibleAssociationRules(frequentSets):
    associationRule = []
    for item in frequentSets: # for all items in the list (combinations of 1,2,3 item set)
        if isinstance(item, list): #The isinstance() function checks if the object (first argument) is an instance 
                                        #or subclass of classinfo class (second argument).
            if len(item) != 0:
                length = len(item) - 1
                while length > 0:
                    combinations = list(itertools.combinations(item, length)) # Create all combinations
                    temp = []
                    LHS = []
                    for RHS in combinations:
                        LHS = set(item) - set(RHS) ## remove the item from RHS list
                        temp.append(list(LHS))
                        temp.append(list(RHS))
                        
                        associationRule.append(temp)
                        temp = []
                    length = length - 1
    return associationRule


# In[5]:


#   This function creates the final output of the algorithm by taking Association Rules as the input
def aprioriResult(rules, itemSet, minSupport, minConfidence):
    returnAprioriOutput = []
    for rule in rules:
        supportOfX = 0
        supportOfXinPercentage = 0
        supportOfXandY = 0
        supportOfXandYinPercentage = 0
        for transaction in itemSet:
            if set(rule[0]).issubset(set(transaction)):
                supportOfX = supportOfX + 1
            if set(rule[0] + rule[1]).issubset(set(transaction)):
                supportOfXandY = supportOfXandY + 1
        supportOfXinPercentage = (supportOfX * 1.0 / countOfTransactions) * 100
        supportOfXandYinPercentage = (supportOfXandY * 1.0 / countOfTransactions) * 100
        confidence = (supportOfXandYinPercentage / supportOfXinPercentage) * 100 # calculating the confidence
        # confidence = (support{X,Y}/Support{X}) * 100
        if confidence >= minConfidence:
            supportOfXAppendString = "Support Of X: " + str(round(supportOfXinPercentage, 2))
            supportOfXandYAppendString = "Support of X & Y: " + str(round(supportOfXandYinPercentage))
            confidenceAppendString = "Confidence: " + str(round(confidence))

            returnAprioriOutput.append(supportOfXAppendString)
            returnAprioriOutput.append(supportOfXandYAppendString)
            returnAprioriOutput.append(confidenceAppendString)
            returnAprioriOutput.append(rule)

    return returnAprioriOutput


# In[14]:


#   We will now request a customer to select from the available datasets
#     and provide an input for the minimum support and minimum confidence.  
#        The datasets available are amazon, nike, BestBuy, K-mart and a custom data (Fruits)   
#           
#         All datasets used for this project are in the form of csv files  
print("Choose the dataset from the below list in order to find the association rule:")
print("1. Amazon")
print("2. Nike")
print("3. BestBuy")
print("4. K-Mart")
print("5. Social Media Custom Data")
print("6. Fruits Custom Data")
print("\n")
fileNumberSelected = input("Select the number from the available options  (1,2,3,4,5,6): ")
minSupport = input('Provide minimum Support: ') # Asking the user to provide a minimum support value
minConfidence = input('Provide minimum Confidence: ') # Asking the user to provide a minimum confidence value
fileName = ""

if fileNumberSelected == '1':
    fileName = "csv/Amazon.csv"
if fileNumberSelected == '2':
    fileName = "csv/Nike.csv"
if fileNumberSelected == '3':
    fileName = "csv/BestBuy_itemset.csv"
if fileNumberSelected == '4':
    fileName = "csv/K-Mart.csv"
if fileNumberSelected == '5':
    fileName = "csv/Customdata.csv"
if fileNumberSelected == '6':
    fileName = "csv/fruits.csv"

minSupport = int(minSupport)
minConfidence = int(minConfidence)

nonFrequentSets = []
allFrequentItemSets = []
tempFrequentItemSets = []
itemSet = []
countOfTransactions = 0
topFrequentArray = []


# In[15]:


#   Reading the data file line by line
with open(fileName,'r') as fp:
    lines = fp.readlines()

for line in lines:
    line = line.rstrip()
    itemSet.append(line.split(","))

countOfTransactions = len(itemSet)

firstCandidateSet = candidateSet1(itemSet)

frequentItemSet = frequentItemSetLk(firstCandidateSet, countOfTransactions, minSupport, itemSet, topFrequentArray)

associationRules = findingPossibleAssociationRules(topFrequentArray)

AprioriOutput = aprioriResult(associationRules, itemSet, minSupport, minConfidence)


counter = 1
if len(AprioriOutput) == 0:
    print("There are no association rules for the support and confidence you provided.")
else:
    for x in AprioriOutput:
        if counter == 4:
            print(str(x[0]) + "------>" + str(x[1]))
            counter = 0
        else:
            print(x, end='  ')
        counter = counter + 1


# In[ ]:




