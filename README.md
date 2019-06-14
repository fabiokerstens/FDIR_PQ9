# FDIR_PQ9

## Purpose
Delft University is currently developing the DELFI-PQ, a 3U pocketcube spacecraft. The DELFI-PQ has to survive the
space environment througout its mission duration in low Earth orbit. An effect of this environment is radiation, which
can cause harm to the spacecraft electronics. Large spacecraft often rely on radiation hardened electronics to 
mitigate this risk, at the cost of significantly increasing the mission cost. Most micro and pico spacecraft like the 
DELFI-PQ rely on commercial-off-the-shelve electronics and sensors, to make the project more affordable. Therefore, in
the present work a open-source simulation platform is build to simulate Single Event Upsets (SEU) due to radiation.

Although work has already been done on this in the past, what is new to this repository is that it includes the DELFI-PQ
PQ9 communication protocol for the simulation of SEUs. Earlier iterations of the SEU simulation tool, such as 
[Delfi-PQ_FDIR](https://github.com/JochimM/Delfi-PQ_FDIR) and [Delfi-PQ_FDIR_Evaluator](https://github.com/FlyOHolic/Delfi-PQ_FDIR_Evaluator), 
are used in the present work as a reference to build upon. 


## Background Information


### Modelling Single Event Upsets

### PQ9 Protocol
The DELFI-PQ uses the PQ9 communication protocol, as is displayed in the figure below. The PQ9 protocol sends packets of at least 5 bytes and at most 260 bytes. The protocol is used for both transmitting and receiving data. 

![pq9_protocol](https://github.com/fabiokerstens/FDIR_PQ9/tree/master/Figures_README/pq9_protocol.JPG)

The first byte contains the destination adress, e.g. the OBC or the ADCS subsystem. The second byte indicates the total length of the message in bytes (this is limited between 0-255 bytes based on the 8-bit architecture). The third byte contains the source adress, e.g. the OBC. 
After the bytes containing the message, the last two bytes are allocated for Cyclic Reduncancy Checking (CRC), which can detect if an error has occured in the packet structure. 

## Design

## How to Use  

### Prerequisites
To run the FDIR code, one requires the MSP432P401R LaunchPad, as well as a USB to micro-USB cable with a computer, running either LINUX or WINDOWS.
In the present work, we use WINDOWS.

### Hardware Setup
To setup the system, connect the LaunchPad to the computer via one of the USB ports. Open WINDOWS PowerShell in administrator mode and locate the repository:

```
cd C:\...\FDIR_PQ9
```

where the dots are to be replaced with the repository directory. Next, run the following commands to deploy the EGSE API from the JAVA target:

```
cd PQ9EGSE
java -jar target/PQ9EGSE-0.1-SNAPSHOT-jar-with-dependencies.jar
```

Now, one can open a webbrowser to visit localhost:8080 to visualize the API and run commands to the board. 

## Results

## Issues Encountered 

## Recommendations