from pathlib import Path

import gdown

from constants import DATA_DIR, WEIGHTS_DIR

try:
    from zipfile import ZipFile
except ImportError:
    from zipfile36 import ZipFile

def unzip(archives_dir: Path) -> None:
    for zip_file in archives_dir.glob('*.zip'):
        with ZipFile(zip_file, 'r') as zip_archive:
            if not zip_file.with_suffix('').is_dir():
                zip_archive.extractall(zip_file.with_suffix(''))


def load_data() -> None:
    gdown.cached_download(
        id='1_HrcPnL5HnmG3m6XvQRK2IYAHf5a5mS_',
        path=str(DATA_DIR / 'example.png'),
        md5='d299412dac2de1ef873f7b1db34c1575'
    )
    gdown.cached_download(
        id='1HGnvRZW-HWkyh7x1_ZlvSAPDcx1OGlNh',
        path=str(DATA_DIR / 'few_data_split.zip'),
        md5='3e2537104a8bb90b538a4816e0b52cb6',
    )
    unzip(archives_dir=DATA_DIR)


def load_weights() -> None:
    gdown.cached_download(
        id='1DUqALy3zY6Lt5aReTz8zFWOrJXgjZHMX',
        path=str(WEIGHTS_DIR / 'mask_rcnn.pth'),
        md5='7e07632e0e22ad6e777123126b0f3df8'
    )
    gdown.cached_download(
        id='1XYwU7x_hk3E3KkJBfUkwk1oEVyuuCjaK',
        path=str(WEIGHTS_DIR / 'edge_segmentation.pth'),
        md5='df1660a95e26a6c65337a58edb344bb4'
    )
    gdown.cached_download(
        id='1tVQ91P3RGo5dX7Pw5vl9kqiS-X6ZNEME',
        path=str(WEIGHTS_DIR / 'yolov5s6.pt'),
        md5='0232b6b3946dd5a4d547e95b09f2b76e'
    )
    unzip(archives_dir=WEIGHTS_DIR)
