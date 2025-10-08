import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AdamW
from torch.utils.data import DataLoader, TensorDataset
import logging
import os
from typing import List, Optional, Tuple

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/training_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ModelHandler:
    """Handles model loading, training, and inference."""
    
    def __init__(self, model_dir: str = 'trained_model'):
        self.model_dir = model_dir
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logging.info(f"Initialized ModelHandler with device: {self.device}")
    
    def is_cuda_available(self) -> bool:
        """Check if CUDA is available."""
        return torch.cuda.is_available()
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded and ready."""
        return self.model is not None and self.tokenizer is not None
    
    def load_existing_model(self) -> bool:
        """
        Load a previously trained model if it exists.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.model_dir):
                logging.info("No existing model found")
                return False
            
            self.model = GPT2LMHeadModel.from_pretrained(self.model_dir)
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_dir)
            self.model.to(self.device)
            self.model.eval()
            
            logging.info("Successfully loaded existing model")
            return True
            
        except Exception as e:
            logging.error(f"Failed to load existing model: {str(e)}")
            return False
    
    def train(self, chat_data: List[str], progress_callback) -> Tuple[bool, str]:
        """
        Train the model on chat data.
        
        Args:
            chat_data: List of preprocessed messages
            progress_callback: Function to report progress (epoch, loss, progress_ratio)
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            logging.info(f"Starting training with {len(chat_data)} messages")
            
            # Initialize tokenizer
            self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Tokenize data
            logging.info("Tokenizing data...")
            tokenized = self.tokenizer(
                chat_data,
                truncation=True,
                padding=True,
                max_length=128,
                return_tensors='pt'
            )
            
            # Create dataset and dataloader
            dataset = TensorDataset(
                tokenized['input_ids'],
                tokenized['attention_mask']
            )
            dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
            
            # Initialize model
            logging.info("Initializing model...")
            self.model = GPT2LMHeadModel.from_pretrained('gpt2')
            self.model.resize_token_embeddings(len(self.tokenizer))
            self.model.to(self.device)
            self.model.train()
            
            # Setup optimizer
            optimizer = AdamW(self.model.parameters(), lr=5e-5)
            
            # Training loop
            num_epochs = 3
            total_batches = len(dataloader) * num_epochs
            completed_batches = 0
            
            logging.info(f"Starting training for {num_epochs} epochs...")
            
            for epoch in range(num_epochs):
                epoch_loss = 0.0
                
                for batch_idx, batch in enumerate(dataloader):
                    input_ids = batch[0].to(self.device)
                    attention_mask = batch[1].to(self.device)
                    
                    # Forward pass
                    outputs = self.model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        labels=input_ids
                    )
                    
                    loss = outputs.loss
                    epoch_loss += loss.item()
                    
                    # Backward pass
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    
                    # Update progress
                    completed_batches += 1
                    progress = completed_batches / total_batches
                    progress_callback(epoch + 1, epoch_loss, progress)
                
                avg_loss = epoch_loss / len(dataloader)
                logging.info(f"Epoch {epoch + 1}/{num_epochs} - Average Loss: {avg_loss:.4f}")
            
            # Save model
            logging.info(f"Saving model to {self.model_dir}...")
            os.makedirs(self.model_dir, exist_ok=True)
            self.model.save_pretrained(self.model_dir)
            self.tokenizer.save_pretrained(self.model_dir)
            
            self.model.eval()
            logging.info("Training completed successfully")
            return True, ""
            
        except Exception as e:
            error_msg = f"Training failed: {str(e)}"
            logging.error(error_msg)
            return False, error_msg
    
    def generate_response(self, user_input: str, max_length: int = 100) -> str:
        """
        Generate a response to user input.
        
        Args:
            user_input: User's message
            max_length: Maximum length of generated response
            
        Returns:
            Generated response text
        """
        try:
            if not self.is_model_loaded():
                return "Error: Model not loaded"
            
            # Encode input
            input_ids = self.tokenizer.encode(user_input, return_tensors='pt').to(self.device)
            attention_mask = torch.ones(input_ids.shape, dtype=torch.long).to(self.device)
            
            # Generate response
            with torch.no_grad():
                output = self.model.generate(
                    input_ids,
                    max_length=max_length,
                    attention_mask=attention_mask,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.8,
                    top_k=50,
                    top_p=0.95,
                    num_return_sequences=1
                )
            
            # Decode and clean response
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Remove the input from response if it's included
            if response.startswith(user_input):
                response = response[len(user_input):].strip()
            
            # If response is empty or too short, return a fallback
            if not response or len(response) < 3:
                response = "I'm not sure how to respond to that."
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logging.error(error_msg)
            return error_msg