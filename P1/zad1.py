#Niestety rozwiązanie z nawrotwami działa zbyt wolno, aby przejść testy

from collections import deque

file = open("zad1_input.txt", "r")
line = file.readline()
file.close()

input = line.split(" ")
file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
turn = input[0]
wKingX = file_map[input[1][0]]
wKingY = int(input[1][1]) - 1
wRookX = file_map[input[2][0]]
wRookY = int(input[2][1]) - 1
bKingX = file_map[input[3][0]]
bKingY = int(input[3][1]) - 1

def movesUntilMate(turn, wKingX, wKingY, wRookX, wRookY, bKingX, bKingY):
    depth = 0
    movesQueue = deque([(turn, wKingX, wKingY, wRookX, wRookY, bKingX, bKingY, 0)])
    while len(movesQueue) > 0:
        move = movesQueue.popleft()
        turn = move[0]
        wKingX = move[1]
        wKingY = move[2]
        wRookX = move[3]
        wRookY = move[4]
        bKingX = move[5]
        bKingY = move[6]
        moves = move[7]


        if turn == "white":
            if wKingX + 1 != wRookX and wKingX + 1 != bKingX - 1 and 0 <= wKingX + 1 < 8:
                movesQueue.append(("black", wKingX + 1, wKingY, wRookX, wRookY, bKingX, bKingY, moves + 1))
            if wKingX - 1 != wRookX and wKingX - 1 != bKingX + 1 and 0 <= wKingX - 1 < 8:
                movesQueue.append(("black", wKingX - 1, wKingY, wRookX, wRookY, bKingX, bKingY, moves + 1))
            if wKingY + 1 != wRookY and wKingY + 1 != bKingY - 1 and 0 <= wKingY + 1 < 8:
                movesQueue.append(("black", wKingX, wKingY + 1, wRookX, wRookY, bKingX, bKingY, moves + 1))
            if wKingY - 1 != wRookY and wKingY - 1 != bKingY + 1 and 0 <= wKingY - 1 < 8:
                movesQueue.append(("black", wKingX, wKingY - 1, wRookX, wRookY, bKingX, bKingY, moves + 1))
            if wKingX + 1 != wRookX and wKingX + 1 != bKingX - 1 and wKingY + 1 != wRookY and wKingY + 1 != bKingY - 1 and 0 <= wKingX + 1 < 8 and 0 <= wKingY + 1 < 8:
                movesQueue.append(("black", wKingX + 1, wKingY + 1, wRookX, wRookY, bKingX, bKingY, moves + 1))
            if wKingX + 1 != wRookX and wKingX + 1 != bKingX - 1 and wKingY - 1 != wRookY and wKingY - 1 != bKingY + 1 and 0 <= wKingX + 1 < 8 and 0 <= wKingY - 1 < 8:
                movesQueue.append(("black", wKingX + 1, wKingY - 1, wRookX, wRookY, bKingX, bKingY, moves + 1))
            if wKingX - 1 != wRookX and wKingX - 1 != bKingX + 1 and wKingY + 1 != wRookY and wKingY + 1 != bKingY - 1 and 0 <= wKingX - 1 < 8 and 0 <= wKingY + 1 < 8:
                movesQueue.append(("black", wKingX - 1, wKingY + 1, wRookX, wRookY, bKingX, bKingY, moves + 1))
            if wKingX - 1 != wRookX and wKingX - 1 != bKingX + 1 and wKingY - 1 != wRookY and wKingY - 1 != bKingY + 1 and 0 <= wKingX - 1 < 8 and 0 <= wKingY - 1 < 8:
                movesQueue.append(("black", wKingX - 1, wKingY - 1, wRookX, wRookY, bKingX, bKingY, moves + 1))
            for i in range(wRookX + 1, 8):
                if i == bKingX:
                    break
                movesQueue.append(("black", wKingX, wKingY, i, wRookY, bKingX, bKingY, moves + 1))
            for i in range(wRookX - 1, -1, -1):
                if i == bKingX:
                    break
                movesQueue.append(("black", wKingX, wKingY, i, wRookY, bKingX, bKingY, moves + 1))
            for i in range(wRookY + 1, 8):
                if i == bKingY:
                    break
                movesQueue.append(("black", wKingX, wKingY, wRookX, i, bKingX, bKingY, moves + 1))
            for i in range(wRookY - 1, -1, -1):
                if i == bKingY:
                    break
                movesQueue.append(("black", wKingX, wKingY, wRookX, i, bKingX, bKingY, moves + 1))
        else:
            if bKingX == wRookX and bKingY == wRookY and (bKingX == wKingX + 1 or bKingX == wKingX - 1 or bKingY == wKingY + 1 or bKingY == wKingY - 1):
                return moves
            if isValidBlackMove(wKingX, wKingY, wRookX, wRookY, bKingX + 1, bKingY):
                movesQueue.append(("white", wKingX, wKingY, wRookX, wRookY, bKingX + 1, bKingY, moves + 1))
            if isValidBlackMove(wKingX, wKingY, wRookX, wRookY, bKingX - 1, bKingY):
                movesQueue.append(("white", wKingX, wKingY, wRookX, wRookY, bKingX - 1, bKingY, moves + 1))
            if isValidBlackMove(wKingX, wKingY, wRookX, wRookY, bKingX, bKingY + 1):
                movesQueue.append(("white", wKingX, wKingY, wRookX, wRookY, bKingX, bKingY + 1, moves + 1))
            if isValidBlackMove(wKingX, wKingY, wRookX, wRookY, bKingX, bKingY - 1):
                movesQueue.append(("white", wKingX, wKingY, wRookX, wRookY, bKingX, bKingY - 1, moves + 1))
            if isValidBlackMove(wKingX, wKingY, wRookX, wRookY, bKingX + 1, bKingY + 1):
                movesQueue.append(("white", wKingX, wKingY, wRookX, wRookY, bKingX + 1, bKingY + 1, moves + 1))
            if isValidBlackMove(wKingX, wKingY, wRookX, wRookY, bKingX + 1, bKingY - 1):
                movesQueue.append(("white", wKingX, wKingY, wRookX, wRookY, bKingX + 1, bKingY - 1, moves + 1))
            if isValidBlackMove(wKingX, wKingY, wRookX, wRookY, bKingX - 1, bKingY + 1):
                movesQueue.append(("white", wKingX, wKingY, wRookX, wRookY, bKingX - 1, bKingY + 1, moves + 1))
            if isValidBlackMove(wKingX, wKingY, wRookX, wRookY, bKingX - 1, bKingY - 1):
                movesQueue.append(("white", wKingX, wKingY, wRookX, wRookY, bKingX - 1, bKingY - 1, moves + 1))
    return "INF"

def isValidBlackMove(wKingX, wKingY, wRookX, wRookY, bKingX, bKingY):
    if bKingX == wRookX and (abs(wKingY - bKingY) > abs(wRookY - bKingY) or wRookX != wKingX):
        return False
    if bKingY == wRookY and (abs(wKingX - bKingX) > abs(wRookX - bKingX) or wRookY != wKingY):
        return False
    if abs(wKingX - bKingX) == 1 or abs(wKingY - bKingY) == 1:
        return False
    if 8 < bKingX <= 0 or 8 < bKingY <= 0:
        return False
    return True

result = movesUntilMate(turn, wKingX, wKingY, wRookX, wRookY, bKingX, bKingY)
print(result)