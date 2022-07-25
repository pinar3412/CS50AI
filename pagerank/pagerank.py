import os
import random
import re
import sys
import copy

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
    distribution = dict()
    if len(corpus[page]) > 0:
        # If page has outgoing links

        for link in corpus.keys():
            random_factor = 1 - damping_factor

            if link in corpus[page]:
                # but every page gets an additional 0.05 because with probability 0.15 we choose randomly among all the pages.
                distribution[link] = damping_factor / len(corpus[page]) + random_factor / len(corpus.keys())

            else:
                # select randomly
                distribution[link] = random_factor / len(corpus.keys())
    else:
        # If page has no outgoing links
        for link in corpus.keys():
            distribution[link] = 1 / len(corpus.keys())

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    global choose_sample
    sample_dict = corpus.copy()

    for i in sample_dict:
        # first clear values for preparing pagerank values
        sample_dict[i] = 0
    print(sample_dict)

    for j in range(n):
        if j == 0:
            choose_sample = random.choice(list(sample_dict.keys()))
            sample_dict[choose_sample] += (1 / n)

        next_sample = transition_model(corpus, choose_sample, damping_factor)
        population = list(next_sample.keys())
        weight = [next_sample[k] for k in population]
        choose_sample = random.choices(population, weight, k=1)[0]
        if j==0:
            continue
        sample_dict[choose_sample] += (1 / n)

    print("dönüyordu", sample_dict, sum(sample_dict.values()))
    return sample_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    print("nanan")
    iterative_dict = corpus.copy()
    newiteration = corpus.copy()
    for i in iterative_dict:
        # first update the values for preparing pagerank values
        iterative_dict[i] = 1 / len(iterative_dict.keys())
    stop = True
    real_dict = None
    while stop:
        real_dict = newiteration.copy()
        for page in corpus:
            constant = 0
            for link in corpus.keys():

                NumLinks = len(corpus[link])
                if page in corpus[link]:
                    constant += (iterative_dict[link] / NumLinks)

                if len(corpus[link]) == 0:
                    constant += (iterative_dict[link] / len(corpus))

            newiteration[page] = (1 - damping_factor) / len(corpus) + damping_factor * constant

        difference = max([abs(newiteration[i] - iterative_dict[i]) for i in iterative_dict])
        if difference < 0.001:
            break
        else:
            iterative_dict = newiteration.copy()
            #stop = True

    print(sum(iterative_dict.values()))
    return real_dict


if __name__ == "__main__":
    main()
