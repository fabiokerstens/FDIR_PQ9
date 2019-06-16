# FDIR_PQ9

## Purpose
Delft University is currently developing the DELFI-PQ, a 3U pocketcube spacecraft. The DELFI-PQ has to survive the
space environment througout its mission duration in low Earth orbit. An effect of this environment is radiation, which
can cause harm to the spacecraft electronics. Large spacecraft often rely on radiation hardened electronics to 
mitigate this risk, at the cost of significantly increasing the mission cost. Most micro and pico spacecraft like the 
DELFI-PQ rely on commercial-off-the-shelve electronics and sensors, to make the project more affordable. 

Therefore, the purpose of this repository is to present a hardware-in-the-loop simulation which can introduce Single 
Event Upsets (SEU) in the memory, in order to validate the correct function of the FDIR on the spacecraft electronics
on Earth. 


## Design
Although work has already been done on this in the past, what is new to this repository is that it includes the DELFI-PQ
PQ9 communication protocol for the simulation of SEUs. Earlier iterations of the SEU simulation tool, such as 
[Delfi-PQ_FDIR](https://github.com/JochimM/Delfi-PQ_FDIR) and [Delfi-PQ_FDIR_Evaluator](https://github.com/FlyOHolic/Delfi-PQ_FDIR_Evaluator), 
are used in the present work as a reference to build upon. 


### Single Event Upsets
Single Event Upsets (SEU) are a type of recoverable error (soft errors) which origin from ionizing parcles interacting
with the spaccraft electronics. SEUs occur in all Bipololar, CMOS or BiCMOS technologies, except in EEPROM or flash 
EEPROM. In the present work, SEUs are modelled through bitflips in memory cells or registers of the electronics. 
The Texas Instruments MSP432P401R LaunchPad is used to run the onboard commands of the DELFI-PQ. This board has the 
following memory allocation:

![memory_allocation](https://github.com/fabiokerstens/FDIR_PQ9/tree/master/Figures_README/memory_allocation.jpg)

In the present work we only model SEUs in the SRAM of the board, which located in 0x0100000 up to 0x01100000 (1,048,576 
up to 17,825,792) and in 0x2000000 up to 0x3FFFFFFF (33,554,432 up to 53,687,091). 

[old range]
Here, the effects of SEUs in the SRAM shall be considered, which for MSP432 is located in memory address 
range 0x2000 0000 to 0x2010 0000. 


### PQ9 Protocol
The DELFI-PQ uses the PQ9 communication protocol, as is displayed in the figure below. The PQ9 protocol sends packets of at least 5 bytes and at most 260 bytes. The protocol is used for both transmitting and receiving data. 

![pq9_protocol](https://github.com/fabiokerstens/FDIR_PQ9/tree/master/Figures_README/pq9_protocol.JPG)

The first byte contains the destination adress, e.g. the OBC or the ADCS subsystem. The second byte indicates the total length of the message in bytes (this is limited between 0-255 bytes based on the 8-bit architecture). The third byte contains the source adress, e.g. the OBC. 
After the bytes containing the message, the last two bytes are allocated for Cyclic Reduncancy Checking (CRC), which can detect if an error has occured in the packet structure. 



## How to Use  

### Prerequisites
To run the FDIR code, one requires the MSP432P401R LaunchPad, as well as a USB to micro-USB cable with a computer, running either LINUX or WINDOWS.
In the presented work, WINDOWS is used, but the same commands can be used for connection via a LINUX terminal.

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

### Software Setup
With the board connected, and the EGSE software running, python can be used to run commands to the board with the client.py file. This can again be done via PowerShell. First the directory must be changed, and then the file called, with the following commands:

```
cd PQ_integretion_testing
python client.py
```

In both the EGSE software and the python files, the memory address must be input in decimal, for which the range is 
536,870,912 to  537,9191,488.


## Results

## Issues Encountered 
When a SEU is sent to some particular memory locations, the microcontroller fully "freezes" and communication with the
board is no longer possible. This state could only be recovered from by pressing the physical reset button on the board.
However, this is not practical in reality if one wants to test the full memory spectrum. Therefore, it is recommended
to implement a watchdog timer on the board to let it reset by itself if no response is detected. 


## Recommendations
