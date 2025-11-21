import random
from collections import defaultdict

# Initialize MENACE model
class MENACE:
    def _init_(self, r_win=3, r_loss=1, r_draw=1):
        self.matchboxes = defaultdict(dict)  
        self.r_win = r_win
        self.r_loss = r_loss
        self.r_draw = r_draw

    def initialize_state(self, state):
        if state not in self.matchboxes:
            legal_moves = [i for i, v in enumerate(state) if v == ' ']
            for move in legal_moves:
                self.matchboxes[state][move] = 3  

    def choose_move(self, state):
        self.initialize_state(state)
        moves = list(self.matchboxes[state].keys())
        weights = list(self.matchboxes[state].values())
        return random.choices(moves, weights=weights)[0]

    def update_rewards(self, history, result):
        for state, move in history:
            if result == "win":
                self.matchboxes[state][move] += self.r_win
            elif result == "loss":
                self.matchboxes[state][move] = max(1, self.matchboxes[state][move] - self.r_loss)
            elif result == "draw":
                self.matchboxes[state][move] += self.r_draw

def check_winner(board):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for (a, b, c) in wins:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def board_full(board):
    return all(cell != ' ' for cell in board)

def train_menace(episodes=500):
    agent = MENACE()
    for _ in range(episodes):
        board = [' '] * 9
        history = []
        turn = 'X'  
        while True:
            state = ''.join(board)
            if turn == 'X':
                move = agent.choose_move(state)
                board[move] = 'X'
                history.append((state, move))
            else:
                legal_moves = [i for i, v in enumerate(board) if v == ' ']
                move = random.choice(legal_moves)
                board[move] = 'O'

            winner = check_winner(board)
            if winner or board_full(board):
                if winner == 'X':
                    agent.update_rewards(history, "win")
                elif winner == 'O':
                    agent.update_rewards(history, "loss")
                else:
                    agent.update_rewards(history, "draw")
                break
            turn = 'O' if turn == 'X' else 'X'
    return agent


def play_game(agent):
    board = [' '] * 9
    while True:
        state = ''.join(board)
        move = agent.choose_move(state)
        board[move] = 'X'
        winner = check_winner(board)
        if winner or board_full(board):
            break
        legal_moves = [i for i, v in enumerate(board) if v == ' ']
        move = random.choice(legal_moves)
        board[move] = 'O'
        if check_winner(board) or board_full(board):
            break
    print('Final board:', board)
    print('Winner:', check_winner(board))

if __name__ == "_main_":
    menace_agent = train_menace(episodes=1000)
    print("Training completed. MENACE ready to play!")
    play_game(menace_agent)