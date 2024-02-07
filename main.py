import os; os.system("cls" if os.name == "nt" else "clear")
try:
    import requests
    import time
except ModuleNotFoundError:
    if input(f"\x1b[38;5;2mInstall required modules?(Y/n)").lower() == "y":
        os.system("pip install requests");os.system("python -m pip install requests");os.system("py -m pip install requests")
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\x1b[38;5;2mSucces. Reopen the program...")
    else:
        input("Installing modules denied. Prees \"enter\" to close the program")
        exit()

def check_for_txts() -> str:
    if not os.path.exists("cookie.txt"):
        with open("cookie.txt", "w", encoding="utf-8") as cookie:
            cookie.write("")
        input(f"\x1b[38;5;1mParse into \"cookie.txt\" your cookie.")
        exit()
    else:
        cookie = open("cookie.txt", "r").read()

    if not os.path.exists("id.txt"):
        with open("id.txt", "w", encoding="utf-8") as ItemFIleId:
            ItemFIleId.write("")
        input(f"\x1b[38;5;1mParse into \"id.txt\" your id.")
        exit()
    else:
        itemID = open("id.txt", "r").read()
    return cookie, itemID

def purchase(cookie: str, itemID: str) -> object:
    session = requests.Session()
    session.cookies.update({".ROBLOSECURITY": cookie})

    req = session.post("https://auth.roblox.com/v2/login")
    csrf_token = req.headers["x-csrf-token"] 

    product = session.post("https://catalog.roblox.com/v1/catalog/items/details", headers={"x-csrf-token": csrf_token}, json={"items": [{"itemType": "1", "id": itemID}]}).json().get("data")

    if product != []and itemID.isdigit():
        price = product[0].get("price", "")
        productId = product[0].get("productId", "")
        assetName = product[0].get("name", "")
        req = session.post(f"https://economy.roblox.com/v1/purchases/products/{str(productId)}", json={"expectedCurrency": 1, "expectedPrice": int(price), "expectedSellerId": 1}, headers={"X-CSRF-TOKEN": csrf_token})
        return req, assetName
    else:
        input(f"\x1b[38;5;196mInvalid id parsed")
        exit()

if __name__ == "__main__":
    #input(f"\x1b[38;5;196m*Note* This bot will purchase only items that are cost 0 robux. This restriction was made for your safety!!! Press \"enter\" to continue...")
    cookie, itemID = check_for_txts()
    req, assetName = purchase(cookie, itemID)
    res = req.json()
    reason = res.get("reason", "")
    if req.status_code == 200:
        if res.get("errors", "") != "" and res.get("errors", "")[0]["message"] == "Unauthorized":
            print(f"\x1b[38;5;196mInvalid cookie parsed")
        elif reason == "Success":
            print(f"\x1b[38;5;2mSuccefuly bought {assetName}")
        elif reason == "AlreadyOwned":
            print(f"\x1b[38;5;196m{assetName} is already owned on this account")
        elif reason == "InsufficientFunds":
            print(f"\x1b[38;5;196mYou dont have enough robux for {assetName}")
    else:
        print(f"\x1b[38;5;196mUnknown error: {req.status_code}")
    input(f"\x1b[38;5;2mPress \"enter\" to leave...")