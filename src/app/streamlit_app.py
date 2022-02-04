import pandas as pd
import streamlit as st
import cv2 as cv2
import plotly.express as px
import matplotlib.pyplot as plt

from src.instance_segmentation.mask_rcnn import MaskRCNN
from src.instance_segmentation.edge_segmentation import EdgeSegmentation
from src.object_detection.yolov5 import YOLOv5
from src.utils import plot_coals_contours_on_img
from constants import WEIGHTS_DIR, DATA_DIR


def create_histogram_plot(fractions):
    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_facecolor('0.8')
    ax.set_ylabel('Кол-во')
    ax.set_xlabel('Размеры камней')
    ax.set_xticks(list(range(0, 1000, 25)))
    ax.hist(fractions, bins=64)
    fig.tight_layout()
    plt.close()
    return fig


@st.cache(allow_output_mutation=True)
def load_mask_rcnn_model(model_path: str,
                         box_conf_th: float = 0.7,
                         nms_th: float = 0.2,
                         segmentation_th: float = 0.7):
    model = MaskRCNN(model_path,
                     box_conf_th=box_conf_th,
                     nms_th=nms_th,
                     segmentation_th=segmentation_th)
    return model


@st.cache(allow_output_mutation=True)
def load_unet_model(model_path: str,
                    width: int = None,
                    height: int = None):
    model = EdgeSegmentation(model_path,
                             width=width,
                             height=height)
    return model


@st.cache(allow_output_mutation=True)
def load_yolov5n6_model(model_path: str,
                        box_conf_th: float = 0.2,
                        nms_th: float = 0.2,
                        amp: bool = True,
                        size: int = 1280,
                        device=None):
    model = YOLOv5(model_path,
                   box_conf_th=box_conf_th,
                   nms_th=nms_th,
                   amp=amp,
                   size=size,
                   device=device)
    return model


def simulate_rtsp_from_video(video_path):
    pass


def streamlit_app():
    if "button_id" not in st.session_state:
        st.session_state["button_id"] = ""
    if "color_to_label" not in st.session_state:
        st.session_state["color_to_label"] = {}

    st.set_page_config(
        page_title="EVRAZ demo app", page_icon=':pencil2:'
    )
    st.title("ЕВРАЗ - CompTech2022")
    st.sidebar.header("Configuration")

    PAGES = {
        'EVRAZ fractions demo page': fractions_demo_app,
        'Antoher page': another_app,
    }
    page = st.sidebar.selectbox('Page:', options=list(PAGES.keys()), key='PAGE_selection')

    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<h6>Made with &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp '
            'with a source code from <a href="https://github.com/andfanilo/streamlit-drawable-canvas">@andfanilo</a> by <a href="https://vk.com/danilov_ps">@p.danilov</a>&nbsp '
            '<a href="https://github.com/JI411">@A. Lekomtsev</a>, <a href="https://github.com/0x0000dead">@S. Vandanov</a>&nbsp <br>'
            '<a href="https://github.com/IldarMurzagaleev">@I. Murzagaleev</a>, <a href="https://github.com/LRDPRDX">@B. Sikach</a>&nbsp '
            'and <a href="https://github.com/asromahin">@A. Romahin</a></h6>',
            unsafe_allow_html=True,
        )

    PAGES[page]()


def another_app():
    # st.sidebar.subheader('Опции')
    st.markdown(
        """
    Страница с демонстрацией работы команды ЕВРАЗ по задаче определения фракционного состава угля на конвейере:
    * Подпунктик;
    *  **Жирным**

    """
    )
    st.write('')


