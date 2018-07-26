from flask import Flask, request, send_from_directory
from find_video import *
from ts2mp4 import *
import os


app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/ls")
def ls():
    return os.getcwd()

@app.route('/query')
def query():
    url = request.args.get("target")
    #print(url)
    video_urls = get_video_urls(url)
    #print(video_urls)
    for url in video_urls:
        url2 = url2url(url)
        print(url2)
        filename = download_video(url2)
        file_out = filename[:-2]+"mp4"
        convert(filename, file_out)
    #filename = "994133356837281792.ts"
    #file_out = filename[:-2]+"mp4"
    return "<img src=\"http://47.93.244.208/download/{}\" />".format(filename[:-2]+"jpg") + "<br /><a href=" +"http://47.93.244.208/download/" +file_out +"> download </a>"


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
