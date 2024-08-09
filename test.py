import copy

def generate_first_paths(board) -> 'list of [board, list of moves]':
    marbles = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == '1':
                marbles += 1
    paths = []
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == '0':
                # jump down
                if r >= 2:
                    if board[r-1][c] == '1' and board[r-2][c] == '1': # the spot 1 above and 2 above are both 1
                        new_board = copy.deepcopy(board)
                        new_board[r][c] = '1'
                        new_board[r-1][c] = '0'
                        new_board[r-2][c] = '0'
                        paths.append([new_board, [(f"R: {r-2}, C: {c}", "DOWN")]])
                # jump up
                if r + 2 < len(board):
                    if board[r+1][c] == '1' and board[r+2][c] == '1': # the spot 1 below and 2 below are both 1
                        new_board = copy.deepcopy(board)
                        new_board[r][c] = '1'
                        new_board[r+1][c] = '0'
                        new_board[r+2][c] = '0'
                        paths.append([new_board, [(f"R: {r+2}, C: {c}", "UP")]])
                # jump right
                if c >= 2:
                    if board[r][c-1] == '1' and board[r][c-2] == '1': # the spot 1 left and 2 left are both 1
                        new_board = copy.deepcopy(board)
                        new_board[r][c] = '1'
                        new_board[r][c-1] = '0'
                        new_board[r][c-2] = '0'
                        paths.append([new_board, [(f"R: {r}, C: {c-2}", "RIGHT")]])
                # jump left
                if c + 2 < len(board[0]):
                    if board[r][c+1] == '1' and board[r][c+2] == '1': # the spot 1 right and 2 right are both 1
                        new_board = copy.deepcopy(board)
                        new_board[r][c] = '1'
                        new_board[r][c+1] = '0'
                        new_board[r][c+2] = '0'
                        paths.append([new_board, [(f"R: {r}, C: {c+2}", "LEFT")]])
    
    return paths

# Input
board = [
    ["1", "1", "1", "1"],
    ["1", "1", "0", "1"],
    ["1", "1", "0", "1"],
    ["1", "1", "1", "1"]
]

# Generate first paths
paths = generate_first_paths(board)
print(paths)

def generate_new_paths(path) -> 'list of [board, list of moves, marbles]':
    new_paths = []

    board = path[0]
    list_of_moves = path[1]
    marbles = path[2]

    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == '0':
                # jump down
                if r >= 2:
                    if board[r-1][c] == '1' and board[r-2][c] == '1': # the spot 1 above and 2 above are both 1
                        new_board = copy.deepcopy(board)
                        new_board[r][c] = '1'
                        new_board[r-1][c] = '0'
                        new_board[r-2][c] = '0'
                        new_paths.append([new_board, list_of_moves + [(f"R: {r-2}, C: {c}", "DOWN")], marbles-1])
                # jump up
                if r + 2 < len(board):
                    if board[r+1][c] == '1' and board[r+2][c] == '1': # the spot 1 below and 2 below are both 1
                        new_board = copy.deepcopy(board)
                        new_board[r][c] = '1'
                        new_board[r+1][c] = '0'
                        new_board[r+2][c] = '0'
                        new_paths.append([new_board, list_of_moves + [(f"R: {r+2}, C: {c}", "UP")], marbles-1])
                # jump right
                if c >= 2:
                    if board[r][c-1] == '1' and board[r][c-2] == '1': # the spot 1 left and 2 left are both 1
                        new_board = copy.deepcopy(board)
                        new_board[r][c] = '1'
                        new_board[r][c-1] = '0'
                        new_board[r][c-2] = '0'
                        new_paths.append([new_board, list_of_moves + [(f"R: {r}, C: {c-2}", "RIGHT")], marbles-1])
                # jump left
                if c + 2 < len(board[0]):
                    if board[r][c+1] == '1' and board[r][c+2] == '1': # the spot 1 right and 2 right are both 1
                        new_board = copy.deepcopy(board)
                        new_board[r][c] = '1'
                        new_board[r][c+1] = '0'
                        new_board[r][c+2] = '0'
                        new_paths.append([new_board, list_of_moves + [(f"R: {r}, C: {c+2}", "LEFT")], marbles-1])

    return new_paths

print(generate_new_paths([[['1', '1', '1', '1'], ['0', '0', '1', '1'], ['1', '1', '0', '1'], ['1', '1', '1', '1']], [('R: 1, C: 0', 'RIGHT')], 13]))