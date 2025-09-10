import customtkinter as ctk
import threading
from typing import List
from src.ui import WhatsAppBotUI
from src.model import load_model, train_model, generate_response
from src.data import preprocess_chat_data

class WhatsAppBotApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.chat_data = None
        # Initialize model and tokenizer as None
        model_tokenizer = load_model()
        self.model = None
        self.tokenizer = None
        if model_tokenizer is not None:
            self.model, self.tokenizer = model_tokenizer
        
        self.ui = WhatsAppBotUI(
            self.root,
            import_callback=self.import_chat_history,
            train_callback=self.start_training,
            send_callback=self.send_message
        )
    
    def import_chat_history(self, chat_data: List[str]):
        """Store imported chat data."""
        self.chat_data = preprocess_chat_data(chat_data)
    
    def start_training(self, update_progress, training_complete, training_error):
        """Start model training in a separate thread."""
        def train():
            try:
                self.model, self.tokenizer = train_model(self.chat_data, update_progress)
                training_complete(time.time() - self.ui.training_start_time)
            except Exception as e:
                training_error(str(e))
        
        threading.Thread(target=train, daemon=True).start()
    
    def send_message(self, message: str):
        """Generate and display bot response."""
        if self.model is None or self.tokenizer is None:
            self.ui.display_message("Bot", "Please train the model first.")
            return
        
        def generate():
            response = generate_response(self.model, self.tokenizer, message)
            self.ui.display_message("Bot", response)
        
        threading.Thread(target=generate, daemon=True).start()
    
    def run(self):
        """Run the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = WhatsAppBotApp()
    app.run()