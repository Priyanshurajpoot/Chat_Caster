from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QPushButton, QLabel, QProgressBar, 
                             QTextEdit, QLineEdit, QFileDialog, QMessageBox,
                             QStatusBar, QFrame)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QTextCursor
from datetime import timedelta
import time

from data_handler import load_chat_file, preprocess_chat_data
from model_handler import ModelHandler
from threads import TrainingThread, ResponseThread


class WhatsAIMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CHAT CASTER ")
        self.setGeometry(100, 100, 1000, 700)
        
        # Initialize data and model handler
        self.chat_data = None
        self.model_handler = ModelHandler()
        self.training_thread = None
        self.response_thread = None
        self.training_start_time = None
        
        # Setup UI
        self.setup_ui()
        self.apply_stylesheet()
        
        # Check for existing model
        self.check_existing_model()
    
    def setup_ui(self):
        """Initialize the main UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        layout.addWidget(self.tabs)
        
        # Setup tabs
        self.setup_tab = self.create_setup_tab()
        self.chat_tab = self.create_chat_tab()
        
        self.tabs.addTab(self.setup_tab, "⚙️ Setup & Training")
        self.tabs.addTab(self.chat_tab, "💬 Chat")
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status_bar()
    
    def create_setup_tab(self):
        """Create the setup and training tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel(" Train Your AI Bot")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Import section
        import_frame = self.create_frame()
        import_layout = QVBoxLayout(import_frame)
        
        import_label = QLabel("Step 1: Import WhatsApp Chat")
        import_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        import_layout.addWidget(import_label)
        
        self.import_btn = QPushButton("📁 Import Chat History (.txt)")
        self.import_btn.setMinimumHeight(45)
        self.import_btn.clicked.connect(self.import_chat)
        import_layout.addWidget(self.import_btn)
        
        self.import_status = QLabel("No chat history imported")
        self.import_status.setStyleSheet("color: #888;")
        import_layout.addWidget(self.import_status)
        
        layout.addWidget(import_frame)
        
        # Training section
        train_frame = self.create_frame()
        train_layout = QVBoxLayout(train_frame)
        
        train_label = QLabel("Step 2: Train the Model")
        train_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        train_layout.addWidget(train_label)
        
        btn_layout = QHBoxLayout()
        self.train_btn = QPushButton("🚀 Start Training")
        self.train_btn.setMinimumHeight(45)
        self.train_btn.setEnabled(False)
        self.train_btn.clicked.connect(self.start_training)
        btn_layout.addWidget(self.train_btn)
        
        self.cancel_btn = QPushButton("⛔ Cancel")
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_training)
        btn_layout.addWidget(self.cancel_btn)
        
        train_layout.addLayout(btn_layout)
        
        self.train_status = QLabel("")
        self.train_status.setAlignment(Qt.AlignCenter)
        self.train_status.setStyleSheet("color: #0ea5e9; font-size: 13px;")
        train_layout.addWidget(self.train_status)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setValue(0)
        train_layout.addWidget(self.progress_bar)
        
        layout.addWidget(train_frame)
        layout.addStretch()
        
        return tab
    
    def create_chat_tab(self):
        """Create the chat interface tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 11))
        layout.addWidget(self.chat_display)
        
        # Input area
        input_frame = self.create_frame()
        input_layout = QHBoxLayout(input_frame)
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message here...")
        self.chat_input.setMinimumHeight(40)
        self.chat_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.chat_input)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setMinimumHeight(40)
        self.send_btn.setMinimumWidth(100)
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        
        layout.addWidget(input_frame)
        
        return tab
    
    def create_frame(self):
        """Create a styled frame widget."""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        return frame
    
    def check_existing_model(self):
        """Check if a trained model already exists."""
        if self.model_handler.load_existing_model():
            self.import_status.setText("✅ Using pre-trained model")
            self.import_status.setStyleSheet("color: #10b981;")
            self.update_status_bar()
    
    @pyqtSlot()
    def import_chat(self):
        """Import WhatsApp chat file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select WhatsApp Chat Export", "", "Text Files (*.txt)"
        )
        
        if not file_path:
            return
        
        try:
            raw_data = load_chat_file(file_path)
            self.chat_data = preprocess_chat_data(raw_data)
            
            if len(self.chat_data) < 10:
                QMessageBox.warning(
                    self, "Warning", 
                    "Too few messages found. Please import a larger chat history."
                )
                return
            
            self.import_status.setText(f"✅ Imported {len(self.chat_data)} messages")
            self.import_status.setStyleSheet("color: #10b981;")
            self.train_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import chat:\n{str(e)}")
    
    @pyqtSlot()
    def start_training(self):
        """Start model training in background thread."""
        if not self.chat_data:
            QMessageBox.warning(self, "Warning", "Please import chat history first")
            return
        
        self.training_start_time = time.time()
        self.train_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.import_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Create and start training thread
        self.training_thread = TrainingThread(self.model_handler, self.chat_data)
        self.training_thread.progress.connect(self.update_training_progress)
        self.training_thread.finished_signal.connect(self.training_complete)
        self.training_thread.error.connect(self.training_error)
        self.training_thread.start()
    
    @pyqtSlot()
    def cancel_training(self):
        """Cancel ongoing training."""
        if self.training_thread and self.training_thread.isRunning():
            self.training_thread.stop()
            self.train_status.setText("⚠️ Training cancelled")
            self.train_status.setStyleSheet("color: #f59e0b;")
            self.reset_training_ui()
    
    @pyqtSlot(int, float, float)
    def update_training_progress(self, epoch, loss, progress):
        """Update training progress display."""
        self.progress_bar.setValue(int(progress * 100))
        elapsed = time.time() - self.training_start_time
        elapsed_str = str(timedelta(seconds=int(elapsed)))
        
        status_text = f"Epoch {epoch}/3 | Loss: {loss:.4f} | Elapsed: {elapsed_str}"
        self.train_status.setText(status_text)
    
    @pyqtSlot()
    def training_complete(self):
        """Handle training completion."""
        elapsed = time.time() - self.training_start_time
        elapsed_str = str(timedelta(seconds=int(elapsed)))
        
        self.progress_bar.setValue(100)
        self.train_status.setText(f"✅ Training completed in {elapsed_str}")
        self.train_status.setStyleSheet("color: #10b981;")
        
        self.reset_training_ui()
        self.update_status_bar()
        
        QMessageBox.information(
            self, "Success", 
            f"Model trained successfully!\nTime: {elapsed_str}"
        )
    
    @pyqtSlot(str)
    def training_error(self, error_msg):
        """Handle training errors."""
        self.train_status.setText(f"❌ Training failed")
        self.train_status.setStyleSheet("color: #ef4444;")
        self.reset_training_ui()
        
        QMessageBox.critical(self, "Training Error", f"Training failed:\n{error_msg}")
    
    def reset_training_ui(self):
        """Reset training UI elements."""
        self.train_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.import_btn.setEnabled(True)
    
    @pyqtSlot()
    def send_message(self):
        """Send user message and get bot response."""
        message = self.chat_input.text().strip()
        if not message:
            return
        
        if not self.model_handler.is_model_loaded():
            self.display_message("System", "⚠️ Please train or load a model first", "system")
            self.tabs.setCurrentIndex(0)
            return
        
        # Display user message
        self.display_message("You", message, "user")
        self.chat_input.clear()
        self.send_btn.setEnabled(False)
        
        # Generate response in background
        self.response_thread = ResponseThread(self.model_handler, message)
        self.response_thread.response_ready.connect(self.display_bot_response)
        self.response_thread.start()
    
    @pyqtSlot(str)
    def display_bot_response(self, response):
        """Display bot response in chat."""
        self.display_message("Bot", response, "bot")
        self.send_btn.setEnabled(True)
    
    def display_message(self, sender, message, msg_type="user"):
        """Display a message in the chat window."""
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if msg_type == "user":
            html = f'<div style="text-align: right; margin: 10px;"><span style="background: #0ea5e9; color: white; padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 70%;"><b>{sender}:</b> {message}</span></div>'
        elif msg_type == "bot":
            html = f'<div style="text-align: left; margin: 10px;"><span style="background: #1e293b; color: white; padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 70%;"><b>{sender}:</b> {message}</span></div>'
        else:
            html = f'<div style="text-align: center; margin: 10px;"><span style="color: #f59e0b;"><i>{message}</i></span></div>'
        
        cursor.insertHtml(html)
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()
    
    def update_status_bar(self):
        """Update status bar with model and device info."""
        device = "GPU" if self.model_handler.is_cuda_available() else "CPU"
        model_status = "Ready" if self.model_handler.is_model_loaded() else "Not Loaded"
        self.status_bar.showMessage(f"Device: {device} | Model: {model_status}")
    
    def apply_stylesheet(self):
        """Apply dark modern theme stylesheet."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QTabWidget::pane {
                border: none;
                background: #1e293b;
            }
            QTabBar::tab {
                background: #1e293b;
                color: #94a3b8;
                padding: 12px 24px;
                border: none;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #0ea5e9;
                color: white;
            }
            QPushButton {
                background: #0ea5e9;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0284c7;
            }
            QPushButton:disabled {
                background: #334155;
                color: #64748b;
            }
            QLabel {
                color: #e2e8f0;
            }
            QLineEdit {
                background: #1e293b;
                color: #e2e8f0;
                border: 2px solid #334155;
                padding: 8px;
                border-radius: 6px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #0ea5e9;
            }
            QTextEdit {
                background: #1e293b;
                color: #e2e8f0;
                border: 2px solid #334155;
                border-radius: 8px;
                padding: 10px;
            }
            QProgressBar {
                border: 2px solid #334155;
                border-radius: 8px;
                text-align: center;
                background: #1e293b;
                color: white;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #06b6d4);
                border-radius: 6px;
            }
            QFrame {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 15px;
            }
            QStatusBar {
                background: #1e293b;
                color: #94a3b8;
            }
        """)