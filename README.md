# FDIR_PQ9

## Prerequisites
To run the FDIR code, one requires the MSP432P401R LaunchPad, as well as a USB to micro-USB cable with a computer, running either LINUX or WINDOWS.
In the present work, we use WINDOWS.

## Hardware Setup
To setup the system, connect the LaunchPad to the computer via one of the USB ports. Open WINDOWS PowerShell in administrator mode and locate the repository:

```
cd C:\...\FDIR_PQ9
```

where the dots are to be replaced with the repository directory. Next, run the following commands to deploy the EGSE API:

```
cd PQ9EGSE
java -jar target/PQ9EGSE-0.1-SNAPSHOT-jar-with-dependencies.jar
```

Now, one can open a webbrowser to visit localhost:8080 to visualize the API and run commands to the board. 