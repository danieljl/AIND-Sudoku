def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs)
                for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
diagonal_units = [[a + b for a, b in z]
                  for z in [zip(rows, cols), zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


# TODO
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4
                      ....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid.
        False if no solution exists.
    """
    grid = grid_values(grid)
    grid = reduce_puzzle(grid)
    grid = search(grid)
    return grid


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
                    then the value will be '123456789'.
    """
    all_digits = '123456789'
    return {box: (values if values != '.' else all_digits)
            for box, values in zip(boxes, grid)}


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    grid = values.copy()
    for box, choices in grid.items():
        if len(choices) != 1:
            continue
        for peer in peers[box]:
            # Equals: grid[peer] = grid[peer].replace(choices, '')
            assign_value(grid, peer, grid[peer].replace(choices, ''))
    return grid


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    result = values.copy()
    for unit in unitlist:
        for digit in '123456789':
            boxes_with_digit = [box for box in unit if digit in values[box]]
            if len(boxes_with_digit) == 1:
                # Equals: result[boxes_with_digit[0]] = digit
                assign_value(result, boxes_with_digit[0], digit)
    return result


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box, choices in values.items()
                                    if len(choices) == 1])

        values = eliminate(values)
        values = only_choice(values)

        solved_values_after = len([box for box, choices in values.items()
                                   if len(choices) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check if there is a box with zero available values:
        if len([box for box, choices in values.items() if len(choices) == 0]):
            return {}
    return values


def search(values):
    """Using depth-first search and propagation,
    create a search tree and solve the sudoku."""
    values = values.copy()

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if not values:
        return {}

    # Chose one of the unfilled square s with the fewest possibilities
    squares_not_solved = {square: choices
                          for square, choices in values.items()
                          if len(choices) > 1}
    if not len(squares_not_solved):
        return values

    def num_choices(square):
        return len(values[square])

    square_fewest = min(squares_not_solved, key=num_choices)

    # Now use recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer!
    for digit in values[square_fewest]:
        # Equals: values[square_fewest] = digit
        assign_value(values, square_fewest, digit)
        solution = search(values)
        if solution:
            return solution
    return {}


if __name__ == '__main__':
    diag_sudoku_grid = ('2.............62....1....7...6..8...3...9...7...6..4'
                        '...4....8....52.............3')
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. '
              'Not a problem! It is not a requirement.')
