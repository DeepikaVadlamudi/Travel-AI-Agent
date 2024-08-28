def detect_intent(query):
    supported_keywords = ["how long", "travel time", "bike", "drive", "walk", "transit", "duration", "from", "to"]
    query_lower = query.lower()
    if any(keyword in query_lower for keyword in supported_keywords):
        return 'Travel Duration Query'
    else:
        return 'General Query'