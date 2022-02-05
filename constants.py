from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent
SRC_DIR = ROOT_DIR / 'src'
TRAIN_DIR = ROOT_DIR / 'train'
WEIGHTS_DIR = ROOT_DIR / 'weights'
DATA_DIR = ROOT_DIR / 'data'
EXAMPLE_IMG = DATA_DIR / 'few_data_split' / 'few_data_train' / '20210712_141048_857A_ACCC8EAF31F3_0.jpg'
