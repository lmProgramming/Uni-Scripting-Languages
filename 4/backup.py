import argparse
import os
import sys
import subprocess
import datetime

def create_backup(directory, backups_dir):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    dirname = os.path.basename(directory)
    backup_filename = f"{timestamp}-{dirname}.zip"
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)
    
    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)
    
    backup_path = os.path.join(backups_dir, backup_filename)
    
    if os.path.exists(backup_path):
        print(f"Error: Backup file '{backup_path}' already exists.")
        sys.exit(1)
    
    subprocess.run(["7z", "a", "-r", backup_path, directory])
    
    history_file = os.path.join(backups_dir, "backup_history.csv")
    with open(history_file, "a") as f:
        f.write(f"{timestamp},{directory},{backup_filename}\n")
    
    print(f"Backup created: {backup_path}")

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    
    parser.add_argument("directory")
    parser.add_argument("BACKUPS_DIR", default=None, nargs="*")
    
    args=parser.parse_args()  
    
    if args.BACKUPS_DIR:    
        backups_dir = args.BACKUPS_DIR
        os.environ["BACKUPS_DIR"] = backups_dir 
    
    if os.getenv("BACKUPS_DIR"):
        backups_dir = os.getenv("BACKUPS_DIR")
    else:
        backups_dir = os.path.expanduser("~/.backups")
        os.environ["BACKUPS_DIR"] = backups_dir
            
    create_backup(args.directory, backups_dir)
