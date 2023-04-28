class Board(object):
    
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.board[3][4], self.board[4][3] = 'X', 'X'
        self.board[3][3], self.board[4][4] = 'O', 'O'

    def count(self, color):
        cnt = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    cnt += 1
        return cnt

    def display(self):
        cur_board = self.board

        print(' ', ' '.join('ABCDEFGH'))
        for i in range(8):
            print(str(i + 1), ' '.join(cur_board[i]))
        
        print("BLACK(X): " + str(self.count('X')))
        print("WHITE(O): " + str(self.count('O')))

    def get_winner(self):
        black_cnt, white_cnt = 0, 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'X':
                    black_cnt += 1
                if self.board[i][j] == 'O':
                    white_cnt += 1
        
        if black_cnt > white_cnt:
            return 0, black_cnt - white_cnt
        elif black_cnt < white_cnt:
            return 1, white_cnt - black_cnt
        else:
            return 2, 0

    def is_on_board(self, i, j):
        return 0 <= i <= 7 and 0 <= j <= 7
    
    def get_op_color(self, color):
        return 'O' if color == 'X' else 'X'
    
    def detect_reverse(self, coord, color):
        if isinstance(coord, str):
            coord = self.board2coord(coord)
        cur_x, cur_y = coord
        if not self.is_on_board(cur_x, cur_y) or self.board[cur_x][cur_y] != '.':
            return False
        
        op_color = self.get_op_color(color)

        reverse_coord = []
        reverse_board = []

        for dx, dy in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = cur_x, cur_y
            x += dx
            y += dy
            while self.is_on_board(x, y) and self.board[x][y] == op_color:
                x += dx
                y += dy  
            if not self.is_on_board(x, y):
                continue
            if self.board[x][y] == color:
                while True:
                    x -= dx
                    y -= dy
                    if x == cur_x and y == cur_y:
                        break
                    reverse_coord.append([x, y])

        if len(reverse_coord) == 0:
            return False
        
        for rc in reverse_coord:
            reverse_board.append(self.coord2board(rc))

        return reverse_board
    
    def get_legal_board(self, color):
        op_color = self.get_op_color(color)
        op_color_near_coord = []

        cur_board = self.board
        for i in range(8):
            for j in range(8):
                if cur_board[i][j] == op_color:
                    for dx, dy in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                        x, y = i + dx, j + dy
                        if self.is_on_board(x, y) and cur_board[x][y] == '.' and (x, y) not in op_color_near_coord:
                            op_color_near_coord.append((x, y))

        coord = [0, 1, 2, 3, 4, 5, 6, 7]
        for c in op_color_near_coord:
            if self.detect_reverse(c, color):
                if c[0] in coord and c[1] in coord:
                    c = self.coord2board(c)
                yield c

    def move(self, coord, color):
        if isinstance(coord, str):
            coord = self.board2coord(coord)
        
        reverse = self.detect_reverse(coord, color)
        if reverse:
            for r in reverse:
                i, j = self.board2coord(r)
                self.board[i][j] = color
            self.board[coord[0]][coord[1]] = color
            
        return reverse

    def board2coord(self, s):
        i, j = str(s[1]).upper(), str(s[0]).upper()
        if i in '12345678' and j in 'ABCDEFGH':
            i = '12345678'.index(i)
            j = 'ABCDEFGH'.index(j)
            return i, j
        return None
    
    def coord2board(self, n):
        i, j = n
        coord = [0, 1, 2, 3, 4, 5, 6, 7]
        if i in coord and j in coord:
            return chr(ord('A') + j) + str(i + 1)
        return None


if __name__ == '__main__':
    board = Board()

    for i in range(3):
        for j in range(5):
            board.board[i][j] = 'X'
    board.board[3][5] = 'X'
    board.display()

    winner = board.get_winner()
    if winner > 0:
        print('BLACK WIN')
    elif winner < 0:
        print('WHITE WIN')
    else:
        print('TIE')

    print(board.is_on_board(-1, 1))
    print(board.coord2board((1, 1)))
    print(board.board2coord('E3'))

    print(board.detect_reverse('C4', 'X'))
    print(board.detect_reverse('F3', 'X'))
    print(*(board.get_legal_board('O')))

    board.move('F2', 'O')
    board.display()