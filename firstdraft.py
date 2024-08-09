import copy

def determine_solution(paths) -> 'The answer':
    new_paths = []

    for path in paths:
        for new_path in generate_new_paths(path):
            board = new_path[0]
            list_of_moves = new_path[1]
            marbles = new_path[2]
            new_paths.append(new_path)
            if marbles == 1:
                return f"Solution found!\nBoard: {board}\nMoves: {list_of_moves}"

    if not new_paths:
        arbitrary_failed_path = paths[0]
        board = arbitrary_failed_path[0]
        list_of_moves = arbitrary_failed_path[1]
        marbles = arbitrary_failed_path[2]
        return f"No solution exists. This was one of the best possible paths, resulting in {marbles} marbles:\nBoard: {board}\nMoves: {list_of_moves}"

    return determine_solution(new_paths)
        
def generate_new_paths(path) -> 'list of [board, list of moves, marbles]':
    new_paths = []

    board = path[0]
    list_of_moves = path[1]
    marbles = path[2]

    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == '0':
                # jump down
                if r >= 2 and board[r-1][c] == '1' and board[r-2][c] == '1':  # the spot 1 above and 2 above are both 1
                    board[r][c], board[r-1][c], board[r-2][c] = '1', '0', '0'
                    new_paths.append([copy.deepcopy(board), list_of_moves + [(f"R: {r-2}, C: {c}", "DOWN")], marbles-1])
                    board[r][c], board[r-1][c], board[r-2][c] = '0', '1', '1'
                # jump up
                if r + 2 < len(board) and board[r+1][c] == '1' and board[r+2][c] == '1':  # the spot 1 below and 2 below are both 1
                    board[r][c], board[r+1][c], board[r+2][c] = '1', '0', '0'
                    new_paths.append([copy.deepcopy(board), list_of_moves + [(f"R: {r+2}, C: {c}", "UP")], marbles-1])
                    board[r][c], board[r+1][c], board[r+2][c] = '0', '1', '1'
                # jump right
                if c >= 2 and board[r][c-1] == '1' and board[r][c-2] == '1':  # the spot 1 left and 2 left are both 1
                    board[r][c], board[r][c-1], board[r][c-2] = '1', '0', '0'
                    new_paths.append([copy.deepcopy(board), list_of_moves + [(f"R: {r}, C: {c-2}", "RIGHT")], marbles-1])
                    board[r][c], board[r][c-1], board[r][c-2] = '0', '1', '1'
                # jump left
                if c + 2 < len(board[0]) and board[r][c+1] == '1' and board[r][c+2] == '1':  # the spot 1 right and 2 right are both 1
                    board[r][c], board[r][c+1], board[r][c+2] = '1', '0', '0'
                    new_paths.append([copy.deepcopy(board), list_of_moves + [(f"R: {r}, C: {c+2}", "LEFT")], marbles-1])
                    board[r][c], board[r][c+1], board[r][c+2] = '0', '1', '1'

    return new_paths

def generate_first_paths(board) -> 'list of [board, list of moves, marbles]':
    marbles = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == '1':
                marbles += 1
    paths = []
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == '0':
                # jump down
                if r >= 2 and board[r-1][c] == '1' and board[r-2][c] == '1':  # the spot 1 above and 2 above are both 1
                    board[r][c], board[r-1][c], board[r-2][c] = '1', '0', '0'
                    paths.append([copy.deepcopy(board), [(f"R: {r-2}, C: {c}", "DOWN")], marbles-1])
                    board[r][c], board[r-1][c], board[r-2][c] = '0', '1', '1'
                # jump up
                if r + 2 < len(board) and board[r+1][c] == '1' and board[r+2][c] == '1':  # the spot 1 below and 2 below are both 1
                    board[r][c], board[r+1][c], board[r+2][c] = '1', '0', '0'
                    paths.append([copy.deepcopy(board), [(f"R: {r+2}, C: {c}", "UP")], marbles-1])
                    board[r][c], board[r+1][c], board[r+2][c] = '0', '1', '1'
                # jump right
                if c >= 2 and board[r][c-1] == '1' and board[r][c-2] == '1':  # the spot 1 left and 2 left are both 1
                    board[r][c], board[r][c-1], board[r][c-2] = '1', '0', '0'
                    paths.append([copy.deepcopy(board), [(f"R: {r}, C: {c-2}", "RIGHT")], marbles-1])
                    board[r][c], board[r][c-1], board[r][c-2] = '0', '1', '1'
                # jump left
                if c + 2 < len(board[0]) and board[r][c+1] == '1' and board[r][c+2] == '1':  # the spot 1 right and 2 right are both 1
                    board[r][c], board[r][c+1], board[r][c+2] = '1', '0', '0'
                    paths.append([copy.deepcopy(board), [(f"R: {r}, C: {c+2}", "LEFT")], marbles-1])
                    board[r][c], board[r][c+1], board[r][c+2] = '0', '1', '1'
    return paths

def validate_input(board):
    return True

# input: X if no marble can go there, 1 if marble in that spot, 0 if no marble in that spot, X if no spot
# path: board, list of moves, marbles left on board
# list of moves: [(position, direction)]
def main():
    height = int(input("Enter board height: "))
    width = int(input("Enter board width: "))
    board = []
    for _ in range(height):
        board.append(list(input()))

    if not validate_input(board):
        print("Invalid input")
        return

    first_paths = generate_first_paths(board)
    print(determine_solution(first_paths))

main()