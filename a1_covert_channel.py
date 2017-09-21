#/*********************************************************************************************
#       Name:	a1_covert_channel.py
#
#       Developer:	Mat Siwoski
#
#       Created On: 2017-09-18
#
#       Description:
#       This is a program that allows for covert channel communication through the TCP/IP protocol
#       suite.
#
#    Revisions:
#    (none)
#
###################################################################################################

#!/usr/bin/env python3


from scapy.all import *
import sys
import socket

host_ip = "192.168.0.1"
pkt = None
msg = None


#########################################################################################################
# FUNCTION
#
#    Name:		setHost
#
#    Prototype:	def setHost
#
#    Developer:	Mat Siwoski
#
#    Created On: 2017-09-18
#
#    Parameters:
#    
#
#    Return Values:
#	
#    Description:
#    This function is for setting the host IP for the client.
#
#    Revisions:
#	(none)
#    
#########################################################################################################
def setHost():
    global host_ip
    host_ip = input("    Set the host IP: ")
    main_menu()

#########################################################################################################
# FUNCTION
#
#    Name:		testIP
#
#    Prototype:	def testIP
#
#    Developer:	Mat Siwoski
#
#    Created On: 2017-09-18
#
#    Parameters:
#    host_ip - IP address of the host
#
#    Return Values:
#	
#    Description:
#    This function is to verify if the IP address entered by the client is valid.
#
#    Revisions:
#	(none)
#    
#########################################################################################################
def testIP(host_ip):
    try:
        if host_ip is None:
            print("IP is not valid. Please set the host IP.")
            return False
        else:
            socket.inet_aton(host_ip)
            return True
    except socket.error:
        print("IP is not valid. Please set the host IP.")
        return False

#########################################################################################################
# FUNCTION
#
#    Name:		craftPacket
#
#    Prototype:	def craftPacket
#
#    Developer:	Mat Siwoski
#
#    Created On: 2017-09-18
#
#    Parameters:
#    character - Character that is being sent in the packet
#
#    Return Values:
#    pkt - the newly created pkt with the inserted character
#	
#    Description:
#    This function is to craft an individual packet that the client is able to send with a covert message
#    embedded in the packet.
#
#    Revisions:
#	(none)
#    
#########################################################################################################
def craftPacket(character):
    global pkt
    char = ord(character)
    pkt=IP(dst=host_ip)/TCP(sport=char, dport=RandNum(0, 65535), flags="E")
    return pkt

#########################################################################################################
# FUNCTION
#
#    Name:		parsePacket
#
#    Prototype:	def parsePacket
#
#    Developer:	Mat Siwoski
#
#    Created On: 2017-09-18
#
#    Parameters:
#    pkt - IP address of the host
#
#    Return Values:
#	
#    Description:
#    This function is to parse the packet received from the client and print out the covert embedded 
#    character.
#
#    Revisions:
#	(none)
#    
#########################################################################################################
def parsePacket(pkt):
    flag=pkt['TCP'].flags
    if flag == 0x40: #Flag is "Echo"
        char = chr(pkt['TCP'].sport)
        print(char)

#########################################################################################################
# FUNCTION
#
#    Name:		client
#
#    Prototype:	def client
#
#    Developer:	Mat Siwoski
#
#    Created On: 2017-09-18
#
#    Parameters:
#
#    Return Values:
#	
#    Description:
#    This function is the client portion of the application. It takes a message and individual crafts
#    the packet with the character and then sends the packet to the server.
#
#    Revisions:
#	(none)
#    
#########################################################################################################
def client():
    global msg
    while True:
        msg = input("Craft a covert message to send (Type Q to go to menu): ")
        if msg == "Q":
            main_menu() 
        msg += "\n"
        print("Sending Message: " + msg)
        for character in msg:
            new_pkt = craftPacket(character)
            send(new_pkt)

#########################################################################################################
# FUNCTION
#
#    Name:		server
#
#    Prototype:	def server
#
#    Developer:	Mat Siwoski
#
#    Created On: 2017-09-18
#
#    Parameters:
#
#    Return Values:
#	
#    Description:
#    This function is the main server function. It sniffs and parses the individual packets out and 
#    displays the individual characters.
#
#    Revisions:
#	(none)
#    
#########################################################################################################    
def server():  
    sniff(filter="tcp", prn=parsePacket)

#########################################################################################################
# FUNCTION
#
#    Name:		intro
#
#    Prototype:	def intro
#
#    Developer:	Mat Siwoski
#
#    Created On: 2017-09-18
#
#    Parameters:
#
#    Return Values:
#	
#    Description:
#    This function prints the intro to the user.
#
#    Revisions:
#	(none)
#    
#########################################################################################################
def intro():
    print("")
    print("    C8505 - Assignment 1 - Covert Channel")
    

#########################################################################################################
# FUNCTION
#
#    Name:		main_menu
#
#    Prototype:	def main_menu
#
#    Developer:	Mat Siwoski
#
#    Created On: 2017-09-18
#
#    Parameters:
#
#    Return Values:
#	
#    Description:
#    This function takes the options for the user and displays the menu.
#
#    Revisions:
#	(none)
#    
#########################################################################################################
def main_menu():
    choice = 0
    print("")
    print("        1. Server")
    print("        2. Client")
    print("        3. Set Host IP")
    print("        4. Quit")
    print("")
    choice = input("Please choose an option: ")
    if choice == "1":
        server()
    elif choice == "2":
        if testIP(host_ip):
            client()
        else:
            main_menu() 
    elif choice == "3":
        setHost()
    elif choice == "4":
        sys.exit()

#########################################################################################################
# FUNCTION
#
#    Name:		main
#
#    Prototype:	def main
#
#    Developer:	Mat Siwoski
#
#    Created On: 2017-09-18
#
#    Parameters:
#
#    Return Values:
#	
#    Description:
#    This function runs the program.
#
#    Revisions:
#	(none)
#    
#########################################################################################################
def main():
    intro()    
    main_menu()

main()
