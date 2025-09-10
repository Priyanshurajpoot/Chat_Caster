WhatsApp AI Bot
A simple AI chatbot that fine-tunes a GPT-Neo model on WhatsApp chat history and allows chatting via a GUI.
Setup

Install Dependencies:
pip install -r requirements.txt


Run the App:
python src/main.py



Usage

Import Chat History:

In the "Setup" tab, click "Import Chat History" and select a WhatsApp chat export (.txt file).
Format expected: DD/MM/YYYY, HH:MM - Sender: Message


Train the Model:

Click "Train Model" to fine-tune GPT-Neo on your chat data.
Monitor progress via the progress bar and status messages.
Cancel training if needed using the "Cancel Training" button.


Chat with the Bot:

Switch to the "Chat" tab.
Type a message and click "Send" to get a response from the trained model.





License
MIT License
