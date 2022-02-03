from pathlib import Path

import gdown

from constants import DATA_DIR, WEIGHTS_DIR

try:
    from zipfile import ZipFile
except ImportError:
    from zipfile36 import ZipFile

def unzip_and_delete(archives_dir: Path) -> None:
    for zip_file in archives_dir.glob('*.zip'):
        with ZipFile(zip_file, 'r') as zip_archive:
            zip_archive.extractall(zip_file.with_suffix(''))
        zip_file.unlink()

def get_data():
    gdown.download(
        id='1_HrcPnL5HnmG3m6XvQRK2IYAHf5a5mS_',
        output=str(DATA_DIR / 'example.png'),
        quiet=False
    )
    gdown.download(
        id='1HGnvRZW-HWkyh7x1_ZlvSAPDcx1OGlNh',
        output=str(DATA_DIR / 'few_data_split.zip'),
        quiet=False
    )
    unzip_and_delete(DATA_DIR)

def get_weights():
    gdown.download(
        id='1DUqALy3zY6Lt5aReTz8zFWOrJXgjZHMX',
        output=str(WEIGHTS_DIR / 'mask_rcnn.pth'),
        quiet=False
    )
    gdown.download(
        id='1XYwU7x_hk3E3KkJBfUkwk1oEVyuuCjaK',
        output=str(WEIGHTS_DIR / 'edge_segmentation.pth'),
        quiet=False
    )
    unzip_and_delete(WEIGHTS_DIR)
