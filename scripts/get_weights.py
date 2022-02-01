import gdown
from constants import WEIGHTS_DIR

try:
    from zipfile import ZipFile
except ImportError:
    from zipfile36 import ZipFile


gdown.download(id='1DUqALy3zY6Lt5aReTz8zFWOrJXgjZHMX', output=str(WEIGHTS_DIR / 'mask_rcnn.pth'), quiet=False)

for zip_file in WEIGHTS_DIR.glob('*.zip'):
    with ZipFile(zip_file, 'r') as zip_archive:
        zip_archive.extractall(zip_file.with_suffix(''))
    zip_file.unlink()
