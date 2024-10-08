# Travel-AI-Agent

A travel agent that answers questions about the current travel duration between two locations for a mode of transport of the user’s choosing. It is a Flask-based web application that integrates voice recognition, OpenAI's GPT-4, Weather APIs, and Google APIs.

## Features
- Voice recognition for user input
- Interaction with Google Maps and Weather APIs
- Integration with OpenAI GPT-4 for natural language understanding
- Storage and retrieval of recent searches
- Text responses

## Requirements
- Python 3.8 or later
- Flask
- OpenAI Python client
- Google Maps API
- OpenWeatherMap API
- SpeechRecognition
- gTTS
- playsound
- dotenv

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/DeepikaVadlamudi/Travel-AI-Agent.git
    ```
2. Create and activate virtual environment by running the following commands: (using Mac)
   

   ``` bash
   python3 -m venv venv
   ```

   ```bash
   source venv/bin/activate
   ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up your environment variables:
    - Create a `.env` file in the root directory with the following content:
      ```
      OPENAI_API_KEY=your_openai_api_key
      GOOGLE_MAPS_API_KEY=your_google_maps_api_key
      WEATHER_API_KEY=your_weather_api_key
      ```

## Running the Application

1. Run the app:
    ```bash
    python views.py
    ```

2. Access the application via `http://127.0.0.1:5000/`.

## Usage

- Use the input field to type your query.
- Click "Get Directions" to get responses.
- Use the "Speak" button to provide voice commands.

