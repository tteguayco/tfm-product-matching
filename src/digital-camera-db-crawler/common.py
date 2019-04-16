import urllib.request

HTML_ENCODING = "utf-8"

def get_html(url):
    f = urllib.request.urlopen(url)
    html = f.read()
    html = html.decode(HTML_ENCODING)
    html = html.replace("\n", " ")
    html = html.replace("\t", " ")
    return html

def add_header_to_url(header, url):
    
    if header not in url:
        return header + url
    else:
        return url
