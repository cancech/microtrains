# microtrains

Micropython library dedicated to providing capabilities that can be run on a Raspeberry Pi Micro, to add additional automation and "animation" to a model train layout. It does not include anything for controlling the trains per say, but rather features that would be on the layout yet separate from the train proper.

## Organization

Divided into modules, with each module containing a single aspect of the functionality. Existing modules and their capabilities are as follows.

* *[common](common)* - contains shared and common functionality, which is not specific to any concrete capability, but rather shared among
* *[lights](lights)* - contains capabilities relating to controlling and managing various lights via GPIO pins
* *tests* - contains unit tests for verifying the functionality of what is within each module
