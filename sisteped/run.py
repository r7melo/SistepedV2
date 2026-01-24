import argparse
from src.main import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true")
    
    if parser.parse_args().dev:
        app.run(host="0.0.0.0", port=5000, debug=True)