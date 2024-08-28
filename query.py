import openai
import json
from metadata import find_place, calc_time_of_day, weather, decide_mode
from config import client

def parse_query(query):
    prompt = (
        f"Extract the origin, destination, and mode of transport from the following query:\n\n"
        f"\"{query}\"\n\n"
        f"If no specific mode of transport is mentioned, return Null value for mode.\n"
        f"Provide the output in JSON format like this:\n"
        f"{{\"origin\": \"...\", \"destination\": \"...\", \"mode\": \"...\"}}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0
        )

        message_content = response.choices[0].message.content.strip()
        data = json.loads(message_content)
        
        origin = data.get('origin')
        destination = data.get('destination')
        mode = data.get('mode')
        # except json.JSONDecodeError:
        #     print(f"Error parsing JSON response: {message_content}")
        #     return None, None, None


        origin_location, resolved_origin = find_place(origin)
        destination_location, resolved_destination = find_place(destination, near_location=origin_location)

        if not mode:
            distance = 5  # Example distance in kilometers
            time_of_day = calc_time_of_day(origin_location['lat'],origin_location['lng'] )
            weather_main, weather_desc, temp = weather(origin_location['lat'], origin_location['lng'])
            print(time_of_day)
            mode = decide_mode(distance, time_of_day)

        # mode_mapping = {
        #     'driving': 'driving',
        #     'bicycling': 'bicycling',
        #     'biking': 'bicycling',
        #     'walking': 'walking',
        #     'transit': 'transit',
        #     'subway' : 'transit',
        #     'metro':'transit',
        #     'car': 'driving',
        #     'train': 'transit'
        # }

        # mode_key = mode_mapping.get(mode.lower())

        print(f"Origin: {resolved_origin}")
        print(f"Destination: {resolved_destination}")
        print(f"Mode: {mode}")

        if not origin_location or not destination_location:
            return None, None, None, None, None
        
        return mode, origin, origin_location, resolved_origin, destination, destination_location, resolved_destination
    
    except openai.RateLimitError:
        print("Rate limit exceeded. Please try again later.")
        return None, None, None, None, None, None, None
    
    except Exception as e:
        print(f"Error parsing query with GPT: {e}")
        return None, None, None, None, None, None, None