# File: board.py
# Author: Enoch Ngan (engan@bu.edu), 8/12/2023
# Description: I create a Board class for an Eight puzzle game with basic
# methods and attributes, such as for moving pieces and keeping track of them. 
    
#
# board.py (Final project)
#
# A Board class for the Eight Puzzle
#
# name: Enoch Ngan
# email: engan@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[0] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.
        
        # loops through each tile of the gameboard
        for r in range(len(self.tiles)):
            # creates an empty list to store a new row
            nrow = []
            for c in range(len(self.tiles[r])):
                # adds the input number into the new row
                nrow += [int(digitstr[3*r + c])]
                # assigns the positions of where the blank is
                if int(digitstr[3*r + c]) == 0:
                    self.blank_r = r
                    self.blank_c = c
            # replaces the empty original row with new row
            self.tiles[r] = nrow
        
    ### Add your other method definitions below. ###
    
    # function 2
    def __repr__(self):
        """ Returns a string representation for a Board object.
        """
        # creates an empty board accumulator variable 
        board = ""
        # loops through each tile of the gameboard
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[r])):
                # tests if the tile is the blank, and adds _ if so
                if self.tiles[r][c] == 0:
                    board += ("_" + " ")
                # adds non 0s to the board string
                else:
                    board += (str(self.tiles[r][c]) + " ")
            # makes a new line for each row
            board += ("\n")
                
        return (board)
    
    # function 3
    def move_blank(self, direction):
        """ returns a boolean value of whether or not the blank can be moved
            in the input direction, and moves the blank 
            input direction: an approriate direction string
        """
        # returns False if input is not a direction string
        if (direction != "up") and (direction != "down") and (direction != "left") and (direction != "right"):
            return False
        
        # following if/else statements returns False if direction cannot
        # be moved
        if direction == "up":
            if self.blank_r == 0:
                return False
            # switches blank with cell one row above
            else:
                self.tiles[self.blank_r][self.blank_c] = self.tiles[self.blank_r - 1][self.blank_c]
                self.tiles[self.blank_r - 1][self.blank_c] = 0
                # updates the blank position
                self.blank_r -= 1
                return True
        
        elif direction == "down":
            if self.blank_r == 2:
                return False
            # switches blank with cell one row below
            else:
                self.tiles[self.blank_r][self.blank_c] = self.tiles[self.blank_r + 1][self.blank_c]
                self.tiles[self.blank_r + 1][self.blank_c] = 0
                # updates the blank position
                self.blank_r += 1
                return True
            
        elif direction == "left":
            if self.blank_c == 0:
                return False
            # switches blank with cell one row to the left
            else:
                self.tiles[self.blank_r][self.blank_c] = self.tiles[self.blank_r][self.blank_c - 1]
                self.tiles[self.blank_r][self.blank_c - 1] = 0
                # updates the blank position
                self.blank_c -= 1
                return True
            
        elif direction == "right":
            if self.blank_c == 2:
                return False
            # switches blank with cell one row to the right
            else:
                self.tiles[self.blank_r][self.blank_c] = self.tiles[self.blank_r][self.blank_c + 1]
                self.tiles[self.blank_r][self.blank_c + 1] = 0
                # updates the blank position
                self.blank_c += 1
                return True
    
    # function 4
    def digit_string(self):
        """ returns a new digitstr of the current Board object
        """
        # creates an empty string to store new digistr
        new_ds = ""
        
        # loops through each self.tiles to add to the empty string
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[r])):
                new_ds += str(self.tiles[r][c])
                
        return new_ds
    
    # function 5
    def copy(self):
        """ returns a deep copy of the board object from the constructor method
        """
        # creates a new Board object with that string
        copy = Board(self.digit_string())
        
        return copy
    
    # function 6
    def num_misplaced(self):
        """ returns an integer of how many misplaced cells there are in the
            board from the goal state
        """
        # creates a Board object of the goal state
        goal_state = Board("012345678")
        # creates an accumulator variable to track misplaced numbers
        num_misplaced = 0
        
        # loops through each cell of the goal state
        for r in range(len(goal_state.tiles)):
            for c in range(len(goal_state.tiles[r])):
                # adds one to the accumulator vairable if the goal state and current state cell 
                # do not match
                if goal_state.tiles[r][c] != self.tiles[r][c] and self.tiles[r][c] != 0:
                    num_misplaced += 1
        
        return num_misplaced
    
    # helper function for heurisitic 2
    def manhattangeo(self):
        """ returns a the sum of all the distances each tile needs to travel
            in order to get to the goal state
        """
        # creates a Board object of the goal state
        goal_state = Board("012345678")
        # creates an accumulator variable to track misplaced numbers
        misplaced = []
        goaltile = []
        totaltravel = 0
        selftile = []
        
        # loops through each cell of the goal state
        for r in range(len(goal_state.tiles)):
            for c in range(len(goal_state.tiles[r])):
                # adds one to the accumulator vairable if the goal state and current state cell 
                # do not match
                if goal_state.tiles[r][c] != self.tiles[r][c] and self.tiles[r][c] != 0:
                    # store the number in a list and row and column of goal in another list
                    misplaced += [goal_state.tiles[r][c]]
                    goaltile += [[r, c]]
                    
        # get the row and column of the number from self
        for num in misplaced:
            for r in range(len(self.tiles)):
                for c in range(len(self.tiles[r])):
                    if self.tiles[r][c] == num:
                        selftile += [[r, c]]


       # compare the two goal state and other list differences and acculate them
        for r in range(len(goaltile)):
            for c in range(len(goaltile[r])):
                totaltravel += abs(goaltile[r][c] - selftile[r][c])
         
        return totaltravel

 
    # function 7
    def __eq__(self, other):
        """ returns a boolean if the self Board object is the same as the
            other Board object
            input other: a Board object
        """
        # tests if the tiles in self.tiles is equal to the tiles in other.tiles
        return self.tiles == other.tiles    
        
if __name__ == "__main__":
    
    # test cases for functions 1 - 6
    b = Board('142358607')
    print(b)
    print(b.move_blank('up'))
    print(b)
    print(b.move_blank('down'))
    print(b)
    print(b.move_blank('left'))
    print(b)
    print(b.move_blank('right'))
    print(b)
    print(b.tiles)
    print("")
    b = Board('142358607')
    print(b)
    b2 = b.copy()
    print(b2)
    b2.move_blank('up')
    print(b2)
    print (b)
    print("")
    b = Board('142358607')
    print(b)
    print(b.num_misplaced())
    print("")
    print(b.move_blank('right'))
    print(b)
    print(b.num_misplaced())
    b1 = Board('012345678')
    b2 = Board('012345678')
    print(b1 == b2)
    b2.move_blank('right')
    print(b1 == b2)
    print("")
    b = Board('142358607')
    print(b.digit_string())