# Introduction

## Purpose of Document

This is a System Requirements Specification document for the coal composition control system in EVRAZ. EVRAZ is a global steel
and mining company and the leading producer of infrastructure steel products. At some point of the production process it must be
decided if the coal has to be ground. This project is intended to build a system that would be able to make this decision or at
least to delegate this task to a production operator along with providing the information which is necessary _and
sufficient_ to decide correctly.

This document describes objectives and goal of the project. Also it describes the functional requirements
 and software architecture which the implementation of the target system is based on.

## Document Conventions

This document uses the following conventions

- The uppercase words MUST and MUST NOT are reserved exclusively for stating rules which must be followed in order the target
system to be accepted;
- The uppercase words SHOULD and SHOULD NOT are reserved exclusively for stating suggestions which are desirable but not essential
to follow;

# Overall Description

# Functional Requirements

## High Priority

1. The system MUST be able to detect separate coal pieces in the image;
2. The system MUST be able to calculate the size of detected pieces;
3. The system MUST be able to create a "real-time" statistics: the coal size distribution displayed as a histogram;
4. The system MUST provide a WEB interface for a production operator to monitor the coal composition in real-time;

## Medium Priority

### Tests

1. The system SHOULD have

### Research

## Low Priority

# Non-Functional Requirements

## Arrangement & Organization

- The project MUST have a remote repository containing
- The work on the project SHOULD be organized with the aim of a task management service (like _Trello_ or others).

## Performance Requirements

- Latency between the conveyor and the picture the operator sees MUST NOT exceed 10 sec.

## Safety Requirements

## Online user Documentaation and Help

### WEB Interface

## Purchased Components

- Video cameras (one camera for one conveyor);
- Transferring infastructure (wires, commutators, switches, routers);
- Servers.

## Documentation Requirements

Documentation must consist of at least 3 documents:

- README.md
- SRS
- User's guide

### README.md

This file describes the purpose of the repo and provides the perspective view of the product.

It should answer the following question:

- What is the product?
- What is the purpose of the product?
- How to use the product?

## System Requirements Specification

This document.

## User's Guide

# The Use Case Model