import re
from typing import List

def load_chat_file(file_path: str) -> List[str]:
    """
    Load WhatsApp chat file.
    
    Args:
        file_path: Path to the chat export file
        
    Returns:
        List of raw chat lines
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def preprocess_chat_data(chat_data: List[str]) -> List[str]:
    """
    Preprocess WhatsApp chat data, extracting valid messages.
    
    Args:
        chat_data: Raw chat lines from file
        
    Returns:
        List of cleaned message texts
    """
    processed_messages = []
    
    # WhatsApp formats can vary, support multiple patterns
    patterns = [
        # Format: DD/MM/YYYY, HH:MM - Name: Message
        r'\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}\s*[-–]\s*([^:]+):\s*(.+)',
        # Format: [DD/MM/YYYY, HH:MM:SS] Name: Message
        r'\[\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?\]\s*([^:]+):\s*(.+)',
        # Format: DD/MM/YY, HH:MM AM/PM - Name: Message
        r'\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}\s*(?:AM|PM)?\s*[-–]\s*([^:]+):\s*(.+)',
    ]
    
    # System messages to filter out
    system_keywords = [
        'media omitted',
        'message deleted',
        'messages and calls are end-to-end encrypted',
        'changed the subject',
        'changed this group',
        'added',
        'left',
        'removed',
        'you created group',
        'security code changed',
        'missed voice call',
        'missed video call'
    ]
    
    for line in chat_data:
        line = line.strip()
        if not line:
            continue
        
        # Try each pattern
        matched = False
        for pattern in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                # Extract message (last group in match)
                message = match.groups()[-1].strip()
                
                # Filter out system messages and media
                if message and not any(keyword in message.lower() for keyword in system_keywords):
                    # Clean message
                    message = clean_message(message)
                    if message and len(message) > 2:  # Minimum length check
                        processed_messages.append(message)
                
                matched = True
                break
        
        # If no pattern matched but line seems like a continuation, add it
        if not matched and processed_messages:
            cleaned = clean_message(line)
            if cleaned and len(cleaned) > 2:
                # Append to last message (multiline message)
                processed_messages[-1] += " " + cleaned
    
    return processed_messages

def clean_message(message: str) -> str:
    """
    Clean individual message text.
    
    Args:
        message: Raw message text
        
    Returns:
        Cleaned message
    """
    # Remove URLs
    message = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', message)
    
    # Remove email addresses
    message = re.sub(r'\S+@\S+', '', message)
    
    # Remove excessive whitespace
    message = ' '.join(message.split())
    
    # Remove special WhatsApp characters
    message = message.replace('\u200e', '')  # Left-to-right mark
    
    return message.strip()

def format_for_training(messages: List[str], max_length: int = 128) -> List[str]:
    """
    Format messages for model training.
    
    Args:
        messages: List of preprocessed messages
        max_length: Maximum message length
        
    Returns:
        Formatted messages ready for tokenization
    """
    formatted = []
    
    for msg in messages:
        # Truncate very long messages
        if len(msg) > max_length * 4:  # Rough character estimate
            msg = msg[:max_length * 4]
        
        formatted.append(msg)
    
    return formatted