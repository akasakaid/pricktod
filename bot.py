import os
import sys
import json
import time
import random
import requests
from colorama import *
from websocket import WebSocket
from datetime import datetime

init(autoreset=True)

merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
hitam = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL
putih = Fore.LIGHTWHITE_EX


class PrickTod:
    def __init__(self):
        self.DEFAULT_COUNTDOWN = 30 * 60

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {message}")

    def active_refill_energy(self, id, ua):
        url = "https://api.prick.lol/v1/boost/energy-regeneration"
        headers = {
            "Accept-Language": "en,en-US;q=0.9",
            "authorization": f"Bearer {id}",
            "User-Agent": ua,
            "X-Requested-With": "org.telegram.messenger",
        }
        res = requests.put(url, headers=headers)
        open(".http_logs.log", "a").write(res.text + "\n")
        free_refill_left = res.json()["result"]["freeEnergyRegeneration"]
        refill_energy = res.json()["result"]["energy"]
        return refill_energy, free_refill_left

    def active_turbo(self, id, ua):
        url = "https://api.prick.lol/v1/boost/turbo"
        headers = {
            "Accept-Language": "en,en-US;q=0.9",
            "authorization": f"Bearer {id}",
            "User-Agent": ua,
            "X-Requested-With": "org.telegram.messenger",
        }
        res = requests.put(url, headers=headers)
        open(".http_logs.log", "a").write(res.text + "\n")
        end_free_turbo = res.json()["result"]["turboEndedAt"].replace("Z", "")
        free_turbo_left = res.json()["result"]["freeTurbo"]
        end_format = round(datetime.fromisoformat(end_free_turbo).timestamp())
        return free_turbo_left, end_format

    def game(self, id):
        list_useragent = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.2535.67",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux i686; rv:126.0) Gecko/20100101 Firefox/126.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/125.0.6422.80 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 EdgiOS/125.2535.60 Mobile/15E148 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.113 Mobile Safari/537.36 EdgA/124.0.2478.104",
            "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.113 Mobile Safari/537.36 EdgA/124.0.2478.104",
            "Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.113 Mobile Safari/537.36 OPR/76.2.4027.73374",
            "Mozilla/5.0 (Linux; Android 10; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.113 Mobile Safari/537.36 OPR/76.2.4027.73374",
        ]
        user_agent = random.choice(list_useragent)
        headers = {
            "User-Agent": user_agent,
            "Sec-WebSocket-Protocol": str(id),
        }
        ws = WebSocket()
        ws.connect("wss://api.prick.lol/ws", header=headers)
        self.log(f"{hijau}connect to wss server !")
        res = ws.recv()
        open(".wss_logs.log", "a",encoding="utf-8").write(res + "\n")
        if '"action":null' in res:
            self.log(f"{merah}id is invalid !")
            return

        data_res = json.loads(res)
        first_name = data_res["data"]["firstName"]
        last_name = data_res["data"]["lastName"]
        balance = data_res["data"]["balance"]
        energy = data_res["data"]["energy"]
        is_blocked = data_res["data"]["isBlocked"]
        free_energy_refill = data_res["data"]["freeEnergyRegeneration"]
        free_turbo = data_res["data"]["freeTurbo"]
        is_turbo = False
        start_turbo = 0
        self.log(f"{hijau}login as : {putih}{first_name} {last_name}")
        self.log(f"{putih}balance : {hijau}{balance}")
        self.log(f"{putih}energy : {hijau}{energy}")
        self.log(f"{putih}free refill energy : {hijau}{free_energy_refill}")
        self.log(f"{putih}free turbo : {hijau}{free_turbo}")
        self.log(f"{hijau}is block ? {putih}{is_blocked}")

        while True:
            if energy == 0:
                return

            if free_turbo > 0:
                if is_turbo is False:
                    free_turbo, end_turbo = self.active_turbo(id, user_agent)
                    self.log(f"{hijau}active turbo successfully !")
                    start_turbo = int(time.time())
                    is_turbo = True

                if (int(time.time()) - start_turbo) >= 60:
                    is_turbo = False
                    start_turbo = 0

            taps = random.randint(12, 20)
            if (taps * 50) > energy:
                taps = int(energy / 50)

            list_taps = [round(time.time() * 1000) for _ in range(taps)]
            data = {"action": "tap", "data": list_taps}
            ws.send(json.dumps(data))
            for i in range(2):
                res = ws.recv()
                open(".wss_logs.log", "a",encoding="utf-8").write(res + "\n")
                data_res = json.loads(res)
                if data_res["action"] == "energy_recovery":
                    _energy = data_res["energy"]
                    self.log(f"{hijau}energy {putih}+{_energy}")
                    continue

                if data_res["action"] == "result-tap":
                    balance = data_res["balance"]
                    energy = data_res["energy"]
                    self.log(f"{hijau}taps : {putih}{taps}")
                    self.log(f"{hijau}balance : {putih}{balance}")
                    self.log(f"{hijau}energy remaining : {putih}{energy}")
                    if is_turbo:
                        self.countdown(3)
                    else:
                        self.countdown(10)
                    break

            if energy <= 100 and free_energy_refill > 0:
                energy, free_energy_refill = self.active_refill_energy(id, user_agent)
                self.log(f"{hijau}refill energy successfully !")
                continue

    def main(self):
        banner = f"""
    {putih}AUTO TAP FOR {hijau}PRICK BOT 
    
    {hijau}By: {putih}t.me/AkasakaID
    {putih}Github: {hijau}@AkasakaID
        """
        arg = sys.argv
        if "noclear" not in arg:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)

        ids = open("id.txt", "r").read().splitlines()
        self.log(f"{hijau}account detected : {putih}{len(ids)}")
        print(f"{putih}~" * 50)
        while True:
            start = int(time.time())
            for no, id in enumerate(ids):
                self.log(f"{hijau}account number : {putih}{no + 1}")
                self.game(id)
                print("~" * 50)

            end = int(time.time())
            total = end - start
            if total > self.DEFAULT_COUNTDOWN:
                continue

            if len(ids) > 1:
                countdown = self.DEFAULT_COUNTDOWN - total
                self.countdown(countdown)
                continue

            self.countdown(self.DEFAULT_COUNTDOWN)


if __name__ == "__main__":
    try:
        app = PrickTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
