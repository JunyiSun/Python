# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Puzzle API

Works in conjunction with solver.py to enable a generic algorithm
to solve one-player puzzles.
"""


class Puzzle:
    """Abstract class for a generic one-player puzzle.

    Note that this class really represents a puzzle *state*
    and not just a generic type of puzzle. In other words,
    an instance of this class could represent one particular
    Sudoku puzzle, with a partially filled-in board.

    The rules of the game are encoded in the 'is_solved'
    and 'extensions' methods.

    Subclasses are responsible for tracking the internal state
    of the puzzle, and implementing four methods:
        - __str__
        - is_solved
        - extensions
        - move
    """
    def __str__(self):
        """Return a human-readable representation of this puzzle.

        @type self: Puzzle
        @rtype: str
        """
        raise NotImplementedError()

    def is_solved(self):
        """Return whether this puzzle is in a solved state.

        @type self: Puzzle
        @rtype: bool
        """
        raise NotImplementedError()

    def extensions(self):
        """Return a list of possible new states reachable by one move.

        First compute a list of possible moves based on the current
        puzzle state. Then, return a list of the new puzzle states
        that the puzzle could be in after each move.

        @type self: Puzzle
        @rtype: list[Puzzle]
        """
        raise NotImplementedError()

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        Raise a ValueError if <move> represents an invalid move.
        Do *NOT* change the state of <self>. This is not a mutating method!

        NOTE: You can ignore this completely until Part 2.

        @type self: Puzzle
        @type move: str
        @rtype: Puzzle
        """
        raise NotImplementedError()

    def is_valid(self, move):
        """
        Return True if the given move is valid,
        Return False otherwise.

        @type self: Puzzle
        @type move: str
        @rtype: bool
        """

        raise NotImplementedError()

    def __eq__(self, other):
        """Return True if the two puzzle objects have the same attribute values.
        Return False if they are different.

        @type self: Puzzle
        @type other: Puzzle
        @rtype: bool
        """
        raise NotImplementedError()

    def hint_generator(self, puzzle):
        """Compare two state of the puzzle and generate a valid hint of move.

        @type puzzle: Puzzle
        @rtype: str
        """
        raise NotImplementedError()
