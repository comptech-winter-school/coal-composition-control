# Documentation of the "Coal Composition Control" project of the CompTech School 2022

This site hosts documentation on the "Coal Composition Control" project and is intended to provide a convenient way to rate the
work of a technical writer.

# Technical Writer

|||
| :---: |:---: |
|<p float="center"><img src="diagrams/bogdan.png" width="150px;"/>|<br>Name: Sikach Bogdan Igorevich</br><br>email: paradox1859@gmail.com</br><br>GitHub: [LRDPRDX](https://github.com/LRDPRDX)</br><br>Telegram: @lrdprdx</br>|

# The Artifacts

* [System Requirements Specification](srs/srs_numbered.md)
* [User's Guide](users_guide/users_numbered.md)
* [README](https://github.com/comptech-winter-school/coal-composition-control) (link to the repo)

# Vision Document

## 1.1 Document Purpose

This document has been conceived with the following objectives:

- To define the product perspective and state the problem the product solves.
- To serve as a connection point for marketing, developers and business.
- To be a pointing vector at the developing stage.
- To help the team to understand the reasons behind the product.

## 1.2 References

1. [Conveyor definition](https://www.seek.com.au/career-advice/role/production-operator)

2. [Production operator definition](https://en.wikipedia.org/wiki/Conveyor_system)

3. [EVRAZ definition](https://www.evraz.com/en/company/)

# 2. Problem Statement

_Coal_ is a necessary component for _steel production_ - the primary business direction of EVRAZ.
If coal fractions are large the coal must be ground.

The problem of

- no process of separation of coal fractions
- no algorithm which makes a decision if grinding is necessary

affects

- EVRAZ

causing the impact of

- inefficient usage of time, power, and equipment
- low quality of produced steel if grinding was necessary but wasn't performed

# 3. Product Overview

The product is a system for the coal fraction analysis on the conveyor.

## 3.1 Brief Description of the Product

The product is supposed to be a solution to the abovementioned problem:

1. A fragment of the conveyor is recorded by a video-camera.
2. The recorded data transfers over the network to the server.
3. Transferred data is being processed by the AI-based algorithm (the main part of the product).
4. The result of the previous step is being processed yet to produce important statistics (histograms, graphs, etc).
