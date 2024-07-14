## Run in this linear order

## Setup virtual environment
python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

## Run the app
streamlit run main.py

## How to use the app

1. Train Classifier - to train the initial model
2. Submit a Ticket - to submit an IT ticket
3. Chat with IT support - to get immediate answers
4. Generate insights - to get a report of the existing tickets