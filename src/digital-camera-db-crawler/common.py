import urllib.request

HTML_ENCODING = "utf-8"

def get_html(url):
    f = urllib.request.urlopen(url)
    html = f.read()
    return html.decode(HTML_ENCODING) 

def add_header_to_url(header, url):
    
    if header not in url:
        return header + url
    else:
        return url
