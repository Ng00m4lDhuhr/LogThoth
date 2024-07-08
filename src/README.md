# Implementation
This folder contains all the code of the tool. the entire program shouldn't require any references to other directories.

# Modules
The project has modular architecture. cross dependencies are disencouraged. 
## Interface
This modules contains an abstracted classes to interact with complex systems and data. It should not provide any functional feature.
## Timeline
Tree-like structure that allows a good range of operations on the timeline while maintaining sorting by date.
## Core
Modules that implements the very pillar functions of the tool. Code here should lean to functional programming.
