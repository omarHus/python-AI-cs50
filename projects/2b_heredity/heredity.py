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
                # print(f"two genes before func is {two_genes}")
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
    joint_probability = 1.0

    # Go through all people and calculate their probabilities
    for person, info in people.items():

        # How many genes are we looking for in person
        num_of_genes = how_many_genes(person, one_gene, two_genes)
        prob_of_gene = 0.0

        # Check if person has parents
        if info['mother'] is None:

            # Probability of having gene is based on unconditional distribution, So get the amount of genes person has
            prob_of_gene = PROBS["gene"][num_of_genes]
        
        # If person has parents then gene is conditional on probability they pass it down
        else:

            # check mother and father gene states
            mother_genes = how_many_genes(info['mother'], one_gene, two_genes)
            prob_mother  = prob_from_parent(mother_genes)
            father_genes = how_many_genes(info['father'], one_gene, two_genes)
            prob_father  = prob_from_parent(father_genes)
            prob_not_mother = 1.0 - prob_mother
            prob_not_father = 1.0 - prob_father

            # Checking for having no genes
            if num_of_genes == 0:

                prob_of_gene = prob_not_mother*prob_not_father

            # Checking for person having one gene
            elif num_of_genes == 1:   
                prob_of_gene = prob_not_mother*prob_father + prob_mother*prob_not_father
            
            # Check for person to have two genes
            else:
                prob_of_gene = prob_mother*prob_father
                
        # Check if person has trait or not
        if person in have_trait:
            trait = True
        else:
            trait = False

        # Probability of having trait given gene is
        prob_of_trait = PROBS["trait"][num_of_genes][trait]

        # Compute Joint probability
        joint_probability *= prob_of_gene*prob_of_trait

    return joint_probability

            
def prob_from_parent(parent_num_of_genes):

    if parent_num_of_genes == 0:
        return PROBS['mutation']     
    elif parent_num_of_genes == 1:
        return 0.5
    else:
        return 1.0-PROBS['mutation']      

def how_many_genes(person, one_gene, two_genes):
    """
    Figure out how many genes a person has
    """
    if person in two_genes:
        return 2
    elif person in one_gene:
        return 1
    else:
        return 0


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person, info in probabilities.items():

        # find the number of genes for person
        num_of_genes = how_many_genes(person, one_gene, two_genes)

        # Find the trait of the person
        if person in have_trait:
            trait = True
        else:
            trait = False
        
        # update joint probability of gene with new joint probability p
        probabilities[person]["gene"][num_of_genes] += p

        # update joint probability of trait with new joint probability p
        probabilities[person]["trait"][trait] += p




def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    # Go through gene and trait distributions and normalize
    for person, info in probabilities.items():

        # Find the distributions         
        gene_distribution  = info["gene"]
        trait_distribution = info["trait"]

        # normalize the distributions and update
        calculate_normalize(gene_distribution)
        calculate_normalize(trait_distribution)



def calculate_normalize(distribution):

    # Get the sum of the probabilites in the distribution
    probs    = distribution.values()
    prob_sum = sum(probs)

    # get a probability factor based on the sum
    prob_factor = 1/prob_sum

    # normalize and update
    for gene, prob in distribution.items():
        distribution[gene] = prob_factor*prob
    




if __name__ == "__main__":
    main()
