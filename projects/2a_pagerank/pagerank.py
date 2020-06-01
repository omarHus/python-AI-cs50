import os
import random
import re
import sys
from random import choice
from numpy.random import choice as w_choice

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
    page_visit_distribution = dict()

    # Assign initial probabilities to each page
    num_of_pages = len(corpus)
    for p in corpus.keys():
        page_visit_distribution[p] = (1 - damping_factor)/num_of_pages
    
    # Assign additional probability to links on the page
    try:
        links = corpus[page]
        num_of_links = len(links)
        for link in links:
            page_visit_distribution[link] = page_visit_distribution.get(link, 0) + (damping_factor/num_of_links)
    except:
        # if there are no links then assign equal probability to all pages including itself
        for link in corpus.keys():
            page_visit_distribution[link] = page_visit_distribution.get(link, 0) + (damping_factor/num_of_pages)

    return page_visit_distribution
        



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # This dictionary is the output with each page name as key and value is estimated page rank
    page_rank = dict()

    # First sample is random
    sample = choice(list(corpus.keys()))
    page_rank[sample] = (1.0-damping_factor)/n

    # Now go through n samples and apply them to their transition model to get the next sample
    for i in range(n):
        # based on prob distribution pick next sample
        prob_distribution = transition_model(corpus, sample, damping_factor)
        pages         = list(prob_distribution.keys())
        probabilities = list(prob_distribution.values())
        next_sample   = w_choice(pages, p=probabilities)

        # add sample to page_rank dictionary and increase the count by 1/n  
        page_rank[next_sample] = page_rank.get(next_sample, 0) + (1.0)/n

        # Make next_sample the current sample and start over
        sample = next_sample
    
    return page_rank





def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = dict()
    n         = len(corpus)
    # Assign an initial probability to all pages in the corpus
    for page in corpus.keys():
        # Assign each page in the corpus a probability 1-d/n
        page_rank[page] = (1.0-damping_factor)/n

    # Assign an additional probability to pages based on links
    error     = [1.0]
    precision = 0.0001
    # Iterate using page rank algorithm until a certain precision is met
    while max(error) > precision:
        error.clear()
        # For each page calculate the page rank
        for page, links in corpus.items():

            # Assign initial probability of first factor
            new_page_rank = (1.0-damping_factor)/n

            # Assign probability due to surfer following a link to page from another page
            try:
                for pages,links in corpus.items():
                    
                    # Go through pages that link to page and find their previous page rank
                    if page in links:
                        # Find number of links on the page that links to original page
                        num_of_links = len(corpus[pages])

                        # Page rank formula
                        new_page_rank += damping_factor*page_rank[pages]/num_of_links
            except:
                # if no links then assign equal probability to each page
                for link in corpus.keys():
                    new_page_rank += damping_dactor*page_rank[link]/n
            
            # calculate error
            error.append(abs(new_page_rank-page_rank[page])) 
            page_rank[page] = new_page_rank

    return page_rank


                



if __name__ == "__main__":
    main()
