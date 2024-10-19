def headers(tele_auth=None, auth=None):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://birdx.birds.dog",
        "Referer": "https://birdx.birds.dog/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    if tele_auth:
        headers["Telegramauth"] = f"tma {tele_auth}"

    if auth:
        headers["Authorization"] = f"tma {auth}"

    return headers
