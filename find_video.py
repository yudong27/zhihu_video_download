# coding: utf-8

import requests
import brotli
import re
import json
from bs4 import BeautifulSoup as BS


def get_video_urls(web_url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0","Accept":"*/*","Accept-Encoding":"gzip, deflate, br"}
    try:
        web = requests.get(web_url,headers=headers)
    except:
        print("Open url error:{}".format(web_url))
        return []
    content = brotli.decompress(web.content)
    content = bytes.decode(content)
    soup = BS(content,'lxml')
    video_box = soup.find_all(class_="video-box")
    video_urls = []
    if len(video_box) > 0:
        for ref in video_box:
            video_url = ref['href'].split('=')[1].replace("%3A",":")
            video_urls.append(video_url)
    else:
        print("No video in web")
        return []
    return video_urls

def url2url(url):
    #video_url = "https://www.zhihu.com/video/1005486648460701696"
    #video_url = "https://lens.zhihu.com/api/videos/1005486648460701696"
    if url.startswith("https://www.zhihu.com/video/"):
        url = "https://lens.zhihu.com/api/videos/" + url.split('/')[-1]
    return url


def download_video(video_url):
    header1 = {"Host": "lens.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer":"https://v.vzuu.com/video/1005486648460701696",
        "x-referer":"" ,
        "content-type": "application/json",
        "origin": "https://v.vzuu.com",
        "Connection": "keep-alive",}
    try:
        json_br = requests.get(video_url,headers=header1)
    except:
        print("Open url error:{}".format(video_url))
        return
    video_json = json.loads(bytes.decode(brotli.decompress(json_br.content)))
    hd_url = video_json['playlist']['ld']['play_url'] #hd, ld, sd
    cover_jpg_url = video_json['cover_info']['thumbnail']
    m3u8 = requests.get(hd_url)
    hd_url_prefix = re.match("https.*/",hd_url).group()
    ts_all = b''
    for line in m3u8.text.split('\n'):
        if line.startswith('#') or len(line) <10:
            pass
        else:
            url1 = hd_url_prefix + line
            #print(url1)
            ts_v = requests.get(url1)
            ts_all += ts_v.content
    filename = video_url.split('/')[-1] + '.ts'
    with open(filename,'wb') as f:
        f.write(ts_all)
    with open(filename[:-2]+"jpg",'wb') as f:
        cover = requests.get(cover_jpg_url)
        f.write(cover.content)
    return filename
            

if __name__ == "__main__":
    url = "https://www.zhihu.com/question/266507374/answer/451742159"
    video_urls = get_video_urls(url)
    print(video_urls)
    for url in video_urls:
        url2 = url2url(url)
        print(url2)
        download_video(url2)
    #video_url = "https://www.zhihu.com/video/1005486648460701696"
    #video_url = "https://lens.zhihu.com/api/videos/1005486648460701696"
    #download_video(video_url)
