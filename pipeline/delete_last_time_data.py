# delete_halifax.py
from pathlib import Path

def main():
    target = Path("./output/result.json")
    if target.exists():
        target.unlink()
        print(f"Deleted {target}")
    else:
        print("No file found.")

if __name__ == "__main__":
    main()