import sys

sys.dont_write_bytecode = True
import os
from core.base import base
from core.info import get_info
from core.task import process_do_task, process_boost_speed
from core.mint import process_mint_worm
from core.game import process_break_egg
from core.upgrade import process_upgrade
from urllib.parse import parse_qs
import time
import json

def read_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as file:
        try:
            config_content = file.read()
            return json.loads(config_content)
        except json.JSONDecodeError as e:
            return {}

def extract_user_name(auth_data: str) -> dict:
    query_params = parse_qs(auth_data)
    user_name = json.loads(query_params['user'][0]).get("username")
    return user_name

config = read_config()

class Birds:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.proxy_file = base.file_path(file_name="proxies.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="Birds")

        # Get config
        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_boost_speed = base.get_config(
            config_file=self.config_file, config_name="auto-boost-speed"
        )

        self.auto_mint_worm = base.get_config(
            config_file=self.config_file, config_name="auto-mint-worm"
        )

        self.auto_break_egg = base.get_config(
            config_file=self.config_file, config_name="auto-break-egg"
        )

        self.auto_upgrade_egg = base.get_config(
            config_file=self.config_file, config_name="auto-upgrade-egg"
        )
        self.cycle_delay = config.get('cycle_delay', 1000)

    def main(self):
        while True:
            accounts = open(self.data_file, "r").read().splitlines()
            proxies = open(self.proxy_file, "r").read().splitlines()
            if len(proxies) < len(accounts):
                proxies.extend([None] * (len(accounts) - len(proxies)))
            else:
                proxies = proxies
            num_acc = len(accounts)
            base.log(self.line)
            base.log(f"{base.green}Numer of accounts: {base.white}{num_acc}")

            for no, (data, proxy_info) in enumerate(zip(accounts, proxies)):
                base.log(self.line)
                user_name = extract_user_name(data)

                base.log(f"{base.green}Account number: {base.white}{no + 1}/{num_acc}")
                base.log(f"{base.green}User name: {base.white}{user_name}")
                if proxy_info:
                    try:
                        base.parse_proxy_info(proxy_info)
                        base.check_ip(proxy_info=proxy_info)
                        proxies = base.format_proxy(proxy_info=proxy_info)
                    except:
                        base.log(f"{base.red}Bad proxy, proxies = None!")
                        proxies = None
                else:
                    base.log(f"{base.red}No proxy used!")
                    proxies = None

                try:
                    get_info(data=data, proxies=proxies)

                    # Do task
                    if self.auto_do_task:
                        base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                        process_do_task(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                    # Boost speed
                    if self.auto_boost_speed:
                        base.log(f"{base.yellow}Auto Boost Speed: {base.green}ON")
                        process_boost_speed(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Boost Speed: {base.red}OFF")

                    # Mint worm
                    if self.auto_mint_worm:
                        base.log(f"{base.yellow}Auto Mint Worm: {base.green}ON")
                        process_mint_worm(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Mint Worm: {base.red}OFF")

                    # Break egg
                    if self.auto_break_egg:
                        base.log(f"{base.yellow}Auto Break Egg: {base.green}ON")
                        process_break_egg(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Break Egg: {base.red}OFF")

                    # Upgrade egg
                    if self.auto_upgrade_egg:
                        base.log(f"{base.yellow}Auto Upgrade Egg: {base.green}ON")
                        process_upgrade(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Upgrade Egg: {base.red}OFF")

                    get_info(data=data, proxies=proxies)

                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            base.log(f"{base.yellow}Wait for {int(self.cycle_delay/1)} seconds!")
            time.sleep(self.cycle_delay)


if __name__ == "__main__":
    try:
        banner = base.create_banner(game_name="Birds")
        base.clear_terminal()
        print(banner)
        birds = Birds()
        birds.main()
    except KeyboardInterrupt:
        sys.exit()
