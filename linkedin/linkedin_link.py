"""
Code snippet that creates a link for posting prefilled text on LinkedIn.
Using 
"""
from urllib.parse import urlencode

def create_linkedin_sharing_link(text, url=None):
    base_url = 'https://www.linkedin.com/shareArticle'
    params = {
        'mini': 'true', #makes it device independent
        'text': text,
    }
    if url:
        params['url'] = url
    
    query_string = urlencode(params)
    return f"{base_url}/?{query_string}"

