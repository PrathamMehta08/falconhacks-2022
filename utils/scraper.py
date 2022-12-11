import __main__
import requests, re, random, json, urllib.parse, inspect, time, hashlib

fallback_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

#download a list of random user-agent strings
def scrape_user_agents():
    headers = {
        "user-agent": fallback_user_agent,
        "referer": "https://user-agents.net/browsers/chrome"
    }
    url = "https://user-agents.net"
    regex = r"<a href='/string/.*?'>(.*?)</a>"
    html = requests.get(url, headers=headers).text

    matches = re.findall(regex, html)
    return matches

#get location of ip
def get_ip_info(ip=None):
    if ip == None:
        url = "https://ipinfo.io/json"
    else:
        url = f"https://ipinfo.io/{ip}/json"
    return requests.get(url).json()

#returns the url to be used with get_location
def get_urls(query, latitude=0, longitude=0, page_size=5, user_agent=fallback_user_agent):
    headers = {
        "user-agent": user_agent,
        "referer": "https://www.forrentuniversity.com/"
    }
    url = f"https://www.forrentuniversity.com/bff/autocomplete/suggestions?query={query}&latitude={latitude}&longitude={longitude}&pagesize={page_size}"
    return requests.get(url, headers=headers).json()

#get listings for a collage/city
def get_location(path, user_agent=fallback_user_agent, page=None, purge_cache=0):
    if page != None:
        path += "/page-"+str(page)

    locations_db = __main__.locations
    cached = locations_db.find_one({"path": path})

    if not purge_cache and cached and time.time() - cached["data"]["request_time"] < 3600:
        print("request was cached")
        return cached["data"]
    else:
        headers = {
            "user-agent": user_agent,
            "referer": "https://www.forrentuniversity.com"+path
        }
        url = "https://www.forrentuniversity.com"+path

        regex = r'<script type="application/ld\+json">([\S\s]*?)</script>'
        regex2 = r'<script id="fru-state" type="application/json">(.*?)</script>'

        html = requests.get(url, headers=headers).text

        data = json.loads(re.findall(regex, html)[0])
        data_full = urllib.parse.unquote_plus(re.findall(regex2, html)[0])
        data_full = data_full.replace("&q;", '"')
        data_full = json.loads(data_full)
        data["full"] = data_full

        regex3 = "G\.http://www\.forrentuniversity\.com/bff/(.*?)\?.+"
        for key in list(data_full.keys()):
            if re.fullmatch(regex3, key):
                new_key = re.findall(regex3, key)[0]
                data_full[new_key] = data_full[key]["body"]["data"]
                del data_full[key]

        for listing in data_full["listing/search/list"]:
            id_hash = hashlib.sha256(listing["siteId"].encode()).hexdigest()
            listing["id"] = id_hash
            listing["request_time"] = time.time()
            listing["type"] = "appartments.com"

        data["request_time"] = time.time()
        locations_db.update_one({"path": path}, {"$set": {"path": path, "data": data}}, upsert=True)

        return data

def get_listing(id, user_agent=fallback_user_agent, purge_cache=0):
    listings_db = __main__.properties
    id_hash = hashlib.sha256(id.encode()).hexdigest()
    cached = listings_db.find_one({"id": id_hash})

    if not purge_cache and cached and time.time() - cached["data"]["request_time"] < 3600:
        print("request was cached")
        return cached["data"]
    else:
        headers = {
            "user-agent": user_agent,
            "referer": "https://www.forrentuniversity.com"
        }
        url = "https://www.forrentuniversity.com/bff/listing/"+id
        listing = requests.get(url, headers=headers).json()["data"]

        id_hash = hashlib.sha256(listing["siteId"].encode()).hexdigest()
        listing["id"] = id_hash
        listing["request_time"] = time.time()
        listing["type"] = "appartments.com"
        listings_db.update_one({"id": id_hash}, {"$set": {"id": id_hash, "data": listing, "type": "appartments.com"}}, upsert=True)

        return listing