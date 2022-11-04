from urllib import response
import requests
import json

from log import logger

# Configのロード
from config import CLOUDFLARE_GLOBAL_API_KEY, CLOUDFLARE_EMAIL


# APIレスポンスの解釈に失敗
class ApiCallError(Exception):
    pass

# APIのレスポンスを解釈
def apiInterpretation(data):
    if(data.status_code != 200):
        logger("ERROR: Api call error. HTTP response status code = %d. Must be 200." % data.status_code)
        raise ApiCallError()
    
    data = data.json()

    if(data['success'] != True):
        logger("ERROR: Api response error. Success is not True. Errors = %s" % json.dumps(data['errors']))
        raise ApiCallError()
    
    return data['result']

# DNSレコードの取得
def getCloudflareDnsRecord(zone_id, record_id):
    global CLOUDFLARE_EMAIL, CLOUDFLARE_GLOBAL_API_KEY

    uri = 'https://api.cloudflare.com/client/v4/zones/'+zone_id+'/dns_records/'+record_id

    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_GLOBAL_API_KEY,
        'Content-Type': 'application/json',
    }

    response = requests.get(uri, headers=headers)

    return apiInterpretation(response)

# DNSレコードのアップデート
def updateCloudflareDnsRecord(zone_id, record_id, record_type, record_name, record_value):
    global CLOUDFLARE_EMAIL, CLOUDFLARE_GLOBAL_API_KEY

    uri = 'https://api.cloudflare.com/client/v4/zones/'+zone_id+'/dns_records/'+record_id

    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_GLOBAL_API_KEY,
        'Content-Type': 'application/json',
    }

    data = '{"type":"'+record_type+'","name":"'+record_name+'","content":"'+record_value+'","ttl":60,"proxied":false}'
    
    response = requests.put(uri, headers=headers, data=data)

    return apiInterpretation(response)

# DNSゾーンIDの取得
def getCloudflareZoneId():
    global CLOUDFLARE_EMAIL, CLOUDFLARE_GLOBAL_API_KEY

    uri = 'https://api.cloudflare.com/client/v4/zones'

    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_GLOBAL_API_KEY,
        'Content-Type': 'application/json',
    }

    response = requests.get(uri, headers=headers)
    
    return apiInterpretation(response)

# DNSゾーンからレコードIDの取得
def getCloudflareDnsRecordId(zone_id):
    global CLOUDFLARE_EMAIL, CLOUDFLARE_GLOBAL_API_KEY

    uri = 'https://api.cloudflare.com/client/v4/zones/'+zone_id+'/dns_records'

    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_GLOBAL_API_KEY,
        'Content-Type': 'application/json',
    }

    response = requests.get(uri, headers=headers)

    return apiInterpretation(response)
