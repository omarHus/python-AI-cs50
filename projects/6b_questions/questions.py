import nltk
import sys
import os
import string
from collections import defaultdict
import numpy as np

FILE_MATCHES = 3
SENTENCE_MATCHES = 3


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

    filenames = os.listdir(directory)
    for file in filenames:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as f:
            files[file] = f.read()
    
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    # Create list of words in document
    words = []
    words = nltk.word_tokenize(document)

    # Remove punctuation and stop words
    punct = str.maketrans('', '', string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english')) 
    words = [str(word.lower()) for word in words if word not in stop_words and word.translate(punct) != '']

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    idf_score = dict()

    # Loop through every document
    for doc in documents:

        # Add every word to dict and make the list a set to count unique values
        words = set(documents[doc])
        for word in words:
            # increment by 1 every time you find a word in a new doc
            idf_score[word] = idf_score.get(word, 0) + 1

    # update to calculate idf score
    num_of_documents = len(documents)
    idf_score.update({word: np.log(num_of_documents/idf_score[word]) for word in idf_score.keys()})

    return idf_score


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    tf_idfs = dict()
    word_count = 0
    # Search each word in query
    for word in query:
        # get idf value
        idf = idfs[word]

        # Find Term Frequency in each file
        file_count = 0
        for file in files:

            # Get term freq
            tf = files[file].count(word)

            #compute tf_idf for this file and word
            tf_idfs[file] = tf_idfs.get(file, 0) + tf*idf
    
    # Sort documents by highest tf_idf
    tf_idfs  = {file: tfidf for file, tfidf in sorted(tf_idfs.items(), key=lambda item: item[1], reverse=True)}
    topfiles = list(tf_idfs.keys())
    
    return topfiles[0:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_score = dict()
    qdt            = dict()

    # Go thru each sentence and assign score based on "matching word measure"
    for sentence in sentences:

        # Get a list of the words in the sentence
        words = list(sentences[sentence])

        # Go thru each word in query
        word_count = 0
        for word in query:

            # Check if word is in the sentence and add idf score
            if word in words:
                sentence_score[sentence] = sentence_score.get(sentence, 0) + idfs[word]
                word_count +=1

         # Get query term density qdt
        qdt[sentence] = word_count/len(sentence)
        sentence_score[sentence] = (sentence_score.get(sentence, 0), qdt[sentence])

    # Sort documents by highest sentence idf, with qdt as tiebreaker
    sentence_score  = {sentence: idf[0] for sentence, idf in sorted(sentence_score.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True)}
    topSentences = list(sentence_score.keys())
    return topSentences[0:n]



if __name__ == "__main__":
    main()
