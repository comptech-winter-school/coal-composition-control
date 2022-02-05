# Coal Composition Control System 

This is an implementation of the [_Coal Composition Control System_](https://comptechschool.com/2022/projects/coal_cv) project of the [_CompTechSchool 2022_](https://comptechschool.com/homepage).

The AI-based system for the coal fraction analysis on the conveyor in real time.

## Structure of this Repo

- [docs](docs)
- [src](src)
- [scripts](scripts)
- [data](data)
- [weights](weights)
- [train](train)

## Installation & Run

## Requirements

- python3
- pip

Clone the repo and change to the project root directory:

```
git clone https://github.com/comptech-winter-school/coal-composition-control
cd coal-composition-control
```

Create an image and run:
```
docker build . -t coal
docker run --name coal-container -it coal
```

After you've done with the demo stop and remove all running containers and images:

```
docker system prune -a 
```

## Research notebooks

1. [Semantic segmentation](https://colab.research.google.com/drive/1HrIuBNUtr-K0jktEsmTXYDOZdR7B6iNi?usp=sharing)
2. [Object detection](https://colab.research.google.com/drive/1V3NdYkR7gqTTmzoc7LXHQPv0L4twMpGm?usp=sharing)
3. [Instance segmentation with Mask R-CNN](https://colab.research.google.com/drive/1-epExQsCQUvenJD_c4E4Ji-ZeDteg_z6?usp=sharing#scrollTo=T2ZmpAt29XzK)
4.

## Team 

| [<img src="https://avatars.githubusercontent.com/u/46760758?v=4" width="75px;"/>](https://github.com/Pashtetickus)<br>[Pashtetickus](https://github.com/Pashtetickus)</br> | [<img src="https://avatars.githubusercontent.com/u/43125377?v=4" width="75px;"/>](https://github.com/asromahin) <br>[asromahin](https://github.com/asromahin) | [<img src="https://avatars.githubusercontent.com/u/41781097?v=4" width="75px;"/>](https://github.com/0x0000dead)<br>[0x0000dead](https://github.com/0x0000dead) | [<img src="https://avatars.githubusercontent.com/u/69035428?v=4" width="75px;"/>](https://github.com/JI411)<br>[JI411](https://github.com/JI411) | [<img src="https://avatars.githubusercontent.com/u/18001464?v=4" width="75px;"/>](https://github.com/IldarMurzagaleev)<br>[Dr_Under](https://github.com/IldarMurzagaleev)</br> | [<img src="https://avatars.githubusercontent.com/u/26169258?v=4" width="75px;"/>](https://github.com/LRDPRDX)<br>[LRDPRDX](https://github.com/LRDPRDX) |
| ---   | --- | --- | --- | --- | --- |
| Павел Данилов | Александр Ромахин | Сергей Ванданов | Александр Лекомцев | Ильдар Мурзагалеев | Богдан Сикач |
| Team Leader, <br>Developer</br> | Project Manager | Data Analyst, <br>Developer</br>| Data Analyst, <br>Developer</br> | Data Analyst, <br>Developer</br> | Technical Writer |
