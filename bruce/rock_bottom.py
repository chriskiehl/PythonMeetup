# rock_bottom.py

# from: http://www.puzzlenode.com/puzzles/11-hitting-rock-bottom

from itertools import takewhile


Rock = '#'
Water = '~'
Space = ' '


def load(lines):
    r'''Returns list of columns, bottom to top.

        >>> load(['12\n', '\n', '123\n', '456\n', '78\n'])
        ([['7', '4', '1'], ['8', '5', '2'], [' ', '6', '3']], 12)
    '''
    num_iterations = int(lines[0])
    rows = [line.rstrip() for line in lines[:0:-1] if line.rstrip()]
    max_len = max(len(row) for row in rows)
    return ([[row[col] if col < len(row) else ' ' for row in rows]
             for col in range(max_len)],
            num_iterations)


def run(board, num_iterations):
    start_row = board[0].index('~')
    board[0][start_row] = Space
    def where_next(row, col):
        current_col = board[col]
        if current_col[row] == Space:
            current_col[row] = '~'
            yield
            if row:
                yield from where_next(row - 1, col)
            if col + 1 < len(board):
                yield from where_next(row, col + 1)
    it = iter(where_next(start_row, 0))
    for _ in range(num_iterations):
        next(it)


def dump(board):
    for column in board:
        print(score_column(column), sep='', end=' ')
    print()


def score_column(column):
    r'''Scores `column` for final output.

        >>> score_column('  ###~~~~     #')
        4
        >>> score_column('  ### ~~~     #')
        '~'
        >>> score_column('  ###         #')
        0
    '''
    row = count(column, Space, 0)
    row += count(column, Rock, row)
    if row < len(column) and column[row] == Space:
        if Water in column:
            return '~'
        else:
            return 0
    return count(column, Water, row)


def count(column, item, starting_row):
    r'''Counts the number of `item`s in `column` starting at `starting_row`.

        >>> count('aabbcc', 'b', 2)
        2
        >>> count('aabbcc', 'a', 2)
        0
    '''
    i = 0
    for i, _ in enumerate(takewhile(lambda x: x == item, column[starting_row:]),
                          1):
        pass
    return i


if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()
    board, num_iterations = load(lines)
    run(board, num_iterations)
    dump(board)
