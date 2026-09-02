from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    return parse_qs(urlparse(url).query).get("v", [None])[0]

def format_docs(retrieved):
    context = "\n".join([doc.page_content for doc in retrieved])
    return context