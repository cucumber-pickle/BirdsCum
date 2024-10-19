import requests
from core.base import base
from core.headers import headers


def get_task(data, proxies=None):
    url = "https://api.birds.dog/project"

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


def do_task(data, task_id, channel_id, slug, point, proxies=None):
    url = "https://api.birds.dog/project/join-task"
    payload = {"taskId": task_id, "channelId": channel_id, "slug": slug, "point": point}

    try:
        response = requests.post(
            url=url,
            headers=headers(tele_auth=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["msg"] == "Successfully"

        return status
    except:
        return None


def check_completed_task(data, proxies=None):
    url = "https://api.birds.dog/user-join-task"

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


def process_do_task(data, proxies=None):
    task_group = get_task(data=data, proxies=proxies)
    completed_tasks = check_completed_task(data=data, proxies=proxies)
    for group in task_group:
        group_name = group["name"]
        task_list = group["tasks"]

        base.log(f"{base.white}Group: {base.yellow}{group_name}")

        for task in task_list:
            task_id = task["_id"]
            task_name = task["title"]
            channel_id = task["channelId"]
            slug = task["slug"]
            point = task["point"]

            task_exists = any(item["taskId"] == task_id for item in completed_tasks)

            if task_exists:
                base.log(f"{base.white}{task_name}: {base.green}Completed")
            else:
                do_task_status = do_task(
                    data=data,
                    task_id=task_id,
                    channel_id=channel_id,
                    slug=slug,
                    point=point,
                    proxies=proxies,
                )

                if do_task_status:
                    base.log(f"{base.white}{task_name}: {base.green}Completed")
                else:
                    base.log(f"{base.white}{task_name}: {base.red}Incomplete")


def boost_speed(data, proxies=None):
    url = "https://api.birds.dog/minigame/boost-speed"

    try:
        response = requests.get(
            url=url,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        speed = data["speed"]

        return speed
    except:
        return None


def update_speed(data, speed, proxies=None):
    url = "https://api.birds.dog/minigame/boost-speed/update-speed"
    payload = {"speed": speed}

    try:
        response = requests.post(
            url=url,
            headers=headers(tele_auth=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["msg"] == "Successfully"

        return status
    except:
        return None


def process_boost_speed(data, proxies=None):
    speed_list = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.5]
    current_speed = boost_speed(data=data, proxies=proxies)
    next_speed = (
        speed_list[speed_list.index(current_speed) + 1]
        if current_speed in speed_list and current_speed != speed_list[-1]
        else None
    )
    if next_speed:
        base.log(
            f"{base.green}Current Speed: {base.white}x {current_speed} - {base.green}Next Speed: {base.white}x {next_speed}"
        )
        update_speed_status = update_speed(data=data, speed=next_speed, proxies=proxies)
        if update_speed_status:
            base.log(f"{base.white}Auto Boost Speed: {base.green}Success")
        else:
            base.log(f"{base.white}Auto Boost Speed: {base.red}Requirement not meet")
    else:
        base.log(
            f"{base.green}Current Speed: {base.white}x {current_speed} - {base.green}Max speed reached"
        )
