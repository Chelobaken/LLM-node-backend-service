import requests
def checkurl(url:str)->bool:
    try:
        requests.get(url=url)
        return True
    except:
        return False
    
        