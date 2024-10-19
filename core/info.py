import requests
from core.base import base
from core.headers import headers


def get_info(data, proxies=None):
    url = "https://api.birds.dog/user"

    try:
        response = requests.get(
            url=url,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        balance = data["balance"]

        print(f"{base.green}Balance: {base.white}{balance:,}")

        return data
    except:
        return None
