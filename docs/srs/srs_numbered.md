# 1. Introduction

## 1.1 Purpose of Document

This is a System Requirements Specification document for the coal composition control system in EVRAZ. EVRAZ is a global steel
and mining company and the leading producer of infrastructure steel products. At some point of the production process it must be
decided if the coal has to be ground. This project is intended to build a system that would be able to make this decision or at
least to delegate this task to a production operator along with providing the information which is necessary _and
sufficient_ to decide correctly.

This document describes objectives and goal of the project. Also it describes the functional requirements
 and software architecture which the implementation of the target system is based on.

## 1.2 Document Conventions

This document uses the following conventions

- The uppercase words MUST and MUST NOT are reserved exclusively for stating rules which must be followed in order the target
system to be accepted;
- The uppercase words SHOULD and SHOULD NOT are reserved exclusively for stating suggestions which are desirable but not essential
to follow;

# 2. Overall Description

# 3. Functional Requirements

## 3.1 High Priority

1. The system MUST be able to detect separate coal pieces in the image;
2. The system MUST be able to calculate the size of detected pieces;
3. The system MUST be able to create a "real-time" statistics: the coal size distribution displayed as a histogram;
4. The system MUST provide a WEB interface to monitor the coal composition in real-time:
 - it MUST display the area of the conveyor recorded;
 - it MUST display the results of the object detection algorithm (e.g. by drawing the contour of a coal piece detected);
 - it MUST display the coal size distribution.

## 3.2 Medium Priority

### 3.2.1 Tests

1. The system SHOULD be accompanied by tests which could be used to validate correct usage on a specific
OS or/and architecture.

### 3.2.2 Research

## 3.3 Low Priority

# 4. Non-Functional Requirements

## 4.1 Arrangement & Organization

1. The project MUST have a remote repository that MUST contain final code;
2. The work on the project SHOULD be organized with the aim of a task management service (like _Trello_ or others).

## 4.2 Performance Requirements

- Latency between the conveyor and the picture the operator sees MUST NOT exceed 10 sec.

## 4.3 Safety Requirements

## 4.4 Online user Documentaation and Help

### 4.4.1 WEB Interface

## 4.5 Purchased Components

- Video cameras (one camera for one conveyor);
- Transferring infastructure (wires, commutators, switches, routers);
- Servers.

## 4.6 Documentation Requirements

Documentation must consist of at least 3 documents:

- README.md;
- SRS (this document);
- User's guide.

### 4.6.1 README.md

This file describes the purpose of the repo and provides the perspective view of the product.

It should answer the following question:

- What is the product?
- What is the purpose of the product?
- How to use the product?

## 4.7 System Requirements Specification

This document.

## 4.8 User's Guide

# 5. The Use Case Model
