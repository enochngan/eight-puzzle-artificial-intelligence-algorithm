# File: eight_puzzle.py
# Author: Enoch Ngan (engan@bu.edu), 8/12/2023
# Description: A file that contains a driver function to test search.py, state.py
# and board.py to perform a full-random state-space search on a given puzzle
# eight_puzzle, and return a solution with steps included. 
#
# eight_puzzle.py (Final Project)
#
# driver/test code for state-space search on Eight Puzzles
#
# name: Enoch Ngan
# email: engan@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

from searcher import *
from timer import *
import math

def create_searcher(algorithm, depth_limit = -1, heuristic = None):
    """ a function that creates and returns an appropriate
        searcher object, based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm the searcher
              should implement
          * depth_limit - an optional parameter that can be used to
            specify a depth limit 
          * heuristic - an optional parameter that can be used to pass
            in a heuristic function
            
        Note: If an unknown value is passed in for the algorithm parameter,
        the function returns None.
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(depth_limit)
## You will uncommment the following lines as you implement
## other algorithms.
    elif algorithm == 'BFS':
        searcher = BFSearcher(depth_limit)
    elif algorithm == 'DFS':
        searcher = DFSearcher(depth_limit)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(depth_limit, heuristic)
    elif algorithm == 'A*':
        searcher = AStarSearcher(depth_limit, heuristic)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, depth_limit = -1, heuristic = None):
    """ a driver function for solving Eight Puzzles using state-space search
        inputs:
          * init_boardstr - a string of digits specifying the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm you want to use
          * depth_limit - an optional parameter that can be used to
            specify a depth limit 
          * heuristic - an optional parameter that can be used to pass
            in a heuristic function
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')

    searcher = create_searcher(algorithm, depth_limit, heuristic)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()

def process_file(filename, algorithm, depth_limit = -1, heuristic = None):
    """ returns a string of results that report the amount of moves and states
        the input algorithm takes on each line of puzzles from the filename
        input filename: a file with digitstrs
        input algorithm: an appropriate algorithm name
        depth_limit: an appropriate depth_limit for algorithms that need it
        heurisitc: an appropriate heuristic (h0, h1, h2)
    """
    # opens the filename and reads it
    f = open(filename, 'r')
    # creates empty accumulator variables to store the amonut of puzzles tested,
    # and the average amount of moves and states  
    puzzles = 0
    avgm = []
    avgs = []
    
    # loops through each line in the file and uses the input algorithm on it
    for line in f:
        # splices the list to get the digitstr
        line = line[0:9]
        # creates a Board and State with that digitstr
        b = Board(line)
        s = State(b, None, 'init')

        # creates a Searcher from the input attributes
        searcher = create_searcher(algorithm, depth_limit, heuristic)
        # returns if it fails to create a searcher
        if searcher == None:
            print('Failed to create a searcher.')

        soln = None
        # stores the solution 
        try:
            soln = searcher.find_solution(s)
        # returns when there is a Keyboard interuption, for example if the
        # algorithms is taking too long
        except KeyboardInterrupt:
            print(f'{line}: search terminated, ', end='')
        
        # returns if there is no solution
        if soln == None:
            print('no solution')
        # returns if the searcher finds a solution, formatting the answer to print
        else:
            print(f'{line}: {soln.num_moves} moves, {searcher.num_tested} states tested')
            # adds to the accumulator variables for each puzzle solved
            puzzles += 1
            avgm += [soln.num_moves]
            avgs += [searcher.num_tested]

    print('')
    print(f'solved {puzzles} puzzles')
    # returns the averages of all the solved puzzles
    if len(avgm) == 0 or len(avgs) == 0:
        pass
    else:
        print(f'averages: {sum(avgm)/len(avgm)} moves, {sum(avgs)/len(avgs)} states tested')
    
         
        