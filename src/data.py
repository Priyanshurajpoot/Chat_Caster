import re
from typing import List

def preprocess_chat_data(chat_data: List[str]) -> List[str]:
    """
    Preprocess WhatsApp chat data, extracting valid messages.
    
    Args:
        chat_data (List[str]): Raw chat lines from file.
    
    Returns:
        List[str]: List of valid message texts.
    """
    processed_data = []
    pattern = r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - (.+?): (.+)'  # Format: Date, Sender, Message

    for line in chat_data:
        match = re.match(pattern, line.strip())
        if match:
            _, _, message = match.groups()
            if not ("Media omitted" in message or "Messages and calls are" in message):
                processed_data.append(message)
    
    return processed_data