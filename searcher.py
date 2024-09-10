import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###
    
    # function 1
    def __init__(self, depth_limit):
        """ the constructor method for object Searcher
            input depth_limit: an appropriate integer indicating the depth
            limit
        """
        # creates an attribute of states as an empty list
        self.states = []
        # creates an attribute of tested sates as 0
        self.num_tested = 0
        self.depth_limit = depth_limit


    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s
    
    # function 2
    def should_add(self, state):
        """ returns a boolean based on whether or not the Searcher object
            should search through the state object
            input state: a state object
        """
        # returns False if there is no depth limit, or it is pass the depth limit
        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        # returns False if the state creates a repeating cycle 
        elif state.creates_cycle():
            return False
        # returns True if the state should be searched
        else:
            return True
        
    # function 3
    def add_state(self, new_state):
        """ adds the input new_state to the list self.states
        """
        # appends new_state to the self.states list
        self.states.append(new_state)
    
    # function 4
    def add_states(self, new_states):
        """ adds an input list new_states to self.states
            input new_state: a list of state objects (successors)
        """
        # loops through each state in new_states
        for state in new_states:
            # tests if the state should be added or not
            if self.should_add(state):
                # adds the state to self.states
                self.add_state(state)
                
    # function 5
    def next_state(self):
        """ chooses the next state to be tested from the list of 
            untested states, removing it from the list and returning it
        """
        # chooses a random state from self.states
        s = random.choice(self.states)
        # removes that state
        self.states.remove(s)
        
        return s
    
    # function 6
    def find_solution(self, init_state):
        """ performs a full-random state-space search that stops when the
            goal state is reached, returning the goal state
            input init_state: a State object
        """
        # adds the ini_state input to the list self.states
        self.states.append(init_state)
        
        # loops through all the self.states until there are none left, or
        # the the goal_state is found
        while len(self.states) > 0:
            # finds a randonm state from self.states, tests it, then removes it
            s = self.next_state()
            # adds one to self.num_tested, keeping track of states tested
            self.num_tested += 1
            # stops if it has reached the goal
            if s.is_goal():
                return s
            # adds the successors of the chosen state to self.states
            else:
                self.add_states(s.generate_successors())
        
        # returns none if the Searcher could not find a solution
        return None
    
### Add your BFSeacher and DFSearcher class definitions below. ###

# class 1
class BFSearcher(Searcher):
    """ A class for objects that perform a Breadth First state-space
        search on an Eight Puzzle.
    """
    def next_state(self):
        """ chooses the next state, which is the state that has been in the 
            list the longest, to be tested, then removes it from the list and
            returns it
        """
        # chooses the first state is self.states
        s = self.states[0]
        # removes that state
        self.states.remove(s)
        
        return s

# class 2
class DFSearcher(Searcher):
    """ A class for objects that perform a Depth First state-space
        search on an Eight Puzzle.
    """
    def next_state(self):
        """ chooses the next state, which is the state that has the longest depth,
            to be tested, then removes it from the list and returns it
        """
        # chooses the last state is self.states
        s = self.states[-1]
        # removes that state
        self.states.remove(s)
        
        return s

def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

### Add your other heuristic functions here. ###

def h1(state):
    """ a heuristic function that returns the number of misplaced tiles"""
    return state.board.num_misplaced()

def h2(state):
    """ a heuristic function that returns a number of the sum of 
        all the distances each tile has to travel to get to the goal
        state"""
    return state.board.manhattangeo()

# class 3
class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
    
    def __init__(self, depth_limit, heuristic):
        """ constructor for a GreedySearcher object
            inputs:
             * depth_limit - the depth limit of the searcher
             * heuristic - a reference to the function that should be used 
             when computing the priority of a state
        """
        # calls the Superclass Searcher to inherit the depth_limit attribute
        super().__init__(depth_limit)
        self.heuristic = heuristic

    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s

    def priority(self, state):
        """ returns an integer score of the priority the state has respectively
            to other states
            input state: a State object
        """
        # calls the heuristic function to get a number of misplaced tiles
        h = self.heuristic(state)
        # calculates the priority to allow the max() function later on
        priority = -1 * h
        
        return priority 
    
    def add_state(self, state):
        """ adds the input state and its priority to the list of lists self.states
        """
        # appends state and its priority to the self.states list of lists
        self.states.append([self.priority(state), state])
        
    def next_state(self):
        """ chooses the next state, which is the state that has the mas priority,
            to be tested, then removes it from the list and returns it
        """
        # chooses the max priority state is self.states
        s = max(self.states)
        # removes that state
        self.states.remove(s)
        
        return s[1]
    
    def find_solution(self, init_state):
        """ performs a full-random state-space search that stops when the
            goal state is reached, returning the goal state
            input init_state: a State object
        """
        # adds the init_state and the priority input to the list self.states
        self.states.append([self.priority(init_state), init_state])
        
        # loops through all the self.states until there are none left, or
        # the the goal_state is found
        while len(self.states) > 0:
            # finds a randonm state from self.states, tests it, then removes it
            s = self.next_state()
            # adds one to self.num_tested, keeping track of states tested
            self.num_tested += 1
            # stops if it has reached the goal
            if s.is_goal():
                return s
            # adds the successors of the chosen state to self.states
            else:
                self.add_states(s.generate_successors())
        
        # returns none if the Searcher could not find a solution
        return None

