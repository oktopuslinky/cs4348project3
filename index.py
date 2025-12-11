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

def search_node(f, node, key):
    """
    Search for a key starting from the given node, returns (node, index).
    """
    pass

def split_child(f, header, parent, i, full_child):
    """
    Splits a full child node during insertion
    """
    pass

def insert_nonfull(f, header, node, key, val):
    """
    Inserts a key into a node that is guaranteed to not be full.
    """
    pass

def insert(f, header, key, val):
    """
    Inserts a new key-value pair into the b-tree.
    """
    pass

def inorder(f, node, out):
    """
    Does inorder traversal of the b-tree
    """
    pass

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