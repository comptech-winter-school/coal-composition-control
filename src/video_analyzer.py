import cv2
import matplotlib.pyplot as plt

from constants import WEIGHTS_DIR
from src.instance_segmentation.edge_segmentation import EdgeSegmentation
from src.instance_segmentation.mask_rcnn import MaskRCNN
from src.object_detection.yolov5 import YOLOv5
from src.utils import plot_coals_contours_on_img
from yolact import Yolact

def setup_model(model_type):
    """
    Initialize specific type model
    :param str model_type: Type of the model, which will be used to predict coals mask. Available models:
        'semantic' - UNet model which predict mask with overlayed edges to separate coals.
        'mask_rcnn' - Mask R-CNN model for coals detection and instance segmentation
        'yolov5' - Yolov5 model for coals boundbox detection
        'yolact' - YOLACT model for instance segmentation
    :return model
    """
    model = None

    if model_type == 'semantic':
        model = EdgeSegmentation(
        weights=WEIGHTS_DIR / 'edge_segmentation.pth',
        segm_th_mask=0.8)
    elif model_type == 'mask_rcnn':
        model = MaskRCNN(
            weights=WEIGHTS_DIR / 'mask_rcnn.pth',
            box_conf_th=0.7,
            nms_th=0.2,
            segmentation_th=0.7,
            device=None)
    elif model_type == 'yolov5':
        model = YOLOv5(
            weights=WEIGHTS_DIR / 'yolov5s6.pt')
    elif model_type == 'yolact':
        model = YolactPredictor(
            WEIGHTS_DIR / 'yolact_base_201_2013_interrupt.pth')
    return model

class Video:
    def __init__(self, path=None, cam_num=0):
        """
        Read video from the input source. It can be RTSP camera or video
        
        :param str path: Path to the input video, if None then cam_num should be selected.
        :param int cam_num: Camera number which will be taken as the input source. 
        """
        self.capture = cv2.VideoCapture(cam_num if path is None else path)

    def get_frame(self):
        _, frame = self.capture.read()
        return _, frame


class VideoAnalyzer:
    def __init__(self, video: Video,
                 analyze_type="basic",
                 model_type="semantic",
                 took_frame=75,
                 cut_params=(400, 568, 512, 1280),
                 bins=64
                 ):
        """
        :param Video video: Object which will be analyzed.
        :param str analyze_type: Analyze type of the input source, has 1 mode:
            'basic' - Analyze every N frame and plot histogram + mask, to avoid multiple counting.
            [not implemented feature]
            'deep' - Assuming that the conveyor speed is constant, 
                     track the center of each coal, predict new possible center, and don't count 
                     coals located in this predicted area; if out of bound - reset tracker;
                     tracking can be implemented with opencv TrackerKCF tracker;
                     also, kalman algorithm can be used to predict the new position of the center.

        :param str model_type: Type of the model, which will be used to predict coals mask. Available models:
            'semantic' - UNet model which predict mask with overlayed edges to separate coals.
            'mask_rcnn' - Mask R-CNN model for coals detection and instance segmentation
            'yolov5' - Yolov5 model for coals boundbox detection
            'yolact' - YOLACT model for instance segmentation
        :param int took_frame: Every :took_frame: will be used to analyze Video.
        :param tuple cut_params: How to cut input Video [x,y,h,w] to avoid perspective transform.
        :param int bins: Split the histogram to this number of bins.
        """

        self.video = video
        self.analyze_type = analyze_type
        self.model_type = model_type
        self.took_frame = took_frame
        self.x, self.y, self.h, self.w = cut_params

        self.model = setup_model(model_type)
        self.result = None
        self.bins = bins

    def analyze(self):
        cur_frame = 0
        if self.analyze_type == "basic":
            while True:
                ret, cur_image = self.video.get_frame()
                if not ret:
                    break
                if cur_frame % self.took_frame == 0:
                    crop_frame = cur_image[self.y:self.y + self.h, self.x:self.x + self.w]
                    coals = self.model.predict(crop_frame)
                    self.result = [coal.get_fraction() for coal in coals]
                    img_with_contours = plot_coals_contours_on_img(crop_frame, coals)
                    cv2.imshow("result", img_with_contours)
                    cur_frame += 1
                    self.plot_histogram()
                    cv2.waitKey(3)

    def plot_histogram(self):
        if self.result:
            plt.hist(self.result, density=False, bins=self.bins)
            plt.ylabel('Count')
            plt.xlabel('Fraction Size')
            plt.show()


if __name__ == '__main__':
    video_path = r"/home/ji411/Downloads/20210712_141048_5E30.mkv"
    test = VideoAnalyzer(Video(video_path))
    test.analyze()
