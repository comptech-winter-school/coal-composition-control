import cv2
import matplotlib.pyplot as plt

from constants import WEIGHTS_DIR
from src.instance_segmentation.edge_segmentation import EdgeSegmentation
from src.instance_segmentation.mask_rcnn import MaskRCNN
from src.utils import plot_coals_contours_on_img


def setup_model(model_type):
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
        pass
    elif model_type == 'yolact':
        pass
    return model

class Video:
    def __init__(self, path=None):
        # read from camera, if it's not recorded video
        self.capture = cv2.VideoCapture(0 if path is None else path)

    def get_capture(self):
        return self.capture


class VideoAnalyzer:
    ''' todo:  rewrite to n classes like strategy pattern
    @analyze_type has 4 mode: 'coarse', 'basic', 'normal', 'deep'
    'coarse' -
    'basic' - took every 75 frame and return map
    'normal' -
    'deep' - use tracker, track centers of coals, while it exists

    @model_type has 3 mode: 'yolov5', 'semantic', 'mask_rcnn'
    '''

    def __init__(self, video: Video,
                 analyze_type="basic",
                 model_type='semantic',
                 took_frame=75,
                 cut_params=(400, 568, 512, 1280),
                 ):
        self.video = video
        self.analyze_type = analyze_type
        self.model_type = model_type
        self.took_frame = took_frame
        self.x, self.y, self.h, self.w = cut_params

        self.model = setup_model(model_type)
        self.result = None

    def analyze(self):
        cur_frame = 0
        key = 113  # q
        capture = self.video.get_capture()
        while True:
            # for video it works fine, but in real camera we
            # need to calculate delay and took not every 75, but maybe 4 frame dut to 1 thread
            ret, cur_image = capture.read()
            if not ret:
                break
            if cur_frame % self.took_frame == 0:
                crop_frame = cur_image[self.y:self.y + self.h, self.x:self.x + self.w]
                coals = self.model.predict(crop_frame)
                self.result = [coal.get_fraction() for coal in coals]
                img_with_contours = plot_coals_contours_on_img(crop_frame, coals)
                cv2.imshow("fraction", img_with_contours)
            cur_frame += 1
            self.plot_histogram()
            key = cv2.waitKey(2)

    def plot_histogram(self):
        if self.result:
            plt.hist(self.result, density=False, bins=64)
            plt.ylabel('Count')
            plt.xlabel('Fraction Size')
            plt.show()


if __name__ == '__main__':
    video_path = r"/home/ji411/Downloads/20210712_141048_5E30.mkv"
    test = VideoAnalyzer(Video(video_path))
    test.analyze()
