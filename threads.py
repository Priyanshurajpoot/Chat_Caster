from PyQt5.QtCore import QThread, pyqtSignal
from typing import List
import logging


class TrainingThread(QThread):
    """Background thread for model training."""
    
    # Signals
    progress = pyqtSignal(int, float, float)  # epoch, loss, progress_ratio
    finished_signal = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, model_handler, chat_data: List[str]):
        super().__init__()
        self.model_handler = model_handler
        self.chat_data = chat_data
        self._is_running = True
    
    def run(self):
        """Execute training in background."""
        try:
            logging.info("TrainingThread started")
            
            def progress_callback(epoch, loss, progress_ratio):
                if self._is_running:
                    self.progress.emit(epoch, loss, progress_ratio)
            
            success, error_msg = self.model_handler.train(
                self.chat_data, 
                progress_callback
            )
            
            if success and self._is_running:
                self.finished_signal.emit()
            elif not success:
                self.error.emit(error_msg)
                
        except Exception as e:
            logging.error(f"TrainingThread error: {str(e)}")
            self.error.emit(str(e))
    
    def stop(self):
        """Stop the training thread."""
        self._is_running = False
        logging.info("TrainingThread stop requested")


class ResponseThread(QThread):
    """Background thread for generating bot responses."""
    
    # Signals
    response_ready = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, model_handler, user_input: str):
        super().__init__()
        self.model_handler = model_handler
        self.user_input = user_input
    
    def run(self):
        """Generate response in background."""
        try:
            logging.info(f"Generating response for: {self.user_input[:50]}...")
            response = self.model_handler.generate_response(self.user_input)
            self.response_ready.emit(response)
            
        except Exception as e:
            logging.error(f"ResponseThread error: {str(e)}")
            self.error.emit(str(e))
            self.response_ready.emit(f"Error: {str(e)}")