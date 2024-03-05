#dla każdego i sprawdzam ile bloków muszę przestawić żeby uzyskać pożądany wynik
#następnie porównuję wyniki i wybieram najmniejszy

def opt_dist(blocks, d):
    minSwitchedBlocks = len(blocks)
    for i in range(0, len(blocks) - d + 1):
        switchedBlocks = blocks[:i].count(1) + blocks[i:i + d].count(0) + blocks[i + d:].count(1)
        if switchedBlocks < minSwitchedBlocks:
            minSwitchedBlocks = switchedBlocks
    return minSwitchedBlocks

file_input = open("zad4_input.txt", "r")
file_output = open("zad4_output.txt", "w")
for line in file_input:
    blocks_str, d_str = line.strip().split()
    blocks = list(map(int, blocks_str))
    d = int(d_str)
    file_output.write(str(opt_dist(blocks, d)) + '\n')
file_input.close()
file_output.close()
