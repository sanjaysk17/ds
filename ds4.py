class ChessGame:
    def __init__(self):
        # 1. Initialization
        self.board = [
            ['r','n','b','q','k','b','n','r'],
            ['p','p','p','p','p','p','p','p'],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            ['P','P','P','P','P','P','P','P'],
            ['R','N','B','Q','K','B','N','R']
        ]
        self.white_turn = True
        self.history = []   # 🔥 stack for backtracking

    # 2. Print Board
    def print_board(self):
        print("\n  a b c d e f g h")
        for i in range(8):
            print(8-i, ' '.join(self.board[i]))
        print()

    # 3. Pawn Moves
    def get_pawn_moves(self, r, c):
        moves = []
        piece = self.board[r][c]
        direction = -1 if piece.isupper() else 1
        start = 6 if piece.isupper() else 1

        # Forward
        if 0 <= r + direction < 8 and self.board[r + direction][c] == ' ':
            moves.append((r + direction, c))

        # 2 step
        if r == start and self.board[r + direction][c] == ' ' and self.board[r + 2*direction][c] == ' ':
            moves.append((r + 2*direction, c))

        # Capture
        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] != ' ' and self.board[nr][nc].isupper() != piece.isupper():
                    moves.append((nr, nc))

        return moves

    # 4. Other Pieces
    def get_piece_moves(self, r, c):
        piece = self.board[r][c]

        if piece.lower() == 'p':
            return self.get_pawn_moves(r, c)

        # Rook
        moves = []
        if piece.lower() == 'r':
            for i in range(8):
                if i != r: moves.append((i, c))
                if i != c: moves.append((r, i))

        # Knight
        if piece.lower() == 'n':
            steps = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for dr, dc in steps:
                nr, nc = r+dr, c+dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    moves.append((nr, nc))

        # Bishop
        if piece.lower() == 'b':
            for d in range(1,8):
                for dr, dc in [(d,d),(d,-d),(-d,d),(-d,-d)]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        moves.append((nr, nc))

        # Queen
        if piece.lower() == 'q':
            moves += self.get_piece_moves(r, c)  # reuse

        # King
        if piece.lower() == 'k':
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        moves.append((nr, nc))

        return moves

    # 6. Validate Move
    def is_valid_move(self, r, c, nr, nc):
        piece = self.board[r][c]

        if piece == ' ':
            return False

        # Turn check
        if piece.isupper() != self.white_turn:
            return False

        # Boundary
        if not (0 <= nr < 8 and 0 <= nc < 8):
            return False

        # Same color capture
        target = self.board[nr][nc]
        if target != ' ' and target.isupper() == piece.isupper():
            return False

        return (nr, nc) in self.get_piece_moves(r, c)

    # 7. Make Move
    def make_move(self, r, c, nr, nc):
        piece = self.board[r][c]
        captured = self.board[nr][nc]

        # 🔥 store (BACKTRACKING)
        self.history.append((r, c, nr, nc, captured))

        self.board[nr][nc] = piece
        self.board[r][c] = ' '

        self.white_turn = not self.white_turn

    # 🔥 Backtracking
    def undo_move(self):
        if not self.history:
            print("No move to undo")
            return

        r, c, nr, nc, captured = self.history.pop()

        self.board[r][c] = self.board[nr][nc]
        self.board[nr][nc] = captured

        self.white_turn = not self.white_turn

    # Convert input
    def convert(self, pos):
        return 8-int(pos[1]), ord(pos[0])-ord('a')

    # 8. Play Game
    def play_game(self):
        while True:
            self.print_board()
            print("White" if self.white_turn else "Black", "turn")

            cmd = input("Enter move (e.g a2 a4) or 'undo': ")

            if cmd == "undo":
                self.undo_move()
                continue

            try:
                s, d = cmd.split()
            except:
                print("Invalid input")
                continue

            r, c = self.convert(s)
            nr, nc = self.convert(d)

            if self.is_valid_move(r, c, nr, nc):
                self.make_move(r, c, nr, nc)
            else:
                print("Invalid move")


game = ChessGame()
game.play_game()