import requests
import time

from core.headers import headers
from core.base import base

def incubate_info(data, proxies=None):
    url = "https://api.birds.dog/minigame/incubate/info"

    try:
        response = requests.get(
            url=url,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        egg_level = data["level"]
        status = data["status"]
        next_level = data.get("nextLevel", None)

        upgraded_at = data["upgradedAt"]
        duration = data["duration"]
        speed = data["speed"]
        end_time = upgraded_at + (duration / speed) * 3600 * 1000

        if next_level:
            base.log(
                f"{base.green}Egg Level: {base.white}{egg_level} - {base.green}Next level available"
            )
        else:
            base.log(f"{base.green}Egg Level: {base.white}{egg_level}")

        return status, next_level, end_time
    except:
        return None, None, None


def incubate_upgrade(data, proxies=None):
    url = "https://api.birds.dog/minigame/incubate/upgrade"

    try:
        response = requests.get(
            url=url,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["status"] == "processing"

        return status
    except:
        return None


def confirm_upgraded(data, proxies=None):
    url = "https://api.birds.dog/minigame/incubate/confirm-upgraded"

    try:
        response = requests.post(
            url=url,
            headers=headers(tele_auth=data),
            json={},
            proxies=proxies,
            timeout=20,
        )
        data = response.text

        return data
    except:
        return None


def process_upgrade(data, proxies=None):
    while True:
        status, next_level, end_time = incubate_info(data=data, proxies=proxies)
        if status == "confirmed":
            if next_level:
                upgrade_status = incubate_upgrade(data=data, proxies=proxies)
                if upgrade_status:
                    base.log(f"{base.white}Auto Upgrade Egg: {base.green}Success")
                else:
                    base.log(
                        f"{base.white}Auto Upgrade Egg: {base.red}Not enough birds to upgrade"
                    )
            else:
                base.log(
                    f"{base.white}Auto Upgrade Egg: {base.yellow}Maximum level reached"
                )
            break
        elif status == "processing":
            current_time = int(time.time() * 1000)
            if current_time >= end_time:
                confirm_upgraded_status = confirm_upgraded(data=data, proxies=proxies)
                if confirm_upgraded_status:
                    base.log(
                        f"{base.white}Auto Upgrade Egg: {base.green}Confirm upgraded"
                    )
                    incubate_info(data=data, proxies=proxies)
            else:
                base.log(
                    f"{base.white}Auto Upgrade Egg: {base.yellow}Egg incubating..."
                )
                break
        else:
            base.log(
                f"{base.white}Auto Upgrade Egg: {base.red}Unknown status {base.white}- {base.yellow}Trying to upgrade..."
            )
            upgrade_status = incubate_upgrade(data=data, proxies=proxies)
            if upgrade_status:
                base.log(f"{base.white}Auto Upgrade Egg: {base.green}Success")
                incubate_info(data=data, proxies=proxies)
            else:
                base.log(
                    f"{base.white}Auto Upgrade Egg: {base.red}Not enough birds to upgrade"
                )
            break
