import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui_main import WhatsAIMainWindow

def main():
    """Initialize and run the Chat Caster application."""
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Chat Caster")
    app.setOrganizationName("Chat Caster")
    
    # Create and show main window
    window = WhatsAIMainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()