# FDIR_PQ9

## Background Information





## Prerequisites
To run the FDIR code, one requires the MSP432P401R LaunchPad, as well as a USB to micro-USB cable with a computer, running either LINUX or WINDOWS.
In the present work, we use WINDOWS.

## Hardware Setup
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


## Packet Configuration
The DELFI-PQ uses the PQ9 communication protocol, as is displayed in the figure below. The PQ9 protocol sends packets of at least 5 bytes and at most 260 bytes. The protocol is used for both transmitting and receiving data. 

![alt text](https://github.com/fabiokerstens/FDIR_PQ9/tree/master/Figures_README/pq9_protocol.JPG)

The first byte contains the destination adress, e.g. the OBC or the ADCS subsystem. The second byte indicates the total length of the message in bytes (this is limited between 0-255 bytes based on the 8-bit architecture). The third byte contains the source adress, e.g. the OBC. 
After the bytes containing the message, the last two bytes are allocated for Cyclic Reduncancy Checking (CRC), which can detect if an error has occured in the packet structure. 

## Recommendations