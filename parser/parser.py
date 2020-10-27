import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""
# These are my non-terminals and I seemingly did an alright job
# Perhaps there is slight over gen on 7 and under gen on 10 which I could have fixed
NONTERMINALS = """
S -> NP NV | S P S | S Conj S
NV ->  V | NV Conj NV | NV Adv | Adv NV | V NP | NP V 
NP -> N | PP NP | Adj NP | Det NP | N NV | NV N | N PP
PP -> P NP | P 
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
    # Converts the sentence to lowercase
    sent = sentence.lower()
    # Tokenizes the lowercase sentence thus splitting it into a list of words
    final = nltk.word_tokenize(sent)
    # Loops through each word
    for x in final:
        counter = 0
        # Loops through each char in said word
        for char in x:
            counter += 1
            # If the there is an alphabetic character in the word, the loop is broken as word is NOT removed
            if char.isalpha() == True:
                break
            # Else if no alphabetical character have been found in the entire word, it is removed
            if counter == len(x):
                final.remove(x)
    return final


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = list()
    # Collects all nodes that have a label of 'N', where 'N' indicates a noun
    for i in tree.subtrees(filter=lambda x: x.label() == 'N'):
        chunks.append(i)
    return chunks




if __name__ == "__main__":
    main()