### Add your AStarSeacher class definition below. ###

class AStarSearcher(GreedySearcher):
    """ A class for objects that perform an informed A* state-space
        search on an Eight Puzzle.
    """
    
    def priority(self, state):
        """ returns an integer score of the priority the state has respectively
            to other states
            input state: a State object
        """
        # calls the heurstic function to get a number of misplaced tiles
        heuristic = self.heuristic(state)
        cost = state.num_moves
        # calculates the priority to allow the max() function later on
        priority = -1 * (heuristic + cost)
        
        return priority


if __name__ == "__main__":
    
    # test cases
    searcher1 = Searcher(-1) 
    print(searcher1)
    searcher2 = Searcher(10)
    print(searcher2)
    b1 = Board('142358607')
    s1 = State(b1, None, 'init')  # initial state
    searcher1 = Searcher(-1)  # no depth limit
    searcher1.add_state(s1)
    searcher2 = Searcher(1)   # depth limit of 1 move!
    searcher1.add_state(s1)
    b2 = b1.copy()
    print(b2.move_blank('left'))
    s2 = State(b2, s1, 'left')    # s2's predecessor is s1
    print(searcher1.should_add(s2))
    print(searcher2.should_add(s2))
    b3 = b2.copy()
    print(b3.move_blank('right'))       # get the same board as b1 
    s3 = State(b3, s2, 'right')   # s3's predecessor is s2
    print(searcher1.should_add(s3))      # adding s3 would create a cycle
    print(searcher2.should_add(s3))
    print(b3.move_blank('left'))         # reconfigure b3
    print(b3.move_blank('up'))
    s3 = State(b3, s2, 'up')      # recreate s3 with new b3 (no cycle)
    print(s3.num_moves)
    print(searcher1.should_add(s3))      # searcher1 has no depth limit
    print(searcher2.should_add(s3))      # s3 is beyond searcher2's depth limit
    
    print("\nfunction 4")
    b = Board('142358607')
    s = State(b, None, 'init')
    searcher = Searcher(-1)
    searcher.add_state(s)
    print(searcher.states)
    succ = s.generate_successors()
    print(succ)
    searcher.add_states(succ)             # add all of the successors
    print(searcher.states)
    print(succ[-1])
    succ2 = succ[-1].generate_successors() 
    print(succ2)
    searcher.add_states(succ2)
    print(searcher.states)
    
    print("\nfunction 6: example 1")
    b = Board('012345678')       # the goal state!
    s = State(b, None, 'init')   # start at the goal
    print(s)
    searcher = Searcher(-1)
    print(searcher)
    print(searcher.find_solution(s))     # returns init state, because it's a goal state
    print(searcher)

    print("\nfunction 6: example 2")
    b = Board('142358607')       
    s = State(b, None, 'init')   
    print(s)
    searcher = Searcher(-1)
    print(searcher)
    print(searcher.find_solution(s))     # returns goal state at depth 11
    print(searcher)
    searcher = Searcher(-1)   # a new searcher with the same init state
    print(searcher)
    print(searcher.find_solution(s))     # returns goal state at depth 5
    print(searcher)
    
    print("\nfunction 7")
    b = Board('142305678')    # only 2 moves from a goal
    print(b)
    s = State(b, None, 'init')   
    searcher = Searcher(-1)
    goal = searcher.find_solution(s)
    print(goal)
    print(goal.print_moves_to())

    print("\nbfs")
    b = Board('142358607')       
    s = State(b, None, 'init')
    print(s)
    bfs = BFSearcher(-1)
    bfs.add_state(s)
    print(bfs.next_state())    # remove the initial state
    succ = s.generate_successors()
    print(succ)
    bfs.add_states(succ)
    print(bfs.next_state())
    print(bfs.next_state())
    
    print("\ndfs")
    b = Board('142358607')       
    s = State(b, None, 'init')
    print(s)
    dfs = DFSearcher(-1)
    dfs.add_state(s)
    print(dfs.next_state())    # remove the initial state
    succ = s.generate_successors()
    print(succ)
    dfs.add_states(succ)
    print(dfs.next_state())
    print(dfs.next_state())

    print("\nadd_states for Greedy Search")
    b = Board('142358607')       
    s = State(b, None, 'init')
    g = GreedySearcher(-1, h1)
    g.add_state(s)
    print(g.states)
    succ = s.generate_successors()
    g.add_state(succ[0])
    print(g.states)
    g.add_state(succ[1])
    print(g.states)
    
    print("\nnext state for Greedy Search")
    b = Board('142358607')       
    s = State(b, None, 'init')
    g = GreedySearcher(-1, h1)  # no depth limit, basic heuristic
    g.add_state(s)
    succ = s.generate_successors()
    g.add_state(succ[1])
    print(g.states)
    print(g.next_state())    # -5 is the higher priority
    print(g.states)
    
    print("\nnext state for AStar Search")
    b = Board('142358607')       
    s = State(b, None, 'init')
    a = AStarSearcher(-1, h1)  # no depth limit, basic heuristic
    a.add_state(s)
    print(a.states)
    succ = s.generate_successors()
    a.add_state(succ[1])
    print(a.states)
    print(a.next_state())    # -5 is the higher priority
    print(a.states)
