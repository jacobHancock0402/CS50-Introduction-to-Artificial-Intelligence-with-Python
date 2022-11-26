import sys
import copy
import math
from collections import OrderedDict

from crossword import *
yessir

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Loops through every variable
        for x in self.domains:
            counter = 0
            # Identifies which way to calculate length
            if x.direction == "across":
                i = 1
            else:
                i = 0
            end = x.cells[-1][i]
            start = x.cells[0][i]
            # Loops through each cells and ensures is it is horizontally or vertically in-line with starting point
            # The axis is determined by the direction of the variable, as seen above
            for y in range(len(x.cells)):
                if x.cells[y][i] != start + y:
                    x.cells.remove(x.cells[y])


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        counter = 0

        rem = copy.deepcopy(self.domains[x])
        overlap = self.crossword.overlaps[x , y]
        poss = list()
        # Finds each letter that would be acceptable for the other variable's character to take on
        if not overlap:
            return False
        for j in self.domains[y]:
            if overlap[1] < len(j):
                dawg = [j[overlap[1]], j]
                poss.append(dawg)
        # Loops through each word in x's domain and check it's overlap character against the acceptable characters
        for w in self.domains[x]:
            for f in poss:
                # Check whether the word is long enough to be index at the overlap position
                if overlap[0] < len(w):
                    # Only true if the word isn't the same as the word y's character came from
                    if w[overlap[0]] == f[0] and w != f[1]:
                        counter = 1
                        # Safe words are removed
                        rem.remove(w)
                        break
        # Loops through dictionary of words that weren't removed, and removes the from the domain of x
        # This then leaves only the acceptable words within x's domain
        if counter > 0:
            for t in rem:
                self.domains[x].remove(t)
            return True
        else:
            return False



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arc isn't supplied then go through every variable
        if arcs == None:
            doc = self.crossword.variables
        # Else go through only the arc that is now supplied
        else:
            doc = arcs
            # Loops through every variable and calls the revise function to ensure arc consistency
        for x in doc:
            for y in doc:
                # Doesn't call revise on same variable
                if y != x:
                    self.revise(x, y)
        # Return False if any variable is empty or None
        for j in self.domains:
            if not j:
                return False
        # Else returns True
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Checks if every variable is in the assignment, indicating a conclusion
        if len(assignment) != len(self.crossword.variables):
            return False
        # Returns False is not every variable has a value assigned
        for x in assignment:
            if not x:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Loops through each variable
        overlap = [0] * 2
        for x in assignment:
            counter = 0
            # Creates a copy of assignment
            # x variable is popped and then assignment is checked to see if an x key is still in the dict
            # If so it is a duplicate so False is returned
            cop = copy.deepcopy(assignment)
            cop.pop(x)
            if x in cop:
                return False
            for y in assignment:
                # Finds overlap point if the two variables are not the same
                if x != y:
                    overlap = self.crossword.overlaps[x , y]
                # ¯\_(ツ)_/¯
                if x == y:
                    counter += 1
                if counter > 1:
                    return False
                # Checks for length equality
                if len(assignment[x]) != x.length:
                    return False
                # Only enters if overlap isn't empty and x and y aren't equal
                if overlap and x != y:
                    # Checks whether word is compatible with overlap index
                    if overlap[0] < len(assignment[x]) and overlap[1] < len(assignment[y]):
                        # Verifies that overlap characters are same
                        if assignment[x][overlap[0]] != assignment[y][overlap[1]]:
                            # If not, False is returned
                            return False
                    # If index isn't possible, then the word isn't long enough for the space
                    else:
                        return False

        return True




    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values a***REMOVED*** the neighbors of `var`.
        """

        score = dict()
        counter = 0
        self.ac3()
        # Creates a key for each word in the variable
        for p in self.domains[var]:
            score[p] = 0
        # Loops through the variable's neighbor
        for x in self.crossword.neighbors(var):
            # Finds overlap position
            loc = self.crossword.overlaps[var,x]
            # Loops through each word in the given variable's domain, and in it's neighbors's domain
            for y in self.domains[var]:
                for j in self.domains[x]:
                    # If the word cut's off it's neighbors, it's score is increased by 1 (min score is better)
                    if y[loc[0]] != j[loc[1]]:
                        score[y] = score[y] + 1
        # Sorts the dict into a list of pairs
        New = sorted(score.items(), key=lambda x: x[1])
        return New




    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Score will always be less than infinity
        MinScore = math.inf
        self.ac3()
        # Loops through every variable
        for x in self.domains:
            # If variable has less values in it's domain than the frontrunning variable, then it takes it's spot
            if len(self.domains[x]) < MinScore and x not in assignment:
                MinScore = len(self.domains[x])
                map = x
            # If the variable has the same length, then it is swapped if it ha
            if len(self.domains[x]) == MinScore and x not in assignment:
                if len(self.crossword.neighbors(x)) > len(self.crossword.neighbors(map)):
                    map = x
        # Returns the variable with the least score
        return map


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        counter = 0
        mem = [0] * 2
        # Loops until creation has finished
        while self.assignment_complete(assignment) == False:
            counter += 1
            self.enforce_node_consistency()
            self.ac3(arcs = assignment)
            # Finds next variable and rank's it's applicable words
            next = self.select_unassigned_variable(assignment)
            rank = self.order_domain_values(next,assignment)
            some_var = len(assignment)
            # Loops through each word and checks to see whether it is compatible
            for x in rank:
                assignment[next] = x[0]
                # If it is compatible and creation is complete, assignment is returned
                if self.assignment_complete(assignment) == True and self.consistent(assignment) == True:
                    return assignment
                # If assignment is complete but variable is not applicable, then it is popped so we can try other words
                if self.assignment_complete(assignment) == True:
                    assignment.pop(next)
                # If it is applicable, the loop is ended so we can choose another variable
                elif self.consistent(assignment) == True:
                    break
                # If the word is not consistent, it is popped off
                if self.consistent(assignment) == False and self.assignment_complete(assignment) != True:
                    assignment.pop(next)
            # If no word was added, there must be a problem deeper within so dictionary is cleared
            if len(assignment) == some_var:
                mem = copy.deepcopy(assignment)
                assignment.clear()


        return assignment



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
