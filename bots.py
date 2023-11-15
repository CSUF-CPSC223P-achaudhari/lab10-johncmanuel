import threading
import time
import json

def load_inventory() -> dict[str, list]:
    with open("inventory.dat") as f:
        inventory = json.load(f)
        return inventory
    
def bot_clerk(items: list):
    cart = []
    lock = threading.Lock()
    threads = []
    maxFetchers = 3
    fetchers = {fetcher: [] for fetcher in range(1, maxFetchers+1)}
    
    i = 1
    for item in items:
        if i == maxFetchers+1: i = 1
        fetchers[i].append(item)
        i += 1
    
    for f in fetchers:
        t = threading.Thread(target=bot_fetcher, args=(fetchers[f], cart, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return cart    

def bot_fetcher(items: list[str], cart: list[list], lock: threading.Lock):
    inventory = load_inventory()
    for item_num in items:
        item = inventory[item_num]
        name, seconds = item[0], item[1]
        time.sleep(seconds)
        cart.append([item_num, name])
