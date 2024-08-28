from flask import render_template, request
from flask import Flask

from dotenv import load_dotenv
from speak import listen, speak
from intent import detect_intent
from duration import calc_duration
from nlresponses import nl_response, generic_response
from db import add_search, recent_searches, init_db
from query import parse_query



load_dotenv()


app = Flask(__name__)

@app.route('/test-route')
def test_route():
    print("Test route accessed")
    return "Test route is working!"

# from . import create_app

# app = create_app()
print("creating app")

@app.route('/', methods=['GET', 'POST'])
def index():
    print("in index")
    response = None
    if request.method == 'POST':
        query = request.form.get('query')

        if 'voice' in request.form:
            query = listen()
            if not query:
                response = "Sorry, I didn't catch that. Please try again."

        if query:
            intent = detect_intent(query)
            if intent == 'Travel Duration Query':
                mode, origin, origin_location, resolved_origin, destination, destination_location, resolved_destination = parse_query(query)
                if origin and destination:
                    duration = calc_duration(origin_location, destination_location, mode)
                    if resolved_origin and resolved_destination:
                        if resolved_origin.lower() == resolved_destination.lower():
                            response = nl_response(f"The origin and destination are the same location: {resolved_origin}. Generate a friendly response indicating no travel is needed.")
                        else:
                            response = nl_response(f"Generate a natural language response stating the {duration} it will take to reach {resolved_destination} from {resolved_origin} by {mode}. Give a short notice about the weather too. Keep it friendly, short, concise, limit to 20 words. Maybe include something about the destination or the route but limit 20 words only. Dont start with sure thing.")
                            add_search(resolved_origin, resolved_destination, mode, duration)
                    else:
                        response = nl_response(f"generate a natural language response that you couldn't retrieve the travel duration for the request.")
                else:
                    response = nl_response(f"generate a natural language response stating that you couldn't understand the origin or destination.")
            else:
                response = generic_response(query)
        
        if 'voice' in request.form:
            speak(response)
        
    history = recent_searches()
    return render_template('index.html', response=response, history=history)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)