from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
import logging
from anthropic import Anthropic
from toolhouse import Toolhouse, Provider

load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load API keys from environment variables
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TH_TOKEN = os.getenv("TOOLHOUSE_API_KEY")

# Initialize Anthropic and Toolhouse clients
client = Anthropic(api_key=CLAUDE_API_KEY)
th = Toolhouse(access_token=TH_TOKEN, provider=Provider.ANTHROPIC)

# Set timezone for the AI Agent
th.set_metadata('timezone', '-7')

# Define system message for the AI agent
system_message = """
IMPORTANT: Be extremely concise in all your answers. Keep it to 280 characters.
You are an agent in charge of recommending events happening in the city of the user's liking. Answer the question as faithfully as you can.
Retrieve knowledge using the tools and sources at your disposal and provide the best answer you can.
Your main source of knowledge is this file which you can access by using a web scraper, but only scrape it once: https://lu.ma/CITY_NAME. You need to replace CITY_NAME with the city name the user provides. For example, if the user asks about events in New Delhi, you would scrape https://lu.ma/new-delhi. Show the entire list of events irrespective of the character value given above. If the user inquires further about any of the events you recommended, give all the details you found while scraping earlier or search the web. In case the user asks about events in a city that doesn't exist, you should reply with "Sorry, I couldn't find any events in CITY_NAME with the data I have access to. Would you want me to look for events in another city?".
Only respond with the details of the answer, like a real recommendation tool would do. In case you run into any issues, report the error you are running into.
"""

def serialize_message(message):
    """Convert message to a serializable format."""
    return {
        "role": message.get("role", ""),
        "content": str(message.get("content", ""))
    }

@app.route('/')
def home():
    session['messages'] = []
    session['first_question'] = True
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    messages = session.get('messages', [])
    first_question = session.get('first_question', True)

    if first_question:
        messages.append({"role": "user", "content": f"I am looking for events in {user_input}"})
        session['first_question'] = False
    else:
        messages.append({"role": "user", "content": user_input})

    try:
        # Generate initial response using Anthropic model
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system=system_message,
            tools=th.get_tools(), # If you'd like to use Bundles, pass your Bundle name here. Example: tools=th.get_tools(event_bot)
            messages=messages
        )

        # Run tools based on the response
        tool_messages = th.run_tools(response)
        messages.extend([serialize_message(msg) for msg in tool_messages])

        # Generate final response
        agent_setup = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system=system_message,
            tools=th.get_tools(), # If you'd like to use Bundles, pass your Bundle name here. Example: tools=th.get_tools(event_bot)
            messages=messages
        )
        agent_reply = agent_setup.content[0].text if agent_setup.content else "No response generated."

        messages.append(serialize_message({"role": "assistant", "content": agent_reply}))
        session['messages'] = messages

        return jsonify({'response': agent_reply})

    except Exception as e:
        logging.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({'response': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)