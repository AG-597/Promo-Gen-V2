import time
import random
import requests
from seleniumbase import Driver
from colorama import Fore, Style
import os

gray = Fore.LIGHTBLACK_EX
orange = Fore.LIGHTYELLOW_EX
lightblue = Fore.LIGHTBLUE_EX

class log:
    @staticmethod
    def slog(type, color, message, time):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ] [ {Fore.CYAN}{time:.2f}s{gray} ]"
        print(log.center(msg))
        
    @staticmethod
    def ilog(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]"
        inputmsg = input(log.center(msg) + " ")
        return inputmsg

    @staticmethod
    def log(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]{Style.RESET_ALL}"
        print(log.center(msg))

    @staticmethod
    def success(message, time):
        log.slog('+', Fore.GREEN, message, time)

    @staticmethod
    def fail(message):
        log.log('X', Fore.RED, message)

    @staticmethod
    def warn(message):
        log.log('!', Fore.YELLOW, message)

    @staticmethod
    def info(message):
        log.log('i', lightblue, message)
        
    @staticmethod
    def input(message):
        return log.ilog('i', lightblue, message)

    @staticmethod
    def working(message):
        log.log('-', orange, message)

    @staticmethod
    def center(text):
        terminal_size = os.get_terminal_size().columns
        return text.center(terminal_size)

def getMail():
    return f'{random.randint(0, 999999999)}@xitroo.com'

def getUser():
    try:
        with open('usernames.txt', 'r') as f:
            names = f.readlines()
        return random.choice(names).strip()
    except Exception as e:
        log.fail(f"Unable To Get Username --> {str(e)}")


def run():
    st = time.time()
    try:
        username = getUser()
        email = getMail()

        page = Driver(headless2=True)
        page.get('https://www.chess.com/register')

        page.click('main > div > div > button[type="button"]')
        page.click('form > div:nth-child(1) > button[type="button"]') 
        page.type("input#registration_email", email)
        page.type("input#registration_password", "JustANugget11!")
        page.click('div:nth-child(6) > button[type="button"]')
        page.type("input#registration_username", username)
        page.click('div.username-wrap > button[type="button"]')

        while page.current_url != 'https://www.chess.com/onboarding/1?returnUrl=https://www.chess.com/home':
            time.sleep(0.1)
        log.info(f"Successfuly Registered --> {username}")
        page.get("https://www.chess.com/onboarding/1?returnUrl=https://www.chess.com/home")

        cookies = page.get_cookies()    
        page.quit()

        CNames = ['PHPSESSID', 'visitorid', 'me', 'osano_consentmanager_uuid', 'pbjs_fabrickId',
                        'pbjs_fabrickId_cst', 'cdn.chesscom.850100.ka.ck', '_sharedid', '_sharedid_cst',
                        'hb_insticator_uid', '__cf_bm', 'experiments', 'GCLB', 'theme_cache_id',
                        '__gads', '__gpi', '__eoi', 'TAPAD', 'asset_push', 'cto_bidid', 'cto_bundle',
                        'psid', 'amp_5cc41a']

        extCok = {name: next((cookie['value'] for cookie in cookies if cookie['name'] == name), None)
                             for name in CNames}

        userid = extCok['theme_cache_id'].split(":")[1] if extCok['theme_cache_id'] else None

        if userid:
            jData = {
                'userUuid': userid,
                'campaignId': '4daf403e-66eb-11ef-96ab-ad0a069940ce',
            }

            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/json',
                'dnt': '1',
                'origin': 'https://www.chess.com',
                'referer': 'https://www.chess.com/play/computer',
                'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            }

            response = requests.post(
                'https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode',
                cookies=extCok,
                headers=headers,
                json=jData,
            )

            code = response.json()['codeValue']
            promo = f"https://promos.discord.gg/{code}"
            log.success(f"Successfuly Got Promo --> {promo[:31]}...", round(time.time()-st,2))
            with open("promos.txt", 'a') as f:
                f.write(f"\n{promo}")
        else:
            log.fail(f"Unable To Retrieve User ID")
    except Exception as e:
        log.fail(f"Error --> {str(e)}")
while True:
    run()
