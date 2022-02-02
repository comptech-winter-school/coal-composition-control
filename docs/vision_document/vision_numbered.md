# 1. Introduction  

## 1.1 Document Purpose

This document has been conceived with the following objectives :

- To define the product perspective and state the problem the product solves
- To serve as a connection point for marketing, developers and business
- To be a pointing vector at the developing stage
- To help the team to understand the reasons behind the product

## 1.2 References

[Conveyor definition](https://www.seek.com.au/career-advice/role/production-operator)

[Production operator definition](https://en.wikipedia.org/wiki/Conveyor_system)

[EVRAZ definition](https://www.evraz.com/en/company/)

**N/A yet**

# 2. Problem Statement

The problem of

- No process of separation of coal fractions
- No algorithm which makes a decision if grinding is necessary

affects

- EVRAZ

causing the impact of

- inefficient usage of time, power, and equipment
- low quality of produced steel if grinding was necessary but wasn't performed

# 3. User Description

## 3.1 Users

| Title | Role | Description of Use |
|:---   |:--- |:--- |
| EVRAZ production operators | User of WEB interface | Monitoring |

## 3.2 User Environment

| Key | Value |
| :---  | :--- |
| Number of users per task | Usually 1 |
| Requirements | PC, Internet connection, Browser |

# 4. Product Overview

The product is the system for the coal fraction analysis on the conveyor.

## 4.1 Brief Description of the Product

The product is supposed to be a solution to the abovementioned problem:

0. A fragment of the conveyor is recorded by a video-camera
1. The recorded data transfers over the network to the server
2. Transferred data is being processed by the AI-based algorithm (the main part of the product)
3. The result of the previous step is being processed yet to produce important statistics (histograms, graphs, etc)
4. The data obtained in the previous step is visualized in the WEB interface
5. The operator decides if grinding is necessary

The following block diagram describes the process

<p float="center">
    <img src="/docs/diagrams/general_block_diagram.png" width="500"/>
</p>

## 4.2 Product Features & Abilities

- Ability to detect separate coal pieces in the image
- Ability to calculate the size of a piece
- Ability to perform analysis and produce necessary statistics (histograms, graphs, etc)
- Ability of using WEB interface as a real time monitoring service
- Ability to decide if grinding is necessary

## 4.3 Cost & Pricing

- Cameras
- Transferring infastructure (wires, commutators, switches, routers)
- Servers
- Software Development

## 4.4 Alternatives

Another solution to the problem would be to develop and integrate a subsystem
into the existing one which would _separate the larger coal fraction from
the entire stream on the conveyor followed by grinding the larger parts_:

<p float="center">
    <img src="/docs/diagrams/alternative.png" width="500"/>
</p>

# 5. Main Functionality

## 5.1 Video Data Analysis 

### 5.1.1 Separation of Coal Grains

### 5.1.2 Statistics

## 5.2 User Interface & Visualization

# 6. Other Requirements

## 6.1 System Requirements

**N/A yet**

## 6.2 Licensing & Installation

**N/A yet**

## 6.3 Performance Requirements

- Real time video analysis (~10 fps)

# 7. Documentation Requirements

Documentation must consist of at least 3 documents:

- README.md
- SRS
- User's guide

## 7.1 README.md

This file describes the purpose of the repo and provides the perspective view of the product.

It should answer the following question:

- What is the product?
- What is the purpose of the product?
- How to use the product?

## 7.2 System Requirements Specification

**N/A yet**

## 7.3 User's Guide

**N/A yet**

## 7.4 Help 

The WEB interface should have:

- Tooltips
- Popup hints

## 7.5 Installation & Configuration

**N/A yet**

# 8. Glossary

- [coal fraction](#coal-fraction)
- [conveyor](#conveyor)
- [evraz](#evraz)
- [grinding](#grinding)
- [production operator](#production-operator)

## 8.1 coal fraction

<sub>in russian: _фракция угля_</sub>

is a category of classification pieces of coal by their size

## 8.2 conveyor

<sub>in russian: _конвейер_</sub>

is a common piece of mechanical handling equipment that moves materials from one location to another.

## 8.3 evraz

<sub>in russian: _ЕВРАЗ_</sub>

is a global steel and mining company and the leading producer
of infrastructure steel products with low-cost production along the value chain.

## 8.4 grinding

<sub>in russian: _помол_</sub>

is the reduction of something to small particles or powder by crushing it.

## 8.5 production operator 

<sub>in russian: _оператор на производстве_</sub>

is an individual who operates equipment to assist with the assembling,
manufacturing, processing and packaging of items along a production line.
