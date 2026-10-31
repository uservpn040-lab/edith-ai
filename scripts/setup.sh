#!/bin/bash
echo "Setting up EDITH..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo ""
echo "Done! Now run: ollama pull llama3.2:1b"
echo "Then: python main.py"
