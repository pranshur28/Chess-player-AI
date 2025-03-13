import os
import urllib.request
import time

def download_chess_pieces():
    """Download chess piece images from Wikimedia Commons."""
    print("Downloading chess piece images from Wikimedia Commons...")
    
    # Create pieces directory if it doesn't exist
    pieces_dir = "pieces"
    if not os.path.exists(pieces_dir):
        os.makedirs(pieces_dir)
    
    # URLs for the chess piece images
    piece_urls = {
        # White pieces
        'wP': 'https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg',
        'wN': 'https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg',
        'wB': 'https://upload.wikimedia.org/wikipedia/commons/b/b1/Chess_blt45.svg',
        'wR': 'https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg',
        'wQ': 'https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg',
        'wK': 'https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg',
        
        # Black pieces
        'bP': 'https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg',
        'bN': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg',
        'bB': 'https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg',
        'bR': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg',
        'bQ': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg',
        'bK': 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg',
    }
    
    # Download each piece
    for piece_name, url in piece_urls.items():
        try:
            # Determine file extension from URL
            extension = url.split('.')[-1]
            file_path = os.path.join(pieces_dir, f"{piece_name}.{extension}")
            
            # Skip if file already exists
            if os.path.exists(file_path):
                print(f"File {file_path} already exists, skipping...")
                continue
            
            # Download the file
            print(f"Downloading {piece_name} from {url}...")
            urllib.request.urlretrieve(url, file_path)
            
            # Small delay to be nice to the server
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error downloading {piece_name}: {e}")
    
    print("Download complete!")
    return True

if __name__ == "__main__":
    download_chess_pieces()
