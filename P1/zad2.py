#Rozwiązane przy użyciu programowania dynamicznego
#dla każdego podciągu od 0 do i sprawdzamy maksymalny wynik jaki możemy uzyskać
#za każdym razem zapisujemy maksymalny wynik i punkt podziału
#na końcu zwracamy wynik i odtwarzamy podział

file = open("words.txt", "r")
polishWords = set()
for line in file:
    polishWords.add(line.strip())
file.close()

def split_text(text):
    n = len(text)
    max_lengths = [0] * (n + 1)
    split_points = [-1] * (n + 1)

    for i in range(1, n + 1):
        max_length = 0
        for j in range(i):
            if max_lengths[j] + len(text[j:i]) ** 2 > max_length and text[j:i] in polishWords:
                max_length = max_lengths[j] + len(text[j:i]) ** 2
                split_points[i] = j
        max_lengths[i] = max_length

    words = []
    i = n
    while i > 0:
        words.append(text[split_points[i]:i])
        i = split_points[i]

    return ' '.join(reversed(words))

file_input = open("zad2_input.txt", "r")
file_output = open("zad2_output.txt", "w")
for line in file_input:
    file_output.write(split_text(line.strip()) + '\n')
file_input.close()
file_output.close()
print("Done")
