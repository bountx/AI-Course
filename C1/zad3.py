import random

polishWords = set(open('words.txt').read().split())

def split_text_randomly(text):
    n = len(text)
    dp = [[] for _ in range(n+1)]  # dp[i] przechowuje indeksy początkowe słów kończących się na i-1
    dp[0] = [0]  # pusty ciąg może być "słowem" na początku

    for i in range(1, n + 1):
        for j in range(i):
            word = text[j:i]
            if word in polishWords and dp[j]:
                dp[i].append(j)

    # odtwarzanie jednego z możliwych podziałów, jeśli istnieje
    if not dp[n]:
        return "Nie można znaleźć podziału"

    result = []
    curr = n

    while curr > 0:
        prev = random.choice(dp[curr])
        result.append(text[prev:curr])
        curr = prev

    return ' '.join(reversed(result))


def split_text_not_randomly(text):
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

random_split_score = 0
not_random_split_score = 0
volume = 0

pan_tadeusz = open('pantadeusz_og.txt').read().split("\n")
pan_tadeusz_without_spaces = open('pantadeusz.txt').read().split("\n")
for line in pan_tadeusz_without_spaces:
    random_split = split_text_randomly(line)
    not_random_split = split_text_not_randomly(line)
    if random_split == pan_tadeusz[volume]:
        random_split_score += 1
    if not_random_split == pan_tadeusz[volume]:
        not_random_split_score += 1
    volume += 1

print(f"Random split effectiveness: {random_split_score / volume * 100}%")
print(f"Not random split effectiveness: {not_random_split_score / volume * 100}%")
    


