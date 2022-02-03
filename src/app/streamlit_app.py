from src.instance_segmentation.mask_rcnn import MaskRCNN
from constants import WEIGHTS_DIR, DATA_DIR

import streamlit as st
import cv2 as cv2
import matplotlib.pyplot as plt


def create_histogram(fractions, figsize=(4, 4)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title('Fractions', fontsize=8)
    plt.hist(fractions, color='g', bins=64)
    # plt.hist(list(fractions.keys()), fractions.values(), color='g')

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


def streamlit_app():
    if "button_id" not in st.session_state:
        st.session_state["button_id"] = ""
    if "color_to_label" not in st.session_state:
        st.session_state["color_to_label"] = {}

    st.set_page_config(
        page_title="EVRAZ demo app", page_icon=':pencil2:'
    )
    st.title("Title")
    st.sidebar.header("Configuration")

    PAGES = {
        'EVRAZ fractions demo page': fractions_demo_app,
        'Antoher page': another_app,
    }
    page = st.sidebar.selectbox('Page:', options=list(PAGES.keys()), key='PAGE_selection')
    PAGES[page]()

    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp '
            'with a source code from <a href="https://github.com/andfanilo/streamlit-drawable-canvas">@andfanilo</a> by <a href="https://vk.com/danilov_ps">@p.danilov</a></h6>',
            unsafe_allow_html=True,
        )


def another_app():
    # st.sidebar.subheader('Опции')
    st.markdown(
        """
    Описание:
    * Подпунктик;
    *  **Жирным**

    """
    )
    st.write('')


def fractions_demo_app():
    # st.sidebar.subheader('Опции')
    st.markdown(
        """
    Описание:
    * Подпунктик;
    *  **Жирным**

    """
    )
    st.write('')

    model = load_mask_rcnn_model(WEIGHTS_DIR / 'mask_rcnn.pth',
                                 box_conf_th=0.7,
                                 nms_th=0.2,
                                 segmentation_th=0.7)

    im = cv2.imread(str(DATA_DIR / 'example.png'))
    coals = model.predict(im)
    test_fractions = [coal.get_fraction() for coal in coals]

    # plot histogram of the fractions
    fig2plot = create_histogram(test_fractions, figsize=(4, 4))
    st.pyplot(fig2plot)
