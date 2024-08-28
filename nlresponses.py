from config import client


def nl_response(lead):
    test_prompt = lead
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": test_prompt},
            ],
            max_tokens=100,
            temperature=0.9,
        )
        print(response)
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error parsing query with GPT: {e}")
        return "I'm sorry, I couldn't process your request at the moment. Please try again later."

def generic_response(query):
    prompt = (
        f"Say that this isnt your area of expertise but you have some information about the query:\n\n"
        f"\"{query}\"\n\n"
        f"Say a thing or two about the query. Limit response to 20 words only")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error parsing query with GPT: {e}")
        return "I'm sorry, I couldn't process your request at the moment. Please try again later."
