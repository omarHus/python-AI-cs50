import tictactoe as ttt


board = ttt.test_state()

while not (ttt.terminal(board)):
    move = ttt.minimax(board)
    print(ttt.player(board))
    print(move)
    board = ttt.result(board, move)
    print(board)

print(f"The winner is {ttt.winner(board)}")

