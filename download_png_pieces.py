import os
import urllib.request
import time

def download_chess_pieces():
    """Download chess piece PNG images from a reliable source."""
    print("Downloading chess piece images...")
    
    # Create pieces directory if it doesn't exist
    pieces_dir = "pieces"
    if not os.path.exists(pieces_dir):
        os.makedirs(pieces_dir)
    
    # URLs for the chess piece images (using a reliable source with PNG images)
    piece_urls = {
        # White pieces
        'wP': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wp.png',
        'wN': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wn.png',
        'wB': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wb.png',
        'wR': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wr.png',
        'wQ': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wq.png',
        'wK': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wk.png',
        
        # Black pieces
        'bP': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bp.png',
        'bN': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bn.png',
        'bB': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bb.png',
        'bR': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/br.png',
        'bQ': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bq.png',
        'bK': 'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bk.png',
    }
    
    # Add a user agent to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Download each piece
    for piece_name, url in piece_urls.items():
        try:
            file_path = os.path.join(pieces_dir, f"{piece_name}.png")
            
            # Skip if file already exists
            if os.path.exists(file_path):
                print(f"File {file_path} already exists, skipping...")
                continue
            
            # Download the file with headers
            print(f"Downloading {piece_name} from {url}...")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            
            # Small delay to be nice to the server
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error downloading {piece_name}: {e}")
    
    print("Download complete!")
    return True

if __name__ == "__main__":
    download_chess_pieces()
