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

<p align="center">
  <img src="https://github.com/fabiokerstens/FDIR_PQ9/tree/master/Figures_README/memory_allocation.JPG">
</p>

In the present work we only model SEUs in the SRAM of the board, which located in 0x0100000 up to 0x01100000 (1,048,576 
up to 17,825,792) and in 0x2000000 up to 0x3FFFFFFF (33,554,432 up to 53,687,091). 

[old range]
Here, the effects of SEUs in the SRAM shall be considered, which for MSP432 is located in memory address 
range 0x2000 0000 to 0x2010 0000. 


### Error Determination
After errors are introduced in the system, it is of interest if these errors indeed propagate through the system or if
the FDIR system sucesfully resolves the error. After introducing a SEU in the memory, we distinguish four different 
errors:

* Corrupted data, corrected by the on-board FDIR (voting etc.). 
* Corrupted data, not corrected by the on-board FDIR.
* Freeze of the system, corrected by the on-board FIDR (watchdog timer).
* Freeze of the system, not corrected by the FDIR. 

Of course, the last state is one we do want to prevent for space missions, as this could potentially mean the loss of 
the systen, as in this state no communication with the vehicle is possible anymore, without a reset of the software. 

The latter two errors are easy to detect with the SEU algorithm. After a freeze of the system has occured, the board 
will no long transmit packets and does not respond to software inputs anymore. This can only be resolved by manually 
pressing the reset button on the board, as no watchdog timer is implemented in the on-board software used in the present
work. 

However, decting corrupted data is much harder, as this requires a reference to compare the data packets with. For this
we first need to get a better understanding of the communication protocol used on the DELFI-PQ, the PQ9 protocol. The 
PQ9 protocol sends data in the form of packets, where the minimum packet length is 5 bytes and the maximum packet length
is 255 bytes, based on the 8-bit architecture. The first byte contains the receiver to which the packet is sent, 
the second byte the size of the message transmitted, the third byte contains the transmitter and finally the last two 
bytes contain a Cyclic Redundancy Check, which is used to verify if errors in the message have occured during tranmission.
A schematic overview of a packet for the housekeeping debug service is shown below, where the message is highlighted:

<p align="center">
  <img src="https://github.com/fabiokerstens/FDIR_PQ9/tree/master/Figures_README/debug_packet.PNG">
</p>

The message contains the housekeeping information of the particular subsystems of DELFI-PQ. The output in the DEBUG 
mode is mainly constant, but also consists of some variable bytes (bytes which change over time). The decimal values 
for the constant bytes when invoking a DEBUG housekeeping request are shown in the figure above. All bytes with a 
variable value can be computed in PYTHON, and are either integer counters or timer values. Once these variable values
are computed, they can be used to create a reference message, together with the constant value bytes. This constructed 
reference message can in term be used to compare against the received message to check for corrupted data errors. 

We assume that during the transmission no errors in the data are introduced, and that the errors that are introduced
during the tranmission are corrected for by the Cyclic Redundancy Check built in the packet. 

It should be noted that this comparison method works only for simple data packets, such as the DEBUG housekeeping request.
This is because all variables in the DEBUG subsystem are well predictable. For other subystems, this becomes more tricky
since the data stored in the packets can be highly variable in time, and non-predictable (e.g. the voltage on a battery
of the EPS subsystem). 




## How to Use  
### Prerequisites
To transmit or receive data to or from the Delfi-PQ, the the following items are required:

* Computer running on either Windows or LINUX, with **Python 2.7** installed. 
* Texas Instruments [MSP432P401R LaunchPad](http://www.ti.com/tool/MSP-EXP432P401R)
* Micro USB to USB C cable. 
* Delfi-PQ subsystems (if being tested). 

### Hardware Overview
Testing of the FDIR of the different subsystems on-board of Delfi-PQ can be done in a modular way, by adding and removing different subsystems to the test environment, as shown in the figure below. 

<p align="center">
  <img src="https://github.com/fabiokerstens/FDIR_PQ9/tree/master/Figures_README/flatsat_overview.png">
</p>

First, the user can select the subsystems to test the FDIR from, by attaching different Delfi-PQ subsystems to to FLATSAT. Communication is done via the RS-485 serial interface. The FLATSAT is a developer board used to connect the Delfi-PQ subsystems to the computer for validation testing. In the present work, the Texas Instruments LaunchPad is used as the FLATSAT interface. Commnication with the computer is done via USB serial. 

On the computer one uses the EGSE application programing interface to transmit and receive data to the Delfi-PQ, via the FLATSAT. Outside the the EGSE GUI, in which the user can commmunicate the Delfi-PQ with in GUI inveronment, the user can also use Python to communicate with Delfi-PQ. The latter gives more flexibility in the testing software that can be used, since the EGSE GUI has limited testing options available. 


### Software Setup
Download this repository and store it on your computer. Connect the FLATSAT to the computer using the micro USB to USB C cable (a green LED should now blink on the board). When using Windows, open Windows PowerShell in administrator mode and run the following command:
```
cd C:\...\FDIR_PQ9\PQ9EGSE
java -jar target/PQ9EGSE-0.1-SNAPSHOT-jar-with-dependencies.jar
```
where the dots are to be replaced with the repository directory. When using LINUX, open the terminal and run the following command:
```
cd C:\...\FDIR_PQ9\PQ9EGSE
sudo java -jar target/PQ9EGSE-0.1-SNAPSHOT-jar-with-dependencies.jar
```

Both cases will load the EGSE application programing interface. This can now be accessed by going to the internet browser and  typing in the adress bar:
```
localhost:8080
```

This will bring you to the EGSE GUI, as shown in the picture below. In the header, define the serial port used by the FLATSAT (COM7 in the figure). Note that one of the ports if for serial communication, and the other only for programming. 

<p align="center">
  <img src="https://github.com/fabiokerstens/FDIR_PQ9/tree/master/Figures_README/egse.gui.png">
</p>

One can test if a sucesfull connection is obtained by sending a ping to **DEBUG**. In the DataLog on the left side of the screen, a transmitted message should now prompt in yellow, as well as a received message in black. 

Running the Python testing software is done via the **client.py**. One can open any Python 2.7 editor (e.g. IDLE) to open this file and run it. Additionally, in one can also run the script diretly via Windows Powershell or LINUX terminal when using the command:

```
cd C:\...\FDIR_PQ9\PQ_integretion_testing
python client.py
```



In both the EGSE software and the python files, the memory address must be input in decimal, for which the range is 
536,870,912 to  537,9191,488.


## Results

<p align="center">
  <img src="https://github.com/fabiokerstens/FDIR_PQ9/blob/master/Figures_README/error_graph.png">
</p>

## Issues Encountered 
When a SEU is sent to some particular memory locations, the microcontroller fully "freezes" and communication with the
board is no longer possible. This state could only be recovered from by pressing the physical reset button on the board.
However, this is not practical in reality if one wants to test the full memory spectrum. Therefore, it is recommended
to implement a watchdog timer on the board to let it reset by itself if no response is detected. 


## Recommendations
* Currently, the testing software is only compatible with Python 2.7. This version is already qutie old and noweadays Python 3.0 is used for most programming applications. Therefore, to keep the testing software future-proof, it is recommended to make the code compatible for both Python 2.7 and Python 3.
