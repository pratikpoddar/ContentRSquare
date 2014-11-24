import requests

def google_suggestions(query):
    url = 'http://suggestqueries.google.com/complete/search?client=firefox&q='+query
    suggestions = requests.get(url).json()[1]
    return suggestions
