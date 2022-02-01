# 1. Introduction  

## 1.1 Document Purpose

This document has been conceived with the following objectives :

- To define the product perspective and state the problem the product solves
- To serve as a connection point for marketing, developers and business
- To be a pointing vector at the developing stage
- To help the team to understand the reasons behind the product

## 1.2 References

**N/A yet**

# 2. Problem Statement

The problem of

- No process of separation of coal fractions
- No algorithm which makes a decision if grinding is necessary

affects

- EVRAZ

causing the impact of

- inefficient usage of time, power, and equipment
- low quality of produced steel

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

The product is the complex system for the coal fraction analysis on the conveyor
which based on AI algorithms (CV, CNNs, ML).

## 4.1 Brief Description of the Product

The following block diagram describes the structure of the product

<p float="center">
    <img src="/docs/diagrams/general_block_diagram.png" width="500"/>
</p>

## 4.2 Product Features & Abilities

- Ability to separate coal grains in the image
- Ability to calculate the size of a grain
- Ability to detect "garbage" on the conveyor
- Ability to perform analysis and produce the necessary statistics (histograms, graphs, etc)
- Ability to decide if grinding is necessary
- Ability of using WEB interface as a real time monitoring service

## 4.3 Assumptions & Dependencies

**N/A yet**

## 4.4 Cost & Pricing

- Cameras
- Transferring infastructure (wires, commutators, switches, routers)
- Servers
- Software Development

# 5. Main Functionality

## 5.1 Video Data Analysis 

### 5.1.1 Separation of Coal Grains

### 5.1.2 Statistics

## 5.2 User Interface & Visualization

# 6. Other Requirements

## 6.1 Applicable Standards

Transfer protocols :

- HTTP
- RTCP

## 6.2 System Requirements

**N/A yet**

## 6.3 Licensing & Installation

**N/A yet**

## 6.4 Performance Requirements

- Real time video analysis (~10 fps)

# 7. Documentation Requirements

Documentation must consist of at least 3 documents:

- README.md
- SRS
- User's guide

## 7.1 README.md

This file describes the purpose of the repo and provides the perspective view of the product.

It should answer the following question:

- What is it?
- What is it for?
- How to install and run?

## 7.2 System Requirements Specification

## 7.3 User's Guide

## 7.4 Help 

WEB interface should have:

- Tooltips
- Popup hints

## 7.5 Installation & Configuration

**N/A yet**

# 8. Glossary

- [coal fraction](#coal-fraction)
- [coal grain](#coal-grain)
- [conveyor](#conveyor)
- [evraz](#evraz)
- [production operator](#production-operator)

## 8.1 coal fraction

## 8.2 coal grain

## 8.3 conveyor

## 8.4 evraz

## 8.5 production operator 
