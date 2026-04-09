import re
import base64
import requests
from bs4 import BeautifulSoup


def extract_doc_id(url):
    match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None


def fetch_google_doc(url):
    """Fetch Google Doc as HTML, extract text and images.
    Returns (text, images) where images is a list of {"media_type": ..., "data": base64...}
    """
    doc_id = extract_doc_id(url)
    if not doc_id:
        raise ValueError(f"Could not extract Google Doc ID from URL: {url}")

    # Fetch as HTML to preserve images
    html_url = f"https://docs.google.com/document/d/{doc_id}/export?format=html"
    resp = requests.get(html_url, allow_redirects=True, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract images
    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue
        try:
            if src.startswith("data:"):
                # Inline base64 image
                match = re.match(r"data:(image/\w+);base64,(.+)", src)
                if match:
                    images.append({
                        "media_type": match.group(1),
                        "data": match.group(2),
                    })
            elif src.startswith("http"):
                # External image URL — download it
                img_resp = requests.get(src, timeout=15)
                img_resp.raise_for_status()
                content_type = img_resp.headers.get("Content-Type", "image/png")
                media_type = content_type.split(";")[0].strip()
                if not media_type.startswith("image/"):
                    media_type = "image/png"
                b64 = base64.b64encode(img_resp.content).decode("utf-8")
                images.append({
                    "media_type": media_type,
                    "data": b64,
                })
        except Exception:
            # Skip images that fail to download
            continue

    # Extract plain text
    text = soup.get_text(separator="\n", strip=True)

    return text, images


def fetch_google_doc_text_only(url):
    """Fallback: fetch as plain text (no images)."""
    doc_id = extract_doc_id(url)
    if not doc_id:
        raise ValueError(f"Could not extract Google Doc ID from URL: {url}")

    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
    resp = requests.get(export_url, allow_redirects=True, timeout=30)
    resp.raise_for_status()
    return resp.text, []


def is_google_doc_url(text):
    return bool(re.search(r"docs\.google\.com/document/d/", text.strip()))
