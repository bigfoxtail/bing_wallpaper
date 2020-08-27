import hashlib
import os
import zipfile

zipf = zipfile.ZipFile("bing_wallpaper.crx", 'w', zipfile.ZIP_DEFLATED)
for file in os.listdir("bing_wallpaper"):
    zipf.write("bing_wallpaper/" + file, file)
zipf.close()
hash_value = ""
with open("bing_wallpaper.crx", "rb") as crxf:
    sha256obj = hashlib.sha256()
    sha256obj.update(crxf.read())
    hash_value = sha256obj.hexdigest()

print(hash_value)