import requests
from core.base import base
from core.headers import headers
import time


def join(data, proxies=None):
    url = "https://api.birds.dog/minigame/egg/join"

    try:
        response = requests.get(
            url=url,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()

        return data
    except:
        return None


def turn(data, proxies=None):
    url = "https://api.birds.dog/minigame/egg/turn"

    try:
        response = requests.get(
            url=url,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()

        return data
    except:
        return None


def play(data, proxies=None):
    url = "https://api.birds.dog/minigame/egg/play"

    try:
        response = requests.get(
            url=url,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()

        return data
    except:
        return None


def claim(data, proxies=None):
    url = "https://api.birds.dog/minigame/egg/claim"

    try:
        response = requests.get(
            url=url,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.text

        return data
    except:
        return None


def process_break_egg(data, proxies=None):
    retries = 0
    while True:
        start_join = join(data=data, proxies=proxies)
        get_turn = turn(data=data, proxies=proxies)
        turns = get_turn["turn"]
        total = get_turn["total"]
        if turns > 0:
            start_play = play(data=data, proxies=proxies)
            if start_play:
                result = start_play.get("result", None)
                if result:
                    base.log(
                        f"{base.white}Auto Break Egg: {base.green}Play Success {base.white}| {base.green}Reward: {base.white}{result}"
                    )
                else:
                    base.log(f"{base.white}Auto Break Egg: {base.red}Play Fail")
            else:
                retries += 1
                if retries > 5:
                    base.log(
                        f"{base.white}Auto Break Egg: {base.red}Maximum retries reached"
                    )
                    break
                base.log(
                    f"{base.white}Auto Break Egg: {base.red}CloudFlare Protected - Retry after 10s: {retries}"
                )
                time.sleep(10)
        elif total > 0:
            start_claim = claim(data=data, proxies=proxies)
            if start_claim:
                base.log(
                    f"{base.white}Auto Break Egg: {base.green}Claim Success | Added {total} points"
                )
            else:
                base.log(f"{base.white}Auto Break Egg: {base.red}Claim Fail")
            break
        else:
            base.log(f"{base.white}Auto Break Egg: {base.red}No turn to crack egg")
            break
