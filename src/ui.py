import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import timedelta
import time
from typing import Callable, Optional

class WhatsAppBotUI:
    def __init__(self, master: ctk.CTk, import_callback: Callable, train_callback: Callable, send_callback: Callable):
        """
        Initialize the UI for the WhatsApp bot.
        
        Args:
            master: Root Tkinter window.
            import_callback: Function to handle chat import.
            train_callback: Function to handle model training.
            send_callback: Function to handle sending messages.
        """
        self.master = master
        self.master.title("WhatsApp AI Bot")
        self.master.geometry("800x600")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.import_callback = import_callback
        self.train_callback = train_callback
        self.send_callback = send_callback
        self.training_start_time = None
        self.is_training = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the tabbed interface."""
        self.notebook = ctk.CTkTabview(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.setup_tab = self.notebook.add("Setup")
        self.chat_tab = self.notebook.add("Chat")
        
        self.setup_setup_tab()
        self.setup_chat_tab()
    
    def setup_setup_tab(self):
        """Set up the Setup tab."""
        frame = ctk.CTkFrame(self.setup_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ctk.CTkButton(frame, text="Import Chat History", command=self.import_chat_history).pack(pady=10)
        self.import_status_label = ctk.CTkLabel(frame, text="No chat history imported.")
        self.import_status_label.pack(pady=10)
        
        self.train_button = ctk.CTkButton(frame, text="Train Model", command=self.start_training)
        self.train_button.pack(pady=10)
        self.cancel_button = ctk.CTkButton(frame, text="Cancel Training", command=self.cancel_training, state=tk.DISABLED)
        self.cancel_button.pack(pady=10)
        
        self.train_status_label = ctk.CTkLabel(frame, text="")
        self.train_status_label.pack(pady=10)
        
        self.progress_label = ctk.CTkLabel(frame, text="Training Progress:")
        self.progress_label.pack(pady=(10, 0))
        self.progress_bar = ctk.CTkProgressBar(frame, width=300)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 10))
    
    def setup_chat_tab(self):
        """Set up the Chat tab."""
        frame = ctk.CTkFrame(self.chat_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.chat_display = ctk.CTkTextbox(frame, height=400, width=600, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.chat_entry = ctk.CTkEntry(input_frame, width=500)
        self.chat_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ctk.CTkButton(input_frame, text="Send", command=self.send_message).pack(side=tk.RIGHT)
    
    def import_chat_history(self):
        """Import chat history from file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    chat_data = file.readlines()
                self.import_status_label.configure(text=f"Imported {len(chat_data)} messages.")
                self.import_callback(chat_data)
                self.train_button.configure(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Error importing chat: {str(e)}")
    
    def start_training(self):
        """Start model training in a separate thread."""
        if not self.import_callback.__self__.chat_data:
            messagebox.showerror("Error", "Please import chat history first.")
            return
        
        self.is_training = True
        self.training_start_time = time.time()
        self.progress_bar.set(0)
        self.train_status_label.configure(text="Training in progress...")
        self.train_button.configure(state=tk.DISABLED)
        self.cancel_button.configure(state=tk.NORMAL)
        
        self.train_callback(self.update_progress, self.training_complete, self.training_error)
    
    def cancel_training(self):
        """Cancel ongoing training."""
        self.is_training = False
        self.train_status_label.configure(text="Training cancelled.")
        self.train_button.configure(state=tk.NORMAL)
        self.cancel_button.configure(state=tk.DISABLED)
        self.progress_bar.set(0)
    
    def update_progress(self, epoch: int, loss: float, progress: float):
        """Update training progress in UI."""
        if not self.is_training:
            return
        
        self.progress_bar.set(progress)
        elapsed_time = time.time() - self.training_start_time
        elapsed_time_str = str(timedelta(seconds=int(elapsed_time)))
        status_text = f"Epoch {epoch}/3 (Loss: {loss:.4f})\nElapsed: {elapsed_time_str}"
        self.train_status_label.configure(text=status_text)
    
    def training_complete(self, total_time: float):
        """Handle training completion."""
        if not self.is_training:
            return
        
        self.is_training = False
        self.progress_bar.set(1)
        elapsed_time_str = str(timedelta(seconds=int(total_time)))
        self.train_status_label.configure(text=f"Training completed in {elapsed_time_str}.")
        self.train_button.configure(state=tk.NORMAL)
        self.cancel_button.configure(state=tk.DISABLED)
        messagebox.showinfo("Success", "Model trained successfully.")
    
    def training_error(self, error: str):
        """Handle training errors."""
        if not self.is_training:
            return
        
        self.is_training = False
        self.train_status_label.configure(text=f"Training failed: {error}")
        self.train_button.configure(state=tk.NORMAL)
        self.cancel_button.configure(state=tk.DISABLED)
        messagebox.showerror("Error", f"Training failed: {error}")
    
    def send_message(self):
        """Send user message and display response."""
        message = self.chat_entry.get().strip()
        if not message:
            return
        
        self.display_message("You", message)
        self.chat_entry.delete(0, tk.END)
        self.send_callback(message)
    
    def display_message(self, sender: str, message: str):
        """Display a message in the chat window."""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.configure(state=tk.DISABLED)