"""
Главный файл шахматного эмулятора
Реализованы дополнительные задания: 1, 5, 6, 7, 8 (Суммарная сложность: 5)
"""

import copy
import os
import sys

# Цвета для текста и фона клеток доски
GREEN_COLOR = "\033[92m"
BLUE_COLOR = "\033[94m"
YELLOW_COLOR = "\033[93m"
RED_COLOR = "\033[91m"
CYAN_COLOR = "\033[96m"
MAGENTA_COLOR = "\033[95m"
RESET_COLOR = "\033[0m"

# Фоновые цвета для шахматной доски и подсветки (Задания 6 и 7)
BG_LIGHT = "\033[47m"  # Светлая клетка
BG_DARK = "\033[100m"  # Темная клетка
BG_GREEN = "\033[42m"  # Подсветка доступного хода
BG_RED = "\033[41m"  # Подсветка угрозы (фигура под боем)
BG_MAGENTA = "\033[45m"  # Выбранная фигура


# ==========================================
# ЯДРО (ДВИЖОК ШАХМАТ)
# ==========================================


class Piece:
    """Класс, представляющий шахматную фигуру (в т.ч. новые из Задания 1)"""

    def __init__(self, color, type_):
        self.color = color
        self.type = type_

    def __repr__(self):
        return f"{self.color}_{self.type}"

    def symbol(self):
        # Добавлены новые фигуры: champion (★), wizard (✧), jumper (⚶)
        symbols = {
            "white": {
                "king": "♔",
                "queen": "♕",
                "rook": "♖",
                "bishop": "♗",
                "knight": "♘",
                "pawn": "♙",
                "champion": "★",
                "wizard": "✧",
                "jumper": "⚶",
            },
            "black": {
                "king": "♚",
                "queen": "♛",
                "rook": "♜",
                "bishop": "♝",
                "knight": "♞",
                "pawn": "♟",
                "champion": "★",
                "wizard": "✧",
                "jumper": "⚶",
            },
        }

        sym = symbols[self.color].get(self.type, "?")
        if self.color == "white":
            return f"{YELLOW_COLOR}{sym}{RESET_COLOR}"
        else:
            return f"{BLUE_COLOR}{sym}{RESET_COLOR}"


