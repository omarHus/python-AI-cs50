import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S  -> NP VP | NP VP NP NP | NP VP Conj NP VP | NP VP Conj VP
NP -> Det N | Det Adj N | Det Adj Adj N | Det Adj Adj Adj N | Adj N | P NP | NP Adv | N
VP -> Adv V | V P | V P NP | V NP | V NP NP | V Adv | V
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Tokenize sentence into list of words
    words = []
    words = nltk.word_tokenize(sentence)

    # Remove words that don't have at least one alpha char
    words = [word.lower() for word in words if has_one_alpha(word)]

    return words



def has_one_alpha(word):
    # Function to check if word has at least one alpha char
    has_alpha = False
    for char in word:
        if char.isalpha():
            has_alpha = True
            return has_alpha
    
    return has_alpha



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []

    # Get all NP subtrees
    for subtree in tree.subtrees(lambda tree: tree.label() == 'NP'):
        # Filter out subtrees that have another NP label
        temp = [subsub for subsub in subtree.subtrees(lambda tree: tree.label() == 'NP')]
        if len(temp) == 1:
            np_chunks.append(temp[0])
    
    return np_chunks


if __name__ == "__main__":
    main()
