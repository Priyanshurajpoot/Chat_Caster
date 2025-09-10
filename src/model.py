import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer, AdamW
from torch.utils.data import DataLoader, TensorDataset
import logging
from typing import Optional, Tuple, List  # Added List here
import os

# Configure logging
logging.basicConfig(
    filename='logs/training_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_model(model_dir: str = 'trained_whatsapp_model_neo') -> Optional[Tuple]:
    """
    Load pre-trained model and tokenizer.
    
    Args:
        model_dir (str): Directory containing saved model.
    
    Returns:
        Optional[Tuple]: (model, tokenizer) if successful, else None.
    """
    try:
        if not os.path.exists(model_dir):
            logging.info(f"No saved model found at {model_dir}. Will use default model.")
            return None
        model = GPTNeoForCausalLM.from_pretrained(model_dir)
        tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
        logging.info("Model loaded successfully.")
        return model, tokenizer
    except Exception as e:
        logging.error(f"Failed to load model: {str(e)}")
        return None

def train_model(chat_data: List[str], update_progress_callback) -> Tuple:
    """
    Train GPT-Neo model on chat data.
    
    Args:
        chat_data (List[str]): Preprocessed chat messages.
        update_progress_callback: Function to update UI progress.
    
    Returns:
        Tuple: Trained (model, tokenizer).
    """
    try:
        tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-125M')
        tokenizer.pad_token = tokenizer.eos_token
        
        tokenized_text = tokenizer(
            chat_data,
            truncation=True,
            padding=True,
            return_tensors="pt",
            max_length=128  # Reduced for simplicity
        )
        
        dataset = TensorDataset(tokenized_text['input_ids'], tokenized_text['attention_mask'])
        dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
        
        model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M')
        model.resize_token_embeddings(len(tokenizer))
        optimizer = AdamW(model.parameters(), lr=1e-5)
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        model.train()
        
        total_epochs = 3
        total_batches = len(dataloader) * total_epochs
        completed_batches = 0
        
        for epoch in range(total_epochs):
            total_loss = 0
            for batch in dataloader:
                input_ids = batch[0].to(device)
                attention_mask = batch[1].to(device)
                
                optimizer.zero_grad()
                outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
                loss = outputs.loss
                total_loss += loss.item()
                loss.backward()
                optimizer.step()
                
                completed_batches += 1
                update_progress_callback(epoch + 1, total_loss, completed_batches / total_batches)
            
            logging.info(f'Epoch {epoch + 1}/{total_epochs}, Loss: {total_loss:.4f}')
        
        model.save_pretrained('trained_whatsapp_model_neo')
        tokenizer.save_pretrained('trained_whatsapp_model_neo')
        return model, tokenizer
    
    except Exception as e:
        logging.error(f"Training failed: {str(e)}")
        raise

def generate_response(model, tokenizer, user_input: str) -> str:
    """
    Generate a response to user input.
    
    Args:
        model: Trained GPT-Neo model.
        tokenizer: GPT2 tokenizer.
        user_input (str): User's message.
    
    Returns:
        str: Generated response.
    """
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        input_ids = tokenizer.encode(user_input, return_tensors='pt').to(device)
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long).to(device)
        
        output = model.generate(
            input_ids,
            max_length=100,
            attention_mask=attention_mask,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95
        )
        
        return tokenizer.decode(output[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error generating response: {str(e)}"