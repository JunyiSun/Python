# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle (see Part 4).
"""
from puzzle import Puzzle


def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: Puzzle | None
    """
    if puzzle.is_solved():
        return puzzle
    else:
        lst = puzzle.extensions()
        if verbose:
            for i in lst:
                print(i)
        # the puzzle is finished answering, but with wrong solution
        if len(lst) == 0:
            return None
        else:
            choices = []
            for status in lst:
                # if one status is a correct solution, return it
                if status.is_solved():
                    return status
                else:
                    # the status is not solved, explore next extension
                    next_step = status.extensions()
                    if verbose:
                        for j in next_step:
                            print(j)
                    choices.extend(next_step)

            # No possible next steps
            if len(choices) == 0:
                return None
            else:
                for choice in choices:
                    # for each next state, recursively solve them
                    if verbose:
                        answer = solve(choice, True)
                    else:
                        answer = solve(choice)
                    # if the answer is a correct solution, return it
                    if answer is not None:
                        return answer
                # When all answers are None
                return None


def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: list[Puzzle]
    """
    final = []
    if puzzle.is_solved():
        final.append(puzzle)
        return final
    else:
        lst = puzzle.extensions()
        if verbose:
            for i in lst:
                print(i)
        # the puzzle is finished answering, but with wrong solution
        if len(lst) == 0:
            return final
        else:
            choices = []
            for status in lst:
                if status.is_solved():
                    final.append(status)
                # not fully solved yet, then explore its next possible steps
                next_step = status.extensions()
                if verbose:
                    for j in next_step:
                        print(j)
                choices.extend(next_step)

            # if there is no possible next steps
            if len(choices) == 0:
                return final
            else:
                for choice in choices:
                    # for each next state, recursively solve them
                    if verbose:
                        answer = solve_complete(choice, True)
                    else:
                        answer = solve_complete(choice)
                    final.extend(answer)
                return final


def hint_by_depth(puzzle, n):
    """Return a hint for the given puzzle state.

    Precondition: n >= 1.

    If <puzzle> is already solved, return the string 'Already at a solution!'
    If <puzzle> cannot lead to a solution or other valid state within
    <n> moves, return the string 'No possible extensions!'

    @type puzzle: Puzzle
    @type n: int
    @rtype: str
    """
    # TO TA:
    # THIS FUNCTION IS NOT RECURSIVE, BUT ITS SUB HELPER FUNCTION
    # build_solution_tree IS A RECURSIVE FUNCTION
    if puzzle.is_solved():
        message = 'Already at a solution!'
    else:
        if hint_by_depth_helper(puzzle, n) is None:
            message = 'No possible extensions!'
        else:
            message = puzzle.hint_generator(hint_by_depth_helper(puzzle, n))
    return message


def hint_by_depth_helper(puzzle, n):
    """
    Return a valid state of the puzzle after one move, which can lead
    to a solution or a valid state within n moves.
    Return None if cannot find any above.

    Precondition: n >= 1.

    @type puzzle: Puzzle
    @type n: int
    @rtype: Puzzle | None
    """

    start = SolutionTree(puzzle)
    solution_tree = build_solution_tree(start, n)
    next_move = solution_tree.items_at_depth(2)
    for obj in next_move:
        if obj.get_root().is_solved():
            return obj.get_root()
        else:
            for dep in range(2, n+1):
                reached_state = obj.items_at_depth(dep)
                for nested_obj in reached_state:
                    if nested_obj.get_root().is_solved():
                        return obj.get_root()
    # if still cannot find any solved solution within n moves,
    # find if there are valid state at nth move
    for obj in next_move:
        reached_state_at_n = obj.items_at_depth(n)
        if not len(reached_state_at_n) == 0:
            return obj.get_root()
    # if neither solution or valid state is found, return None
    return None


def build_solution_tree(root, n):
    """
    Build a solution tree recursively that contains possible states of
    the puzzle until nth moves by giving its root.

    @type root: SolutionTree
    @type n: int
    @rtype: SolutionTree
    """
    puzzle = root.get_root()
    exten = puzzle.extensions()
    for element in exten:
        subroot = SolutionTree(element)
        root.add_extensions([subroot])
    n -= 1
    if n < 1:
        return root
    else:
        for obj in root.get_extensions():
            lst = obj.get_root().extensions()
            for sol in lst:
                subroot2 = SolutionTree(sol)
                obj.add_extensions([subroot2])
        n -= 1
        if n < 1:
            return root
        else:
            for choice in root.get_extensions():
                for nest_obj in choice.get_extensions():
                    build_solution_tree(nest_obj, n)
            return root


class SolutionTree:
    """ A tree data structure that contains all possible puzzle states
    until specified steps of valid move.

    """
    # === Private Attributes ===
    # @type _root: Puzzle
    #     The puzzle associated with this solution tree
    # @type _extensions: list[SolutionTree]
    #     The all possible extensions associated with this solution tree

    def __init__(self, puzzle):
        """Initialize the solution tree.

        @type puzzle: Puzzle
        @rtype: None
        """
        self._root = puzzle
        self._extensions = []

    def is_empty(self):
        """Return whether this tree is empty.

        @type self: SolutionTree
        @rtype: bool
        """
        return self._root is None

    def add_extensions(self, new_trees):
        """ Add new tree extensions to the solution tree.

        @type new_trees: list[SolutionTree]
        @rtype: None
        """
        if self.is_empty():
            raise ValueError()
        else:
            self._extensions.extend(new_trees)

    def get_root(self):
        """Return the root value of solution tree
        @rtype: Puzzle
        """
        return self._root

    def get_extensions(self):
        """Return a list of extensions of solution tree
        @rtype: list[SolutionTree]
        """
        return self._extensions

    def items_at_depth(self, d):
        """
        Return a sorted list of all items in this solution tree at depth <d>.

        Precondition: d >= 1.

        @type self: SolutionTree
        @type d: int
        @rtype: list[SolutionTree]
        """
        result = []
        if self.is_empty():
            return result
        elif d == 1:
            result.append(self._root)
            return result
        else:
            if d == 2:
                return self._extensions
            else:
                for extension in self._extensions:
                    result.extend(extension.items_at_depth(d-1))
                return result

if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    from word_ladder_puzzle import WordLadderPuzzle
    s = SudokuPuzzle([['', '', '', ''],
                      ['', '', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])
    # s = SudokuPuzzle(
    #     [['E', 'C', '', '', 'G', '', '', '', ''],
    #      ['F', '', '', 'A', 'I', 'E', '', '', ''],
    #      ['', 'I', 'H', '', '', '', '', 'F', ''],
    #      ['H', '', '', '', 'F', '', '', '', 'C'],
    #      ['D', '', '', 'H', '', 'C', '', '', 'A'],
    #      ['G', '', '', '', 'B', '', '', '', 'F'],
    #      ['', 'F', '', '', '', '', 'B', 'H', ''],
    #      ['', '', '', 'D', 'A', 'I', '', '', 'E'],
    #      ['', '', '', '', 'H', '', '', 'G', 'I']]
    # )
    # s = WordLadderPuzzle('mist', 'cars')
    # r = SolutionTree(s)
    # tree = build_solution_tree(r, 4)
    # pos = tree.items_at_depth(5)
    # for item in pos:
    #     print(item._root)

    # solution = solve(s)
    # print(solution)
    solution = solve_complete(s, True)
    for a in solution:
        print(a)
