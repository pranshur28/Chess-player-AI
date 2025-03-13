import chess
import chess.engine
import chess.svg
import random
import time
import os
import platform
from IPython.display import display, SVG

class ChessGame:
    def __init__(self, player_color='white', difficulty='medium'):
        self.board = chess.Board()
        self.player_color = chess.WHITE if player_color.lower() == 'white' else chess.BLACK
        self.computer_color = not self.player_color
        self.difficulty = difficulty
        self.move_history = []
        
        # Set up difficulty levels (depth for engine search)
        self.difficulty_levels = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }
        
        # Try to load Stockfish engine if available
        self.engine = None
        try:
            if platform.system() == "Windows":
                stockfish_path = "stockfish/stockfish-windows-x86-64-avx2.exe"
            elif platform.system() == "Linux":
                stockfish_path = "stockfish/stockfish-ubuntu-x86-64-avx2"
            elif platform.system() == "Darwin":  # macOS
                stockfish_path = "stockfish/stockfish-macos-x86-64-modern"
            
            if os.path.exists(stockfish_path):
                self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        except Exception as e:
            print(f"Stockfish engine not available: {e}")
            print("Using random move selection for computer.")
    
    def display_board(self):
        """Clear the console and display the current board state."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print the board in ASCII format
        print("\n  a b c d e f g h")
        print(" +-----------------+")
        
        for i in range(8):
            rank = 8 - i
            print(f"{rank}|", end=" ")
            
            for j in range(8):
                square = chess.square(j, 7 - i)
                piece = self.board.piece_at(square)
                
                if piece is None:
                    # Use different background for alternating squares
                    if (i + j) % 2 == 0:
                        print(".", end=" ")
                    else:
                        print(" ", end=" ")
                else:
                    # Map piece symbols to unicode characters
                    symbol = piece.symbol()
                    if symbol.isupper():  # White pieces
                        print(symbol, end=" ")
                    else:  # Black pieces
                        print(symbol, end=" ")
            
            print(f"|{rank}")
        
        print(" +-----------------+")
        print("  a b c d e f g h\n")
        
        # Display game status
        if self.board.is_checkmate():
            print("Checkmate!")
        elif self.board.is_stalemate():
            print("Stalemate!")
        elif self.board.is_check():
            print("Check!")
            
        # Show whose turn it is
        turn = "White" if self.board.turn == chess.WHITE else "Black"
        print(f"{turn} to move")
        
        # Show move history
        if self.move_history:
            print("\nMove history:")
            for i, move in enumerate(self.move_history):
                if i % 2 == 0:
                    print(f"{i//2 + 1}. {move}", end=" ")
                else:
                    print(f"{move}")
            if len(self.move_history) % 2 != 0:
                print()
    
    def get_player_move(self):
        """Get a move from the player."""
        while True:
            try:
                move_uci = input("\nEnter your move (e.g., 'e2e4') or 'help' for commands: ")
                
                # Handle special commands
                if move_uci.lower() == 'help':
                    print("\nCommands:")
                    print("  help     - Show this help message")
                    print("  quit     - Exit the game")
                    print("  undo     - Take back the last move")
                    print("  moves    - Show legal moves")
                    print("  restart  - Start a new game")
                    continue
                elif move_uci.lower() == 'quit':
                    return 'quit'
                elif move_uci.lower() == 'undo':
                    if len(self.move_history) >= 2:
                        self.board.pop()  # Remove computer's move
                        self.board.pop()  # Remove player's move
                        self.move_history.pop()  # Remove from history
                        self.move_history.pop()  # Remove from history
                        self.display_board()
                    else:
                        print("Cannot undo at the beginning of the game.")
                    continue
                elif move_uci.lower() == 'moves':
                    legal_moves = list(self.board.legal_moves)
                    print("\nLegal moves:")
                    for move in legal_moves:
                        print(f"  {move.uci()} ({self.board.san(move)})")
                    continue
                elif move_uci.lower() == 'restart':
                    self.board = chess.Board()
                    self.move_history = []
                    self.display_board()
                    if self.computer_color == chess.WHITE:
                        return 'computer_turn'
                    continue
                
                # Parse the move
                if len(move_uci) == 4:
                    from_square = chess.parse_square(move_uci[0:2])
                    to_square = chess.parse_square(move_uci[2:4])
                    move = chess.Move(from_square, to_square)
                elif len(move_uci) == 5:  # Promotion, e.g., 'e7e8q'
                    from_square = chess.parse_square(move_uci[0:2])
                    to_square = chess.parse_square(move_uci[2:4])
                    promotion = {'q': chess.QUEEN, 'r': chess.ROOK, 
                                'b': chess.BISHOP, 'n': chess.KNIGHT}[move_uci[4].lower()]
                    move = chess.Move(from_square, to_square, promotion=promotion)
                else:
                    # Try to parse as SAN notation (e.g., "Nf3")
                    try:
                        move = self.board.parse_san(move_uci)
                    except ValueError:
                        print("Invalid move format. Use 'e2e4' format or standard algebraic notation.")
                        continue
                
                # Check if the move is legal
                if move in self.board.legal_moves:
                    san_move = self.board.san(move)
                    self.board.push(move)
                    self.move_history.append(san_move)
                    return move
                else:
                    print("Illegal move. Try again.")
            except ValueError as e:
                print(f"Invalid input: {e}")
            except IndexError:
                print("Invalid square. Use algebraic notation (e.g., 'e2e4').")
    
    def get_computer_move(self):
        """Generate a move for the computer based on difficulty."""
        if self.engine:
            # Use Stockfish engine with time limit based on difficulty
            time_limit = chess.engine.Limit(time=0.1 * self.difficulty_levels[self.difficulty])
            result = self.engine.play(self.board, time_limit)
            move = result.move
        else:
            # Fallback to random legal moves if no engine is available
            legal_moves = list(self.board.legal_moves)
            move = random.choice(legal_moves)
        
        # Make the move and add to history
        san_move = self.board.san(move)
        self.board.push(move)
        self.move_history.append(san_move)
        
        # Show the computer's move
        print(f"Computer plays: {move.uci()} ({san_move})")
        time.sleep(1)  # Pause briefly so the player can see the move
        
        return move
    
    def play(self):
        """Main game loop."""
        print("\nWelcome to Chess Player AI!")
        print(f"You are playing as {'White' if self.player_color else 'Black'}")
        print(f"Difficulty: {self.difficulty.capitalize()}")
        
        # If computer goes first (player is black)
        if self.computer_color == chess.WHITE:
            self.display_board()
            print("Computer is thinking...")
            self.get_computer_move()
        
        # Main game loop
        while not self.board.is_game_over():
            self.display_board()
            
            # Player's turn
            if self.board.turn == self.player_color:
                move = self.get_player_move()
                if move == 'quit':
                    break
                elif move == 'computer_turn':
                    continue
            
            # Computer's turn
            else:
                print("Computer is thinking...")
                self.get_computer_move()
            
            # Check for game over after each move
            if self.board.is_game_over():
                self.display_board()
                
                # Determine the result
                if self.board.is_checkmate():
                    winner = "Black" if self.board.turn == chess.WHITE else "White"
                    print(f"Checkmate! {winner} wins!")
                elif self.board.is_stalemate():
                    print("Game ended in stalemate!")
                elif self.board.is_insufficient_material():
                    print("Game ended due to insufficient material!")
                elif self.board.is_fifty_moves():
                    print("Game ended due to fifty-move rule!")
                elif self.board.is_repetition():
                    print("Game ended due to threefold repetition!")
                else:
                    print("Game over!")
        
        # Clean up
        if self.engine:
            self.engine.quit()
        
        print("Thanks for playing!")

def main():
    # Get player preferences
    print("Welcome to Chess Player AI!")
    
    while True:
        color = input("Do you want to play as white or black? (white/black): ").lower()
        if color in ['white', 'black']:
            break
        print("Please enter 'white' or 'black'.")
    
    while True:
        difficulty = input("Select difficulty (easy/medium/hard): ").lower()
        if difficulty in ['easy', 'medium', 'hard']:
            break
        print("Please enter 'easy', 'medium', or 'hard'.")
    
    # Create and start the game
    game = ChessGame(player_color=color, difficulty=difficulty)
    game.play()

if __name__ == "__main__":
    main()
