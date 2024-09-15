import platform
import shutil
from colorama import Fore
import requests
import random
from faker import Faker
import time
from modules.__LOG__ import log
from concurrent.futures import ThreadPoolExecutor
import random
import os

def __LOGO__():
    logo = """
   _____            _               
  / ____|          | |              
 | |    _   _ _ __ | |__   ___ _ __ 
 | |   | | | | '_ \| '_ \ / _ \ '__|
 | |___| |_| | |_) | | | |  __/ |   
  \_____\__, | .__/|_| |_|\___|_|   
         __/ | |                    
        |___/|_|                    
        
        [+] discord.gg/csolve
        [+] t.me/csolver
        [+] csolver.xyz       
                             
    """
    
    width = shutil.get_terminal_size().columns
    lines = logo.split('\n')
    banner = '\n'.join(line.center(width) for line in lines)
    print(Fore.CYAN + banner)

def __NAME__():
    return (Faker().first_name()+Faker().last_name()).lower()

def __CLS__():
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def __PROXY__():
    with open('./data/proxies.txt','r') as f:
        proxies = f.read().splitlines()
        
    return random.choice(proxies)

def __UUID__():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "referer": "https://www.chess.com/friends?name=csolver.xyz",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
    r = requests.get(f"https://www.chess.com/member/{__NAME__()}", headers=headers)
    try:
      uuid = r.text.split('data-user-uuid="')[1].split('"')[0]
      log.info(f"Genning Promo --> {uuid[:15]}...")
      return uuid
    except:
      return None

def __GEN__():
    while True:
        proxy = __PROXY__()
        st = time.time()
        proxies={
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        uuid = __UUID__()
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.chess.com",
            "priority": "u=1, i",
            "referer": "https://www.chess.com/play/computer/discord-wumpus?utm_source=partnership&utm_medium=article&utm_campaign=discord2024_bot",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }
        jData = {
            "userUuid": uuid,
            "campaignId": "4daf403e-66eb-11ef-96ab-ad0a069940ce",
        }
        r = requests.post(
            "https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode",
            headers=headers,
            json=jData,
            proxies=proxies
        )
        try:
            code = r.json()["codeValue"]
            promo = f'https://promos.discord.gg/{code}'
            
            log.success(f"Got Promo --> {promo}", round(time.time()-st,2))
            
            with open('./output/promos.txt','a') as f:
                f.write(f'\n{promo}')
        except Exception as e:
            pass

def __MAIN__():
    __CLS__()
    __LOGO__()
    promos = int(log.input(f"Promos --> "))
    for _ in range(promos):
        with ThreadPoolExecutor(max_workers=promos) as exc:
            exc.submit(__GEN__)
        
if __name__ == '__main__':
    __MAIN__()
    
