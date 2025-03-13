import pygame
import chess
import sys
import time
import random
import os
from pygame import gfxdraw

# Initialize pygame
pygame.init()

# Constants
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)  # Light brown
DARK_SQUARE = (181, 136, 99)    # Dark brown
HIGHLIGHT = (124, 252, 0)       # Green for highlighting selected pieces
LIGHT_MOVE_HIGHLIGHT = (247, 236, 118)  # Light yellow for highlighting possible moves on light squares
DARK_MOVE_HIGHLIGHT = (187, 174, 60)    # Darker yellow for highlighting possible moves on dark squares
TEXT_COLOR = (50, 50, 50)

# Piece symbols (using Unicode chess symbols) - fallback if images fail to load
PIECE_SYMBOLS = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

class ChessGUI:
    def __init__(self, player_color='white', difficulty='medium'):
        # Set up the display
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 40))  # Extra space for status bar
        pygame.display.set_caption("Chess GUI")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Set up the board
        self.board = chess.Board()
        self.player_color = chess.WHITE if player_color.lower() == 'white' else chess.BLACK
        self.computer_color = not self.player_color
        self.difficulty = difficulty
        
        # Set up difficulty levels (depth for move search)
        self.difficulty_levels = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }
        
        # Game state variables
        self.selected_square = None
        self.possible_moves = []
        self.game_over = False
        self.status_message = "Your turn" if self.board.turn == self.player_color else "Computer's turn"
        
        # Set up fonts
        self.piece_font = pygame.font.SysFont('Arial', 50)
        self.status_font = pygame.font.SysFont('Arial', 20)
        
        # Load chess piece images
        self.piece_images = self.load_piece_images()
        
        # If computer plays white, make the first move
        if self.computer_color == chess.WHITE:
            self.make_computer_move()
    
    def load_piece_images(self):
        """Load chess piece images from the pieces directory."""
        piece_images = {}
        pieces_dir = "pieces"
        
        # Map chess.py piece symbols to image file prefixes
        piece_map = {
            'P': 'wP', 'N': 'wN', 'B': 'wB', 'R': 'wR', 'Q': 'wQ', 'K': 'wK',
            'p': 'bP', 'n': 'bN', 'b': 'bB', 'r': 'bR', 'q': 'bQ', 'k': 'bK'
        }
        
        # Try to load each piece image
        for symbol, prefix in piece_map.items():
            try:
                # Look for PNG files
                png_path = os.path.join(pieces_dir, f"{prefix}.png")
                if os.path.exists(png_path):
                    # Load and scale the image
                    img = pygame.image.load(png_path)
                    piece_images[symbol] = pygame.transform.scale(img, (SQUARE_SIZE-10, SQUARE_SIZE-10))
                    print(f"Loaded PNG image for {symbol}")
                    continue
                
                # If PNG not found, look for SVG files
                svg_path = os.path.join(pieces_dir, f"{prefix}.svg")
                if os.path.exists(svg_path):
                    print(f"Found SVG for {symbol}, but skipping (using text fallback)")
            except Exception as e:
                print(f"Error loading piece image for {symbol}: {e}")
        
        return piece_images
    
    def draw_board(self):
        """Draw the chess board with pieces."""
        # Draw squares
        for row in range(8):
            for col in range(8):
                # Determine base square color
                base_color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                
                # Check if this square is a possible move
                square = self.coords_to_square(col, row)
                if square in self.possible_moves:
                    # Use a glowing highlight color based on the base square color
                    if (row + col) % 2 == 0:  # Light square
                        color = LIGHT_MOVE_HIGHLIGHT
                    else:  # Dark square
                        color = DARK_MOVE_HIGHLIGHT
                else:
                    color = base_color
                
                # Draw the square
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Highlight selected square
                if self.selected_square is not None:
                    selected_col, selected_row = self.square_to_coords(self.selected_square)
                    if row == selected_row and col == selected_col:
                        pygame.draw.rect(self.screen, HIGHLIGHT, 
                                        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                        
                        # Draw a border around the selected square
                        pygame.draw.rect(self.screen, (50, 150, 50), 
                                        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
        
        # Draw coordinate labels
        label_font = pygame.font.SysFont('Arial', 12)
        for i in range(8):
            # Draw rank numbers (1-8)
            rank_label = label_font.render(str(8 - i), True, TEXT_COLOR)
            self.screen.blit(rank_label, (5, i * SQUARE_SIZE + 5))
            
            # Draw file letters (a-h)
            file_label = label_font.render(chr(97 + i), True, TEXT_COLOR)
            self.screen.blit(file_label, (i * SQUARE_SIZE + SQUARE_SIZE - 15, BOARD_SIZE - 15))
        
        # Draw pieces
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)  # Convert to chess.square (0-63)
                piece = self.board.piece_at(square)
                if piece:
                    symbol = piece.symbol()
                    
                    # Try to use image if available
                    if symbol in self.piece_images:
                        img = self.piece_images[symbol]
                        img_rect = img.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                                      row * SQUARE_SIZE + SQUARE_SIZE // 2))
                        self.screen.blit(img, img_rect)
                    else:
                        # Fall back to text symbol
                        text_symbol = PIECE_SYMBOLS[symbol]
                        color = WHITE if piece.color == chess.WHITE else BLACK
                        text = self.piece_font.render(text_symbol, True, color)
                        text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                                        row * SQUARE_SIZE + SQUARE_SIZE // 2))
                        self.screen.blit(text, text_rect)
        
        # Draw status bar
        pygame.draw.rect(self.screen, (200, 200, 200), (0, BOARD_SIZE, BOARD_SIZE, 40))
        status_text = self.status_font.render(self.status_message, True, TEXT_COLOR)
        self.screen.blit(status_text, (10, BOARD_SIZE + 10))
    
    def square_to_coords(self, square):
        """Convert a chess square (0-63) to board coordinates (col, row)."""
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)  # Flip the row since we draw from top to bottom
        return col, row
    
    def coords_to_square(self, col, row):
        """Convert board coordinates (col, row) to a chess square (0-63)."""
        return chess.square(col, 7 - row)  # Flip the row for chess.square
    
    def get_clicked_square(self, pos):
        """Convert mouse position to board square."""
        if pos[1] >= BOARD_SIZE:  # Click is in the status bar
            return None
            
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        return self.coords_to_square(col, row)
    
    def make_computer_move(self):
        """Generate and make a move for the computer."""
        if self.board.is_game_over() or self.board.turn != self.computer_color:
            return
            
        self.status_message = "Computer is thinking..."
        pygame.display.flip()
        
        # Simulate thinking time
        time.sleep(0.5)
        
        # Get legal moves
        legal_moves = list(self.board.legal_moves)
        
        # Simple move selection based on difficulty
        if self.difficulty == 'easy':
            # Random move
            move = random.choice(legal_moves)
        else:
            # Try to find a capture or check move
            capture_moves = [move for move in legal_moves if self.board.is_capture(move)]
            check_moves = []
            
            # Look for check moves
            for move in legal_moves:
                self.board.push(move)
                if self.board.is_check():
                    check_moves.append(move)
                self.board.pop()
            
            # Prioritize captures and checks based on difficulty
            if self.difficulty == 'hard' and check_moves:
                move = random.choice(check_moves)
            elif (self.difficulty == 'medium' or self.difficulty == 'hard') and capture_moves:
                move = random.choice(capture_moves)
            else:
                move = random.choice(legal_moves)
        
        # Make the move
        san_move = self.board.san(move)
        self.board.push(move)
        
        # Update status message
        self.status_message = f"Computer played: {san_move}"
        
        # Check for game over
        self.check_game_over()
    
    def handle_player_move(self, from_square, to_square):
        """Handle a move from the player."""
        move = chess.Move(from_square, to_square)
        
        # Check if promotion is needed
        piece = self.board.piece_at(from_square)
        if piece and piece.piece_type == chess.PAWN:
            # Check if pawn is moving to the last rank
            to_rank = chess.square_rank(to_square)
            if (piece.color == chess.WHITE and to_rank == 7) or (piece.color == chess.BLACK and to_rank == 0):
                # Promote to queen automatically for simplicity
                move = chess.Move(from_square, to_square, promotion=chess.QUEEN)
        
        # Make the move if legal
        if move in self.board.legal_moves:
            san_move = self.board.san(move)
            self.board.push(move)
            self.status_message = f"You played: {san_move}"
            
            # Check for game over
            if not self.check_game_over():
                # Computer's turn
                self.make_computer_move()
            
            return True
        return False
    
    def check_game_over(self):
        """Check if the game is over and update status message accordingly."""
        if self.board.is_game_over():
            self.game_over = True
            
            if self.board.is_checkmate():
                winner = "You win!" if self.board.turn != self.player_color else "Computer wins!"
                self.status_message = f"Checkmate! {winner}"
            elif self.board.is_stalemate():
                self.status_message = "Game ended in stalemate!"
            elif self.board.is_insufficient_material():
                self.status_message = "Draw due to insufficient material!"
            elif self.board.is_fifty_moves():
                self.status_message = "Draw by fifty-move rule!"
            elif self.board.is_repetition():
                self.status_message = "Draw by repetition!"
            
            return True
        
        elif self.board.is_check():
            self.status_message += " Check!"
        
        return False
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    # Press 'r' to restart
                    if event.key == pygame.K_r:
                        self.board = chess.Board()
                        self.selected_square = None
                        self.possible_moves = []
                        self.game_over = False
                        self.status_message = "Game restarted"
                        
                        # If computer plays white, make the first move
                        if self.computer_color == chess.WHITE:
                            self.make_computer_move()
                
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    # Only allow player to move on their turn
                    if self.board.turn == self.player_color:
                        pos = pygame.mouse.get_pos()
                        clicked_square = self.get_clicked_square(pos)
                        
                        if clicked_square is not None:
                            # If a square is already selected, try to move
                            if self.selected_square is not None:
                                if self.handle_player_move(self.selected_square, clicked_square):
                                    self.selected_square = None
                                    self.possible_moves = []
                                else:
                                    # If the move is invalid, check if the clicked square has a player's piece
                                    piece = self.board.piece_at(clicked_square)
                                    if piece and piece.color == self.player_color:
                                        self.selected_square = clicked_square
                                        # Find all legal moves from this square
                                        self.possible_moves = []
                                        for move in self.board.legal_moves:
                                            if move.from_square == self.selected_square:
                                                self.possible_moves.append(move.to_square)
                                    else:
                                        self.selected_square = None
                                        self.possible_moves = []
                            else:
                                # Select the square if it has a player's piece
                                piece = self.board.piece_at(clicked_square)
                                if piece and piece.color == self.player_color:
                                    self.selected_square = clicked_square
                                    # Find all legal moves from this square
                                    self.possible_moves = []
                                    for move in self.board.legal_moves:
                                        if move.from_square == self.selected_square:
                                            self.possible_moves.append(move.to_square)
                                else:
                                    self.selected_square = None
                                    self.possible_moves = []
            
            # Draw the board and pieces
            self.draw_board()
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    # Create and start the game with default values
    print("Welcome to Chess GUI!")
    print("\nUsing default settings:")
    print("- Playing as white")
    print("- Medium difficulty")
    
    # Create and start the game
    game = ChessGUI(player_color='white', difficulty='medium')
    print("\nGame controls:")
    print("- Click on your pieces to select them")
    print("- Click on a highlighted square to move")
    print("- Press 'r' to restart the game")
    print("- Close the window to quit")
    game.run()

if __name__ == "__main__":
    main()
