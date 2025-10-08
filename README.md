![CHAT CASTER
](<Chat caster .png>)

A desktop application that trains a custom AI chatbot on your WhatsApp chat history using GPT-2. Built with PyQt5 and PyTorch, Chat Caster allows you to create a personalized AI that mimics conversation patterns from your exported WhatsApp chats.



 🌟 Features

- **Import WhatsApp Chats**: Load exported WhatsApp chat history (.txt files)
- **Custom AI Training**: Fine-tune GPT-2 model on your conversation data
- **Modern UI**: Dark-themed, user-friendly interface built with PyQt5
- **Real-time Training Progress**: Track training epochs, loss, and elapsed time
- **Interactive Chat**: Chat with your trained AI model in real-time
- **GPU Acceleration**: Automatic CUDA detection for faster training
- **Background Processing**: Non-blocking training and response generation
- **Model Persistence**: Save and load trained models for reuse

## 📋 Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (optional, but recommended for faster training)
- WhatsApp chat export file

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/chat-caster.git
cd chat-caster
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For GPU support, install CUDA-enabled PyTorch:
```bash
# Visit https://pytorch.org/get-started/locally/ for your specific configuration
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 📱 Exporting WhatsApp Chats

### On Android:
1. Open WhatsApp and navigate to the chat you want to export
2. Tap the three dots (⋮) in the top-right corner
3. Select **More** → **Export chat**
4. Choose **Without media**
5. Save the .txt file

### On iOS:
1. Open the chat in WhatsApp
2. Tap the contact/group name at the top
3. Scroll down and tap **Export Chat**
4. Choose **Without Media**
5. Save the file

## 🎯 Usage

### Starting the Application

```bash
python main.py
```

### Training Your Model

1. **Navigate to Setup & Training Tab**
   - Click on the "⚙️ Setup & Training" tab

2. **Import Chat History**
   - Click "📁 Import Chat History (.txt)"
   - Select your exported WhatsApp chat file
   - The app will display the number of messages imported

3. **Start Training**
   - Click "🚀 Start Training"
   - Monitor progress through the progress bar
   - Training typically takes 5-30 minutes depending on chat size and hardware
   - Cancel training anytime using the "⛔ Cancel" button

4. **Training Complete**
   - Once finished, the model is automatically saved
   - You're ready to chat!

### Chatting with Your AI

1. **Navigate to Chat Tab**
   - Click on the "💬 Chat" tab

2. **Send Messages**
   - Type your message in the input field
   - Press Enter or click "Send"
   - The AI will generate a response based on your training data

## 🏗️ Project Structure

```
chat-caster/
│
├── main.py                 # Application entry point
├── ui_main.py             # Main UI window and logic
├── data_handler.py        # WhatsApp chat parsing and preprocessing
├── model_handler.py       # GPT-2 model training and inference
├── threads.py             # Background threads for training/inference
├── requirements.txt       # Python dependencies
│
├── trained_model/         # Saved model directory (created after training)
│   ├── config.json
│   ├── pytorch_model.bin
│   └── tokenizer files
│
└── logs/                  # Training logs (created automatically)
    └── training_log.txt
```

 🔧 Configuration

 Model Parameters

Edit `model_handler.py` to customize training:

```python
# Training epochs
num_epochs = 3  # Line 98

# Learning rate
lr=5e-5  # Line 101

# Batch size
batch_size=4  # Line 86

# Max sequence length
max_length=128  # Line 76
```

 Generation Parameters

Adjust response generation in `model_handler.py`:

```python
temperature=0.8    # Creativity (0.1-1.0)
top_k=50          # Top K sampling
top_p=0.95        # Nucleus sampling
max_length=100    # Response length
```
 📊 Technical Details

 Model Architecture
- **Base Model**: GPT-2 (124M parameters)
- **Framework**: PyTorch + Hugging Face Transformers
- **Training**: Fine-tuning with causal language modeling

Data Processing
- Supports multiple WhatsApp date formats
- Filters system messages and media notifications
- Removes URLs and email addresses
- Handles multi-line messages

 Performance
- **Training Time**: 5-30 minutes (depends on data size and hardware)
- **Memory**: ~2-4GB RAM (CPU) or ~4-6GB VRAM (GPU)
- **Model Size**: ~500MB on disk

⚠️ Limitations

- Requires substantial chat history (recommended: 500+ messages)
- AI responses may not always be coherent or contextually perfect
- Training quality depends on input data diversity
- Generated responses are based on patterns, not understanding

 🐛 Troubleshooting

 "Too few messages found"
- Ensure your chat export has at least 10 messages
- Check that the file format is correct (.txt)

 "CUDA out of memory"
- Reduce batch size in `model_handler.py`
- Close other GPU-intensive applications
- Use CPU training (automatic fallback)

 Import errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Ensure Python version is 3.8+

 Model not loading
- Delete `trained_model/` folder and retrain
- Check `logs/training_log.txt` for errors

## 🔒 Privacy & Security

- **All data stays local**: No data is sent to external servers
- **Your chats, your device**: Training and inference happen entirely on your machine
- **No cloud dependencies**: Works completely offline after initial setup

 Building Executable

To create a standalone executable:

```bash
pyinstaller --onefile --windowed --name "ChatCaster" main.py
```

The executable will be in the `dist/` folder.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

 👨‍💻 Authors

 PRIYANSHU RAJPOOT

 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/) for the GPT-2 implementation
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [PyTorch](https://pytorch.org/) for the deep learning backend

 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

