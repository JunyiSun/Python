# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Word ladder module.

Your task is to complete the implementation of this class so that
you can use it to play Word Ladder in your game program.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

    Note that there are many possible solutions, and in fact a shorter one
    exists for the above puzzle. Do you see it? make cake care cure

Implementation details:
- We have provided some starter code in the constructor which reads in a list
  of valid English words from wordsEn.txt. You should use this list to
  determine what moves are valid.
- **WARNING**: unlike Sudoku, Word Ladder has the possibility of getting
  into infinite recursion if you aren't careful. The puzzle state
  should keep track not just of the current word, but all words
  in the ladder. This way, in the 'extensions' method you can just
  return the possible new words which haven't already been used.
"""
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwxyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle."""

    # === Private attributes ===
    # @type _words: list[str]
    #     List of allowed English words
    # @type _narrow_words: list[str]
    #     List of allowed English words that are same length as the given word
    # @type _start: str
    #     The given start word
    # @type _target: str
    #     The give target word
    # @type _ladder: list[str]
    #     List of valid words that the user inputs to build the word ladder

    def __init__(self, start, target, ladder=None):
        """Create a new word ladder puzzle with given start and target words.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @type ladder: list[str]
        @rtype: None
        """
        self._words = []
        with open('wordsEnTest.txt') as wordfile:
            for line in wordfile:
                self._words.append(line.strip())
        self._narrow_words = []
        for word in self._words:
            if len(word) == len(start):
                self._narrow_words.append(word)
        self._start = start
        self._target = target
        if ladder is None:
            self._ladder = []
        else:
            self._ladder = ladder

    def __str__(self):
        """Return a human-readable string representation of <self>

        @type self: WordLadderPuzzle
        @rtype: str

        >>> w = WordLadderPuzzle('mist','mire')
        >>> print(w)
        START: mist
        TARGET: mire
        <BLANKLINE>
        """

        w = ''
        w += 'START: ' + self._start + '\n'
        for item in self._ladder:
            w += item + '\n'
        w += 'TARGET: ' + self._target + '\n'
        return w

    def is_solved(self):
        """Return True if the word_ladder has been solved,
        Return False otherwise.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> w = WordLadderPuzzle('mist','mire')
        >>> w.is_solved()
        False
        >>> s = WordLadderPuzzle('mist','mist')
        >>> s.is_solved()
        True
        """

        if len(self._ladder) == 0:
            if not self._start == self._target:
                if not len(self._start) == len(self._target):
                    return False
                match = self._diffone(self._start, self._target)
                if match is False:
                    return False
        else:
            for i in range(len(self._ladder)):
                # compare first in ladder with start
                if i == 0:
                    match = self._diffone(self._ladder[i], self._start)
                    if match is False:
                        return False
                else:
                    # compare each word in ladder with one before
                    match = self._diffone(self._ladder[i], self._ladder[i-1])
                    if match is False:
                        return False
                # compare last word in ladder with target
                if i == (len(self._ladder) - 1):
                    match = (self._ladder[i] == self._target)
                    if match is False:
                        return False
                if self._ladder[i] not in self._narrow_words:
                    return False
        return True

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        You should *not* perform any moves which produce a word
        that is already in the ladder.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> w = WordLadderPuzzle('mire','cars')
        >>> s = w.extensions()[0]
        >>> print(s)
        START: mire
        mare
        TARGET: cars
        <BLANKLINE>
        >>> a = s.extensions()[0]
        >>> print(a)
        START: mire
        mare
        care
        TARGET: cars
        <BLANKLINE>

        """

        possible = []
        if len(self._ladder) == 0:
            # intersection of words that both in _narrow_words(list contains
            # all words with same length) and _possible_words(list contains
            # all permutation of that word with one character difference)
            more_nar = list(set(self._narrow_words).
                            intersection(self._possible_words(self._start)))
            for word in more_nar:
                if self._diffone(word, self._start):
                    possible.append(word)
        else:
            more_nar = list(set(self._narrow_words).intersection
                            (self._possible_words(self._ladder[-1])))

            for word in more_nar:
                if self._diffone(word, self._ladder[-1]):
                    possible.append(word)
        possible.sort()
        results = [self._extend(word) for word in possible]
        return results

    def move(self, move):
        """Return a new word ladder puzzle state specified
        by making the given move.

        Raise a ValueError if <move> represents an invalid move.
        Do *NOT* change the state of <self>. This is not a mutating method!

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: WordLadderPuzzle
        """
        if move not in self._narrow_words:
            raise ValueError
        if move in self._ladder:
            raise ValueError
        if move == self._start:
            raise ValueError
        if len(self._ladder) == 0:
            if not len(move) == len(self._start):
                raise ValueError
            if not self._diffone(move, self._start):
                raise ValueError
        else:
            if not len(move) == len(self._ladder[-1]):
                raise ValueError
            if not self._diffone(move, self._ladder[-1]):
                raise ValueError

        new_ladder = []
        for element in self._ladder:
            new_ladder.append(element)
        new_ladder.append(move)
        return WordLadderPuzzle(self._start, self._target, new_ladder)

    def is_valid(self, move):
        """Return True if the given move is valid,
        Return False otherwise.

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: bool
        """
        if move not in self._narrow_words:
            return False
        if move in self._ladder:
            return False
        if move == self._start:
            return False
        if len(self._ladder) == 0:
            if not len(move) == len(self._start):
                return False
            if not self._diffone(move, self._start):
                return False
        else:
            if not len(move) == len(self._ladder[-1]):
                return False
            if not self._diffone(move, self._ladder[-1]):
                return False
        return True

    def __eq__(self, other):
        """Return True if the two puzzle objects have the same _start, _target,
        and _ladder attributes.
        Return False if they are different.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle
        @rtype: bool
        """
        if not self._start == other._start:
            return False
        if not self._target == other._target:
            return False

        if not len(self._ladder) == len(other._ladder):
            return False
        else:
            for index in range(len(self._ladder)):
                if not self._ladder[index] == other._ladder[index]:
                    return False
            return True

    def hint_generator(self, puzzle):
        """Compare two states of the puzzle and generate a valid hint of move.

        @type self: WordLadderPuzzle
        @type puzzle: WordLadderPuzzle
        @rtype: str
        """
        index = len(self._ladder)
        return puzzle._ladder[index]

    # ------------------------------------------------------------------------
    # Helpers for method 'is_solved' and 'extensions'
    # ------------------------------------------------------------------------

    def _diffone(self, first, second):
        """Return True if two given words are different
        exactly by one character; Return False if they are the same or
        different for more than one characters.

        @type first:  str
        @type second: str
        @rtype: bool
        """
        one_diff = False
        if first == second:
            return False
        for c1, c2 in zip(first, second):
            if not c1 == c2:
                if one_diff:
                    return False
                else:
                    one_diff = True
        return True

    def _possible_words(self, word):
        """Return a list of all possible word choices from the given word.
        These choices are exactly one character different as the given word.

        @type word: str
        @rtype: list[str]
        """
        result = []
        for i in range(len(word)):
            for char in CHARS:
                new = word[:i] + word[i].replace(word[i], char, 1) + word[i+1:]
                if new not in self._ladder:
                    if not new == self._start:
                        result.append(new)
        return result

    def _extend(self, word):
        """Return a new word ladder puzzle that has the given word
        appended to the original ladder list.

        @type word: str
        @rtype: WordLadderPuzzle
        """
        new_ladder = []
        for element in self._ladder:
            new_ladder.append(element)
        new_ladder.append(word)
        return WordLadderPuzzle(self._start, self._target, new_ladder)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
