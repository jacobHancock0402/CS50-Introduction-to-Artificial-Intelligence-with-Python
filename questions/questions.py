import nltk
import os
import sys
import string
import math
import copy

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    # Changes directory to the one containing the txt files
    os.chdir(f"{os.getcwd()}\\{directory}")
    # Lists txt files within the directory
    path = os.listdir()
    # Loops through each file
    for x in path:
        # Opens file
        file = open(x, 'r', encoding='UTF-8')
        # Reads it into the value of that key for that file
        files[x] = file.read()
        # Closes file
        file.close()
    return files



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    bad = list()
    # Convert whole string to lowercase
    temp = document.lower()
    # Tokenizes the string thus splitting it into words
    tokens = nltk.word_tokenize(temp)
    # Loops through each token
    for x in tokens:
        # If token is punctuation or a stopword, it is removed
        if x in string.punctuation or x in nltk.corpus.stopwords.words('english'):
            tokens.remove(x)
    return tokens



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    idf = dict()
    # Loops through each file / sentences
    for x in documents:
        # Loops through each word within the file / sentence
        for y in documents[x]:
            count = 0
            # Only loops through if the value hasn't been computed == More efficient
            if y not in idf:
                # Checks number of times the word appears in different documents
                for j in documents:
                    if y in documents[j]:
                        count += 1
                # If the word is in atleast one documents, then idf for that word is calculated
                if count > 0:
                    idf[y] = math.log((len(documents) / count))

    return idf



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    bs = list()
    final = list()
    order = dict()
    new = dict()
    # Loops through each file
    for x in files:
        # Loops through each query word
        for y in query:
            count = 0
            # Loops through each word in the file
            for j in files[x]:
                # If the word is in the file, frequency it updated
                if y in j:
                    count += 1
            # If word is in atleast one file
            if count > 0:
                # Then it's tf-idf value is calculated
                if x in order and y in idfs:
                    order[x] = order[x] + (count * idfs[y])
                elif x not in order and y in idfs:
                    order[x] = (count * idfs[y])
    # Sorts dict by value of tf-idf, in ascending order
    sort_order = sorted(order.items(), key=lambda x: x[1], reverse=False)

    counter = 0
    for t in sort_order:
        new[t[0]] = t[1]
    for i in new:
        # Loops through until number of values is correct
        if counter == (len(new) - 1):
            # Values are removed to decrease length to n
            for e in bs:
                new.pop(e)
            # Now sorts in descending order
            sort_order = sorted(new.items(), key=lambda x: x[1], reverse=True)
            # Loops through the list of tuples and take's the filenames
            for p in sort_order:
                final.append(p[0])
            return final
        counter += 1
        # List is in ascending order, so least values are appended then removed later
        bs.append(i)
        





def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    order = dict()
    prop = dict()
    new = dict()
    newp = dict()
    bs = list()
    finall = list()
    real = dict()
    # Loops through each key
    for x in sentences:
        # Loops through each word in query
        for y in query:
            count = 0
            # Checks how many words within the sentences are key words
            for j in sentences[x]:
                if y == j:
                    count += 1
            # Value of idf is only added if it's value has been computed, it's in atleast one sentences and is not a stopword
            if count > 0 and y in idfs and y not in nltk.corpus.stopwords.words('english'):
                # Calculates the number of words in the sentence that are key words
                if x in prop:
                    prop[x] = prop[x] + count
                if x not in prop:
                    prop[x] = count
                # Calculates the sum of idf values for query words in the sentences, dismissing frequency
                if x in order:
                    order[x] = order[x] + idfs[y]
                if x not in order:
                    order[x] = idfs[y]
        # Calculates the proportion of the sentence's words that are keywords
        if x in prop:
            prop[x] = prop[x] / len(sentences[x])
    # Creates a dict where the keys are sentences and the values are tuples of the values above
    for a in prop:
        real[a] = (prop[a], order[a])
    # Sorts the dict by the idf values
    sort_order = sorted(real.items(), key=lambda x: x[1][1], reverse=True)




    # Loops through every sentences
    for h in range(len(sort_order)):
        for e in range(len(sort_order)):
            # If the two sentences idf's are equal, but their query density is not, then their positions are adjusted
            if sort_order[h][1][1] == sort_order[e][1][1] and sort_order[e][1][0]> sort_order[h][1][0] and e > h:
                cop = copy.deepcopy(sort_order[h])
                sort_order[h] = sort_order[e]
                sort_order[e] = cop


    counter = 0
    # Orders the dict in ascending order
    for t in range(len(sort_order) - 1,-1, -1):
        new[sort_order[t][0]] = sort_order[t][1]
    # Same method seen in top_files where lesser elements are removed until length of the list is equal to n
    for i in new:
        if counter == (len(new) - n):
            for e in bs:
                new.pop(e)
            sort_order = sorted(new.items(), key=lambda x: x[1][1], reverse=True)
            break
        counter += 1
        bs.append(i)
    for q in sort_order:
        finall.append(q[0])
    return finall





if __name__ == "__main__":
    main()
