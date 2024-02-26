def opt_dist(blocks, d):
    minSwitchedBlocks = len(blocks)
    for i in range(0, len(blocks) - d + 1):
        switchedBlocks = blocks[:i].count(1) + blocks[i:i + d].count(0) + blocks[i + d:].count(1)
        if switchedBlocks < minSwitchedBlocks:
            minSwitchedBlocks = switchedBlocks
    return minSwitchedBlocks

print(opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 0))
