# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import solve, solve_complete, hint_by_depth


class Controller:
    """Class responsible for connection between puzzles and views.

    You may add new *private* attributes to this class to help you
    in your implementation.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle associated with this game controller
    # @type _view: View
    #     The view associated with this game controller
    # @type _data: StateTree
    #     The tree that stores all the state data associated with the game
    # @type _index: [int, int]
    #     The index that labels every state data that is stored in the data
    # @type _undo: bool
    #     The indicator that shows if the previous command is :UNDO or not

    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = puzzle
        self._data = StateTree(puzzle)     # with index [0, 0]
        self._index = [0, 0]
        self._undo = False
        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
        """
        return str(self._puzzle)

    def undo(self, current):
        """
        Return the parent node info(includes its puzzle state and index)
         of the current position in the tree.

        @type current: Puzzle
        @rtype: list
                A list contains previous puzzle state and previous index
        """
        if self._data.get_prev(current)[1]:
            return self._data.get_prev(current)[0]
        else:
            raise ValueError

    def attempt(self, current):
        """
        Return a list of input info (including the command they typed and
        the puzzle state from that command) the user has tried under current
        state.

        @type current: Puzzle
        @rtype: list[list[str, Puzzle]]
        """
        results = []
        if self._data.get_attempt(current)[1]:
            for subtree in self._data.get_attempt(current)[0]:
                temp = subtree.command + '\n' + '----------------' +\
                       '\n' + str(subtree.state)
                results.append(temp)
        else:
            raise ValueError
        return results

    def save_move(self, action, prev_state, prev_index):
        """ Save the latest puzzle state into self._data as well as its
        previous information.

        @type action: str
        @type prev_state: Puzzle
        @type prev_index: tuple
        @rtype: None
        """
        if self._undo:
            test = StateTree(self._puzzle, tuple(self._index),
                             prev_state, prev_index, action)
            self._index[0] += 1
            # if have a different input, update x and y and save
            # if have an existing input, update y only
            if test not in self._data:
                self._index[1] += 1
                new = StateTree(self._puzzle, tuple(self._index),
                                prev_state, prev_index, action)
                self._data.save(new, prev_state)
            self._undo = False
        else:
            self._index[0] += 1
            new = StateTree(self._puzzle, tuple(self._index),
                            prev_state, prev_index, action)
            if new not in self._data:
                self._data.save(new, prev_state)

    def to_solve(self):
        """ To solve the puzzle.

        @rtype: tuple
        """
        result = solve(self._puzzle)
        if result is None:
            message = 'The puzzle is unsolvable from the current state'
            return (message, True)
        else:
            return (str(result), True)

    def to_solve_all(self):
        """ To give all solutions of the puzzle.

        @rtype: tuple
        """
        result_all = solve_complete(self._puzzle)
        if len(result_all) == 0:
            message = 'The puzzle is unsolvable from the current state'
            return (message, True)
        else:
            return ('\n'.join(map(str, result_all)), True)

    def to_undo(self):
        """ To undo the puzzle.

        @rtype: tuple
        """
        if self._index[0] > 0:
            current = self._puzzle
            self._puzzle = self.undo(current)[0]
            self._index = list(self.undo(current)[1])
            self._undo = True
            return (self.state(), False)
        else:
            message = 'Already in the initial state.'
            return (message, False)

    def to_attempt(self):
        """ To give all previous attempts of the current state.

        @rtype: tuple
        """
        current = self._puzzle
        attempts = self.attempt(current)
        if len(attempts) == 0:
            print('You have not tried anything yet!')
        return ('\n'.join(map(str, attempts)), False)

    def to_hint(self, action):
        """ To give hint of the puzzle at current state.

        @type action: str
        @rtype: tuple
        """
        typed = action.split()
        if len(typed) == 2:
            try:
                n = int(typed[1])
            except ValueError:
                message = 'Please type the number of moves!'
                return (message, False)
            if n < 1:
                message = 'Please type a positive number!'
                return (message, False)
            else:
                hint = hint_by_depth(self._puzzle, n)
                return (hint, False)
        else:
            message = 'Please type the number of moves!'
            return (message, False)

    def to_react(self, action):
        """ To change the puzzle state according to the user's command.

        @type action: str
        @rtype: tuple
        """
        if len(action) == 0:
            if self._puzzle.is_solved():
                return (self.state(), True)
            else:
                print('Invalid move. Please try again!\n')
                return (self.state(), False)
        else:
            if self._puzzle.is_valid(action):
                prev_state = self._puzzle
                prev_index = tuple(self._index)
                # move
                self._puzzle = self._puzzle.move(action)
                # save move
                self.save_move(action, prev_state, prev_index)
                # print the current state
                if self._puzzle.is_solved():
                    return (self.state(), True)
                else:
                    return (self.state(), False)
            else:
                message = 'Invalid move. Please try again!\n'
                return (message, False)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """
        if action == 'exit':
            return ('', True)

        elif action == ':SOLVE':
            return self.to_solve()

        elif action == ':SOLVE-ALL':
            return self.to_solve_all()

        elif action == ':UNDO':
            return self.to_undo()

        elif action == ':ATTEMPTS':
            return self.to_attempt()

        elif action.startswith(':HINT'):
            return self.to_hint(action)

        else:
            return self.to_react(action)


class StateTree:
    """ A tree data structure that contains all the state that the user has
    reached from the puzzle game.

    === Public Attributes ===
    @type state: Puzzle
        The original puzzle state stored at the tree's root.
    @type input: list[StateTree]
        A list of all puzzle state the user has reached.
    @type tup: tuple(int, int)
        A tuple that indexes the position of each state in the tree.
    @type prev_state: Puzzle | None
        The puzzle state of the parent node.
        It is None if the node is the root.
    @type prev_index: tuple(int, int) | None
        The index tuple of the parent node.
        It is None if the node is the root.
    @type command: str
        The command that the user typed to get to this state.
        It is None if the state is the root(original puzzle state).

    """

    def __init__(self, state, tup=(0, 0), prev_state=None,
                 prev_index=None, command=None):
        """Initialize the state tree.

        @type state: Puzzle
        @type tup: tuple(int, int)
        @type prev_state: Puzzle
        @type prev_index: tuple(int, int)
        @type command: str
        @rtype: None
        """
        self.state = state
        self.input = []
        self.tup = tup
        self.prev_state = prev_state
        self.prev_index = prev_index
        self.command = command

    def is_empty(self):
        """Return True if this tree is empty.

        @type self: StateTree
        @rtype: bool
        """
        return self.state is None

    def add_child(self, child):
        """ Add new child state node to the input list of the current state.

        @type child: StateTree
        @rtype: None
        """
        if self.is_empty():
            raise ValueError()
        else:
            self.input.append(child)

    def __contains__(self, obj):
        """Return True if the tree contains the given puzzle state.

        @type obj: StateTree
        @rtype: bool
        """
        is_found = False
        if self.is_empty():
            return False

        else:
            if self.state == obj.state:
                is_found = True
            else:
                for subtree in self.input:
                    if subtree.__contains__(obj):
                        is_found = True
            return is_found

    def save(self, child, curr):
        """ Insert a child node under given puzzle state.
        @type child: StateTree
        @type curr: Puzzle
        @rtype: bool
        """
        if self.state == curr:
            self.add_child(child)
            return True
        else:
            for state_obj in self.input:
                if state_obj.state == curr:
                    state_obj.add_child(child)
                    return True
                else:
                    if state_obj.save(child, curr):
                        return True
        return False

    def get_prev(self, curr):
        """ Return a tuple contains information(puzzle state and index) about
        the parent node of given puzzle state, along with a boolean:
        True if there is a parent node; False if it is already the root.

        @type curr: Puzzle
        @rtype: tuple(list[Puzzle, tuple], bool)
        """
        result = []
        if self.state == curr:
            result.append(self.prev_state)
            result.append(self.prev_index)
            return result, True
        else:
            for sub in self.input:
                if sub.state == curr:
                    result.append(sub.prev_state)
                    result.append(sub.prev_index)
                    return result, True
                else:
                    if sub.get_prev(curr)[1]:
                        res = sub.get_prev(curr)
                        return res
        return result, False

    def get_attempt(self, curr):
        """ Return a tuple with the list of all puzzle state the user has tried,
        along with a boolean express: True if there are attempts recorded,
        False if the user has not tried anything yet.

        @type curr: Puzzle
        @rtype: tuple(list[StateTree], bool)
        """
        if self.state == curr:
            return self.input, True
        else:
            for sub in self.input:
                if sub.state == curr:
                    return sub.input, True
                else:
                    if sub.get_attempt(curr)[1]:
                        res = sub.get_attempt(curr)
                        return res
        return [], False

if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    from word_ladder_puzzle import WordLadderPuzzle
    # s = SudokuPuzzle([['A', 'B', '', 'D'],
    #                   ['C', 'D', '', 'B'],
    #                   ['B', '', '', ''],
    #                   ['D', '', '', '']])
    s = WordLadderPuzzle('mist', 'cars')
    c = Controller(s)