class ChessEngine:
    """Движок шахмат со сложными правилами пешки и кастомными режимами"""

    def __init__(self, mode="standard"):
        self.mode = mode
        self.board = self.create_board(mode)
        self.turn = "white"
        self.move_log = []
        self.game_over = False
        self.winner = None
        self.move_count = 0
        self.en_passant_target = None  # Задание 8: Клетка для взятия на проходе

    def create_board(self, mode):
        """Создает расстановку. Задание 1: поддержка режима 'fairy' с новыми фигурами"""
        board = [[None for _ in range(8)] for _ in range(8)]

        for c in range(8):
            board[1][c] = Piece("black", "pawn")
            board[6][c] = Piece("white", "pawn")

        if mode == "fairy":
            # Заменяем ферзя, слонов и коней на новые фигуры
            placement = [
                "rook",
                "jumper",
                "wizard",
                "champion",
                "king",
                "wizard",
                "jumper",
                "rook",
            ]
        else:
            placement = [
                "rook",
                "knight",
                "bishop",
                "queen",
                "king",
                "bishop",
                "knight",
                "rook",
            ]

        for c, type_ in enumerate(placement):
            board[0][c] = Piece("black", type_)
            board[7][c] = Piece("white", type_)

        return board

    def switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"

    def get_valid_moves_for_piece(self, r, c, board):
        piece = board[r][c]
        moves = []

        directions = {
            "rook": [(-1, 0), (1, 0), (0, -1), (0, 1)],
            "bishop": [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            "knight": [
                (-2, -1),
                (-2, 1),
                (-1, -2),
                (-1, 2),
                (1, -2),
                (1, 2),
                (2, -1),
                (2, 1),
            ],
            "king": [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ],
            # Задание 1: Правила новых фигур
            # Чемпион: ходит на 1 или 2 клетки по прямой (может перепрыгивать)
            "champion": [
                (-2, 0),
                (2, 0),
                (0, -2),
                (0, 2),
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            ],
            # Колдун: ходит на 1 или 3 клетки по диагонали (может перепрыгивать)
            "wizard": [
                (-3, -3),
                (-3, 3),
                (3, -3),
                (3, 3),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ],
            # Прыгун: ходит ровно на 2 клетки в любом направлении
            "jumper": [
                (-2, -2),
                (-2, 2),
                (2, -2),
                (2, 2),
                (-2, 0),
                (2, 0),
                (0, -2),
                (0, 2),
            ],
        }
        directions["queen"] = directions["rook"] + directions["bishop"]

        # --- ЗАДАНИЕ 8: ПЕШКА (Взятие на проходе) ---
        if piece.type == "pawn":
            direction = -1 if piece.color == "white" else 1
            if 0 <= r + direction < 8 and board[r + direction][c] is None:
                moves.append((r + direction, c))
                start_row = 6 if piece.color == "white" else 1
                if r == start_row and board[r + direction * 2][c] is None:
                    moves.append((r + direction * 2, c))

            for dc in [-1, 1]:
                if 0 <= r + direction < 8 and 0 <= c + dc < 8:
                    target = board[r + direction][c + dc]
                    if target and target.color != piece.color:
                        moves.append((r + direction, c + dc))
                    # Взятие на проходе
                    elif self.en_passant_target == (r + direction, c + dc):
                        moves.append((r + direction, c + dc))

        # --- ПРЫГАЮЩИЕ ФИГУРЫ (вкл. новые) ---
        elif piece.type in ["knight", "king", "champion", "wizard", "jumper"]:
            for dr, dc in directions[piece.type]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    target = board[nr][nc]
                    if target is None or target.color != piece.color:
                        moves.append((nr, nc))

        # --- ДАЛЬНОБОЙНЫЕ ФИГУРЫ ---
        elif piece.type in ["rook", "bishop", "queen"]:
            for dr, dc in directions[piece.type]:
                for i in range(1, 8):
                    nr, nc = r + dr * i, c + dc * i
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target is None:
                            moves.append((nr, nc))
                        elif target.color != piece.color:
                            moves.append((nr, nc))
                            break
                        else:
                            break
                    else:
                        break
        return moves

    def is_check(self, color, board):
        king_pos = None
        for r in range(8):
            for c in range(8):
                p = board[r][c]
                if p and p.type == "king" and p.color == color:
                    king_pos = (r, c)
                    break
        if not king_pos:
            return False
        opponent = "black" if color == "white" else "white"
        for r in range(8):
            for c in range(8):
                p = board[r][c]
                if p and p.color == opponent:
                    moves = self.get_valid_moves_for_piece(r, c, board)
                    if king_pos in moves:
                        return True
        return False

    def get_legal_moves(self, r, c):
        piece = self.board[r][c]
        if not piece or piece.color != self.turn:
            return []
        pseudo_moves = self.get_valid_moves_for_piece(r, c, self.board)
        legal_moves = []
        for move in pseudo_moves:
            temp_board = [row[:] for row in self.board]
            temp_board[move[0]][move[1]] = temp_board[r][c]
            temp_board[r][c] = None

            # Взятие на проходе на копии доски для корректной проверки шаха
            if piece.type == "pawn" and move == self.en_passant_target:
                temp_board[r][move[1]] = None

            if not self.is_check(self.turn, temp_board):
                legal_moves.append(move)
        return legal_moves

    def get_all_possible_moves(self, color, board_state=None):
        board = board_state if board_state else self.board
        moves = []
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece.color == color:
                    valid_moves = self.get_valid_moves_for_piece(r, c, board)
                    for move in valid_moves:
                        moves.append(((r, c), move))
        return moves

    def is_checkmate(self):
        if not self.is_check(self.turn, self.board):
            return False
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == self.turn:
                    if len(self.get_legal_moves(r, c)) > 0:
                        return False
        return True

    def make_move(self, start, end, promote_to="queen"):
        r1, c1 = start
        r2, c2 = end
        piece = self.board[r1][c1]

        if not piece or piece.color != self.turn:
            return False
        legal_moves = self.get_legal_moves(r1, c1)
        if (r2, c2) not in legal_moves:
            return False

        state_snapshot = {
            "board": copy.deepcopy(self.board),
            "turn": self.turn,
            "move_count": self.move_count,
            "game_over": self.game_over,
            "en_passant_target": self.en_passant_target,
        }
        self.move_log.append(state_snapshot)

        # Выполняем взятие на проходе
        if piece.type == "pawn" and (r2, c2) == self.en_passant_target:
            self.board[r1][c2] = None

        # Установка флага для будущего взятия на проходе
        if piece.type == "pawn" and abs(r1 - r2) == 2:
            self.en_passant_target = ((r1 + r2) // 2, c1)
        else:
            self.en_passant_target = None

        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = None

        # Задание 8: Превращение пешки
        if piece.type == "pawn" and (r2 == 0 or r2 == 7):
            self.board[r2][c2].type = promote_to

        self.switch_turn()
        self.move_count += 1

        if self.is_checkmate():
            self.game_over = True
            self.winner = "black" if self.turn == "white" else "white"
        return True

    def undo_move(self):
        if not self.move_log:
            return False
        state = self.move_log.pop()
        self.board = state["board"]
        self.turn = state["turn"]
        self.move_count = state["move_count"]
        self.game_over = state["game_over"]
        self.en_passant_target = state["en_passant_target"]
        self.winner = None
        return True


def parse_square(sq_str):
    try:
        c = ord(sq_str[0].lower()) - ord("a")
        r = 8 - int(sq_str[1])
        if 0 <= r < 8 and 0 <= c < 8:
            return (r, c)
    except:
        pass
    return None


# ==========================================
# UI И НАВИГАЦИЯ (State Machine)
# ==========================================


class AdvancedChessEmulator:
    def __init__(self):
        self.engine = ChessEngine()
        self.current_state = "main_menu"
        self.selected_square = None  # Для подсветки доступных ходов (Задание 6)
        self.show_threats = False  # Для подсветки угроз (Задание 7)

    def run(self):
        self.print_header()
        while True:
            try:
                if self.current_state == "main_menu":
                    self.show_main_menu()
                elif self.current_state == "play_match":
                    self.play_match()
                else:
                    self.current_state = "main_menu"
            except KeyboardInterrupt:
                print(f"\n\n{RED_COLOR}🔚 Выход из программы...{RESET_COLOR}")
                break
            except Exception as e:
                print(f"\n{RED_COLOR}❌ Ошибка: {e}{RESET_COLOR}")
                self.current_state = "main_menu"

    def print_header(self):
        print(
            f"{CYAN_COLOR}=================================================={RESET_COLOR}"
        )
        print(
            f"{YELLOW_COLOR}♟️   ПРОДВИНУТЫЙ ЭМУЛЯТОР ШАХМАТ (MAX COMPLEXITY)  ♙{RESET_COLOR}"
        )
        print(
            f"{CYAN_COLOR}=================================================={RESET_COLOR}"
        )

    def show_main_menu(self):
        print(f"\n{CYAN_COLOR}=== ГЛАВНОЕ МЕНЮ ==={RESET_COLOR}")
        status = (
            "Продолжить"
            if self.engine.move_count > 0 and not self.engine.game_over
            else "Начать"
        )

        print(f"1 - 🎮 {status} классическую партию")
        print("2 - 🌟 Начать СКАЗОЧНЫЕ ШАХМАТЫ (3 новые фигуры)")
        print("0 - 👋 Выход")
        print(f"\n{YELLOW_COLOR}Выберите опцию: {RESET_COLOR}", end="")

        choice = input().strip()

        if choice == "1":
            if self.engine.game_over or self.engine.mode != "standard":
                self.engine = ChessEngine("standard")
            self.current_state = "play_match"
        elif choice == "2":
            self.engine = ChessEngine("fairy")
            self.current_state = "play_match"
        elif choice == "0":
            sys.exit()

    def print_board_styled(self):
        """Задание 6 и 7: Вывод доски с подсветкой доступных ходов и угроз"""
        legal_destinations = set()
        if self.selected_square:
            moves = self.engine.get_legal_moves(*self.selected_square)
            legal_destinations = {end for end in moves}

        threatened_squares = set()
        if self.show_threats:
            opponent = "black" if self.engine.turn == "white" else "white"
            moves = self.engine.get_all_possible_moves(opponent)
            threatened_squares = {end for start, end in moves}

        print(f"\n{CYAN_COLOR}    a  b  c  d  e  f  g  h{RESET_COLOR}")

        for r in range(8):
            row_s = f"{CYAN_COLOR}{8 - r} {RESET_COLOR}"
            for c in range(8):
                piece = self.engine.board[r][c]

                # Логика цветов фона
                is_selected = self.selected_square == (r, c)
                is_legal_dest = (r, c) in legal_destinations
                is_threatened = (
                    (r, c) in threatened_squares
                    and piece
                    and piece.color == self.engine.turn
                )

                if is_selected:
                    bg = BG_MAGENTA
                elif is_legal_dest:
                    bg = BG_GREEN
                elif is_threatened:
                    bg = BG_RED
                else:
                    bg = BG_LIGHT if (r + c) % 2 == 0 else BG_DARK

                sym = piece.symbol() if piece else " "
                row_s += f"{bg} {sym} {RESET_COLOR}"

            row_s += f"{CYAN_COLOR} {8 - r}{RESET_COLOR}"
            print(row_s)

        print(f"{CYAN_COLOR}    a  b  c  d  e  f  g  h{RESET_COLOR}\n")

    def play_match(self):
        if self.engine.game_over:
            print(
                f"\n{YELLOW_COLOR}🏆 МАТ! Победили {self.engine.winner.upper()}!{RESET_COLOR}"
            )
            input(f"{CYAN_COLOR}Нажмите Enter для выхода в меню...{RESET_COLOR}")
            self.current_state = "main_menu"
            return

        self.print_board_styled()

        turn_str = (
            f"{YELLOW_COLOR}БЕЛЫЕ{RESET_COLOR}"
            if self.engine.turn == "white"
            else f"{BLUE_COLOR}ЧЕРНЫЕ{RESET_COLOR}"
        )
        print(f"Ход: {turn_str} | Всего ходов: {self.engine.move_count}")
        print(
            f"{CYAN_COLOR}Команды: {RESET_COLOR}'e2' (выбрать), 'e2e4' (ход), 'undo', 'threats' (угрозы), '0' (в меню)"
        )

        cmd = input(f"{YELLOW_COLOR}Ваш выбор: {RESET_COLOR}").strip().lower()

        if cmd == "0":
            self.current_state = "main_menu"
            return

        if cmd == "undo":
            self.engine.undo_move()
            self.selected_square = None
            return

        if cmd == "threats":
            self.show_threats = not self.show_threats
            return

        # Задание 6: Интерактивный выбор фигуры (написал 'e2')
        if len(cmd) == 2:
            sq = parse_square(cmd)
            if sq:
                piece = self.engine.board[sq[0]][sq[1]]
                if piece and piece.color == self.engine.turn:
                    self.selected_square = sq
                else:
                    self.selected_square = None
                    print(
                        f"{RED_COLOR}❌ Это не ваша фигура или клетка пуста!{RESET_COLOR}"
                    )
            return

        # Совершение хода: 'e2e4' или если фигура уже выбрана 'e4'
        start, end = None, None
        if len(cmd) == 4:
            start, end = parse_square(cmd[:2]), parse_square(cmd[2:])
        elif len(cmd) == 2 and self.selected_square:
            start, end = self.selected_square, parse_square(cmd)

        if start and end:
            # Задание 8: Проверка на превращение пешки
            piece = self.engine.board[start[0]][start[1]]
            promote_to = "queen"
            if piece and piece.type == "pawn" and (end[0] == 0 or end[0] == 7):
                if end in self.engine.get_legal_moves(*start):
                    print(
                        f"{MAGENTA_COLOR}🌟 Пешка достигла края! В кого превратить? (queen, rook, bishop, knight){RESET_COLOR}"
                    )
                    choice = input("Выбор: ").strip().lower()
                    if choice in ["queen", "rook", "bishop", "knight"]:
                        promote_to = choice

            if self.engine.make_move(start, end, promote_to):
                self.selected_square = None
            else:
                print(f"\n{RED_COLOR}❌ Недопустимый ход!{RESET_COLOR}")
        else:
            print(
                f"\n{RED_COLOR}❌ Неправильный формат! Введите откуда и куда (например: e2e4) или кликните e2{RESET_COLOR}"
            )


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    app = AdvancedChessEmulator()
    app.run()
