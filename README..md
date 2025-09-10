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



Notes

The model is saved in trained_whatsapp_model_neo/ after training.
Logs are stored in logs/training_log.txt.
Requires a WhatsApp chat export file (e.g., from WhatsApp's "Export Chat" feature).
Training may take time; use a GPU for faster results.

Troubleshooting

Model not loading: Ensure the trained_whatsapp_model_neo/ directory exists or train a new model.
Memory issues: Reduce dataset size or use a smaller model (e.g., EleutherAI/gpt-neo-125M).

License
MIT License