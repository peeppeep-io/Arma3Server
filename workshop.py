import os
import re
import subprocess
import urllib.request

import keys

WORKSHOP = "steamapps/workshop/content/107410/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"  # noqa: E501


def download(mods):
    for id in mods:
        steamcmd = [
            "/steamcmd/steamcmd.sh",
            "+force_install_dir", "/arma3",
            "+login", os.environ["STEAM_USER"], os.environ["STEAM_PASSWORD"],
            "+workshop_download_item", "107410", id,
            "+quit"
        ]
        while(True):
            with open('steam_cmd_logs.txt', 'w') as out_file, open('steam_cmd_logs_err.txt', 'w') as err_file:
                subprocess.call(steamcmd,stdout=out_file, stderr=err_file)
            with open('steam_cmd_logs.txt', 'r') as out_file:
                lines = out_file.readlines()
            is_match = False
            pattern = r'Success\. Downloaded item (\d+)'
            for line in reversed(lines):
                match = re.search(pattern, line)
                if match:
                    is_match = True
                    break
            if is_match:
                break


def preset(mod_file):
    if mod_file.startswith("http"):
        req = urllib.request.Request(
            mod_file,
            headers={"User-Agent": USER_AGENT},
        )
        remote = urllib.request.urlopen(req)
        with open("preset.html", "wb") as f:
            f.write(remote.read())
        mod_file = "preset.html"
    mods = []
    moddirs = []
    with open(mod_file) as f:
        html = f.read()
        regex = r"filedetails\/\?id=(\d+)\""
        matches = re.finditer(regex, html, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            mods.append(match.group(1))
            moddir = WORKSHOP + match.group(1)
            moddirs.append(moddir)
        download(mods)
        for moddir in moddirs:
            keys.copy(moddir)
    return moddirs
