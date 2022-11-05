import time

import cloudflare
import interface
from log import logger

from config import CLOUDFLARE_RECORD_ID, CLOUDFLARE_RECORD_NAME, CLOUDFLARE_ZONE_ID, PRIMARY_HOST_ADDRESS, LOOP_INTERVAL, ONLINE_CHECK_ADDRESS, USE_PRIORITY, PRIORITY_FILE_PATH

# グローバル変数
hostAddress = ''
dnsAddress = ''

def main():
    global hostAddress, dnsAddress
    logger('Main start.')

    # DNSアドレスの取得
    record = cloudflare.getCloudflareDnsRecord(CLOUDFLARE_ZONE_ID, CLOUDFLARE_RECORD_ID)
    dnsAddress = record['content']

    # ループ
    while(True):
        # プライマリがオフライン かつ セカンダリがオンライン 又は セカンダリ優先 のとき
        if((interface.checkOnline(PRIMARY_HOST_ADDRESS) != 0 and interface.checkOnline(ONLINE_CHECK_ADDRESS) == 0) or prioritySecondary()):
            # Secondary up.
            # セカンダリアドレスを取得
            hostAddress = interface.getGlobalAddress()
            # DNSレコードのアドレスがセカンダリホストのアドレス"でない"か確認
            if(hostAddress != dnsAddress):
                logger('Switch to this secondary.')
                dnsAddress = hostAddress
                updateAddress()
        else:
            # Primary up.
            # DNSレコードのアドレスがプライマリホストのアドレス"でない"か確認
            if(PRIMARY_HOST_ADDRESS != dnsAddress):
                logger('Switch to primary.')
                dnsAddress = PRIMARY_HOST_ADDRESS
                updateAddress()
        
        time.sleep(LOOP_INTERVAL)


# DNSアドレスを更新
def updateAddress():
    global dnsAddress

    logger("Attempt to update dns. : %s" % (dnsAddress))

    # オンラインになるまで繰り返し
    while(True):
        # オンラインか確認
        if(interface.checkOnline(ONLINE_CHECK_ADDRESS) == 0):
            # オンライン
            logger("Check online. dest=%s : Online." % (ONLINE_CHECK_ADDRESS))
            break
        # オフライン
        logger("Check online. : Offline.")

        # 遅延
        time.sleep(LOOP_INTERVAL)

    # DNSの更新
    cloudflare.updateCloudflareDnsRecord(CLOUDFLARE_ZONE_ID, CLOUDFLARE_RECORD_ID, "A", CLOUDFLARE_RECORD_NAME, dnsAddress)
    logger("Successful DNS update.")


# セカンダリを優先するかどうか
def prioritySecondary():
    if(USE_PRIORITY):
        with open(PRIORITY_FILE_PATH, mode='r') as p:
            priority = p.read().replace('\n', '')
            if(priority == 'SECONDARY'):
                return True
            return False
    return False
    

# mainを実行
main()
