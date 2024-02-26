file = open("words.txt", "r")
polishDictionary = set()
for line in file:
    polishDictionary.add(line.strip())
file.close()

def divideIntoWords(text):
    if len(text) == 0:
        return []
    dividedWords = []
    for i in range(min(len(text), 30), 0, -1):
        if text[:i] in polishDictionary:
            rest = divideIntoWords(text[i:])
            if rest is not None:
                dividedWords.append(text[:i])
                dividedWords.extend(rest)
                print(dividedWords)
                return dividedWords
    return None
    

file = open("pantadeuszbezspacji.txt", "r")
lines = file.readlines()
file.close()

newFile = open("zad2_output.txt", "w")
               
for line in lines:
    words = divideIntoWords(line.strip())
    if words is not None:
        newFile.write(" ".join(words) + "\n")
    else:
        print("Error: ", line)