BLOCK_SIZE = 512
MAGIC = b"4348PRJ3"

T = 10
MAX_KEYS = 2*T - 1
MAX_CHILDREN = 2*T

def u64(x): 
    return x.to_bytes(8, 'big')
def from_u64(b): 
    return int.from_bytes(b, 'big')

class Header:
    """
    This is the 512 byte header block stored at block 0 of the index file.
    The header has:
        - MAGIC (8 bytes): identifies the file format
        - root (8 bytes): this is the block ID of the root b-tree node, 0 if tree is empty.
        - next_block (8 bytes): next unused block
    All values are stored as big-endian unsigned 64-bit integers.
    """
    def __init__(self, root=0, next_block=1):
        self.root = root
        self.next_block = next_block

    @staticmethod
    def read(f):
        """
        Reads header block from file and returns Header object.
        """
        f.seek(0)
        data = f.read(BLOCK_SIZE)
        if data[:8] != MAGIC:
            raise ValueError("Invalid magic number")
        root = from_u64(data[8:16])
        next_block = from_u64(data[16:24])
        return Header(root, next_block)

    def write(self, f):
        """
        Writes header structure to block 0 in the index file
        """
        buf = MAGIC + u64(self.root) + u64(self.next_block)
        buf = buf.ljust(BLOCK_SIZE, b"\x00")
        f.seek(0)
        f.write(buf)

class Node:
    """
    Represents one b-tree node stored in a 512-byte block.
    """

    def __init__(self, block_id, parent=0, nkeys=0, keys=None, vals=None, children=None):
        self.block_id = block_id
        self.parent = parent
        self.nkeys = nkeys
        self.keys = keys or [0]*MAX_KEYS
        self.vals = vals or [0]*MAX_KEYS
        self.children = children or [0]*MAX_CHILDREN

    @staticmethod
    def read(f, block_id):
        """
        Reads b-tree node from given block id, returns fully populated node instance
        """
        f.seek(block_id * BLOCK_SIZE)
        data = f.read(BLOCK_SIZE)
        if len(data) < BLOCK_SIZE:
            raise ValueError("Invalid node read")
        off = 0

        bid = from_u64(data[off:off+8]); off+=8
        parent = from_u64(data[off:off+8]); off+=8
        nkeys  = from_u64(data[off:off+8]); off+=8

        keys = [from_u64(data[off+i*8:off+(i+1)*8]) for i in range(MAX_KEYS)]
        off += 8*MAX_KEYS
        vals = [from_u64(data[off+i*8:off+(i+1)*8]) for i in range(MAX_KEYS)]
        off += 8*MAX_KEYS
        children = [from_u64(data[off+i*8:off+(i+1)*8]) for i in range(MAX_CHILDREN)]

        return Node(bid, parent, nkeys, keys, vals, children)

    def write(self, f):
        """
        Writes the node to its block in the index file
        """
        buf = b""
        buf += u64(self.block_id)
        buf += u64(self.parent)
        buf += u64(self.nkeys)
        for k in self.keys:
            buf += u64(k)
        for v in self.vals:
            buf += u64(v)
        for c in self.children:
            buf += u64(c)
        buf = buf.ljust(BLOCK_SIZE, b"\x00")
        f.seek(self.block_id*BLOCK_SIZE)
        f.write(buf)

### START B-tree functions ###

def search_node(f, node, key):
    """
    Search for a key starting from the given node, returns (node, index).
    """
    while True:
        i = 0
        while i < node.nkeys and key > node.keys[i]:
            i += 1

        if i < node.nkeys and node.keys[i] == key:
            return node, i

        child_id = node.children[i]
        if child_id == 0:
            return None, None

        node = Node.read(f, child_id)

def split_child(f, header, parent, i, full_child):
    """
    Splits a full child node during insertion
    """
    new_block = header.next_block
    header.next_block += 1

    new = Node(new_block, parent.block_id)
    new.nkeys = T-1

    for j in range(T-1):
        new.keys[j] = full_child.keys[j+T]
        new.vals[j] = full_child.vals[j+T]

    for j in range(T):
        new.children[j] = full_child.children[j+T]

    full_child.nkeys = T-1

    for j in range(parent.nkeys, i, -1):
        parent.children[j+1] = parent.children[j]

    parent.children[i+1] = new.block_id

    for j in range(parent.nkeys-1, i-1, -1):
        parent.keys[j+1] = parent.keys[j]
        parent.vals[j+1] = parent.vals[j]

    parent.keys[i] = full_child.keys[T-1]
    parent.vals[i] = full_child.vals[T-1]
    parent.nkeys += 1

    full_child.write(f)
    new.write(f)

def insert_nonfull(f, header, node, key, val):
    """
    Inserts a key into a node that is guaranteed to not be full.
    """
    i = node.nkeys - 1
    if node.children[0] == 0:
        while i >= 0 and key < node.keys[i]:
            node.keys[i+1] = node.keys[i]
            node.vals[i+1] = node.vals[i]
            i -= 1
        node.keys[i+1] = key
        node.vals[i+1] = val
        node.nkeys += 1
        node.write(f)
    else:
        while i >= 0 and key < node.keys[i]:
            i -= 1
        i += 1
        child = Node.read(f, node.children[i])
        if child.nkeys == MAX_KEYS:
            split_child(f, header, node, i, child)
            if key > node.keys[i]:
                i += 1
            node.write(f)
            child = Node.read(f, node.children[i])
        insert_nonfull(f, header, child, key, val)

def insert(f, header, key, val):
    """
    Inserts a new key-value pair into the b-tree.
    """
    if header.root == 0:
        rid = header.next_block
        header.next_block += 1
        root = Node(rid, 0, 1, [key]+[0]*(MAX_KEYS-1), [val]+[0]*(MAX_KEYS-1), [0]*MAX_CHILDREN)
        header.root = rid
        header.write(f)
        root.write(f)
        return

    root = Node.read(f, header.root)
    if root.nkeys == MAX_KEYS:
        new_root_id = header.next_block
        header.next_block += 1
        new_root = Node(new_root_id, 0, 0, [0]*MAX_KEYS, [0]*MAX_KEYS, [0]*MAX_CHILDREN)
        new_root.children[0] = root.block_id
        root.parent = new_root_id
        header.root = new_root_id
        split_child(f, header, new_root, 0, root)
        insert_nonfull(f, header, new_root, key, val)
        header.write(f)
        new_root.write(f)
    else:
        insert_nonfull(f, header, root, key, val)
        header.write(f)

def inorder(f, node, out):
    """
    Does inorder traversal of the b-tree
    """
    for i in range(node.nkeys+1):
        if node.children[i] != 0:
            inorder(f, Node.read(f, node.children[i]), out)
        if i < node.nkeys:
            out.append((node.keys[i], node.vals[i]))

### END B-tree functions ###

def cmd_create(path):
    """
    Creates a new index file
    """
    pass

def cmd_insert(idx, key, val):
    """
    Inserts a key-value pair into the index file.
    """
    pass

def cmd_search(idx, key):
    """
    Searches for a key in the index file and returns the result
    """
    pass

def cmd_print(idx):
    """
    Prints all key-value pairs in sorted order
    """
    pass

def cmd_extract(idx, outcsv):
    """
    Extracts all key-value pairs from the b-tree into a CSV file.
    """
    pass

def cmd_load(idx, csvf):
    """
    Loads key-value pairs from CSV file and inserts them into the b-tree.
    """
    pass

def main():
    pass

if __name__ == "__main__":
    main()