import subprocess
from config import HTTP_CHECK_HOST_NAME, HTTP_CHECK_HOST_PORT, HTTP_CHECK_HOST_URI, HTTP_CHECK_HOST_TIMEOUT

# 成功時return 0
def httpCheck(hostIP):
    cmd = ["curl", "--max-time", HTTP_CHECK_HOST_TIMEOUT, "--resolve", HTTP_CHECK_HOST_NAME +":"+ HTTP_CHECK_HOST_PORT +":"+ hostIP, HTTP_CHECK_HOST_URI]
    result = subprocess.run(cmd, capture_output=True, text=True)

    return result.returncode

status = httpCheck("124.110.25.63")
print(status)
