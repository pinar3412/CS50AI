import math
import os
import string
import nltk
import sys
from nltk import word_tokenize

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
    d = {}
    for textfile in os.listdir(directory):
        with open(os.path.join(directory, textfile), encoding="utf-8") as of:
            d[textfile] = of.read()
    return d


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.
    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.

    """

    document = document.lower()
    token_word = word_tokenize(document)
    for word in token_word.copy():
        if word in string.punctuation or word in nltk.corpus.stopwords.words("english"):
            token_word.remove(word)
    return token_word

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.
    Any word that appears in at least one of the documents should be in the
    resulting dictionary.

    """
    all_uniquewords = set()
    idfs = dict()

    for doc in documents:
        all_uniquewords.update(documents[doc])

    for word in all_uniquewords:
        count = 0
        for document in documents:
            if word in documents[document]:
                count += 1
        if count != 0:
             idfs[word] = math.log(len(documents) / count)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    finalpoint = {}

    for word in query:
        if word in idfs:
            for filesname in files:
                tf = 0
                for words in files[filesname]:
                    if word == words:
                        tf +=1

                finalpoint[filesname] = + tf * idfs[word]

    sorted_fp = sorted(finalpoint, key=lambda k: finalpoint[k], reverse=True)[0:n]
    return sorted_fp


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    topSentences = dict()
    for sentence in sentences:
        rank = 0
        qtd = 0
        for word in query:
            if word in sentences[sentence]:
                qtd += sentences[sentence].count(word)
                rank += idfs[word]

        density = (qtd / len(sentences[sentence]))
        topSentences[sentence] = [rank, density]

    topScores = sorted(topSentences.keys(), key=lambda x: topSentences[x], reverse=True)[0:n]

    return topScores

" """"scores = {}
    for sentence in sentences.items():
        rank = 0
        for word in query:
            if word in sentences[sentence]:
                rank += idfs[word]

            density = sum([sentence.count(x) for x in query]) / len(sentence)
            scores[sentence] = (rank, density)


    sorted_by_score = [i for (i, j) in sorted(scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)][:n]

        return sorted_by_score """

if __name__ == "__main__":
    main()