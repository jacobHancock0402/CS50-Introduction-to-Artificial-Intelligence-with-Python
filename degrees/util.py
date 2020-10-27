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

score = [0] * 1000
    moves = actions(board)
    counter = [0] * (len(moves))
    for u in range(len(moves)):
        board2 = copy.deepcopy(board)
        while terminal(board2) == False:
            move = actions(board2)
            board2[move[u][0]][move[u][1]] = player(board2)
            if utility(board2) == 1:
                if num_moves(board2) - num_moves(board) < winlen[u]:
                    winlen[u] = num_moves(board2) - num_moves(board)
                score[u] = 1
                break
                if utility(board2) == -1:
                    board2[move[u][0]][move[u][1]] = EMPTY
                    count += 1



                        if terminal(board) == True:
        return None
    moves = stackFrontier
    moves.frontier =  actions(board)
    for u in range len(moves):
        board2 = copy.deepcopy(board)
        if player(board) = X:
            y = 0
            while terminal(board2) == False:
                for w in range(len(actions(board2)))
                    while moves.frontier[y] != "explored":
                    temp = actions(board2)
                    tempo = Node("unexplored", -1, [0][0] * 3)
                    tempo.action = result(board2,temp[w])
                    moves.frontier.add(tempo)
                    moves.frontier[-1].parent = board
                for y in range(len(moves.froniter),0,-1):
                    while moves.froniter[y].state != "explored":
                        board2[moves.frontier[y].action[0]][moves.frontier[y].action[1]] = X
                    if utility(board2) = 1:
                        if num_moves > winlen[u]:
                            winlen[u] = num_moves
                        score[u] = 1
                    elif utility(board2) == -1:
                        board2 = moves.frontier[y].parent
                    else:
                        min

def max(board,frontier)

        while terminal(board2) == False:
            for w in range(len(actions(board2)))
                temp = actions(board2)
                tempo = Node("unexplored", -1, [0][0] * 3)
                tempo.action = temp[w]
                moves.frontier.add(tempo)
                moves.frontier[-1].parent = board
                for y in range(len(moves.froniter),0,-1):
                    while moves.froniter[y].state != "explored":
                        board2[moves.frontier[y].action[0]][moves.frontier[y].action[1]] = X
                    if utility(board2)= 1:
                        if num_moves > winlen[u]:
                            winlen[u] = num_moves
                            return winlen[u]
                        score[u] = 1
                    elif moves.frontier[y]

                        for i in range(len(score)):
        if score[i] == 1:
            win_count += 1
    if win_count > 1:
        win = min(winlen)
        for s in range(len(winlen)):
            if winlen[s] == win:
                return moves[s]

    else:
        win = max(score)
        for x in range(len(score)):
                if win == scroe[x]:
                    return moves[x]


                                    if x.length != len(x.cells) or x.length != len(assignment[x]):
                    return False