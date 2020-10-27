import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Initializes everyone's gene and trait combinations
    Input = [one_gene,two_genes,have_trait]
    # If person not in one gene, two gene or have trait, then they will have no trait and 0 genes
    classic = ['gene', 0]
    prob = dict()
    chance = list()
    modern =  ['trait',0,False]
    for f in people.keys():
        # Creates a key for each person
        prob.update({f : [0] * 2})
    for x in people.keys():
        x_name = list()
        # maybe delete
        prob[x][0] = classic
        prob[x][1] = modern
        # Assigns the correct gene or trait value if person is in one gene, two gene or have trait
        if x in one_gene or x in two_genes or x in have_trait:
            for y in range(len(Input)):
                if x in Input[y]:
                    x_name.append(y)
            for w in range(len(x_name)):
                if x_name[w] == 0:
                    combo = ['gene', 1]
                    prob[x][0] = combo
                if x_name[w] == 1:
                    combo = ['gene', 2]
                    prob[x][0] = combo
                if x_name[w] == 2:
                    combo = ["trait",prob[x][0][1],True]
                    prob[x][1] = combo
        # Person's trait list gene value is set to value in the gene list
        bruh = prob[x][0][1]
        prob[x][1][1] = bruh
        modern = ['trait',0,False]

    # Loops through everyone and calculates the probability of their trait and gene lists
    for p in (prob):
        for j in range(len(prob[p])):
            # If person does not have parents, or we are in their trait list, we will use generic probability values
            if not people[p]['father'] or j == 1:
                    # Maybe it's len is 1 as it's a list with 2 items within
                # Probability that a person has so many genes
                if j == 0:
                    chance.append(PROBS[prob[p][0][0]][prob[p][0][1]])
                # Probability that a person has so many genes and does or does not have the trait
                elif j == 1:
                    chance.append(PROBS[prob[p][1][0]][prob[p][1][1]][prob[p][1][2]])
            # Else probability of the person's genes are calculated by looking at all the possibilities that would cause his parents to give them that number genes
            else:
                father = p
                counter = 0
                # Loops through the person's parents and then their parents until top of family tree is found
                while people[father]['father']:
                    child = father
                    father = people[father]['father']
                # New loop then runs until the bottom of the tree
                while counter == 0:
                    mother = people[child]["mother"]
                    totm = prob[father][0][1]
                    totf = prob[mother][0][1]
                    # Number of genes child has
                    need = prob[child][0][1]
                    # Number of genes father and mother have combined
                    total = totf + totm
                    diff = total - need
                    num = 0
                    # Checks every possible total and need combination
                    # This section is quite badly written as I pretty much hard coded everything instead of using something more dynamic
                    # Despite this, it does meet the requirements of the task
                    if total == 2:
                        # If both parents have 1 gene each
                        if totf == totm:
                            if need == 0:
                                num = 1
                            if need == 0 or need == 2:
                                # 2 genes can only be dropped with a 0.5 squared as both parents have a 0.5 chance of dropping one
                                # This also applies to 0 genes as both parents have a 0.5 chance of droppling 0 genes
                                # If child needs 0 genes, you could also have the parents drop one then mutate
                                bro = (0.5) * (0.5) + ((num) * 0.5 * (PROBS["mutation"])) * (0.5 * (PROBS["mutation"]))
                            # If child need 1 gene the only possibility is one parents drops a gene, and the other doesn't
                            if need == 1:
                                bro = ((0.5) * (0.5)) + ((0.5) * (0.5))
                        # Else one parent has 2 and other has 0
                        else:
                            # 2 Gene parent must drop 1 gene, and the other's must mutate
                            # To achieve 0 genes, this also applies, as 0 gene wouldn't mutate and other would
                            if need == 2 or need == 0:
                                bro = ((1 - PROBS["mutation"]) * (PROBS["mutation"]))
                            # Else need == 1
                            else:
                                # Either 2 gene parent drops 1 one and other doesnt't mutate
                                # Or both genes mutate
                                bro = (((1 - PROBS["mutation"])) * (1 - PROBS["mutation"])) + (((PROBS["mutation"])) * (PROBS["mutation"]))
                        chance.append(bro)

                    elif total == 1:
                        # If need is 1, you can get a 0.5 chance of one parent dropping one gene and the other dropping 0
                        # If need is 1 , you could also have a 0 drop from one parent and the other have it's gene mutate
                        # If need is 0, you would have one parent drop nothing with 0.5 chance, and other not mutate
                        if need < 2:
                            bro = (0.5 * (1 - PROBS["mutation"])) + (((need * 0.5)  * (PROBS["mutation"])))
                        # Else need = 2 so one parent must drop their one gene, and other must have theirs mutate
                        else:
                            bro = ((0.5) * (PROBS["mutation"]))
                        chance.append(bro)
                    elif total == 0:
                        # If child needs 2 genes, then both of parents must mutate
                        if need == 2:
                            bro = (PROBS["mutation"]) * (PROBS["mutation"])
                        # If child needs 1 gene, then one of the parents gene's must mutate, and the other doesn't
                        elif need == 1:
                            bro = (PROBS["mutation"]) * (1 - PROBS["mutation"]) + (PROBS["mutation"]) * (1 - PROBS["mutation"])
                        # Else need is 0 so neither mutates
                        else:
                            bro = (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])
                        chance.append(bro)
                    elif total == 3:
                        # Parent with one must drop nothing, and the parents of the other must have theirs mutate
                        if need == 0:
                            bro = ((0.5) * (PROBS["mutation"]))
                        # Either one parent drops nothing and the other drops one
                        # Or one parent drops one and other's mutates
                        elif need == 1:
                            bro = ((1 - PROBS["mutation"]) * (0.5)) + ((PROBS["mutation"]) * (0.5))
                        # Both parents must drop one without mutation
                        elif need == 2:
                            bro = ((1 - PROBS["mutation"]) * (0.5))
                        chance.append(bro)
                    elif total == 4:
                        # Both genes must mutate
                        if need == 0:
                            bro = PROBS["mutation"] * PROBS["mutation"]
                        # Either parent must drop one, and the other parent's mutates
                        elif need == 1:
                            bro = ((PROBS["mutation"]) * (1 - PROBS["mutation"])) + ((PROBS["mutation"]) * (1 - PROBS["mutation"]))
                        # Both parents must drop 1 without mutation
                        elif need == 2:
                            bro = ((1 - PROBS["mutation"]) * (1 - PROBS["mutation"]))
                        chance.append(bro)
                    # If person is a parents, then loops continues
                    if child in people.values():
                        counter = 0
                    # Else loop exits
                    if child not in people.values():
                        counter = 1
    total = 0
    # Mutliplies the whole list
    # Goes through list two elements at a time by multipying the element it's on by the element ahead of it
    for k in range(0,len(chance) - 1,2):
        if total == 0:
            total = chance[k] * chance[k + 1]
        else:
            total = total * (chance[k] * chance[k + 1])
    return total






