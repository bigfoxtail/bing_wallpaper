#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import time
import zipfile
import demjson
import requests
import shutil
import hashlib

if os.path.exists('bing_wallpaper'):
    shutil.rmtree('bing_wallpaper')
os.mkdir('bing_wallpaper')

print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
c_year = time.strftime("%Y", time.gmtime())
c_monthdate = time.strftime("%m%d", time.gmtime())
version = "1." + c_year + "." + c_monthdate

bing_wallpaper = '{"response":{"protocol":"3.1","server":"prod","app":[{"appid":"gccbbckogglekeggclmmekihdgdpdgoe","status":"ok","updatecheck":{"status":"ok","urls":{"url":[{"codebase":"https://github.com/bigfoxtail/bing_wallpaper/releases/latest/download/bing_wallpaper.crx"}]},"manifest":{"version":"1.0.0","packages":{"package":[{"name":"bing_wallpaper.crx","hash_sha256":"ba8b38b3d9eb556cc3118f75453a59219436358f38160dabee80234335ce57ed","required":true}]}}}}]}}'
manifest = '{"description":"Brave NTP sponsored images component","key":"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2LqZaGPvWc9IDVNQ5Qg9oet/Pp4Qj/Ihm3HfXx+aYyrAoS1raI52rZv+qtVE8iCN+H5Vy35S4tKifwflUvxD+BRVLsxdjrCMPU/PcEoBAPB0WfNrJwWYSnT4r+Y8PHBh/ujHyk3IHZKkT3gAIh6SZ0MJszHqnDxwuDdpuR66HOfuy+oJ1SlaC4fzfFuUlSbobY/Ho56+Y5QE9yvXCwHIlqFLip04TKO+KrjfwS/+PP0ewq78OP+I0qrv3dw2zNGijJDJk8Zw1Lj9D/BHI1HSNy1RdNM3Vk9ufT3TXg/pR9fq0CLCLkiedu3qdmdu/T6zblbF8zgh+Ehuh7mk2MHgMwIDAQAB","manifest_version":2,"name":"Brave NTP sponsored images","version":"1.0.0"}'
photo = '{"schemaVersion":1,"logo":{"imageUrl":"logo.png","alt":"Visit cn.bing.com","companyName":"Microsoft","destinationUrl":"https://cn.bing.com/"},"wallpapers":[]}'
bing_wallpaper_url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=6&pid=hp&uhd=1&uhdwidth=2880&uhdheight=1620'

headers = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.68 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9,zh;q=0.8,und;q=0.7",
}

manifest_json = demjson.decode(manifest)
photo_json = demjson.decode(photo)
bing_wallpaper_json = demjson.decode(bing_wallpaper)

manifest_json['version'] = version
try:
    rs = requests.session()
    res = rs.get(bing_wallpaper_url, headers=headers)
    res.encoding = 'utf-8'
    resjson = demjson.decode(res.text)
    i = 1
    for image in resjson['images']:
        image_url = "https://cn.bing.com" + image['url']
        try:
            img_name = 'background-' + str(i) + '.jpg'
            img_r = requests.get(image_url)
            img_f = open('./bing_wallpaper/' + img_name, 'wb')
            img_f.write(img_r.content)
            img_json = {"imageUrl": img_name, "focalPoint": {"x": 1350, "y": 720}}
            photo_json['wallpapers'].append(img_json)
            i = i + 1
        except Exception as e:
            print(e)
except Exception as e:
    print(e)

f = "./bing_wallpaper/manifest.json"
with open(f, "w") as file:
    file.write(json.dumps(manifest_json))

f = "./bing_wallpaper/photo.json"
with open(f, "w") as file:
    file.write(json.dumps(photo_json))

zipf = zipfile.ZipFile("bing_wallpaper.crx", 'w', zipfile.ZIP_DEFLATED)
for file in os.listdir("bing_wallpaper"):
    zipf.write("bing_wallpaper/" + file, file)
zipf.close()
hash_value=""
with open("bing_wallpaper.crx", "rb") as crxf:
    sha256obj = hashlib.sha256()
    sha256obj.update(crxf.read())
    hash_value = sha256obj.hexdigest()

bing_wallpaper_json['response']['app'][0]['updatecheck']['manifest']['version'] = version
bing_wallpaper_json['response']['app'][0]['updatecheck']['manifest']['packages']['package'][0]['hash_sha256'] = hash_value

f = "./bing_wallpaper.json"
with open(f, "w") as file:
    file.write(")]}'\n")
    file.write(json.dumps(bing_wallpaper_json))
