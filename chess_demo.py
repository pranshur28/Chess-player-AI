import chess
import random
import time
import os

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_board(board):
    """Display the chess board in ASCII format."""
    clear_screen()
    
    print("\n  a b c d e f g h")
    print(" +-----------------+")
    
    for i in range(8):
        rank = 8 - i
        print(f"{rank}|", end=" ")
        
        for j in range(8):
            square = chess.square(j, 7 - i)
            piece = board.piece_at(square)
            
            if piece is None:
                # Use different background for alternating squares
                if (i + j) % 2 == 0:
                    print(".", end=" ")
                else:
                    print(" ", end=" ")
            else:
                # Map piece symbols to unicode characters
                symbol = piece.symbol()
                print(symbol, end=" ")
        
        print(f"|{rank}")
    
    print(" +-----------------+")
    print("  a b c d e f g h\n")
    
    # Display game status
    if board.is_checkmate():
        print("Checkmate!")
    elif board.is_stalemate():
        print("Stalemate!")
    elif board.is_check():
        print("Check!")
        
    # Show whose turn it is
    turn = "White" if board.turn == chess.WHITE else "Black"
    print(f"{turn} to move")

def auto_demo():
    """Run an automatic demo of a chess game."""
    print("Chess Game Demo - Auto-playing 10 random moves")
    print("Press Ctrl+C to exit")
    
    board = chess.Board()
    moves = []
    
    try:
        # Play 10 random moves
        for i in range(10):
            display_board(board)
            
            # Get a random legal move
            legal_moves = list(board.legal_moves)
            if not legal_moves:
                break
                
            move = random.choice(legal_moves)
            san_move = board.san(move)
            
            # Show the move
            print(f"Move {i+1}: {move.uci()} ({san_move})")
            moves.append(san_move)
            
            # Make the move
            board.push(move)
            time.sleep(2)  # Pause to see the board
            
            # Check for game over
            if board.is_game_over():
                display_board(board)
                print("Game over!")
                break
        
        # Show final board and move history
        display_board(board)
        print("\nMove history:")
        for i, move in enumerate(moves):
            if i % 2 == 0:
                print(f"{i//2 + 1}. {move}", end=" ")
            else:
                print(f"{move}")
        if len(moves) % 2 != 0:
            print()
            
        print("\nDemo complete! To play interactively, run 'python chess_player_ai.py' in your terminal.")
        print("For more information, see the README.md file.")
        
    except KeyboardInterrupt:
        print("\nDemo stopped by user.")

if __name__ == "__main__":
    auto_demo()
