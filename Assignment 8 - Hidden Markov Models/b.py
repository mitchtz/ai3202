import sys
import math
#Worked with Mitch Zinser and the Wikipedia example
def emissionProbability():
    print("Emission Probability")
    countingDictionary = {}
    letters = ['a','b','c','d','e','f','g','h','i','j','k', 'l', 'm', 'n', 'o', 'p','q','r','s','t','u','v','w','x','y','z', '_']
    for letter in letters:
        for letter2 in letters:
            countingDictionary[(letter,letter2)] = 1
    with open("typos20.data","r") as textfile:
        for a in textfile.readlines():
            if (a[0],a[2]) in countingDictionary:
                countingDictionary[(a[0],a[2])] = countingDictionary[(a[0],a[2])] + 1
 
    probabilityDictionary = {}
    for i in sorted(countingDictionary):
        numCount = countingDictionary[i]
        denCount = 27
        t1 = i[0]
        for i2 in countingDictionary:
            t2 = i2[0]
            if t1 == t2:
                denCount = denCount + countingDictionary[i2]
        probabilityDictionary[i] = numCount/denCount
    #   print(i,countingDictionary[i])
    #   print(i,probabilityDictionary[i])
    return probabilityDictionary
 
def transitionProbability():
    print("Transition Probability")
    countingDictionary = {}
    fileStringArray = []
     
    letters = ['a','b','c','d','e','f','g','h','i','j','k', 'l', 'm', 'n', 'o', 'p','q','r','s','t','u','v','w','x','y','z', '_']
    for letter in letters:
        for letter2 in letters:
            countingDictionary[(letter,letter2)] = 1
 
    with open("typos20.data","r") as textfile:
        for a in textfile.readlines():
            fileStringArray.append(a[0])
    index = 0
    for i in fileStringArray:
        if index+1 == len(fileStringArray):
            break
        elif (fileStringArray[index],fileStringArray[index+1]) in countingDictionary:
            countingDictionary[(fileStringArray[index],fileStringArray[index+1])] = countingDictionary[(fileStringArray[index],fileStringArray[index+1])] + 1
        else:
            print("error")
        index += 1
 
    probabilityDictionary = {}
    for i in sorted(countingDictionary):
        numCount = countingDictionary[i]
        denCount = 27
        t1 = i[0] 
        for i2 in countingDictionary:
            t2 = i2[0]
            if t1 == t2:
                denCount = denCount + countingDictionary[i2]
        probabilityDictionary[i] = numCount/denCount
    #   print(i,countingDictionary[i])
    #   print(i,probabilityDictionary[i])
    #   print(total)
    return probabilityDictionary
 
def probabilityDistribution():
    print("Initial Probability Distribution")
    countingDictionary = {}
    fileStringArray = []
    with open("typos20.data","r") as textfile:
        for a in textfile.readlines():
            fileStringArray.append(a[0])
    index = 0
    for i in fileStringArray:
        if index+1 == len(fileStringArray):
            break
        elif (fileStringArray[index]) in countingDictionary:
            countingDictionary[fileStringArray[index]] = countingDictionary[fileStringArray[index]] + 1
        else:
            countingDictionary[fileStringArray[index]] = 2
        index += 1
 
    probabilityDictionary = {}
    denCount = 27 + len(fileStringArray)
    for i in sorted(countingDictionary):
        numCount = countingDictionary[i]
        probabilityDictionary[i] = numCount/denCount
    #   print(i,countingDictionary[i])
    #   print(i,probabilityDictionary[i])
    #print("denCount is: " + str(denCount))
    return probabilityDictionary
 
#obs is the output, e(t)
#states is the hidden value, x(t)
#start_p is the start probability
#trans_p is the transition probability matrix
#emit_p is the emission probability shit
def viterbi(obs, states, start_p, trans_p, emit_p):
    #V is a list of dictionaries
    V = [{}]
    path = {}
     
    # Initialize base cases (t == 0)
    for y in states:
        #the 0th dictionary, which is linked to an array, indexed by y
        V[0][y] = math.log(start_p[y]) + math.log(emit_p[(y,obs[0])])
        path[y] = [y]
    #print("Base case done")
    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            (prob, state) = max((V[t-1][y0] + math.log(trans_p[(y0,y)]) + math.log(emit_p[(y, obs[t])]), y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]
            #print(V[t][y])
 
        # Don't need to remember the old paths
        path = newpath
    #print("Viterbi ran")
    # Return the most likely sequence over the given time frame
    n = len(obs) - 1
    #print(*dptable(V), sep='')
    (prob, state) = max((V[n][y], y) for y in states)
    print("Control ended")
    return (prob, path[state])
 
def main():
    ObservationArray = []
    stateArray = ['a','b','c','d','e','f','g','h','i','j','k', 'l', 'm', 'n', 'o', 'p','q','r','s','t','u','v','w','x','y','z', '_']
    emissionDict = {}
    transitionDict = {}
    initialProbabilityDict = {}
    ActualArray = []
    with open("typos20Test.data","r") as textfile:
        for a in textfile.readlines():
            ObservationArray.append(a[2])
            ActualArray.append(a[0])
    emissionDict = emissionProbability()
    transitionDict = transitionProbability()
    initialProbabilityDict = probabilityDistribution()
    viterbiCall = viterbi(ObservationArray, stateArray, initialProbabilityDict, transitionDict, emissionDict)
    correct = 0
    for i in range(len(ActualArray)):
        if ActualArray[i] == viterbiCall[1][i]:
            correct += 1
    print(1-(correct/len(ActualArray)))
 
if __name__ == "__main__": main()