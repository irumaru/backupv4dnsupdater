import cloudflare


print('config.yamlのemailとappKeyを使います。')

sites = cloudflare.getCloudflareZoneId()

print("Num    ZoneID                              NAME")
count = 0
for site in sites:
    print("%2d     %s    %s" % (count, site['id'], site['name']))
    count += count + 1

print('DNSレコードIDを調べるZoneID番号を選択してください。')
select = int(input())

zoneId = sites[select]['id']

records = cloudflare.getCloudflareDnsRecordId(zoneId)

print('RecordID                            TYPE     NAME')
for record in records:
    print("%s    %5s    %s" % (record['id'], record['type'], record['name']))