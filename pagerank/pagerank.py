import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}
    page_corpus = corpus[page]
    if page_corpus:
        for page in corpus:
            distribution[page] = (1 - damping_factor) / len(corpus)
            if page in page_corpus:
                distribution[page] += damping_factor / len(page_corpus)
    else:
        for page in corpus:
            distribution[page] = damping_factor / len(corpus)

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    all_pages = corpus.keys()
    for page in all_pages:
        pagerank[page] = 0

    page = random.choice(list(all_pages))
    tm = transition_model(corpus, page, damping_factor)
    for i in range(n):
        total = []
        for page in tm:
            total += [page] * round(tm[page] * 100)
        page = random.choice(total)
        pagerank[page] += 1 / n
        tm = transition_model(corpus, page, damping_factor)

    return pagerank


def iterative_helper(corpus, pagerank, damping_factor):
    """
    Recursively calculate pagerank
    """
    new_pagerank = {}
    for page in pagerank:
        prob = 0.0 

        # link is page that link to current page
        for link in corpus:
            if page in corpus[link]:
                prob += damping_factor * pagerank[link] / len(corpus[link])

            if not corpus[link]:
                prob += damping_factor *  pagerank[link] / len(corpus)

        new_pagerank[page] = (1 - damping_factor) / len(corpus) + prob

    for page in pagerank:
        if 0.001 < abs(new_pagerank[page] - pagerank[page]):
            return iterative_helper(corpus, new_pagerank, damping_factor)
    return new_pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    for page in corpus:
        pagerank[page] = 1 / len(corpus)

    return iterative_helper(corpus, pagerank, damping_factor)

if __name__ == "__main__":
    main()
