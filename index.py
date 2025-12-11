class Header:
    """
    This is the 512 byte header block stored at block 0 of the index file.
    The header has:
        - MAGIC (8 bytes): identifies the file format
        - root (8 bytes): this is the block ID of the root b-tree node, 0 if tree is empty.
        - next_block (8 bytes): next unused block
    All values are stored as big-endian unsigned 64-bit integers.
    """
    def init():
        pass

    @staticmethod
    def read(f):
        """
        Reads header block from file and returns Header object.
        """
        pass

    def write(self, f):
        """
        Writes header structure to block 0 in the index file
        """
        pass

class Node:
    """
    Represents one b-tree node stored in a 512-byte block.
    """

    @staticmethod
    def read(f, block_id):
        """
        Reads b-tree node from given block id, returns fully populated node instance
        """
        pass

    def write(self, f):
        """
        Writes the node to its block in the index file
        """
        pass

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