import cv2
import matplotlib.pyplot as plt

from src.utils import plot_coals_contours_on_img, setup_model


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

    @segmentation_type has 3 mode: 'yolov5', 'semantic', 'mask_rcnn'
    '''

    def __init__(self, video: Video,
                 analyze_type="basic",
                 segmentation_type='semantic',
                 took_frame=1,
                 cut_params=(400, 568, 512, 1320),
                 ):
        self.video = video
        self.analyze_type = analyze_type
        self.segmentation_type = segmentation_type
        self.took_frame = took_frame
        self.x, self.y, self.h, self.w = cut_params

        self.model = setup_model(segmentation_type)
        self.result = None

    def analyze(self):
        cur_frame = 0
        key = 113  # q
        capture = self.video.get_capture()
        while True:
            # for video it works fine, but in real camera we
            # need to calculate delay and took not every 75, but maybe 4 frame dut to 1 thread
            if key == 113 & 0xff:
                ret, cur_image = capture.read()
                if ret:
                    if cur_frame % self.took_frame == 0:
                        crop_frame = cur_image[self.y:self.y + self.h, self.x:self.x + self.w]
                        coals = self.model.predict(crop_frame)
                        self.result = [coal.get_fraction() for coal in coals]
                        # img_with_contours = plot_coals_contours_on_img(crop_frame, coals)
                        # cv2.imshow("fraction", img_with_contours)
                else:
                    break
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
    video_path = r"E:\comptech\comptech\1\20210712_141048_857A_ACCC8EAF31F3\20210712_14\20210712_141048_5E30.mkv"
    test = VideoAnalyzer(Video(video_path))
    test.analyze()
