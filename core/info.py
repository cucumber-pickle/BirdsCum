import requests
from core.base import base
from core.headers import headers
import random



def get_info(data, proxies=None):
    url = "https://api.birds.dog/user"
    guild_me = "https://api.birds.dog/guild/me"
    newest_guild = "https://api.birds.dog/guild/list?type=village&filter=newest"

    try:
        guild = requests.get(
            url=guild_me,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        now_guild = guild.json()
        if now_guild:
            base.log(base.green + f'You allredy in guild {base.white}{now_guild.get("guild").get("name")}')
        else:
            newest_guild = requests.get(
                url=newest_guild,
                headers=headers(tele_auth=data),
                proxies=proxies,
                timeout=20,
            )
            new_guilds = newest_guild.json()

            # Extracting _id and name pairs
            id_name_pairs = {item['_id']: item['name'] for item in new_guilds}

            # Randomly selecting one _id
            random_id = random.choice(list(id_name_pairs.keys()))

            # Getting the corresponding name
            corresponding_name = id_name_pairs[random_id]

            join_guild_url = f"https://api.birds.dog/guild/join/{random_id}"
            join_guild = requests.get(
                url=join_guild_url,
                headers=headers(tele_auth=data),
                proxies=proxies,
                timeout=20,
            )
            base.log(base.green + f'You have joined the guild {base.white}{corresponding_name}')

        response = requests.get(
            url=url,
            headers=headers(tele_auth=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        balance = data["balance"]

        base.log(f"{base.green}Balance: {base.white}{balance:,}")

        return data
    except:
        return None