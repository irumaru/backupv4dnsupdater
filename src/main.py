import time

import cloudflare
import interface
import httpCheck
from log import logger
import log

from config import CLOUDFLARE_RECORD_ID, CLOUDFLARE_RECORD_NAME, CLOUDFLARE_ZONE_ID, PRIMARY_HOST_ADDRESS, SECONDARY_HOST_ADDRESS, LOOP_INTERVAL, ONLINE_CHECK_ADDRESS, USE_PRIORITY, PRIORITY_FILE_PATH

# グローバル変数
secondaryHostAddress = ''
dnsAddress = ''

# 冗長なログ
useStatusLog = log.WiseLogger()

def main():
    global secondaryHostAddress, dnsAddress
    logger('Main start.')

    # 冗長なログ
    hostStatusLog = log.WiseLogger()

    # DNSアドレスの取得
    record = cloudflare.getCloudflareDnsRecord(CLOUDFLARE_ZONE_ID, CLOUDFLARE_RECORD_ID)
    dnsAddress = record['content']

    # ループ
    while(True):
        # セカンダリアドレスを取得
        if SECONDARY_HOST_ADDRESS == 'dyncmic':
            secondaryHostAddress = interface.getGlobalAddress()
        else:
            secondaryHostAddress = SECONDARY_HOST_ADDRESS
        
        # 状態の取得
        p = httpCheck.repeatCheckOnline(PRIMARY_HOST_ADDRESS)
        s = httpCheck.repeatCheckOnline(secondaryHostAddress)
        hostStatusLog.print(getUpTimeMessage(p, s))
        
        # プライマリ優先
        if(priority('PRIMARY')):
            usePrimary()
        # セカンダリ優先
        elif(priority('SECONDARY')):
            useSecondary()
        # プライマリとセカンダリがオンライン
        elif(p == True and s == True):
            usePrimary()
        # プライマリがオンライン かつ セカンダリがオフライン
        elif(p == True and s == False):
            usePrimary()
        # プライマリがオフライン かつ セカンダリがオンライン
        elif(p == False and s == True):
            useSecondary()
        # 全てオフライン
        else:
            usePrimary()
        
        time.sleep(LOOP_INTERVAL)

def usePrimary():
    global dnsAddress

    # Primary up.
    useStatusLog.print('Use primary.')
    # DNSレコードのアドレスがプライマリホストのアドレス"でない"か確認
    if(PRIMARY_HOST_ADDRESS != dnsAddress):
        logger('Switch to primary.')
        dnsAddress = PRIMARY_HOST_ADDRESS
        updateAddress()

def useSecondary():
    global dnsAddress

    # Secondary up.
    useStatusLog.print('Use secondary.')
    # DNSレコードのアドレスがセカンダリホストのアドレス"でない"か確認
    if(secondaryHostAddress != dnsAddress):
        logger('Switch to this secondary.')
        dnsAddress = secondaryHostAddress
        updateAddress()

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
def priority(p):
    if(USE_PRIORITY):
        with open(PRIORITY_FILE_PATH, mode='r') as p:
            priority = p.read().replace('\n', '')
            if(priority == p):
                logger(p + ' has priority')
                return True
            return False
    return False

def getUpTimeMessage(p, s):
    p = 'OK!' if p else 'Offline'
    s = 'OK!' if s else 'Offline'

    mes = 'Primary: ' + p + '  Secondary: ' + s

    return mes

# mainを実行
main()
