import cv2 as cv2

from constants import WEIGHTS_DIR, DATA_DIR
from src.instance_segmentation.mask_rcnn import MaskRCNN
from src.semantic_segmentation.semantic_segmentation import SemanticSegmentation
from src.utils import plot_coals_contours_on_img, visualize_semantic_segmentation


def video_creator(model,
                  video_path,
                  visualize_method=plot_coals_contours_on_img,
                  cut_params=(400, 568, 512, 1320),
                  save_file_name='1_video.mp4',
                  frames_range_to_save=None):
    """
    Args:
        frames_range_to_save: for example - (300, 750) .
    """
    cap = cv2.VideoCapture(str(video_path))
    frame_counter = 0

    if frames_range_to_save:
        left_cut_by_frame, right_cut_by_frame = frames_range_to_save
        cap.set(cv2.CAP_PROP_POS_FRAMES, left_cut_by_frame)

    # characteristics from the original video
    # w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # suppose my gtx 1070 gives 0.22 sec to inference mask_rcnn on 1 frame, so my fps ~ 4,
    # and form best_model3.pth (efficient_net-b3? or Unet) it take ~ 0.15 sec so my fps would be ~ 6
    my_realtime_fps = 6
    x, y, h, w = cut_params

    # output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(str(DATA_DIR / f'{save_file_name}'), fourcc, my_realtime_fps, (w, h))

    while cap.isOpened():
        ret, frame = cap.read()
        frame_counter += 1

        # Avoid problems when video finish
        if ret:
            # Saving from the desired frames
            if frames_range_to_save:
                if frame_counter <= (right_cut_by_frame - left_cut_by_frame):
                    crop_frame = frame[y:y+h, x:x+w]
                    coals = model.predict(crop_frame)
                    img_with_contours = visualize_method(crop_frame, coals)
                    out.write(img_with_contours)
            else:
                crop_frame = frame[y:y + h, x:x + w]
                coals = model.predict(crop_frame)
                img_with_contours = visualize_method(crop_frame, coals)
                out.write(img_with_contours)
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    model_mask_rcnn = MaskRCNN(
        weights=WEIGHTS_DIR / 'mask_rcnn.pth',
        box_conf_th=0.7,
        nms_th=0.2,
        segmentation_th=0.7,
        device='cuda:0'
    )

    model_semantic_effi_b0 = SemanticSegmentation(
        weights=WEIGHTS_DIR / 'best_model3.pth',
        segm_th_mask=0.8)

    test_videos_params = {
                                    #   x,   y,   h,   w
        '1_video.mp4': {'cut_params': (400, 568, 512, 1344),
                        'video_path': str(DATA_DIR / '20210712_141048_5E30.mkv'),
                        'frames_range': None},
        '2_video.mp4': {'cut_params': (500, 568, 512, 1344),
                        'video_path': str(DATA_DIR / '20210712_142102_6239.mkv'),
                        'frames_range': (300, 755)},
    }

    for video_name, video_params in test_videos_params.items():
        video_creator(model_semantic_effi_b0,
                      video_params['video_path'],
                      visualize_method=visualize_semantic_segmentation,
                      cut_params=video_params['cut_params'],
                      save_file_name=video_name,
                      frames_range_to_save=video_params['frames_range'])
