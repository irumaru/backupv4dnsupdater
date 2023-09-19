import ipaddress
import subprocess
import requests

from log import logger

from config import GLOBAL_ADDRESS_CHECK

# 例外
class getAddressError(Exception):
    pass

# ホストが属するネットワークのグローバルアドレスを取得
def getGlobalAddress():
    response = requests.get(GLOBAL_ADDRESS_CHECK)

    if(response.status_code != 200):
        logger("ERROR: Get address error. HTTP status code = %d. Must be 200." % response.status_code)
        raise getAddressError

    # IPv4アドレスであることを強制
    address = ipaddress.IPv4Address(response.text.replace('\n', ''))

    # 文字列で返す
    return str(address)

# インターネット接続を確認
# return 0で接続
def checkOnline(dest):
    cmd = ["ping", "-c", "1", "-W", "2", dest]
    result = subprocess.run(cmd, capture_output=True, text=True)

    return result.returncode