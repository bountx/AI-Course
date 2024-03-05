#Udało mi się znaleźć 12 kart, które dają szansę na wygraną większą niż 50%.
#Niestety nie udało mi się znaleźć 13 kart, które dają szansę na wygraną większą niż 50%.

#By przyspieszyć szukanie potencjalnych rozwiązań zaczynałem od wielu baz 9 kart, które dają szansę na wygraną większą niż 50%.

from collections import Counter
import random

def compareTwoCardSets(setB, setF):
    setB_score = 1
    setF_score = 1

    setB_values = [card[0] for card in setB]
    setF_values = [card[0] for card in setF]

    setB_counts = Counter(setB_values)
    setF_counts = Counter(setF_values)

    #SetB Flush
    if all(card[1] == setB[0][1] for card in setB):
        setB_score = max(setB_score, 6)

        #SetB Straight Flush, SetF can't be higher
        if all(setB[i][0] == setB[i+1][0] for i in range(4)):
            return 0
    
    if 4 in setB_counts.values(): #SetB Four of a Kind
        setB_score = max(setB_score, 8)
    elif 3 in setB_counts.values() and 2 in setB_counts.values(): #SetB Full House
        setB_score = max(setB_score, 7)
    elif all(setB[i][0] == setB[i+1][0] + 1 for i in range(4)): #SetB Straight
        setB_score = max(setB_score, 5)
    elif 3 in setB_counts.values(): #SetB Three of a Kind
        setB_score = max(setB_score, 4)
    elif sum(count == 2 for count in setB_counts.values()) == 2: #SetB Two Pairs
        setB_score = max(setB_score, 3)
    elif 2 in setB_counts.values(): #SetB One Pair
        setB_score = max(setB_score, 2)
    
    if 4 in setF_counts.values(): #SetF Four of a Kind
        setF_score = max(setF_score, 8)
    elif 3 in setF_counts.values() and 2 in setF_counts.values(): #SetF Full House
        setF_score = max(setF_score, 7)
    elif all(card[1] == setF[0][1] for card in setF): #SetF Flush
        setF_score = max(setF_score, 6)
    elif all(setF[i][0] == setF[i+1][0] + 1 for i in range(4)): #SetF Straight
        setF_score = max(setF_score, 5)
    elif 3 in setF_counts.values(): #SetF Three of a Kind
        setF_score = max(setF_score, 4)
    elif sum(count == 2 for count in setF_counts.values()) == 2: #SetF Two Pairs
        setF_score = max(setF_score, 3)
    elif 2 in setF_counts.values(): #SetF One Pair
        setF_score = max(setF_score, 2)
    
    if setB_score > setF_score:
        return 1
    else:
        return 0

def generateRandomSetB(cards):
    setB = []
    setOfCards = set()
    for _ in range(5):
        card = random.choice(cards)
        while card in setOfCards:
            card = random.choice(cards)
        setB.append(card)
        setOfCards.add(card)
    setB.sort()
    return setB

def generateRandomSetF():
    setF = []
    setOfCards = set()
    for _ in range(5):
        card = (random.randint(10, 13), random.choice(['H', 'D', 'C', 'S']))
        while card in setOfCards:
            card = (random.randint(10, 13), random.choice(['H', 'D', 'C', 'S']))
        setF.append(card)
        setOfCards.add(card)
    return setF

def estimateProbabilityOfWinning(cards):
    iterations = 2000
    wins = 0
    for _ in range(iterations):
        setB = generateRandomSetB(cards)
        setF = generateRandomSetF()
        wins += compareTwoCardSets(setB, setF)
    return wins / iterations

def generateRandomCardB(setOfCards):
    card = (random.randint(2, 9), random.choice(['H', 'D', 'C', 'S']))
    while card in setOfCards:
        card = (random.randint(2, 9), random.choice(['H', 'D', 'C', 'S']))
    return card

def generateBestCards():
    bestLength = 0
    for _ in range(300):
        cards = [(2, 'C'), (2, 'D'), (2, 'H'), (2, 'S'), (3, 'C'), (3, 'D'), (3, 'H'), (3, 'S'), (4, 'C'), (4, 'D'), (4, 'H'), (4, 'S')]
        setOfCards = set(cards)
        

        for i in range(6):
            probability = estimateProbabilityOfWinning(cards)

            if probability > 0.5 and len(cards) >= bestLength:
                bestLength = len(cards)
                cards.sort()
                print(bestLength, probability, cards)
            
            cards.append(generateRandomCardB(setOfCards))
            setOfCards.add(cards[-1])
        
    return bestLength
        




print(estimateProbabilityOfWinning([(2, 'C'), (2, 'D'), (2, 'H'), (2, 'S'), (3, 'C'), (3, 'D'), (3, 'H'), (3, 'S'), (4, 'C'), (4, 'D'), (4, 'H'), (4, 'S'), (5, 'H')]))
print(generateBestCards())