def fractions_demo_app():
    # st.sidebar.subheader('Опции')
    st.markdown(
        """
    Страница с демонстрацией работы команды **ЕВРАЗа** по задаче определения фракционного состава угля на конвейере.
    
    Более подробное описание - будет. А сейчас можете нажать на кнопку *Начать анализ* и посмотреть, что будет. 
    """
    )
    st.write('')

    if 'histogram_history' not in st.session_state:
        st.session_state['histogram_history'] = pd.DataFrame(columns=['Размер камней'])
    if 'Executed' not in st.session_state:
        st.session_state['Executed'] = 'initialized'

    videos_list = {'Видео 1': str(DATA_DIR / 'example_video_1.mkv'),
                   'Видео 2': str(DATA_DIR / 'example_video_2.mkv'),
                   }
    models_list = {'Mask R-CNN': load_mask_rcnn_model(WEIGHTS_DIR / 'mask_rcnn.pth',
                                                      box_conf_th=0.7,
                                                      nms_th=0.2,
                                                      segmentation_th=0.7),

                   'Unet': load_unet_model(WEIGHTS_DIR / 'edge_segmentation.pth',
                                           width=1280,
                                           height=640),

                   'Yolov5n6': load_yolov5n6_model(WEIGHTS_DIR / 'yolov5n6.pt',
                                                   box_conf_th=0.2,
                                                   nms_th=0.2,
                                                   amp=True,
                                                   size=1280,
                                                   device=None),
                   }


    visualize_methods = {'Mask R-CNN': plot_coals_contours_on_img,
                         'Unet': plot_coals_contours_on_img,
                         'Yolov5n6': plot_coals_contours_on_img,
                         }

    with st.form('perform_analysis'):
        _, selection_center_col, _ = st.columns([0.1, 6, 0.1])
        with selection_center_col:
            selected_video = st.selectbox(
                'Выберите видео из списка:',
                videos_list,
                key='videos_list')

            selected_model_name = st.selectbox(
                'Выберите модель:',
                models_list,
                key='models_list')

            st.write('')
            save_hist_history = st.checkbox(label='Копить историю фракций?', value=True)
            st.write('')

        _, center_col_submit_button, _ = st.columns([2, 2.25, 1])
        with center_col_submit_button:
            perform_analysis_button = st.form_submit_button(label='Начать анализ:')

    model = models_list[selected_model_name]
    video_path = videos_list[selected_video]
    visualize_method = visualize_methods[selected_model_name]

    placeholder_img = st.empty()
    placeholder_plot = st.empty()

    if not save_hist_history:
        st.session_state['histogram_history'] = pd.DataFrame(columns=['Размер камней'])

    if perform_analysis_button:
        cap = cv2.VideoCapture(str(video_path))
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        frame_counter = 0
        success = True
        x, y, h, w = 400, 568, 512, 1344    # cutting frame params

        while success:
            success, frame = cap.read()
            frame_counter += 1

            if frame_counter % 2 == 0:
                crop_frame = frame[y:y + h, x:x + w]
                coals = model.predict(crop_frame)
                test_fractions = [coal.get_fraction() for coal in coals]
                crop_frame_with_contours = visualize_method(crop_frame, coals)

                test_fractions = pd.DataFrame(test_fractions, columns=['Размер камней'])
                if save_hist_history:
                    st.session_state['histogram_history'] = pd.concat([st.session_state['histogram_history'],
                                                                       test_fractions],
                                                                      ignore_index=True)
                    df2plot = st.session_state['histogram_history']['Размер камней']
                else:
                    df2plot = test_fractions

                _col_1, img_col, _col_2 = placeholder_img.columns([0.01, 4, 0.01])
                _col_3, plot_column, _col_4 = placeholder_plot.columns([0.2, 5, 1])

                with img_col:
                    crop_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2RGB)
                    img_col.image(crop_frame, caption='Кадры с конвейера')
                    crop_frame_with_contours = cv2.cvtColor(crop_frame_with_contours, cv2.COLOR_BGR2RGB)
                    img_col.image(crop_frame_with_contours, caption=f'Обработка моделю: {selected_model_name}')

                with plot_column:
                    # plot histogram of a fractions
                    fig = px.histogram(df2plot, nbins=64, x='Размер камней')
                    fig.update_layout(
                        title_text='Распределение фракций:',
                        # xaxis_title_text='Размер камней',
                        yaxis_title_text='Количество',
                        bargap=0.01,  # gap between bars of adjacent location coordinates
                        bargroupgap=0.01  # gap between bars of the same location coordinates
                    )
                    # fig = create_histogram_plot(df2plot)
                    plot_column.plotly_chart(fig)
        st.success('Анализ закончен!')
