# Introduction  

## Document Purpose

This document has been conceived with the following objectives :

- To define the product perspective and state the problem the product solves
- To serve as a connection point for marketing, developers and business
- To be a pointing vector at the developing stage
- To help the team to understand the reasons behind the product

## References

**N/A yet**

# Problem Statement

The problem of

- No process of separation of coal fractions
- No algorithm which makes a decision if grinding is necessary

affects

- EVRAZ

causing the impact of

- inefficient usage of time, power, and equipment
- low quality of produced steel if grinding was necessary but wasn't performed

# User Description

## Users

| Title | Role | Description of Use |
|:---   |:--- |:--- |
| EVRAZ production operators | User of WEB interface | Monitoring |

## User Environment

| Key | Value |
| :---  | :--- |
| Number of users per task | Usually 1 |
| Requirements | PC, Internet connection, Browser |

# Product Overview

The product is the system for the coal fraction analysis on the conveyor
which based on AI algorithms (CV, CNNs, ML).

## Brief Description of the Product

The following block diagram describes the structure of the product

<p float="center">
    <img src="/docs/diagrams/general_block_diagram.png" width="500"/>
</p>

## Product Features & Abilities

- Ability to separate coal grains in the image
- Ability to calculate the size of a grain
- Ability to detect "garbage" on the conveyor
- Ability to perform analysis and produce the necessary statistics (histograms, graphs, etc)
- Ability to decide if grinding is necessary
- Ability of using WEB interface as a real time monitoring service

## Cost & Pricing

- Cameras
- Transferring infastructure (wires, commutators, switches, routers)
- Servers
- Software Development

## Alternatives

Another solution to the problem would be to develop and integrate a subsystem
in the main procedure which would __separate the coal fraction that have to be ground from
the entire stream on the conveyor__:

<p float="center">
    <img src="/docs/diagrams/alternative.png" width="500"/>
</p>


# Main Functionality

## Video Data Analysis 

### Separation of Coal Grains

### Statistics

## User Interface & Visualization

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

- What is it?
- What is it for?
- How to install and run?

## System Requirements Specification

## User's Guide

## Help 

WEB interface should have:

- Tooltips
- Popup hints

## Installation & Configuration

**N/A yet**

# Glossary

- [coal fraction](#coal-fraction)
- [coal grain](#coal-grain)
- [conveyor](#conveyor)
- [evraz](#evraz)
- [grinding](#grinding)
- [production operator](#production-operator)

## coal fraction

## coal grain

## conveyor

## evraz

## grinding

## production operator 