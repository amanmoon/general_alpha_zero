from Games.TicTacToe.TicTacToe import TicTacToe
from Games.TicTacToe.TicTacToeNN import ResNet
from Alpha_MCTS import Alpha_MCTS

import numpy as np

import torch

game = "TicTacToe"
args = {
    "MODEL_PATH" : f"/home/adrinospy/Programming/Projects/AI ML/general_alpha_zero/Games/{game}/models_n_optimizers/",

    "ADVERSARIAL" : True,

    "TEMPERATURE" : 1,
    "DIRICHLET_EPSILON" : 0.25,
    "DIRICHLET_ALPHA" : 0.3,
    "NO_OF_SEARCHES" : 10,
    "EXPLORATION_CONSTANT" : 2,
}


tictactoe = TicTacToe()
device = torch.device("cuda" if torch.cuda.is_available else "cpu")

model = ResNet(tictactoe, 9, 128, device)
model.eval()

path = args["MODEL_PATH"] + "model.pt"
model.load_state_dict(torch.load(path))

mcts = Alpha_MCTS(tictactoe, args, model)

state = tictactoe.initialise_state()
player = 1

while True:
    print(state)
        
    if player == 1:
        valid_moves = tictactoe.get_valid_moves(state)
        print("valid_moves", [i for i in range(tictactoe.possible_state) if valid_moves[i] == 1])
        action = int(input(f"{player}:"))

        if valid_moves[action] == 0:
            print("action not valid")
            continue
            
    else:
        neutral_state = tictactoe.change_perspective(state, player)
        mcts_probs = mcts.search(neutral_state)
        print(mcts_probs)
        action = np.argmax(mcts_probs)
        
    state = tictactoe.make_move(state, action, player)
    
    is_terminal, value = tictactoe.know_terminal_value(state, action)
    
    if is_terminal:
        print(state)
        if value == 1:
            print(player, "won")
        else:
            print("draw")
        break

    player = tictactoe.get_opponent(player)