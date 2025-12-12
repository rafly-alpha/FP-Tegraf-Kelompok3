class Node:
    def __init__(self, value, seq):
        self.value = value
        self.seq = seq[:]
        self.children = []

def build_tree(arr):
    roots = []

    for num in arr:
        new_nodes = []

        for root in roots:
            explore_add(root, num, new_nodes)

        new_nodes.append(Node(num, [num]))
        roots.extend(new_nodes)

    return roots

def explore_add(node, num, new_nodes):
    if num > node.value:
        new_seq = node.seq + [num]
        new_node = Node(num, new_seq)
        node.children.append(new_node)
        new_nodes.append(new_node)

    for child in node.children:
        explore_add(child, num, new_nodes)



def collect_all_sequences(roots):
    seqs = set()

    for root in roots:
        seqs.add(tuple(root.seq))

    return [list(t) for t in seqs]


def get_all_LIS(sequences):
    max_len = max(len(seq) for seq in sequences)
    return [seq for seq in sequences if len(seq) == max_len], max_len



# MAIN
arr = [4, 1, 13, 7, 0, 2, 8, 11, 3]

roots = build_tree(arr)
all_sequences = collect_all_sequences(roots)
LIS_list, L = get_all_LIS(all_sequences)

print("=== Semua subsekuensi meningkat ===")
for seq in sorted(all_sequences):
    print(seq)

print("\n=== Largest Monotonically Increasing Subsequence ===")
print(f"Length : {L}")
for seq in LIS_list:
    print(seq)
