import sys
from PyQt5.QtWidgets import QApplication
from log_viewer import LogViewer

def main():            
    app = QApplication(sys.argv)
    
    log_viewer = LogViewer(app)
    log_viewer.show()
    sys.exit(app.exec_())       

if __name__ == "__main__":
    main()