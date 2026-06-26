ROWS = 3
COLS = 3
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
    v0 = r0[::-1]
    v1 = r1[::-1]
    v2 = r2[::-1]
    v3 = r3[::-1]
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

def main():
    print(board_hash([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]), board_hash([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3']]))
    print(count_components([['1', '0', '0'], ['1', '0', '0'], ['0', '0', '1']]))


    


main()