import re
from urllib.parse import urlparse, parse_qs

def get_video_id(url: str) -> str | None:
    if not url:
        return None
    url = url.strip()
    
    # Direct 11-char video ID
    if re.fullmatch(r"[a-zA-Z0-9_-]{11}", url):
        return url
        
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    
    # Short URLs: youtu.be/<id>
    if "youtu.be" in hostname:
        path = parsed.path.strip("/")
        return path.split("/")[0] if path else None

    # Standard youtube.com URLs
    if "youtube.com" in hostname:
        if parsed.path == "/watch" or "/watch" in parsed.path:
            v = parse_qs(parsed.query).get("v")
            if v:
                return v[0]
        for prefix in ("/shorts/", "/embed/", "/v/", "/live/"):
            if parsed.path.startswith(prefix):
                return parsed.path[len(prefix):].split("/")[0]
                
    # Fallback regex
    match = re.search(r"(?:v=|\/)([a-zA-Z0-9_-]{11})(?:\?|&|\/|$)", url)
    return match.group(1) if match else None

def format_docs(retrieved):
    context = "\n".join([doc.page_content for doc in retrieved])
    return context