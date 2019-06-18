# FDIR_PQ9

## 1. Purpose
Delft University of Technology is currently developing the [Delfi-PQ](https://www.tudelft.nl/lr/subsites/delfi-space/delfi-pq/), a 3U PocketCube spacecraft, expected to launch in 2019. Throughout its mission, Delfi-PQ will be in a severe radiation environment in low Earth orbit, which could potentially harm the spacecraft electronics. The radiation effect focussed on in the present work is the Single Event Upset (SEU), which origins from ionizing parcles interacting with the spaccraft electronics. The SEU is a soft error (recoverable) with unpredictable consequences. One of the consequences of SEUs are changes in memory locations, which could result in retrieving incorrect housekeeping data from the spacecraft. 

Clearly SEUs should be corrected for, which is normally done by an on-board Fault Detection, Isolation and Recovery (FDIR) algorithm. FDIR algorithms are vital for the correct in-orbit operation of the Delfi-PQ and hence shall be tested extensively on Earth to validate correct function. For large spacecraft, this is often done by using radiation hardened electronics or by testing the flight computer in a radiation environment. Both these options add a lot of cost to the overal mission, which is often not possible for small spacecraft, such as Delfi-PQ. Therefore, **the purpose of this repository is to simulate SEUs by means of real time fault injection, in an attempt to validate the Delfi-PQ FDIR algorithm**. 

The repository is made open-source and allows students from all over the world to contribute to the project. 


## 2. Design
### 2.1 Literature Overiew
In the past, several attempet were already made on developing to develop a FDIR validation simulation, which have been used throughout this work as a reference. Firstly, [Delfi-PQ_FDIR](https://github.com/JochimM/Delfi-PQ_FDIR), uses an Arduino to simulate the spacecraft. Errors are only injected in the SRAM memory and communication is done via standard USB serial. Error checking is done by asking housekeeping data, which contains the names of the authors as well as the borwein pi approximation. Since both housekeeping parameters are fixed and can be well modelled, the authors can check for errors in the received data. Their simulations oututs a memory map of the memory loction and specific bits in which soft errors (wrong housekeeping data) and hard errors (Arduino crash) occur. 

Another attempt was made in the [Delfi-PQ_FDIR_Evaluator](https://github.com/FlyOHolic/Delfi-PQ_FDIR_Evaluator), where the authors used two Texas Instruments MSP432P401R LaunchPad development boards, which is identical to the development board used in the present work. They use Python to inject error in the SRAM zone of the memory (0x20000000-0x20100000). Their board is programmed to continuously transmit the message "Hello World", which can have a different output if errors are introduced in the board. They distinguish four types of errors of which the two most relevant are: (1) *lockup* in which the boards stops responding, (2) *data corruption* in which the outputted "Hello World" string is corrupted.

### 2.2 Memory Overview
To simulate created errors due to SEUs the approach used in this work injects failures in the memory of the Delfi-PQ. The on-board memory is modelled with the FLATSAT interface or the MSP432P401R LaunchPad, which both have the same microcontroller. The memory map for the particular microcontroller used is shown in the figure below (source: [Texas Instruments](http://www.ti.com/lit/ds/symlink/msp432p401r.pdf)). 

<p align="center">
  <img src="figures/memory_allocation.JPG" width="700">
</p>

Like the previous iterations of the FDIR evalaution software, the errors are only injected in the SRAM region of the board, which is located at 0x20000000-0x20100000 (or at 0x01000000-0x01100000 on the code part, this is the same memory). 

### 2.3 Error Injection
Testing of the FDIR of the different subsystems on-board of Delfi-PQ can be done in a modular way, by adding and removing different subsystems to the test environment, as shown in the figure below. 

<p align="center">
  <img src="figures/flastsat_overview.PNG" width="150">
</p>

Here, the FLATSAT is used for communication between the spacecraft subsystems and computer for testing and debugging. FLATSAT can acces the common bus for every subsystem and provides small processing of the data. Communication between FLATSAT and the subsystems is done via the RS-485 serial interface, and between FLATSAT and the computer via USB serial. On the computer one uses the EGSE application programing interface to transmit and receive data to the Delfi-PQ, via the FLATSAT. The errors can be injected in the SRAM manually via the EGSE GUI or automatically via the **client.py** script witten in Python. The software loop running on the **client.py** file is whon in the flowchart below:

<p align="center">
  <img src="figures/flowchart.png" width="600">
</p>

Every iteration of the loop starts with pinging the target subsystem, and checking if a packet is received back. If for some reason no packet is received, the bus is reset and a new ping command is send the the subsystem. Next, the memory adress is defined in the SRAM memory range defined in the previous section. This is a random process, for which the results are **uniformly distributed - WRITE SOMETHING ABOUT THE RANDOM FUNCTION USED**. 

After the definition of the memory location to inject the fault in, the **FTDebug** function is called. Despite the target memory adress, the function also requires a bit mask and an operator, which can either be *set*, *clear* or *toggle*. These operators essentially perform a bitwise operations with the target byte and the mask byte, as shown in the figure below. 

<p align="center">
  <img src="figures/bitwise_operation.PNG" width="600">
</p>

In the present work, the operator is defined as *and*, with a constant bit mask of 255 (i.e. 0xFFFFFFFF). This command essentially changes the target byte to the value 0xFFFFFFFF and hence injects a fault in the memory. Hereafter, a **housekeeping** request is send to the target subsystem and the Python scripts verifies if two packets have received (one from FTDebug and one from housekeeping). Packets can get lost during a lockup of the system as a result of the fault injection, or due to errors in the transmission, which are filtered out by the Cyclic Redundancy Check (CRC) build in the PQ9 protocol. When the CRC finds an error, the EGSE application programming interface automatically rejects the packet. Hence, when running the **client_adb.py**, no packet will show up. To counteract this, a housekeeping loop is implemented, called, which transmist a housekeeping request op to three times when no packet is received. For more information about the CRC or PQ9 protocol, the reader is referred to the [PQ9 and CS14 Interface Standard](https://dataverse.nl/dataset.xhtml?persistentId=hdl:10411/3V8RUF).

If two packets have come in after sending the housekeeping request, the error determination code is runned, which is explained in more detail in section 2.4. In case only packet came in (from FTDebug), the system automatically request the housekeeping again. If again nog packets comes in, the pakcets are added to the **missing_packets.json** file and the bus is reset. The **missing_packets.json** file ...............


### 2.4 Error Determination
After errors are introduced in the system, it is of interest if these errors indeed propagate through the system or if the FDIR system sucesfully resolves the error. After introducing a SEU in the memory, we distinguish four different errors:

* Corrupted data, corrected by the on-board FDIR (voting etc.). 
* Corrupted data, not corrected by the on-board FDIR.
* Freeze of the system, corrected by the on-board FIDR (watchdog timer).
* Freeze of the system, not corrected by the FDIR. 

Of course, the last state is one we do want to prevent for space missions, as this could potentially mean the loss of the systen, as in this state no communication with the vehicle is possible anymore, without a reset of the software. 

The latter two errors are easy to detect with the SEU algorithm. After a freeze of the system has occured, the board will no long transmit packets and does not respond to software inputs anymore. This can only be resolved by manually pressing the reset button on the board, as no watchdog timer is implemented in the on-board software used in the present work. 

However, decting corrupted data is much harder, as this requires a reference to compare the data packets with. For this we first need to get a better understanding of the communication protocol used on the Delfi-PQ, the [PQ9 protocol](https://dataverse.nl/dataset.xhtml?persistentId=hdl:10411/3V8RUF). The PQ9 protocol sends data in the form of packets, where the minimum packet length is 5 bytes and the maximum packet length is 255 bytes, based on the 8-bit architecture. The first byte contains the receiver to which the packet is sent, 
the second byte the size of the message transmitted, the third byte contains the transmitter and finally the last two bytes contain a Cyclic Redundancy Check, which is used to verify if errors in the message have occured during tranmission. A schematic overview of a packet for the housekeeping debug service is shown below, where the message is highlighted: 

<p align="center">
  <img src="figures/debug_packet.PNG">
</p>

The message contains the housekeeping information of the particular subsystems of Delfi-PQ. The output in the DEBUG 
mode is mainly constant, but also consists of some variable bytes (bytes which change over time). The decimal values 
for the constant bytes when invoking a DEBUG housekeeping request are shown in the figure above. The packets returnd by invoking an ADB housekeeping request when conncted to the FLATSAT are larger, but still contain variable bytes for the counter and fixed bytes representing testing 2 (0xcafe) and testing 4 (0xdeadbeef). The counter will be used to identify missing packages, while testing 2 and testing 4 will be used to check the data produced by housekeeping is not corrupt 

<!--- All bytes with a variable value can be computed in PYTHON, and are either integer counters or timer values.  Once these variable values are computed, they can be used to create a reference message, together with the constant value bytes. This constructed reference message can in term be used to compare against the received message to check for corrupted data errors. --->

We assume that during the transmission no errors in the data are introduced, and that the errors that are introduced
during the tranmission are corrected for by the Cyclic Redundancy Check built in the packet. 

It should be noted that this comparison method works only for simple data packets, such as the DEBUG housekeeping request.
This is because all variables in the DEBUG subsystem are well predictable. For other subystems, this becomes more tricky
since the data stored in the packets can be highly variable in time, and non-predictable (e.g. the voltage on a battery
of the EPS subsystem). 


## 3. How to Use  
### 3.1 Prerequisites
To transmit or receive data to or from the Delfi-PQ, the the following items are required:

* Computer running on either Windows or LINUX, with **Python 2.7** installed. 
* Texas Instruments [MSP432P401R LaunchPad](http://www.ti.com/tool/MSP-EXP432P401R)
* Micro USB to USB C cable. 
* Delfi-PQ ADB subsystem with FLATSAT. 

### 3.2 Software Setup
Download this repository and store it on your computer. Connect the FLATSAT to the computer using the micro USB to USB C cable (a green LED should now blink on the board). When using Windows, open Windows PowerShell in administrator mode and run the following command:
```
cd C:\...\FDIR_PQ9\PQ9EGSE
java -jar target/PQ9EGSE-0.1-SNAPSHOT-jar-with-dependencies.jar
```
where the dots are to be replaced with the repository directory. When using LINUX, open the terminal and run the following command:
```
cd FDIR_PQ9\PQ9EGSE
sudo java -jar target/PQ9EGSE-0.1-SNAPSHOT-jar-with-dependencies.jar
```

Both cases will load the EGSE application programing interface. This can now be accessed by going to the internet browser and  typing in the adress bar:
```
localhost:8080
```

This will bring you to the EGSE GUI, as shown in the picture below. In the header, define the serial port used by the FLATSAT (COM7 in the figure). Note that one of the ports if for serial communication, and the other only for programming. 

<p align="center">
  <img src="figures/egse_gui.png">
</p>

One can test if a sucesfull connection is obtained by sending a ping to **DEBUG** if connected to the TI MSP342 or to **ADB** if connected to the PQ hardware. In the DataLog on the left side of the screen, a transmitted message should now prompt in yellow, as well as a received message in black. 

Running the Python testing software is done via the **client_adb.py** when connected to the PQ hardware, or **client_ti.py** for testing the code wth TI board. One can open any Python 2.7 editor (e.g. IDLE) to open this file and run it. Additionally, one can also run the script diretly via Windows Powershell or LINUX terminal when using the command:

```
cd FDIR_PQ9\PQ_integretion_testing
python client_adb.py
```
In both the EGSE software and the python files, the memory address must be input in decimal, for which the range is 
536,870,912 to  537,9191,488. At present **client_adb.py** looks in the range of 536864505 to 536884505, but this can be increased. 

All the addresses tested are recorded in .json files, to ensure no data is lost if the python crashes. These are located in the folder address_logs. The types of errors occuring at the varying memory locations can be plotted using the **error_graphs.py** file. This is the files used to produce the results in the following section.  

```
python error_graphs.py
```


## 4. Results

### 4.1 Testing with LaunchPad
In the first phase of the software testing campaign tests were performed with the LaunchPad development board, where simple ping, housekeeping and FTDebug commands were tested. The LaunchPad board was configured ran on a software very comparable to the one present on FLATSAT, and provided a simple and fast way to verify the software. For tests with the LaunchPad  **ADD RESULTS HERE**

<p align="center">
  <img src="figures/error_graph.png">
</p>



### 4.2 Testing with FLATSAT
The second phase of the testing campaign consted of tests witht he FLATSAD with the ADB subystem of Delfi-PQ attached. 
<p align="center">
  <img src="figures/hardware_overview.PNG">
</p>





## 5. Issues Encountered 
When a SEU is sent to some particular memory locations, the microcontroller fully "freezes" and communication with the
board is no longer possible. This state could only be recovered from by pressing the physical reset button on the board.
However, this is not practical in reality if one wants to test the full memory spectrum. Therefore, it is recommended
to implement a watchdog timer on the board to let it reset by itself if no response is detected. 

During the testing phase of the project, many issues were encountered with deploying EGSI from LINUX in a virtualbox environment. This often solved itself by fully shutting down the virtual box and restarting it. 



## 6. Recommendations
* Currently, the testing software is only compatible with Python 2.7. This version is already qutie old and noweadays Python 3.0 is used for most programming applications. Therefore, to keep the testing software future-proof, it is recommended to make the code compatible for both Python 2.7 and Python 3.

* Modify the script to allow for the change of a single bit in the memory byte, instead of setting the whole byte to 0xFFFFFFFF. 
