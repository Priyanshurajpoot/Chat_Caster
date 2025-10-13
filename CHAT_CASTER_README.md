# Chat Caster - Personalized AI Chatbot Trainer

<center><img width="200" height="200" alt="Chat Caster" src="https://github.com/user-attachments/assets/34eaa0ab-f0e7-4090-885d-9041cdb84ff7" /></center>

**Chat Caster** is a desktop application that trains a custom AI chatbot on your WhatsApp chat history using GPT-2. Built with PyQt5 and PyTorch, Chat Caster allows you to create a personalized AI that mimics conversation patterns from your exported WhatsApp chats.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-GPU%20Support-orange.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Issues](https://img.shields.io/github/issues/Priyanshurajpoot/Chat_Caster)](https://github.com/Priyanshurajpoot/Chat_Caster/issues)

---

## 👨‍💻 About the Developer

**Priyanshu Rajpoot**  
*MCA Post Graduate | Python Developer | Prompt Engineer | AI Enthusiast*

- 🔗 **LinkedIn**: [priyanshux5](https://linkedin.com/in/priyanshux5)
- 💻 **GitHub**: [Priyanshurajpoot](https://github.com/Priyanshurajpoot)
- 📧 **Email**: priyanshux5xraj@gmail.com

**Core Interests**: Prompt Engineering, Artificial Intelligence, Machine Learning, NLP, Generative AI  
**Primary Skills**: Python, PyQt5, PyTorch, Transformers, OpenCV, Chrome Extension API, OAuth 2.0, Data Analysis, GUI Development

---

## ✨ Features

### Core Capabilities
- **📱 Import WhatsApp Chats** - Load exported WhatsApp chat history (.txt files)
- **🤖 Custom AI Training** - Fine-tune GPT-2 model on your conversation data
- **🎨 Modern UI** - Dark-themed, user-friendly interface built with PyQt5
- **📊 Real-time Training Progress** - Track training epochs, loss, and elapsed time
- **💬 Interactive Chat** - Chat with your trained AI model in real-time
- **⚡ GPU Acceleration** - Automatic CUDA detection for faster training
- **🔄 Background Processing** - Non-blocking training and response generation
- **💾 Model Persistence** - Save and load trained models for reuse

### Technical Features
- **Privacy-First** - All processing happens locally on your device
- **Multiple Format Support** - Handles various WhatsApp export formats
- **Smart Preprocessing** - Cleans and prepares chat data automatically
- **Customizable Training** - Adjustable hyperparameters for optimal results
- **Error Handling** - Comprehensive error reporting and recovery

---

## 🚀 Quick Start

### Installation

#### Method 1: From Source (Recommended)
```bash
# Clone the repository
git clone https://github.com/Priyanshurajpoot/Chat_Caster.git
cd Chat_Caster

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Method 2: Download Executable
1. Visit **[Releases](https://github.com/Priyanshurajpoot/Chat_Caster/releases)**
2. Download the latest `ChatCaster.exe`
3. Run the executable (no installation required)

### GPU Support (Optional)
For faster training, install CUDA-enabled PyTorch:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 📱 Exporting WhatsApp Chats

### On Android:
1. Open WhatsApp and navigate to the desired chat
2. Tap the three dots (⋮) in the top-right corner
3. Select **More** → **Export chat**
4. Choose **Without media**
5. Save the `.txt` file to your computer

### On iOS:
1. Open the chat in WhatsApp
2. Tap the contact/group name at the top
3. Scroll down and tap **Export Chat**
4. Choose **Without Media**
5. Save the file to your computer

---

## 🎯 Usage Guide

### Starting the Application

```bash
python main.py
```

### Training Your AI Model

1. **Navigate to Setup & Training Tab**
   - Click on the "⚙️ Setup & Training" tab in the application

2. **Import Chat History**
   - Click "📁 Import Chat History (.txt)"
   - Select your exported WhatsApp chat file
   - The app will display the number of messages imported

3. **Start Training**
   - Click "🚀 Start Training"
   - Monitor progress through the real-time progress indicators
   - Training typically takes 5-30 minutes depending on:
     - Chat size (number of messages)
     - Hardware (CPU vs GPU)
     - Training parameters

4. **Training Complete**
   - Once finished, the model is automatically saved
   - You're ready to start chatting!

### Chatting with Your AI

1. **Navigate to Chat Tab**
   - Click on the "💬 Chat" tab

2. **Send Messages**
   - Type your message in the input field
   - Press Enter or click "Send" button
   - The AI will generate a response based on your training data

---

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

---

## ⚙️ Configuration

### Model Parameters

Customize training by editing `model_handler.py`:

```python
# Training configuration (lines 75-105)
num_epochs = 3           # Number of training passes
learning_rate = 5e-5     # Learning rate for optimization
batch_size = 4           # Training batch size
max_length = 128         # Maximum sequence length
```

### Generation Parameters

Adjust response generation in `model_handler.py`:

```python
# Response generation settings
temperature = 0.8        # Creativity control (0.1-1.0)
top_k = 50               # Top-K sampling for diversity
top_p = 0.95             # Nucleus sampling threshold
max_length = 100         # Maximum response length
```

---

## 📊 Technical Details

### Model Architecture
- **Base Model**: GPT-2 (124M parameters)
- **Framework**: PyTorch + Hugging Face Transformers
- **Training Method**: Fine-tuning with causal language modeling
- **Tokenizer**: GPT-2 tokenizer with custom vocabulary

### Data Processing Pipeline
1. **Format Detection** - Supports multiple WhatsApp date formats
2. **Message Filtering** - Removes system messages and media notifications
3. **Text Cleaning** - Removes URLs and email addresses
4. **Multi-line Handling** - Properly processes multi-line messages
5. **Tokenization** - Converts text to model-understandable tokens

### Performance Characteristics
- **Training Time**: 5-30 minutes (data and hardware dependent)
- **Memory Usage**: 
  - CPU: ~2-4GB RAM
  - GPU: ~4-6GB VRAM
- **Model Size**: ~500MB on disk after training
- **Inference Speed**: Real-time responses

---

## 🔒 Privacy & Security

### Data Protection
- **Local Processing Only** - No data is sent to external servers
- **Complete Offline Operation** - Works without internet after setup
- **Your Device, Your Data** - All processing happens on your machine
- **No Cloud Dependencies** - Fully functional offline

### Security Features
- No external API calls during training or inference
- Local file system storage only
- No telemetry or data collection
- Transparent data handling

---

## 🐛 Troubleshooting

### Common Issues & Solutions

**"Too few messages found"**
- Ensure your chat export has at least 10 meaningful messages
- Verify the file format is correct (.txt)
- Check that the file contains actual conversation data

**"CUDA out of memory"**
- Reduce batch size in `model_handler.py` (line 86)
- Close other GPU-intensive applications
- The application will automatically fall back to CPU training

**Import Errors**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Ensure Python version is 3.8 or higher
- Check for conflicting package versions

**Model Not Loading**
- Delete the `trained_model/` folder and retrain
- Check `logs/training_log.txt` for detailed error information
- Ensure sufficient disk space for model files

**Training Takes Too Long**
- Use GPU acceleration if available
- Reduce the number of training epochs
- Consider using a smaller chat history for initial testing

---

## 📦 Building Executable

To create a standalone executable:

```bash
pyinstaller --onefile --windowed --name "ChatCaster" main.py
```

The executable will be generated in the `dist/` folder and can be distributed without Python dependencies.

### Build Options
```bash
# For production build with optimizations
pyinstaller --onefile --windowed --name "ChatCaster" --clean --noconfirm main.py

# Include additional data files if needed
pyinstaller --onefile --windowed --add-data "templates;templates" main.py
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Reporting Bugs
1. [Open an issue](https://github.com/Priyanshurajpoot/Chat_Caster/issues) with detailed description
2. Include steps to reproduce the problem
3. Provide system information and error logs

### Suggesting Features
1. Create a feature request with clear use cases
2. Explain the benefits for users
3. Consider implementation complexity

### Development Process
1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

### Development Guidelines
- Follow Python PEP 8 style guide
- Add type hints for better code clarity
- Include docstrings for all functions
- Update documentation for new features
- Test across different environments

---

## ⚠️ Limitations & Considerations

### Current Limitations
- Requires substantial chat history (recommended: 500+ messages for good results)
- AI responses may not always be perfectly coherent or contextually accurate
- Training quality heavily depends on input data diversity and quality
- Generated responses are based on learned patterns, not true understanding
- Limited to text-based conversations (no media support)

### Best Practices
- Use chat exports with diverse conversation topics
- Ensure clean, well-formatted chat data
- Train with conversations that have clear question-answer patterns
- Experiment with different training parameters for optimal results

---

## 📄 License

This project is licensed under the MIT License:

```text
MIT License

Copyright (c) 2024 Chat Caster

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support & Contact

- **🐛 Report Issues**: [GitHub Issues](https://github.com/Priyanshurajpoot/Chat_Caster/issues)
- **🚀 Downloads**: [GitHub Releases](https://github.com/Priyanshurajpoot/Chat_Caster/releases)
- **📧 Email**: priyanshux5xraj@gmail.com
- **👨‍💻 Developer**: [Priyanshu Rajpoot](https://linkedin.com/in/priyanshux5)

---

## 🙏 Acknowledgments

### Technologies Used
- **[Hugging Face Transformers](https://huggingface.co/transformers/)** - GPT-2 implementation and model management
- **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/)** - Modern GUI framework for desktop applications
- **[PyTorch](https://pytorch.org/)** - Deep learning backend and GPU acceleration
- **[WhatsApp](https://www.whatsapp.com/)** - Chat export functionality and data source

### Special Thanks
- The open-source community for continuous inspiration
- Beta testers for valuable feedback and testing
- Contributors who help improve the project
- Users who trust us with their chat data

---

## 🔗 Quick Links

- **📂 Repository**: [Chat Caster on GitHub](https://github.com/Priyanshurajpoot/Chat_Caster.git)
- **🚀 Releases**: [Latest Releases](https://github.com/Priyanshurajpoot/Chat_Caster/releases)
- **🐛 Issues**: [Report Issues](https://github.com/Priyanshurajpoot/Chat_Caster/issues)
- **👨‍💻 Developer**: [Priyanshu Rajpoot](https://linkedin.com/in/priyanshux5)

---

**Python Developer | Prompt Engineer | AI Enthusiast**  
*Creating intelligent applications that learn from your conversations*

---

## AUTHOR
**Priyanshu Rajpoot**  
*MCA Post Graduate | AI Developer | Python Specialist*