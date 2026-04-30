MOD = 10**6 + 3

class Candidate:
    def __init__(self, board, moves):
        self.board = board
        self.moves = moves

binpow = []
def precompute():
    n = 1
    for _ in range(30):
        binpow.append(n)
        n *= 2
        n = n % MOD

def h(board): # hash
    return tuple(tuple(row) for row in board)

def hu(board): # hueristic (0, 1) bad to good
    return 1

visited = set()
def solve(candidate):
    board = candidate.board
    moves = candidate.moves
    
    board_hash = h(board)
    if board_hash not in visited:
        visited.add(board_hash)
        next_candidates = []
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == '0':
                    # jump down
                    if r >= 2 and board[r-1][c] == '1' and board[r-2][c] == '1':  # the spot 1 above and 2 above are both 1
                        board[r][c], board[r-1][c], board[r-2][c] = '1', '0', '0'
                        next_candidates.append(Candidate([row[:] for row in board], moves+["down"]))
                        board[r][c], board[r-1][c], board[r-2][c] = '0', '1', '1'
                    # jump up
                    if r + 2 < len(board) and board[r+1][c] == '1' and board[r+2][c] == '1':  # the spot 1 below and 2 below are both 1
                        board[r][c], board[r+1][c], board[r+2][c] = '1', '0', '0'
                        next_candidates.append(Candidate([row[:] for row in board], moves+["up"]))
                        board[r][c], board[r+1][c], board[r+2][c] = '0', '1', '1'
                    # jump right
                    if c >= 2 and board[r][c-1] == '1' and board[r][c-2] == '1':  # the spot 1 left and 2 left are both 1
                        board[r][c], board[r][c-1], board[r][c-2] = '1', '0', '0'
                        next_candidates.append(Candidate([row[:] for row in board], moves+["right"]))
                        board[r][c], board[r][c-1], board[r][c-2] = '0', '1', '1'
                    # jump left
                    if c + 2 < len(board[0]) and board[r][c+1] == '1' and board[r][c+2] == '1':  # the spot 1 right and 2 right are both 1
                        board[r][c], board[r][c+1], board[r][c+2] = '1', '0', '0'
                        next_candidates.append(Candidate([row[:] for row in board], moves+["left"]))
                        board[r][c], board[r][c+1], board[r][c+2] = '0', '1', '1'

        if next_candidates == []:
            return board

        for c in next_candidates:
            result = solve(c)
            if result is not None:
                return result


def validate_input(rows, cols, board):
    if len(board) == rows and len(board[0]) == cols:
        return True
    return False

# input: X if no marble can go there, 1 if marble in that spot, 0 if no marble in that spot
# path: board, list of moves, marbles left on board
# list of moves: [(position, direction)]
def main():
    rows = int(input("Enter # of rows in board: "))
    cols = int(input("Enter # of cols in board: "))
    board = []
    for _ in range(rows):
        board.append(list(input()))

    if not validate_input(rows, cols, board):
        print("Invalid input")
        return

    # first_paths = generate_first_paths(board)
    # print(determine_solution(first_paths))
    precompute()
    print(solve(Candidate(board, [])))

if __name__ == "__main__":
    main()