import csv
import sys
import sqlite3

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open("people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open("movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open("stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    count = 0
    negative = 0
    coup = 0
    person = list(people.values())
    # Queue Frontier used for Breadth First Search
    front = QueueFrontier()
    tempo = 0
    # Return a set of tuples containing the ids of the people who starred with the source in the id of the movie
    sauce = neighbors_for_person(source)
    for x in range(len(person)):
        # Creates a sorted list version of the data in order to index in
        why = sorted(sauce)
        for p in range(len(why)):
            # Only adds people who aren't the source
            if why[p] == source:
                negative = negative + 1
            else:
                # Creates an empty node object
                temp = Node("unexplored", -1, [0] * 2)
                # Sets it value the ids of the neighbor and movie
                temp.action = why[p]
                # Checks if neighbor is target, then returning the list of the connection to get there
                if temp.action[1] == target:
                    front.add(temp)
                    front.frontier[0].state = "link"
                    peth = make_path(front, source, target)
                    return peth

                count = count + 1
                front.add(temp)
                # Only adds goes to access the neighbors's once neighbors of source are added
                # This preserves the Breadth First Search
                coup = 0
                for z in range(len(front.frontier)):
                    if front.frontier[z].state == "unexplored":
                        coup = coup + 1

                if len(why) == len(front.frontier) - negative or (len(why) <= len(front.frontier) - negative and coup > 0 ):
                    # Goes through nodes from first added until finds one that hasn't been explored
                    for y in range(len(front.frontier)):
                        if front.frontier[y].state == "unexplored":
                            temps = front.frontier[y].action[1]
                            tempa = front.frontier[y].action
                            idiot = neighbors_for_person(temps)
                            variable = sorted(idiot)
                            # Checks neighbors of node to see if target
                            for k in range(len(variable)):
                
                                if target in variable[k]:
                                    nod = Node("link", -1, [0] * 2)
                                    nod.action = variable[k]
                                    front.add(nod)
                                    front.frontier[-1].parent = y

                                    
                                 
                                    

                                    pets = make_path(front, source, target)
                                    return pets
                            # Else node isn't target so neighbors of node are added to be explored if earlier neighbors aren't target               
                            front.frontier[y].state = "explored"
                            for u in range(len(variable)):
                                tmp = Node("unexplored", -1, [0] * 2)
                                tmp.action = ***REMOVED***[u]
                                if tmp.action[1] != target:
                                    front.add(tmp)
                                    front.frontier[-1].parent = y
                                    y = 0

                                # Ensures if target is found, that the node is recognized and creates a path instead of moving to the next node
                                else:
                                    nod = Node("link", -1, [0] * 2)
                                    nod.action = variable[u]
                                    front.add(nod)
                                    front.frontier[-1].parent = y
                                    pets = make_path(front, source, target)
                                    return pets
                                    
                                      
def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

# Function that is called to create a list of tuples that shows the path from source to target


def make_path(frontier, source, target):
    pet = list()
    can = 0
    what = list()
    for loc in range((len(frontier.frontier)) - 1, -1, -1):
        if can > 0:
            loc = frontier.frontier[loc].parent
        if loc == -1:
            return pet
        pet.insert(0, frontier.frontier[loc].action)
        loc = frontier.frontier[loc].parent
        if loc != -1:
            pet.insert(0, frontier.frontier[loc].action)
            frontier.frontier[loc].state = "link"
            if frontier.frontier[loc].action[1] == source:
                return pet
        
        if loc == -1:
            return pet
        if frontier.frontier[loc].action not in pet and frontier.frontier[loc].parent == - 1:
            pet.insert(0, frontier.frontier[loc].action)
        loc = frontier.frontier[loc].parent
        if loc == -1:
            return pet
        can +=1
        pet = list(dict.fromkeys(pet))

    return pet


if __name__ == "__main__":
    main()
