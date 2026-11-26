# Day 4 – Streaming LLM Chatbot

A Python CLI chatbot built using the Anthropic Messages API.

## Features
- Streaming responses
- Conversation history
- Token usage tracking
- Estimated API cost logging
- Environment-based API key management
- API retry configuration

## Technologies
- Python
- Anthropic API
- python-dotenv

## Project Files
- `chat.py` – Main streaming chatbot
- `hello.py` – Hello-world API example
- `cost_log.csv` – Token and cost log
- `.gitignore` – Protects sensitive files
- `requirements.txt` – Dependencies

## Run
Install dependencies:

`pip install -r requirements.txt`

Add your Anthropic API key to `.env`, then run:

`python chat.py`

Note: Live API testing is pending due to insufficient API credits.
