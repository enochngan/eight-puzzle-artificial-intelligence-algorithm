# File: state.py
# Author: Enoch Ngan (engan@bu.edu), 8/12/2023
# Description: I create a State class that has multiple methods and attributes,
# such as generate successors of the input State class. 
    
#
# state.py (Final project)
#
# A State class for the Eight Puzzle
#
# name: Enoch Ngan
# email: engan@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

from board import *

# a 2-D list that corresponds to the tiles in the goal state
GOAL_TILES = [[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8]]

# the list of possible moves, each of which corresponds to
# moving the blank cell in the specified direction
MOVES = ['up', 'down', 'left', 'right']

class State:
    """ A class for objects that represent a state in the state-space 
        search tree of an Eight Puzzle.
    """
    ### Add your method definitions here. ###
    
    # function 1
    def __init__(self, board, predecessor, move):
        """ the constructor class for State object
            input board: a Board object
            input predecessor: the State object the current State was derived 
            from
            input move: an appropriate direction string
        """
        self.board = board
        self.predecessor = predecessor
        self.move = move
        
        # if there are no predecessors, num_moves equals 0
        if self.predecessor == None:
            self.num_moves = 0
        # add 1 to current num_moves for each predecessor 
        else:
            self.num_moves = self.predecessor.num_moves + 1

    def __repr__(self):
        """ returns a string representation of the State object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = self.board.digit_string() + '-'
        s += self.move + '-'
        s += str(self.num_moves)
        return s
    
    def creates_cycle(self):
        """ returns True if this State object (the one referred to
            by self) would create a cycle in the current sequence of moves,
            and False otherwise.
        """
        # You should *NOT* change this method.
        state = self.predecessor
        while state != None:
            if state.board == self.board:
               return True
            state = state.predecessor
        return False

    def __gt__(self, other):
        """ implements a > operator for State objects
            that always returns True. This will be needed to break
            ties when we use max() on a list of [priority, state] pairs.
            If we don't have a > operator for State objects,
            max() will fail with an error when it tries to compare
            two [priority, state] pairs with the same priority.
        """
        # You should *NOT* change this method.
        return True
    
    # function 2
    def is_goal(self):
        """ returns a boolean value if the current state is equal to the goal state"""
        # tests if GOAL_TILES has the same tiles as self.board.tiles
        return GOAL_TILES == self.board.tiles
    
    # function 3
    def generate_successors(self):
        """ returns a list of possible successors for the current state object
        """
        # creates an empty list of successors
        successors = []
        # parses through each direction from list MOVES
        for m in MOVES:
            # creates a deep copy of the board
            b = self.board.copy()
            # checks if the blank can move in the given direction, adding the
            # new state into the list if it can
            if b.move_blank(m):
                new_state = State(b, self, m)
                successors.append(new_state)

        return successors
    
    # function 7
    def print_moves_to(self):
        """ prints the sequence of moves from the intial state object to 
            the goal state
        """
        # the base case: prints the initial state when the state has no
        # predecessor
        if self.predecessor == None:    
            print('initial state:')
            print(self.board)
        # the recursive case: calls the method on the predecessor of the state
        # object, and prints out the board
        else:
            self.predecessor.print_moves_to()
            print(f"move the blank {self.move}:")
            print(self.board)

if __name__ == "__main__":
    
    # test cases for functions 1 - 3
    b1 = Board('142358607')
    s1 = State(b1, None, 'init')
    print(s1)
    b2 = b1.copy()
    b2.move_blank('up')
    s2 = State(b2, s1, 'up')
    print(s2)
    s1 = State(Board('102345678'), None, 'init')
    print(s1.is_goal())
    s2 = State(Board('012345678'), s1, 'left')
    print(s2.is_goal())
    
    print("function 3")
    b1 = Board('142358607')
    print(b1)
    s1 = State(b1, None, 'init')
    print(s1)
    succ = s1.generate_successors()   
    print(succ)
    print(s1)
    print(succ[2])
    print(succ[2].generate_successors())
    print(succ[0].generate_successors())
    
    
    