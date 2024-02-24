import socket
import pickle
import sys
import time
import random


'''
Anselmo-Andrew-csci466.
'''

class Packet():


    def __init__(self,sequence_number,message, length, corrupt_probability,checksum):
        self.sequence_number = sequence_number
        self.message = message
        self.length = length
        self.corrupt_probability = corrupt_probability
        self.checksum = checksum
    
    def set_message(self,new_message):
        self.message = new_message

    def set_length(self,length):
        self.length = length
    
    def get_length(self):
        return self.length 

    def set_corrupt_probability(self,corrupt_probability):
        self.corrupt_probability = corrupt_probability

    def get_corrupt_probability(self):
        return self.corrupt_probability 

    def get_message(self):
        return self.message

    def get_sequence(self):
        return self.sequence_number

    def set_checksum(self,checksum):
        self.checksum = checksum

    def get_checksum(self):
        return self.checksum


def main():

    pirate_message = ""

    packet_list = []
    message = input("Enter your message: ")

    #corrupt prob
    corrupt_probability = float(sys.argv[3])

    #this is the length
    n = int(sys.argv[2]) 

    #Making array of segments from message 
    message_segments = [message[i:i+n] for i in range(0, len(message), n)]
    #print(message_segments)

    #creating packet objects, values will need to be updated  
    for i in range(len(message_segments)):
        #Packet(sequence_number, message, length, corrupt_probability, checksum)
        ob = Packet(i+1,"",4,2,"",)
        packet_list.append(ob)
     
    #updating values 
    k = 0
    for i in message_segments:
        packet_list[k].set_message(message_segments[k])

        packet_list[k].set_corrupt_probability(corrupt_probability)
        

        chance = random.uniform(0.01,1)
        if chance <= corrupt_probability:
            packet_list[k].set_checksum("invalid")
        else:
            packet_list[k].set_checksum("valid")

        '''
        print("-----------")
        print("k is : " , k)
        print(packet_list[k].get_sequence())
        print(packet_list[k].get_message())
        print(packet_list[k].get_corrupt_probability())
        print(packet_list[k].get_checksum())
        '''

        k+=1


    packet_list.append(Packet((len(message_segments)+1),"FIN",n,corrupt_probability,"valid"))

    port = int(sys.argv[1]) #6000 
    host = socket.gethostname()
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket.connect( (host,port) )

    
    for each_packet in packet_list:

        data = pickle.dumps(each_packet)
        clientSocket.send(data)
        print("Sending",each_packet.get_sequence())
        data2 = clientSocket.recv(1024).decode() ##
        if str(data2) == "NCK":
            chance = random.uniform(0.01,1)
            if chance <= corrupt_probability:
                packet_list[k].set_checksum("invalid")
            else:
                packet_list[k].set_checksum("valid")
        print(data2) ##
        print("")
        time.sleep(1)

    #Waiting to get message back
    print("Waiting for response ...")



    while True:
        
        data = clientSocket.recv(1024)
       
        ob = pickle.loads(data)

        if ob.get_checksum() == "valid":
            data2 = "ACK"
            clientSocket.send((data2).encode()) ##
        else:
            data2 = "NCK"
            clientSocket.send((data2).encode()) ##

        print(ob.get_message())
        print(ob.get_sequence())
        print("")

        if ob.get_message() != "FIN":
            pirate_message += ob.get_message()
        

        if ob.get_message() == "FIN":
            break

    print("Our message translated to pirate: ")
    print(pirate_message)
    

    print("Client done")

if __name__ == "__main__":
    main()

