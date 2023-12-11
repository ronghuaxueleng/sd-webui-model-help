import shutil
import requests
from tqdm import tqdm


class Downloader(object):
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path

    def start(self):
        res_length = requests.get(self.url, stream=True)
        file_size = int(res_length.headers['Content-Length'])
        with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, ascii=True,
                  desc=self.file_path) as bar:
            with requests.get(self.url, stream=True) as r:
                with open(self.file_path, 'wb') as fp:
                    for chunk in r.iter_content(chunk_size=512):
                        if chunk:
                            fp.write(chunk)
                            bar.update(len(chunk))
        return "done"

    def download_file(self):
        """
        如果你想让下载速度更快，可以使用shutil.copyfileobj()方法直接把文件流写进硬盘里
        """
        with requests.get(self.url, stream=True) as r:
            with open(self.file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)


if __name__ == '__main__':
    url = "https://hf-mirror.com/stabilityai/stable-diffusion-2-1/resolve/main/vae/diffusion_pytorch_model.fp16.bin"
    path = "D:/test.mp4"
    downloader = Downloader(url, path)
    downloader.start()
