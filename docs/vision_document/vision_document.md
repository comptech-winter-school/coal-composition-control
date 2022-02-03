# Introduction  

## Document Purpose

This document has been conceived with the following objectives:

- To define the product perspective and state the problem the product solves.
- To serve as a connection point for marketing, developers and business.
- To be a pointing vector at the developing stage.
- To help the team to understand the reasons behind the product.

## References

1. [Conveyor definition](https://www.seek.com.au/career-advice/role/production-operator)

2. [Production operator definition](https://en.wikipedia.org/wiki/Conveyor_system)

3. [EVRAZ definition](https://www.evraz.com/en/company/)

# Problem Statement

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

# Product Overview

The product is a system for the coal fraction analysis on the conveyor.

## Brief Description of the Product

The product is supposed to be a solution to the abovementioned problem:

0. A fragment of the conveyor is recorded by a video-camera.
1. The recorded data transfers over the network to the server.
2. Transferred data is being processed by the AI-based algorithm (the main part of the product).
3. The result of the previous step is being processed yet to produce important statistics (histograms, graphs, etc).
4. The data obtained in the previous step is visualized in the WEB interface.
5. The operator decides if grinding is necessary.

The following block diagram describes the process

![diag](../diagrams/general_block_diagram.png)

## Product Features & Abilities

- Ability to detect separate coal pieces in the image.
- Ability to calculate the size of a piece.
- Ability to perform analysis and produce necessary statistics (histograms, graphs, etc).
- Ability of using WEB interface as a real time monitoring service.
- Ability to decide if grinding is necessary.

## Cost & Pricing

- Cameras.
- Transferring infastructure (wires, commutators, switches, routers).
- Servers.
- Software Development.

## Alternatives

Another solution to the problem would be to develop and integrate a subsystem
into the existing one which would _separate the larger coal fraction from
the entire stream on the conveyor followed by grinding the larger coal pieces_:

![alternative](../diagrams/alternative.png)

But this approach is accompanied by the following difficulties:

- Developing and integration of such a system may be extremely expensive.
- The entire production process would have to be suspended for a long time.

# Main Functionality

The most important content of the product is _software_ which can be divided into 3 groups:

- Computer vision.
- Data analysis.
- User interface.

![software](../diagrams/software.png)

## Computer Vision 

This part consists of AI-driven algorithms and techniques of image analysis, and intended to
accomplish the following tasks:

- Locate separate coal pieces in a photo (a video frame).
- Isolate a coal piece from its surroundings (e.g. finding the pixel mask of a piece).
- Prepare data for further analysis.

## Data analysis

This part is intended to analyze the data produced by the CV-part
and to construct the figures of merit based on which the resulting decision is made.

## User Interface & Visualization

This part is a point of interraction between the user and the product. And

- Show the results of the CV-part in the recorded video (e.g. by drawing contours of the detected coal pieces).
- Display statistics (histograms, time graphs).
- (if necessary) Provide tools to interract with the equipment.

# User Description

## Users

| Title | Role | Description of Use |
|:---   |:--- |:--- |
| EVRAZ production operators | User of WEB interface | Monitoring the coal composition |

## User Environment

| Key | Value |
| :---  | :--- |
| Number of users per task | Usually 1 |
| Requirements | PC, Internet connection, Browser |

# Other Requirements

## System Requirements

**N/A yet**

## Licensing & Installation

**N/A yet**

## Performance Requirements

- Real time video analysis (~10 fps)

# Documentation Requirements

Documentation must consist of at least 3 documents:

- README.md
- SRS
- User's guide

## README.md

This file describes the purpose of the repo and provides the perspective view of the product.

It should answer the following question:

- What is the product?
- What is the purpose of the product?
- How to use the product?

## System Requirements Specification

## User's Guide

**N/A yet**

# Installation & Configuration

# Glossary

- [coal fraction](#coal-fraction)
- [conveyor](#conveyor)
- [evraz](#evraz)
- [grinding](#grinding)
- [production operator](#production-operator)

## coal fraction

<sub>in russian: _фракция угля_</sub>

is a standardized size of a piece of coal (e.g. large, medium, small)

## conveyor

<sub>in russian: _конвейер_</sub>

is a common piece of mechanical handling equipment that moves materials from one location to another.

## evraz

<sub>in russian: _ЕВРАЗ_</sub>

is a global steel and mining company and the leading producer
of infrastructure steel products with low-cost production along the value chain.

## grinding

<sub>in russian: _помол_</sub>

is the reduction of something to small particles or powder by crushing it.

## production operator 

<sub>in russian: _оператор на производстве_</sub>

is an individual who operates equipment to assist with the assembling,
manufacturing, processing and packaging of items along a production line.
