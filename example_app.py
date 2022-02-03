import cv2

from constants import DATA_DIR, WEIGHTS_DIR
from scripts.download import load_data, load_weights
from src.instance_segmentation.edge_segmentation import EdgeSegmentation
from src.instance_segmentation.mask_rcnn import MaskRCNN

if __name__ == '__main__':
    load_data()
    load_weights()

    image = cv2.imread(str(DATA_DIR / 'few_data_split' / 'few_data_train' / '20210712_141048_857A_ACCC8EAF31F3_0.jpg'))

    if image is None:
        raise FileNotFoundError('check path to image')

    mask_rcnn = MaskRCNN(WEIGHTS_DIR / 'mask_rcnn.pth')
    coals = mask_rcnn.predict(image)
    print([coal.get_fraction() for coal in coals])

    edge_segmentation = EdgeSegmentation(WEIGHTS_DIR / 'edge_segmentation.pth')
    coals = edge_segmentation.predict(image)
    print([coal.get_fraction() for coal in coals])
