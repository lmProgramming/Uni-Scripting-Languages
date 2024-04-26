import argparse
import os
import sys
import subprocess
import csv

def restore_backup(backups_dir, restore_dir):    
    history_file = os.path.join(backups_dir, "backup_history.csv")
    if not os.path.exists(history_file):
        print("Error: Backup history file does not exist.")
        sys.exit(1)
    
    backups = []
    with open(history_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            backups.append(row)
    
    if not backups:
        print("No backups found in history.")
        sys.exit(1)
    
    print("Available backups:")
    for i, backup in enumerate(backups):
        print(f"{i}. {backup[0]} - {backup[1]} - {backup[2]}")
    
    choice = input("Enter the number of the backup you want to restore: ")
    try:
        choice = int(choice)
        if choice < 0 or choice > len(backups) - 1:
            raise ValueError
    except ValueError:
        print("Invalid choice.")
        sys.exit(1)
    
    backup_path = os.path.join(backups_dir, backups[choice][2])
    
    if not os.path.exists(backup_path):
        print(f"Error: Backup file '{backup_path}' not found.")
        sys.exit(1)
            
    print(restore_dir)
    
    subprocess.run(["RMDIR", "/S", "/Q", restore_dir], shell=True)
    subprocess.run(["7z", "x", backup_path, f"-o{restore_dir}"], shell=True)

if __name__ == "__main__":    
    parser=argparse.ArgumentParser()
    
    parser.add_argument("directory")
    parser.add_argument("BACKUPS_DIR", nargs="*")
    
    if os.getenv("BACKUPS_DIR"):
        backups_dir = os.getenv("BACKUPS_DIR")
    else:
        backups_dir = os.path.expanduser("~/.backups")        
    
    args=parser.parse_args()  
    
    if args.BACKUPS_DIR:    
        backups_dir = args.BACKUPS_DIR  
        
    restore_dir = os.path.abspath(args.directory) if args.directory else os.getcwd()
            
    restore_backup(backups_dir, restore_dir)
