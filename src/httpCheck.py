import subprocess
import time
from config import HTTP_CHECK_HOST_NAME, HTTP_CHECK_HOST_PORT, HTTP_CHECK_HOST_URI, HTTP_CHECK_HOST_TIMEOUT, HTTP_CHECK_HOST_RETRY

# 成功時return 0
def checkOnline(hostIP):
    cmd = ["curl", "--max-time", str(HTTP_CHECK_HOST_TIMEOUT), "--resolve", HTTP_CHECK_HOST_NAME +":"+ str(HTTP_CHECK_HOST_PORT) +":"+ hostIP, HTTP_CHECK_HOST_URI]
    result = subprocess.run(cmd, capture_output=True, text=True)

    return result.returncode

# HTTP_CHECK_HOST_RETRY回試行して接続できないときにFalseを返す
def repeatCheckOnline(hostIP):
    for i in range(HTTP_CHECK_HOST_RETRY):
        if checkOnline(hostIP) == 0:
            return True
        time.sleep(1)
    
    return False
