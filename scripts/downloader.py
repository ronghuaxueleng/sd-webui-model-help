import shutil
import sys
import requests
import os


class Downloader(object):
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path

    def start(self):
        res_length = requests.get(self.url, stream=True)
        total_size = int(res_length.headers['Content-Length'])
        print(res_length.headers)
        print(res_length)
        if os.path.exists(self.file_path):
            temp_size = os.path.getsize(self.file_path)
            print("当前：%d 字节， 总：%d 字节， 已下载：%2.2f%% " % (temp_size, total_size, 100 * temp_size / total_size))
        else:
            temp_size = 0
            print("总：%d 字节，开始下载..." % (total_size,))

        headers = {'Range': 'bytes=%d-' % temp_size,
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}
        res_left = requests.get(self.url, stream=True, headers=headers)

        with open(self.file_path, "ab") as f:
            for chunk in res_left.iter_content(chunk_size=1024):
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()

                done = int(50 * temp_size / total_size)
                sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                sys.stdout.flush()

    def download_file(self):
        """
        如果你想让下载速度更快，可以使用shutil.copyfileobj()方法直接把文件流写进硬盘里
        """
        with requests.get(self.url, stream=True) as r:
            with open(self.file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)


if __name__ == '__main__':
    url = "https://vd2.bdstatic.com/mda-imt4u2h7u35k/xxxxxxx"
    path = "C:/test.mp4"
    downloader = Downloader(url, path)
    downloader.start()

