import time

import demjson

time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
c_year = time.strftime("%Y", time.localtime())
c_monthdate = time.strftime("%m%d", time.localtime())
version = "1." + c_year + "." + c_monthdate

bing_wallpaper = '{"response":{"protocol":"3.1","server":"prod","app":[{"appid":"gccbbckogglekeggclmmekihdgdpdgoe","status":"ok","updatecheck":{"status":"ok","urls":{"url":[{"codebase":"https://huwoo.net/bing_wallpaper.crx"}]},"manifest":{"version":"1.0.0","packages":{"package":[{"name":"bing_wallpaper.crx","hash_sha256":"ba8b38b3d9eb556cc3118f75453a59219436358f38160dabee80234335ce57ed","required":true}]}}}}]}}'
bing_wallpaper_json = demjson.decode(bing_wallpaper)


bing_wallpaper_json['response']['app'][0]['updatecheck']['manifest']['version'] = version
bing_wallpaper_json['response']['app'][0]['updatecheck']['manifest']['packages']['package'][0]['hash_sha256'] = "00"
