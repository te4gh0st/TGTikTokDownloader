#  Copyright © 2024 te4gh0st (Vitaliy Timtsurak). All rights reserved.
#  Licensed under the Apache License, Version 2.0

import dataclasses
import random
import re
import uuid

import requests
from bs4 import BeautifulSoup as Bs4

from helper import random_ua, get_content
from loguru import logger


class DownloaderException(Exception):
    ...


class FailedDownload(DownloaderException):
    ...


@dataclasses.dataclass
class VideInfo:
    filename: str
    uuid: uuid.UUID
    source: str
    url: str


class Downloader:
    def __init__(self, output_name: str):
        self.output_name = output_name
        logger.info("[TK DOWNLOADER] - Initialization")

    def _tiktapio(self, url: str):
        logger.info("[TK DOWNLOADER]:[tiktapio] - Start")
        ses = requests.Session()
        ses.headers.update({
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Length': '53',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'pll_language=en; PHPREFS=full',
            'Origin': 'https://tiktap.io',
            'Referer': 'https://tiktap.io/',
            'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            "User-Agent": random_ua()
        })

        data = {
            "url": url,
            "token": ""
        }
        ses.headers.update({
            "Content-Length": str(len(str(data)))
        })
        res = ses.post("https://tiktap.io/api.php", data=data)
        if res.json()["status"] != "success":
            logger.warning("[TK DOWNLOADER]:[tiktapio] - response status not ok")
            return False

        videoData = res.json()["video_data"]

        if "nwm_video_url_HQ" in videoData.keys():
            video_url = res.json()["video_data"]["nwm_video_url_HQ"]
            res = get_content(video_url, self.output_name)
            logger.success("[TK DOWNLOADER]:[tiktapio] - download success")
            return res

        if "nwm_video_url" in videoData.keys():
            video_url = res.json()["video_data"]["nwm_video_url"]
            res = get_content(video_url, self.output_name)
            logger.success("[TK DOWNLOADER]:[tiktapio] - download success")
            return res

        logger.warning("[TK DOWNLOADER]:[tiktapio] - download failed")
        return False

    def _snaptikpro(self, url: str):
        logger.info("[TK DOWNLOADER]:[snaptikpro] - Start")
        try:
            ses = requests.Session()
            ses.headers.update({
                "User-Agent": random_ua()
            })

            res = ses.get("https://snaptik.pro/")
            token = re.search('<input type="hidden" name="token" value="(.*?)">', res.text).group(1)
            data = {
                "url": url,
                "token": token,
                "submit": "1"
            }
            res = ses.post("https://snaptik.pro/action", data=data)

            if res.json()["error"]:
                logger.warning("[TK DOWNLOADER]:[snaptikpro] - response has error")
                return False

            video_url = re.search('<div class="btn-container mb-1"><a href="(.*?)" target="_blank" rel="noreferrer">',
                                  res.json()["html"]).group(1)
            if len(video_url) <= 0:
                logger.warning("[TK DOWNLOADER]:[snaptikpro] - video url not found")
                return False

            res = get_content(video_url, self.output_name)
            logger.success("[TK DOWNLOADER]:[snaptikpro] - download success")
            return res

        except AttributeError:
            logger.warning("[TK DOWNLOADER]:[snaptikpro] - download failed")
            return False

    def _tiktapiocom(self, url: str):
        logger.info("[TK DOWNLOADER]:[tiktapiocom] - Start")
        try:
            ses = requests.Session()
            ses.headers.update({
                'User-Agent': random_ua()
            })
            res = ses.get('https://tiktokio.com/id/')
            open('hasil.html', 'w', encoding='utf-8').write(res.text)
            prefix = re.search(r'<input type="hidden" name="prefix" value="(.*?)"/>', res.text).group(1)
            data = {
                'prefix': prefix,
                'vid': url
            }
            ses.headers.update({
                'Content-Length': str(len(str(data))),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Hx-Current-Url': 'https://tiktokio.com/',
                'Hx-Request': 'true',
                'Hx-Target': 'tiktok-parse-result',
                'Hx-Trigger': 'search-btn'
            })
            res = ses.post('https://tiktokio.com/api/v1/tk-htmx', data=data)
            parser = Bs4(res.text, 'html.parser')
            video_url = parser.find_all('div', attrs={'class': 'tk-down-link'})[0].find('a').get('href')
            res = get_content(video_url, self.output_name)
            logger.success("[TK DOWNLOADER]:[tiktapiocom] - download success")
            return res

        except KeyError:
            logger.warning("[TK DOWNLOADER]:[tiktapiocom] - except KeyError")
            return False
        except AttributeError:
            logger.warning("[TK DOWNLOADER]:[tiktapiocom] - except AttributeError")
            return False
        except IndexError:
            logger.warning("[TK DOWNLOADER]:[tiktapiocom] - except IndexError")
            return False

    def _tikmatecc(self, url: str):
        logger.info("[TK DOWNLOADER]:[tikmatecc] - Start")
        try:
            headers = {
                "Host": "europe-west3-instadown-314417.cloudfunctions.net",
                "User-Agent": "socialdownloader.p.rapidapi.com",
                "Accept": "*/*",
                "Accept-Language": "ar",
                "Accept-Encoding": "gzip, deflate"
            }
            api = "https://europe-west3-instadown-314417.cloudfunctions.net/yt-dlp-1?url=" + url
            res = requests.get(api, headers=headers)
            if res.text[0] != "{":
                return False

            error = res.json()["null"] or res.json()["error"] or res.json()["Error"]
            if error:
                logger.warning("[TK DOWNLOADER]:[tikmatecc] - response has error")
                return False

            videoUrl = res.json()["LINKS"]
            res = get_content(videoUrl)
            logger.success("[TK DOWNLOADER]:[tiktapiocom] - download success")
            return res

        except AttributeError:
            logger.warning("[TK DOWNLOADER]:[tikmatecc] - except AttributeError")
            return False

        except IndexError:
            logger.warning("[TK DOWNLOADER]:[tikmatecc] - except IndexError")
            return False

        except KeyError:
            logger.warning("[TK DOWNLOADER]:[tikmatecc] - except KeyError")
            return False

    def _musicaldown(self, url: str):
        logger.info("[TK DOWNLOADER]:[musicaldown] - Start")
        ses = requests.Session()
        ses.headers.update({
            "User-Agent": random_ua()
        })
        res = ses.get("https://musicaldown.com/en")
        open("hasil.html", "w", encoding="utf-8").write(res.text)
        parsing = Bs4(res.text, 'html.parser')
        allInput = parsing.findAll('input')
        data = {}
        for i in allInput:
            if i.get("id") == "link_url":
                data[i.get("name")] = url
                continue

            data[i.get("name")] = i.get("value")

        res = ses.post("https://musicaldown.com/download", data=data, allow_redirects=True)
        if res.text.find("Convert Video Now") >= 0:
            data = re.search(r"data: '(.*?)'", res.text).group(1)
            urlSlider = re.search(r"url: '(.*?)'", res.text).group(1)
            res = ses.post(urlSlider, data={"data": data})
            if res.text.find('"success":true') >= 0:
                urlVideo = res.json()["url"]
                res = get_content(urlVideo, self.output_name)
                logger.success("[TK DOWNLOADER]:[musicaldown] - download success")
                return res
            logger.warning("[TK DOWNLOADER]:[musicaldown] - failed download")
            return False

        parsing = Bs4(res.text, 'html.parser')
        allUrlDownload = parsing.findAll("a", attrs={"style": "margin-top:10px;"})
        if len(allUrlDownload) <= 0:
            logger.warning("[TK DOWNLOADER]:[musicaldown] - url not found")
            return False

        i = random.randint(0, 1)
        urlVideo = allUrlDownload[i].get("href")
        res = get_content(urlVideo, self.output_name)
        logger.success("[TK DOWNLOADER]:[musicaldown] - download success")
        return res

    @staticmethod
    def download(url: str) -> VideInfo:
        _uuid = uuid.uuid4()
        logger.info(f"[TK DOWNLOADER]:[download] - Try downloading | URL:{url} | UUID:{_uuid}")
        video_name = f"./temp/tt_video-{_uuid}.mp4"
        dl = Downloader(video_name)
        text = url

        status = dl._tiktapio(text)
        if status:
            logger.success("[TK DOWNLOADER]:[download] - success download with tiktapio !")
            return VideInfo(video_name, _uuid, "tiktapio", url)

        status = dl._tiktapiocom(text)
        if status:
            logger.success("[TK DOWNLOADER]:[download] - success download with tiktapiocom !")
            return VideInfo(video_name, _uuid, "tiktapiocom", url)

        status = dl._tikmatecc(text)
        if status:
            logger.success("[TK DOWNLOADER]:[download] - success download with tikmatecc !")
            return VideInfo(video_name, _uuid, "tikmatecc", url)

        status = dl._snaptikpro(text)
        if status:
            logger.success("[TK DOWNLOADER]:[download] - success download with snaptikpro !")
            return VideInfo(video_name, _uuid, "snaptikpro", url)

        status = dl._musicaldown(text)
        if status:
            logger.success("[TK DOWNLOADER]:[download] - success download with musicaldown !")
            return VideInfo(video_name, _uuid, "musicaldown", url)

        logger.critical("[TK DOWNLOADER]:[download] : failed to download the video")
        raise FailedDownload("failed to download the video")
