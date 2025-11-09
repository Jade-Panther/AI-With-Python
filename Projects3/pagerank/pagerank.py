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
    print('Corpus:', corpus)
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
    probabilities = {}
    pageLinks = corpus[page]

    if len(pageLinks) > 0:
        # Probability of going to any page because of randomness
        randProb = (1 - damping_factor) / (len(pageLinks) + 1)
        for page in corpus:
            probabilities[page] = randProb

        # Add all the probabilities together to get the total for each page
        for link in pageLinks:
            probabilities[link] = round(randProb + (damping_factor / len(pageLinks)), 4);
    else:
        for page in corpus:
            probabilities[page] = round(1 / len(corpus), 4)

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize 
    pageVisits = {}
    for page in corpus:
        pageVisits[page] = 0

    # Randomly visit one page
    currPage = random.choice(list(pageVisits.keys()))
    pageVisits[currPage] += 1

    # Sample
    for i in range(1, n):
        pages = transition_model(corpus, currPage, damping_factor)
        sample = random.choices(list(pages.keys()), weights=list(pages.values()))[0]
        pageVisits[sample] += 1
        currPage = sample
        
    # Convert to probabilities
    pageRanks = {}
    for page in pageVisits:
        pageRanks[page] = pageVisits[page] / n

    return pageRanks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initalize the ranks to 1 / N
    ranks = {}
    for page in corpus:
        ranks[page] = 1 / len(corpus)
    
    while True:
        newRanks = {}
        for page in corpus:
            rank = (1 - damping_factor) / len(corpus)

            for i in corpus:
                if page in corpus[i]:
                    numLinks = len(corpus[i])
                    rank += damping_factor * (ranks[i] / numLinks)

            newRanks[page] = rank

        # Calculate the difference to know when to stop
        diff = max(abs(newRanks[p] - ranks[p]) for p in ranks)
        ranks = newRanks
        if diff < 0.001:
            break;
    
    return ranks


if __name__ == "__main__":
    main()
