# coal-composition-control

## Installation

### Docker (recommended):
```
git clone https://github.com/comptech-winter-school/coal-composition-control
cd coal-composition-control
docker build . -t coal
docker run --rm --name coal-container -it coal
```
чтобы удалить все образы и контейнеры
```
docker system prune -a 
```

### From source:
```
git clone https://github.com/comptech-winter-school/coal-composition-control
cd coal-composition-control
pip install -r requirements.txt
streamlit run startup.py
```

## Research notebooks

1. [Semantic segmentation](https://colab.research.google.com/drive/1HrIuBNUtr-K0jktEsmTXYDOZdR7B6iNi?usp=sharing)
2. [Object detection](https://colab.research.google.com/drive/1V3NdYkR7gqTTmzoc7LXHQPv0L4twMpGm?usp=sharing)
3. [Instance segmentation with Mask R-CNN](https://colab.research.google.com/drive/1-epExQsCQUvenJD_c4E4Ji-ZeDteg_z6?usp=sharing#scrollTo=T2ZmpAt29XzK)
4. [Instance segmentation with Yolact](https://colab.research.google.com/drive/1UM3GE05vaBJJIx657Y9X2RDoQgLaAjv6?usp=sharing)
5. [Classic edge detectors](https://colab.research.google.com/drive/1qqCTqAYwOOr5AGAJ8_fIrWTmNs8PkhTp?usp=sharing)