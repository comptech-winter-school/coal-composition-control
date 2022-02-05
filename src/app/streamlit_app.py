import time
import pandas as pd
import streamlit as st
import cv2 as cv2
import plotly.express as px
import matplotlib.pyplot as plt

from PIL import Image
from src.utils import plot_coals_contours_on_img
from constants import DATA_DIR, SRC_DIR
from src.video_analyzer import setup_model


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


@st.cache(suppress_st_warning=True,
          allow_output_mutation=True,
          ttl=5 * 60)
def cached_setup_model(model_name):
    return setup_model(model_name)


def streamlit_app():
    if "button_id" not in st.session_state:
        st.session_state["button_id"] = ""
    if "color_to_label" not in st.session_state:
        st.session_state["color_to_label"] = {}

    page_icon = Image.open(str(DATA_DIR / 'favicon-32x32.png'))
    page_icon = page_icon.convert("RGBA")
    st.set_page_config(
        page_title="EVRAZ coal fractions demo", page_icon=page_icon
    )

    with open(SRC_DIR / 'app/st_form_wo_border.css') as form_style_file:
        st.markdown(f'<style>{form_style_file.read()}</style>', unsafe_allow_html=True)

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
    if 'pixels2centimeters' not in st.session_state:
        st.session_state['pixels2centimeters'] = 30 / 250  # let's pretend 30cm coal ~= 250px on image
    if 'Executed' not in st.session_state:
        st.session_state['Executed'] = 'initialized'

    videos_list = {'Видео 1': str(DATA_DIR / 'example_video_1.mkv'),
                   'Видео 2': str(DATA_DIR / 'example_video_2.mkv'),
                   }

    models_list = {'Mask R-CNN': 'mask_rcnn', 'Unet': 'semantic',
                   'Yolov5s6': 'yolov5', 'Yoloact': 'yolact'}

    visualize_methods = {'Mask R-CNN': plot_coals_contours_on_img,
                         'Unet': plot_coals_contours_on_img,
                         'Yolov5s6': plot_coals_contours_on_img,
                         'Yoloact': plot_coals_contours_on_img,
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
            save_hist_history = st.checkbox(label='Копить историю фракций по кадрам?', value=True)
            st.write('')

        _, center_col_submit_button, _ = st.columns([2, 2.25, 1])
        with center_col_submit_button:
            perform_analysis_button = st.form_submit_button(label='Начать анализ:')
            st.write('')

    model = cached_setup_model(models_list[selected_model_name])
    video_path = videos_list[selected_video]
    visualize_method = visualize_methods[selected_model_name]

    placeholder_img = st.empty()
    placeholder_plot = st.empty()

    hist_col_name = 'Размер камней (см)'

    if perform_analysis_button:
        st.session_state['histogram_history'] = pd.DataFrame(columns=[hist_col_name])
        cap = cv2.VideoCapture(str(video_path))

        frame_counter = 0
        success = True
        x, y, h, w = 400, 568, 512, 1344  # cutting frame params

        while success:
            success, frame = cap.read()
            frame_counter += 1

            if frame_counter % 2 == 0:
                crop_frame = frame[y:y + h, x:x + w]
                coals = model.predict(crop_frame)
                test_fractions = [coal.get_fraction() for coal in coals]
                crop_frame_with_contours = visualize_method(crop_frame, coals)

                test_fractions = pd.DataFrame(test_fractions, columns=[hist_col_name])
                test_fractions = test_fractions * st.session_state['pixels2centimeters']
                if save_hist_history:
                    st.session_state['histogram_history'] = pd.concat([st.session_state['histogram_history'],
                                                                       test_fractions],
                                                                      ignore_index=True)
                    df2plot = st.session_state['histogram_history'][hist_col_name]
                else:
                    df2plot = test_fractions

                _col_1, img_col, _col_2 = placeholder_img.columns([0.01, 4, 0.01])
                _col_3, plot_column, _col_4 = placeholder_plot.columns([0.2, 5, 1])

                with img_col:
                    time.sleep(0.2)  # let streamlit process image drawing for several users
                    crop_frame_with_contours = cv2.cvtColor(crop_frame_with_contours, cv2.COLOR_BGR2RGB)
                    img_col.image(crop_frame_with_contours, caption=f'Обработка моделю: {selected_model_name}')

                with plot_column:
                    # plot histogram of a fractions
                    fig = px.ecdf(df2plot, x=hist_col_name, ecdfnorm='percent')
                    fig.add_vline(x=3, annotation_text=" Граница решения", line_width=4,
                                  line_dash="dash", line_color="green", opacity=1)
                    fig.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='LightPink')
                    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='LightPink')
                    fig.update_layout(
                        # title_text='Распределение фракций:',
                        yaxis_title_text='Процент',
                    )
                    plot_column.plotly_chart(fig)
        st.success('Анализ закончен!')
