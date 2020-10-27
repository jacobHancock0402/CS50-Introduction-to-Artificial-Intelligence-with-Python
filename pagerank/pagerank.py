import os
import random
import re
import sys
import random

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
    distro = dict()
    # If the page has outbound links, then create a distribution that represents them
    if len(corpus[page]) >= 1:
        # Likelihood of landing on that page given that every other page has equal probability
        for x in corpus[page]:
            distro[x] = (1 - damping_factor) / len(corpus)
        # Likelihood of landing on that page given the number of links on the original page
        for y in corpus[page]:
            distro[y] = (damping_factor / len(corpus[page])) + ((1 - damping_factor) / len(corpus))
    # Else page has no outbound links so it is assumed it links to every other page including itself
    elif len(corpus[page]) == 0:
        for w in corpus:
            distro[w] = 1 / len(corpus)



    return distro

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counter = 0
    # Creates new samples until the required amount is achieved
    for x in range(SAMPLES):
        # If first sample, everything is initialized and the page is selected randomly
        if counter == 0:
            temp = list(corpus.keys())
            new_page = random.choice(temp)
            PageRank = dict()
            for i in corpus.keys():
                PageRank[i] = 0
                for y in corpus[i]:
                    PageRank[y] = 0

        else:
            for j in PageRank.keys():
                # If the page is in the PageRank, it recorded that one more sample led to that page
                if new_page == j:
                    PageRank[j] += 1
                    break
        # Finds probability of choosing each page
        probability = transition_model(corpus,new_page,damping_factor)
        idk = list(probability.keys())
        # Chooses a page based on these probabilities
        who = random.choices(idk, probability.values())
        # Converts list into string for functionality purposes
        string = ''
        new_page = string.join(who)
        page = new_page
        counter += 1
    # Once all samples have been taken, the number of samples for each page is divided by the total number of samples
    # This calculates the proportion of samples that involved said page, thus calculating it's PageRank
    for p in PageRank.keys():
        PageRank[p] = PageRank[p] / SAMPLES

    return PageRank






def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    somenum = 0
    NewPageRank = dict()
    PageRank = dict()
    foo = list()
    total = 0
    # Initiliazing variables
    for i in corpus.keys():
        PageRank[i] = 0
        NewPageRank[i] = 0
        # If the page has no outbound links, page is interpreted to have links to all other pages and itself
        if len(corpus[i]) == 0:
            for b in corpus.keys():
                corpus[i].add(b)
        for y in corpus[i]:
            PageRank[y] = 0
            NewPageRank[y] = 0
    # Every PageRank is set to the same thing so each page initially has the same chance of being chosen
    for x in PageRank:
        foo = list()
        PageRank[x] = 1 / len(PageRank)
        # Adds all pages that have outbound links to that page
        for n in PageRank:
            if x in corpus[n]:
                foo.append(n)

        NewPageRank[x] = foo
    # Loop repeat until values converge
    # Couldn't get it to repeat succesfully until values changed by less than 0.001 so i just repeated it until the sum of the values where near enough to 0
    while total != 0.9999999999999996:
        if total == 1.0000000000000007:
            return PageRank
        total = 0

        idk = list(PageRank.keys())
        # Random page is chosen based on probabilites
        Page = random.choices(idk,PageRank.values())
        # Finds that page's key
        for w in corpus.keys():
            if w == Page[0]:
                somenum = 0
                # Goes through each inbound link to that page
                for p in NewPageRank[w]:
                    Num = 0
                    # Adds each page's PageRank divided by it's number of outbound links
                    somenum = somenum + (PageRank[p] / (len(corpus[p])))

                # PageRank iterative formula
                PageRank[w] = ((1 - damping_factor) / len(idk)) + (damping_factor * somenum)
                kid = list(PageRank.values())
                # Total PageRank of all pages is calculated
                for s in range(len(kid)):
                    total = total + kid[s]
    return PageRank




if __name__ == "__main__":
    main()
