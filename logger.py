import threading
import time
import zlib
import brotli
import hashlib
from mitmproxy import http

log_queue = []
stop_flag = False

def short_id(s):
    return hashlib.sha1(s).hexdigest()[:8]

def decompress(content, encoding):
    try:
        if encoding == "gzip":
            return zlib.decompress(content, 16+zlib.MAX_WBITS)
        elif encoding == "deflate":
            return zlib.decompress(content)
        elif encoding == "br":
            return brotli.decompress(content)
        else:
            return content
    except:
        return content

def looks_like_text(data):
    try:
        data.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

def background_writer():
    with open("proxniff.txt", "a") as f:
        while not stop_flag or log_queue:
            if log_queue:
                item = log_queue.pop(0)
                kind, url, headers, body, encoding, req_id = item
                body = decompress(body, encoding)
                if looks_like_text(body):
                    body_str = body.decode(errors='replace')
                else:
                    body_str = f"BINARY CONTENT <{len(body)} BYTES>"
                msg = f"\n--- {kind} [{url}] ID:{req_id} ---\n{headers}\n\n{body_str}\n"
                f.write(msg)
            else:
                time.sleep(0.01)

threading.Thread(target=background_writer, daemon=True).start()

def request(flow: http.HTTPFlow):
    req = flow.request
    headers = "\n".join(f"{k}: {v}" for k, v in req.headers.items())
    raw_for_id = (req.method + req.url + headers).encode()
    req_id = short_id(raw_for_id)
    flow.metadata["log_id"] = req_id

    log_queue.append((
        "REQUEST", 
        f"{req.method} {req.url}",
        headers,
        req.raw_content or b"",
        req.headers.get("Content-Encoding", "").lower(),
        req_id
    ))

def response(flow: http.HTTPFlow):
    resp = flow.response
    headers = "\n".join(f"{k}: {v}" for k, v in resp.headers.items())
    req_id = flow.metadata.get("log_id", "unknown")

    log_queue.append((
        "RESPONSE", 
        flow.request.url,
        headers,
        resp.raw_content or b"",
        resp.headers.get("Content-Encoding", "").lower(),
        req_id
    ))
