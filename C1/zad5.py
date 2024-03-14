from collections import Counter
from itertools import combinations

def classify_hand(cards):
    """
    Classifies a hand of cards into the appropriate poker category, with improved handling for tens.
    """
    values_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    values = [c[0] if c[0] != '1' else 'T' for c in cards]  # Replace '10' with 'T' for tens, as they are represented with two characters
    suits = [c[-1] for c in cards]
    value_counts = Counter(values)
    suit_counts = Counter(suits)

    is_flush = max(suit_counts.values()) == 5

    sorted_values = sorted(values, key=lambda x: values_map[x])

    is_straight = all(values_map[sorted_values[i]] + 1 == values_map[sorted_values[i+1]] for i in range(len(sorted_values) - 1))
    
    if is_straight and is_flush:
        return "Straight Flush"
    elif max(value_counts.values()) == 4:
        return "Four of a Kind"
    elif sorted(value_counts.values()) == [2, 3]:
        return "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight:
        return "Straight"
    elif max(value_counts.values()) == 3:
        return "Three of a Kind"
    elif list(value_counts.values()).count(2) == 2:
        return "Two Pair"
    elif 2 in value_counts.values():
        return "Pair"
    else:
        return "High Card"

face_card_hands = ['A♠', 'A♥', 'A♦', 'A♣', 'K♠', 'K♥', 'K♦', 'K♣', 'Q♠', 'Q♥', 'Q♦', 'Q♣', 'J♠', 'J♥', 'J♦', 'J♣']
non_face_card_hands = [f'{n}{s}' for n in range(2, 11) for s in ['♠', '♥', '♦', '♣']]

face_card_combinations = list(combinations(face_card_hands, 5))
non_face_card_combinations = list(combinations(non_face_card_hands, 5))

face_card_categories = Counter(classify_hand(hand) for hand in face_card_combinations)

non_face_card_categories = Counter(classify_hand(hand) for hand in non_face_card_combinations)

total_possible_matches = len(face_card_combinations) * len(non_face_card_combinations)

non_face_card_wins = 0

categories_map = {
    "Straight Flush": 8,
    "Four of a Kind": 7,
    "Full House": 6,
    "Flush": 5,
    "Straight": 4,
    "Three of a Kind": 3,
    "Two Pair": 2,
    "Pair": 1,
    "High Card": 0
}
# Iterating through categories from strongest to weakest
for category, strength in reversed(list(categories_map.items())):
    if category in non_face_card_categories: 
        for face_category, face_strength in reversed(list(categories_map.items())):
            if face_strength < strength: 
                non_face_card_wins += non_face_card_categories[category] * sum(face_card_categories[k] for k, v in face_card_categories.items() if categories_map[k] < strength)


non_face_card_win_probability = non_face_card_wins / total_possible_matches



print(non_face_card_win_probability)
