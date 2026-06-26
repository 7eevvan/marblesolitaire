# =====================================
# CONSTANTS
# =====================================
import time
MIN_HEURISTIC = 0.5
HEURISTIC_CHECK_FREQ = 20
ROWS = 0
COLS = 0
VERBOSE = True

# board copy paste:
'''
1101
1101
0000
0100
'''
'''
XX111XX
XX111XX
1111111
1110111
1111111
XX111XX
XX111XX
'''

'''
XX111XX
X11111X
1111111
1110111
1111111
X11111X
XX111XX
'''
# =====================================
# HELPERS
# =====================================
class Candidate:
    def __init__(self, board, marbles, moves):
        self.board = board
        self.marbles = marbles
        self.moves = moves

def rotate90(board):
    return [[board[ROWS - 1 - r][c] for r in range(ROWS)] for c in range(COLS)]

def board_hash(board):
    r0 = board
    r1 = rotate90(r0)
    r2 = rotate90(r1)
    r3 = rotate90(r2)
    h0 = [row[::-1] for row in r0]
    h1 = [row[::-1] for row in r1]
    h2 = [row[::-1] for row in r2]
    h3 = [row[::-1] for row in r3]
    boards = [r0,r1,r2,r3,h0,h1,h2,h3]
    return min(tuple(tuple(row) for row in b) for b in boards)

def count_components(board):
    R, C = len(board), len(board[0])
    visited = set()

    def neighbors(r, c):
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C:
                yield nr, nc
        for dr, dc in [(2,0),(-2,0),(0,2),(0,-2)]: # two away
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C:
                yield nr, nc

    def dfs(r, c):
        stack = [(r,c)]
        while stack:
            x,y = stack.pop()
            for nx, ny in neighbors(x,y):
                if (nx,ny) not in visited and board[nx][ny] == '1':
                    visited.add((nx,ny))
                    stack.append((nx,ny))

    components = 0

    for r in range(R):
        for c in range(C):
            if board[r][c] == '1' and (r,c) not in visited:
                visited.add((r,c))
                dfs(r,c)
                components += 1

    return components

def heuristic(candidate): # 0 = bad, 1 = good
    board = candidate.board
    marbles = candidate.marbles

    components = count_components(board)

    if components >= 5:
        return 0
    if marbles >= 15 and components >= 4:
        return 0
    if marbles >= 11 and components >= 3:
        return 0
    if marbles == 3 and components >= 2:
        return 0

    return 1

def validate_input(rows, cols, board):
    return len(board) == rows and len(board[0]) == cols


# =====================================
# SOLVE (dfs)
# =====================================
iterations = 0
visited = set()
solved = False
best_marbles = 1000000
pruned = 0 # for heuristic usefulness testing
def solve(candidate):
    global pruned
    global best_marbles
    global iterations
    global solved

    if solved:
        return

    best = candidate
    board = candidate.board
    marbles = candidate.marbles
    moves = candidate.moves
    
    if marbles == 1:
        solved = True
        return best

    if VERBOSE:
        if marbles < best_marbles:
            print(marbles)
            print(board)
            best_marbles = marbles
            

    # hash check
    explore = True
    key = board_hash(board)
    if key in visited:
        explore = False
    # heuristic check
    if explore:
        iterations += 1
        if iterations % HEURISTIC_CHECK_FREQ == 0:
            if heuristic(candidate) < MIN_HEURISTIC:
                pruned += 1
                explore = False

    if explore:
        visited.add(key)
        next_candidates = []
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == '0':
                    # jump down
                    if r >= 2 and board[r-1][c] == '1' and board[r-2][c] == '1':  # the spot 1 above and 2 above are both 1
                        new_board = [row[:] for row in board]
                        new_board[r][c] = '1'
                        new_board[r-1][c] = '0'
                        new_board[r-2][c] ='0'
                        next_candidates.append(Candidate(new_board, marbles-1, moves+[(f"{r-2}, {c}", "down")]))
                    # jump up
                    if r + 2 < len(board) and board[r+1][c] == '1' and board[r+2][c] == '1':  # the spot 1 below and 2 below are both 1
                        new_board = [row[:] for row in board]
                        new_board[r][c] = '1'
                        new_board[r+1][c] = '0'
                        new_board[r+2][c] ='0'
                        next_candidates.append(Candidate(new_board, marbles-1, moves+[(f"{r+2}, {c}", "up")]))
                    # jump right
                    if c >= 2 and board[r][c-1] == '1' and board[r][c-2] == '1':  # the spot 1 left and 2 left are both 1
                        new_board = [row[:] for row in board]
                        new_board[r][c] = '1'
                        new_board[r][c-1] = '0'
                        new_board[r][c-2] ='0'
                        next_candidates.append(Candidate(new_board, marbles-1, moves+[(f"{r}, {c-2}", "right")]))
                    # jump left
                    if c + 2 < len(board[0]) and board[r][c+1] == '1' and board[r][c+2] == '1':  # the spot 1 right and 2 right are both 1
                        new_board = [row[:] for row in board]
                        new_board[r][c] = '1'
                        new_board[r][c+1] = '0'
                        new_board[r][c+2] ='0'
                        next_candidates.append(Candidate(new_board, marbles-1, moves+[(f"{r}, {c+2}", "left")]))

        for c in next_candidates:
            result = solve(c)
            if result and result.marbles < best.marbles:
                best = result

    return best







# =====================================
# MAIN
# input: X if invalid spot, 1 if marble in that spot, 0 if no marble in that spot
# list of moves: [(position, direction)]
# =====================================
def main():
    global ROWS, COLS
    print("Max 10 rows and 10 cols\nX if invalid spot, 1 if marble in that spot, 0 if no marble in that spot")
    rows = int(input("# of rows in board: "))
    cols = int(input("# of cols in board: "))
    ROWS = rows
    COLS = cols

    board = []
    for _ in range(rows):
        board.append(list(input()))

    if not validate_input(rows, cols, board):
        print("Invalid input")
        return

    marbles = 0
    for row in board:
        for x in row:
            if x == "1":
                marbles += 1

    start_time = time.perf_counter()
    best = solve(Candidate(board, marbles, []))
    end_time = time.perf_counter()
    
    print(best.board)
    print(best.moves)

    print(len(visited))
    print(iterations)
    print(pruned)
    print(end_time-start_time)

if __name__ == "__main__":
    main()