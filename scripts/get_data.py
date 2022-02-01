import gdown
from constants import DATA_DIR

try:
    from zipfile import ZipFile
except ImportError:
    from zipfile36 import ZipFile


gdown.download(id='1_HrcPnL5HnmG3m6XvQRK2IYAHf5a5mS_', output=str(DATA_DIR / 'example.png'), quiet=False)
gdown.download(id='1HGnvRZW-HWkyh7x1_ZlvSAPDcx1OGlNh', output=str(DATA_DIR / 'few_data_split.zip'), quiet=False)

for zip_file in DATA_DIR.glob('*.zip'):
    with ZipFile(zip_file, 'r') as zip_archive:
        zip_archive.extractall(zip_file.with_suffix(''))
    zip_file.unlink()
