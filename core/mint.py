import requests

from core.base import base
from core.headers import headers


def mint_status(data, proxies=None):
    url = "https://worm.birds.dog/worms/mint-status"

    try:
        response = requests.get(
            url=url,
            headers=headers(auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["data"]["status"]

        return status
    except:
        return None


def mint(data, proxies=None):
    url = "https://worm.birds.dog/worms/mint"

    try:
        response = requests.post(
            url=url,
            headers=headers(auth=data),
            json={},
            proxies=proxies,
            timeout=20,
        )
        data = response.json()

        return data
    except:
        return None


def process_mint_worm(data, proxies=None):
    status = mint_status(data=data, proxies=proxies)
    if status == "MINT_OPEN":
        start_mint_worm = mint(data=data, proxies=proxies)
        mint_worm_status = start_mint_worm["message"] == "SUCCESS"
        if mint_worm_status:
            worm_type = start_mint_worm["minted"]["type"]
            energy = start_mint_worm["minted"]["reward"]
            base.log(
                f"{base.white}Auto Mint Worm: {base.green}Success {base.white}| {base.green}Worm type: {base.white}{worm_type} - {base.green}Energy: {base.white}{energy}"
            )
        else:
            base.log(f"{base.white}Auto Mint Worm: {base.red}Fail")
    elif status == "WAITING":
        base.log(f"{base.white}Auto Mint Worm: {base.red}Not time to mint")
    else:
        base.log(f"{base.white}Auto Mint Worm: {base.red}Unknown status - {status}")
