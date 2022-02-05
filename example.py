import cv2

from constants import WEIGHTS_DIR, EXAMPLE_IMG
from src.instance_segmentation.yolact import YolactPredictor
from src.utils import plot_coals_contours_on_img

image = cv2.imread(str(EXAMPLE_IMG))
yol_model = YolactPredictor(WEIGHTS_DIR / 'yolact.pth')
coals = yol_model.predict(image)
print([coal.get_fraction() for coal in coals])
if coals:
    cv2.imshow('Contours', plot_coals_contours_on_img(image, coals))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
