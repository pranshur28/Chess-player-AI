import os
import urllib.request
import zipfile
import io

def download_chess_pieces():
    """Download chess piece images from a GitHub repository."""
    print("Downloading chess piece images...")
    
    # URL for chess pieces (using a common open-source set)
    url = "https://github.com/lichess-org/lila/raw/master/public/piece/cburnett/standard.zip"
    
    try:
        # Create pieces directory if it doesn't exist
        pieces_dir = "pieces"
        if not os.path.exists(pieces_dir):
            os.makedirs(pieces_dir)
        
        # Download the zip file
        response = urllib.request.urlopen(url)
        zip_data = io.BytesIO(response.read())
        
        # Extract the zip file
        with zipfile.ZipFile(zip_data) as zip_ref:
            zip_ref.extractall(pieces_dir)
        
        print("Chess piece images downloaded successfully!")
        return True
    except Exception as e:
        print(f"Error downloading chess pieces: {e}")
        return False

if __name__ == "__main__":
    download_chess_pieces()
