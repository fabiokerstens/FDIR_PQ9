import json
import socket
import time
import signal

class pq:
    """ Class for communication protocol of the spacecraft bus with the pc. """
    # Class containing ....
    # - .s
    # -
    # - Connect to the bus using the ip adress and serial port.
    # -
    # -
    # -

    # Initializer: initial value of all objects in the class.
    def __init__(self, ip, port, timeout, buffer_size, fname, log_period):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(timeout)
        self.s.connect((ip, port))
        self.buf = ""
        self.buffer_size = buffer_size
        self.data = ""

        self.f = open(fname,'a')
        self.log_period = log_period
        self.time_prev=  time.time()
        self.time_new =  0

    def close(self):
        # Instance method to close the log file and serial communication.
        self.f.close()
        self.s.close()

    def get_data(self):
        # Instance method to receive the data from the spacecraft bus. It uses a
        # try-except logic. In case an error occurs in receiving the data, an
        # empty string is returned. Otherwise, the data is taken.
        try:
            data = self.s.recv(self.buffer_size)
        except:
            return ""

        # Add the new data to the data instance attribute and write the data
        # string to the log file.
        self.data += data
        self.f.write(data)

        #print "received data:", data

        # Add the current time stamp (sec.) to the time_new instance attribute.
        self.time_new =  time.time()

        # If the the maximum log period is reached, the internal I/O buffer is
        # flushed to save memory, and the instance attribute time_prev is set to
        # time_new.
        if self.time_new - self.time_prev > self.log_period*60:
            print('Still here', self.time_new)
            self.time_prev = self.time_new
            self.f.flush()

        return data

    def get_packets(self):
        # Instance method to convert the obtained data of get_data to packets . 
        packets = []
        sps = self.data.splitlines(True)
        self.data = ""
        for sp in sps:
            self.buf += sp
            if "\n" in self.buf:
                packet = json.loads(self.buf)
                self.buf = ""
                packets.append(packet)

        return packets

    def ping(self, destination):
        # Instance method to ping the one of the destinations at the spacecraft
        # bus.
        print("Sending")
        msg = {}
        msg['_send_'] = 'Ping'
        msg['Destination'] = destination
        packet = json.dumps(msg, ensure_ascii=False)
        print(packet)
        self.s.send(packet + "\n")

	def ftdebug(self, MemAddr, FTOper, Operator):
		# Function for the bit flipping 
		print("Flipping")
		msg = {}
		msg['_send_'] = 'FTDebug'
		msg['MemAddr'] = MemAddr
		msg['FTOper'] = FTOper
		msg['Operator'] = Operator
		packet = json.dumps(msg, ensure_ascii=False)
		print(packet)
		self.s.send(packet + "\n")
		
		


    def houskeeping(self, destination):
        # Function to get the housekeeping data from the subsystems.
        print("Sending")
        msg = {}
        msg['_send_'] = 'GetTelemetry'
        msg['Destination'] = destination
        packet = json.dumps(msg, ensure_ascii=False)
        print(packet)
        self.s.send(packet + "\n")
