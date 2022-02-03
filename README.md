# coal-composition-control

## Installation
From source:
```
git clone https://github.com/comptech-winter-school/coal-composition-control
cd coal-composition-control
pip install -r requirements.txt
python scripts/get_data.py
python scripts/get_weights.py
```

Docker:
```
git clone https://github.com/comptech-winter-school/coal-composition-control
cd coal-composition-control
docker build . -t coal
docker run --name coal-container -it coal

```

## Research notebooks

1. [Semantic segmentation](https://colab.research.google.com/drive/1HrIuBNUtr-K0jktEsmTXYDOZdR7B6iNi?usp=sharing)