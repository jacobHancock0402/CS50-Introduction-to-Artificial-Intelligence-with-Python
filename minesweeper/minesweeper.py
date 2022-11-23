import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    # Checks Sentence to see if we can say with certainty it's a mine
    def known_mines(self):
        # If the number of surrounding cells is equal to number of surrounding bombs, then all of them must be bombs
        if len(self.cells) == self.count:
            return self.cells

    # Replica of the Function above but for safes instead
    def known_safes(self):
        # If no mines around the cell, all surrounding cells must be safe
        if self.count == 0:
            return self.cells
    # Updates the sentence to indicate the cell is a mine
    def mark_mine(self, cell):
        if cell in self.cells:
            # Mine is removed so one less mine to be counted
            self.cells.remove(cell)
            self.count -= 1
    # Updates the sentence to indicate the cell is safe
    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
    # Gets all surrounding cells, as in all cells that are within one square
    def get_sets(self, cell, count):
        lit = [0] * 2
        sets = set()
        for w in range(cell[0] - 1, cell[0] + 2):
            for s in range(cell[1] - 1, cell[1] + 2):
                # Takes X and Y values of the cell
                lit[0] = w
                lit[1] = s
                temps = tuple(lit)
                # Only takes cells that are within the board boundaries
                if lit[0] >= 0 and lit[0] <= 7 and lit[1] >= 0 and lit[1] <= 7 :
                    # Ensures subset method can be used by creating smaller sentences
                    if temps not in self.moves_made:
                        sets.add(temps)
        # Returns a sentence with all the surrounding cells and the number that are bombs
        end = Sentence(sets,count)
        return end
    # Implementation of the subset method
    def order_mines(self,sentence):
        end = list()
        pooper = 0
        counter = 0
        # Loops through every sentence and checks wether or not either sentences are subsets of eachother
        for s in range(len(self.knowledge)):
            counter = 0
            # Checks for sentences that are subsets
             if (sentence.cells in self.knowledge[s].cells or self.knowledge[s].cells in sentence.cells) and sentence.cells != self.knowledge[s].cells:
                # If they are subsets, then check for which is the subset
                if len(sentence.cells) > len(self.knowledge[s].cells):
                    timp = list()
                    tamp = set()
                    # Loops through whole set of cells
                    for u in sentence.cells:
                        # If its in the subset, we take it out. Basically performing the action of taking away the cells
                        if u not in self.knowledge[s].cells:
                            timp.clear()
                            del tamp
                            timp.insert(0, u[0])
                            timp.insert(1, u[1])
                            tamp = tuple(timp)
                            if counter == 0:
                                se = Sentence({"None","None"},0)
                                se.cells.remove("None")
                            else:
                                se.cells.add(tamp)

                            counter += 1
                    if counter == 0:
                        se = Sentence({"None","None"}, 0)
                        se.cells.remove("None")
                    # Count is the set's count minus subset's count
                    se.count = sentence.count - self.knowledge[s].count
                    if se.count < 0:
                        se.count = 0
                    if "None" not in se.cells:

                        pooper += 1
                        end.append(se)
                # Same as above but if the other sentence is the subset
                elif len(self.knowledge[s].cells) > len(sentence.cells):
                    counter = 0
                    timp = list()
                    tamp = set()
                    # So now we take away from opposite sentences
                    for u in self.knowledge[s].cells:
                        if u not in sentence.cells:
                            timp.clear()
                            del tamp
                            timp.insert(0, u[0])
                            timp.insert(1, u[1])
                            tamp = tuple(timp)
                            if counter == 0:
                                ses = Sentence({"None","None"},0)
                                ses.cells.remove("None")
                            else:
                                ses.cells.add(tamp)
                            counter += 1
                    if counter == 0:
                        ses = Sentence({"None","None"}, 0)
                        ses.cells.remove("None")
                    ses.count = self.knowledge[s].count - sentence.count
                    if ses.count < 0:
                        ses.count = 0
                    if "None" not in ses.cells:
                        pooper += 1
                        end.append(ses)
        # Returns every new sentence that can be created
        return end

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        self.moves_made.add(cell)
        self.mark_safe(cell)
        # Gets all cells around the cell
        tempo = self.get_sets(cell,count)
        if tempo not in self.knowledge:
            self.knowledge.append(tempo)
        # Loops through entire knowledge base checking for what it can infer, call safe or call mine
        for x in range ((len(self.knowledge))):
            # Checks whether or not the sentence the cells can be seen as mines, or as safes
            safe = Sentence.known_safes(Sentence(self.knowledge[x].cells,self.knowledge[x].count))
            mine = Sentence.known_mines(Sentence(self.knowledge[x].cells,self.knowledge[x].count))
            if safe != None:
                ido = list(safe)
                if len(safe) != 1:
                    for u in range(len(safe)):
                        self.mark_safe(ido[u])
                else:
                    self.mark_safe(ido[0])

            if mine != None:
                dude = list(mine)
                if len(mine) != 1:
                    for y in range(len(mine)):
                        self.mark_mine(dude[y])
                else:
                    self.mark_mine(dude[0])



            # Calls subset method to see if it can infer anything
            idk = self.order_mines(self.knowledge[x])
            for p in range(len(idk)):
                variable = idk[p]
                if variable.cells != "None":
                    self.knowledge.append(idk[p])







    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # If the move is safe and hasn't already being taken, then return it
        for x in self.safes:
            if x not in self.moves_made:
                return x
        # Else return it and make a random move
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly a***REMOVED*** cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        cutter = 0
        clear = list()
        temp = [0] * 2
        # Loops through whole board and adds any cells that aren't mines or are already filled
        for x in range(self.width):
            for y in range(self.height):
                temp[0] = x
                temp[1] = y
                tup = tuple(temp)

                if tup not in self.moves_made and tup not in self.mines:
                    cutter += 1
                    clear.append(tup)
        # If no moves can be taken, then player has won
        if cutter == 0:
            return None
        # Else randomly pick a cell from the one's available
        else:
            return random.choice(clear)