def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Loops through each person and add a new value in the appropriate locations
    for x in probabilities:
        # If x is one of the gene or trait sets, then the corresponding location in the probabilities dict is where the value is added
        if x in have_trait:
            probabilities[x]["trait"][True] = probabilities[x]["trait"][True] + p
        # Otherwise the probability for not having the trait or having 0 genes is added
        if x not in have_trait:
            probabilities[x]["trait"][False] = probabilities[x]["trait"][False] + p
        if x in one_gene:
             probabilities[x]["gene"][1] = probabilities[x]["gene"][1] + p
        if x in two_genes:
             probabilities[x]["gene"][2] = probabilities[x]["gene"][2] + p
        if x not in one_gene and x not in two_genes:
            probabilities[x]["gene"][0] = probabilities[x]["gene"][0] + p




def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for x in probabilities:
        # Finds which value is the largest
        if probabilities[x]["trait"][True] + probabilities[x]["trait"][False] != 1:
            if probabilities[x]["trait"][True] < probabilities[x]["trait"][False]:
                numerator = probabilities[x]["trait"][False]
                denominator = probabilities[x]["trait"][True]
            else:
                numerator = probabilities[x]["trait"][True]
                denominator = probabilities[x]["trait"][False]
            # Calculates the ratio between the two values
            # Total is found and then the values of one part is valued by dividing the total by 2, the number of elements
            num = numerator + denominator
            parts = num / float(2)
            # Ratio is then fond by dividing values of both numbers by the value of each part
            ratioN = numerator / float(parts)
            ratioD = denominator / float(parts)
            # Loops through and calculates a new total while the total is not close enough to 1
            while numerator + denominator != 1:
                if numerator + denominator > 0.9999 and numerator + denominator < 1.0001:
                    break
                # If total is greater than 1, then value must be increased
                if numerator + denominator < 1:
                    # Both number are increased by multiplying a constant by their respective ratio, and then adding that to their value
                    numerator = numerator + (0.0001 * ratioN)
                    denominator = denominator + (0.0001 * ratioD)
                # Else value must be decreased
                else:
                    # Same method as above, but new values are then subtracted from the values
                    numerator = numerator - (0.0001 * ratioN)
                    denominator = denominator - (0.0001 * ratioD)
            if probabilities[x]["trait"][True] < probabilities[x]["trait"][False]:
                probabilities[x]["trait"][False] = numerator
                probabilities[x]["trait"][True] = denominator
            else:
                probabilities[x]["trait"][False] = denominator
                probabilities[x]["trait"][True] = numerator

        # Ratio is found again using same process
        collection = list(probabilities[x]["gene"].values())
        collection2 = list(probabilities[x]["gene"].values())
        Highest = max(collection)
        collection.remove(Highest)
        Middle = max(collection)
        Min = min(collection)
        temp = Highest + Middle + Min
        part = temp / float(len(collection))
        maxR = Highest / float(part)
        total = (Highest * temp) + (Middle * temp) + (Min * temp)
        middleR = Middle / float(part)
        minR = Min / float(part)
        # Again ratio's are kept in proportion like above, but now for genes
        while Highest + Middle + Min != 1:
            if Highest + Middle + Min > 0.9999 and Highest + Middle + Min < 1.0001 :
                break
                # Could calculate difference and then use the decimal place below that
            if Highest + Middle + Min < 1:
                Highest = Highest + (0.0001 * (maxR))
                Middle = Middle + (0.0001 * middleR)
                Min = Min + (0.0001 * minR)
            else:
                Highest = Highest - (0.0001 * (maxR))
                Middle = Middle - (0.0001 * middleR)
                Min = Min - (0.0001 * minR)
        # As there are 3 numbers, we have to find the corresponding position in probabilities
        for d in probabilities[x]["gene"]:
            # Loops through each value in genes and and checks whether they equal the max, middle, or min value
            if probabilities[x]["gene"][d] == max(collection2):
                probabilities[x]["gene"][d] = Highest
            elif probabilities[x]["gene"][d] == min(collection2):
                probabilities[x]["gene"][d] = Min
            else:
                probabilities[x]["gene"][d] = Middle




if __name__ == "__main__":
    main()
