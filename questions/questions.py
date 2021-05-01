import nltk
from nltk.corpus import stopwords
import sys
import math
import os
import string

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
    content = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r", encoding="utf8") as f:
            content[filename] = f.read()
    return content


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = nltk.word_tokenize(document)
    stop = set(stopwords.words('english'))
    words = [
        word.lower() for word in document
        if word not in stop
        and not all(char in string.punctuation for char in word)
    ]
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()
    for name in documents:
        words.update(documents[name])

    idfs = {}
    for word in words:
        f = sum(word in documents[name] for name in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranks = {}
    for name in files:
        ranks[name] = 0
        for word in query:
            tf = files[name].count(word)
            ranks[name] += tf * idfs[word]
    ranked = [
        name for name, _ in sorted(
                                ranks.items(),
                                key=lambda tfidf: tfidf[1],
                                reverse=True
                            )
    ]
    return ranked[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = {}
    for sentence in sentences:
        ranks[sentence] = [0, 0]
        for word in query:
            if word in sentences[sentence]:
                ranks[sentence][0] += idfs[word]
                # query term density
                qtd = (
                    sentences[sentence].count(word) / len(sentences[sentence])
                )
                ranks[sentence][1] += qtd
    ranked = [
        sentence for sentence, _ in sorted(
                                ranks.items(),
                                key=lambda item: (item[1][0], item[1][1]),
                                reverse=True
                            )
    ]
    return ranked[:n]


if __name__ == "__main__":
    main()
