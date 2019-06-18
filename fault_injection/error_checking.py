# Katy Blyth


# class error_checks:
#
#     # Check the bit string output of the packet
#
#     def __init__(self, packet, boot_counter, counter):
#         self.packet = packet
#         self.boot_counter = boot_counter
#         self.counter = counter
#         self.source = packet['Service']


def housekeeping_check(packet):

    # if packet['DBGSW1'] != "OFF" or packet['DBGSW2'] != "OFF":
    #     print "Error in board button reading"
    #     return False

    if packet['testing4'] != "3735928559" or packet['testing2'] != "51966":
        print "Error in reading of testing 2 or 4"
        return False

    # print hex(int(packet['testing2'])), hex(int(packet['testing4']))

    # if packet['SoftwareBootCounter'] != str(0):
    #     print "Error in software boot counter"
    #     return False
    #
    # if str(boot_counter) != packet['BootCounter']:
    #     print "Error in boot counter"
    #     return False

    return True



