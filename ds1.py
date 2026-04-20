# Node class for Trie
class TrieNode:
    def __init__(self):
        self.children = {}        # stores next characters
        self.is_end = False       # marks end of a word


# Trie class
class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Insert a word into Trie
    def insert(self, word):
        current = self.root

        for ch in word:
            if ch not in current.children:
                current.children[ch] = TrieNode()

            current = current.children[ch]

        current.is_end = True   # mark end of word


    # Search words with given prefix
    def search(self, prefix):
        current = self.root

        # Move through prefix
        for ch in prefix:
            if ch not in current.children:
                return []   # no match found

            current = current.children[ch]

        # Find all words starting from this node
        return self.collect_words(current, prefix)


    # Helper function to collect words
    def collect_words(self, node, prefix):
        result = []

        # If current node is end of a word
        if node.is_end:
            result.append(prefix)

        # Explore all children
        for ch in node.children:
            result += self.collect_words(node.children[ch], prefix + ch)

        return result


# Main function
def main():
    trie = Trie()

    while True:
        print("\n1. Insert word")
        print("2. Autocomplete")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            word = input("Enter word: ")
            trie.insert(word)
            print("Word inserted!")

        elif choice == '2':
            prefix = input("Enter prefix: ")
            words = trie.search(prefix)

            if words:
                print("Suggestions:", words)
            else:
                print("No words found")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice")


# Run program
if __name__ == "__main__":
    main()