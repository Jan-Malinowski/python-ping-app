import socket
import struct
import time
import select
import sys
import getopt

def init():
    args=sys.argv[1:]
    options="hc:t:l"

    count=5
    ttl=255
    limit=True
    dest_ip=sys.argv[-1]

    try:
        arguments, values=getopt.getopt(args, options)
        for currentArg, currentVal in arguments:
            if currentArg == "-h":
                print("help")
                return
            elif currentArg == "-c":
                count=int(currentVal)
            elif currentArg == "-t":
                ttl=int(currentVal)
            elif currentArg == "-l":
                limit=False
    except getopt.error as err:
        print("flag -c [val] ---> sets ping count to val (default 5)")
        print("flag -t [val] ---> sets ttl to val (default 255)")
        print("flag -l ---> never ending pings")
        print("Example use: sudo python3 ping.py -c 5 127.0.0.1")
        return

    return dest_ip, count, ttl, limit

def checksum(source_string):
    sum=0

    if len(source_string)%2: # obsługa nie parzystej dlugosci
        source_string+=b'\x00' # dodanie pustego bajtu

    for i in range(0, len(source_string), 2):  # sumowanie 16-bitowych blokow
        word=source_string[i]+(source_string[i+1] << 8)
        sum=sum+word

        sum=(sum & 0xffff)+(sum >> 16) #jestli suma ma wiecej niz 16 bitow dodaj nadmiar do konca
        
    return ~sum & 0xffff # negacja i zwrocenie 16 bitowego wyniku

def create_packet(id):
    header=struct.pack('bbHHh', 8, 0, 0, id, 1) # Typ, Kod, Checksum, ID, Seq ||| bbHHh -> char char unshort unshort short
    data=b'test-test-test'
    cur_checksum=checksum(header+data)
    header=struct.pack('bbHHh', 8, 0, cur_checksum, id, 1)
    return header + data



def receive_ping(my_socket, id, timeout, send_time):
    while True:
        ready=select.select([my_socket], [], [], timeout)
        if ready[0]==[]:
            print("Request time out")
            return False
        
        time_received=time.time()
        rec_packet, addr=my_socket.recvfrom(1024)
        icmp_header=rec_packet[20:28]
        type, code, checksum, packet_id, seq=struct.unpack("bbHHh", icmp_header)

        if packet_id==id:
            delay=(time_received-send_time)*10000
            print(f"Answer from {addr[0]}: time={delay:.2f}ms")
            return True

def main():
    config=init()
    if not config:
        print(f"Problem with config init: {config}")
        print(f"try python3 ping.py -h")
        return

    dest_ip, count, ttl, limit=config

    print(f"\Pinging {dest_ip}, TTL={ttl}:")

    try:
        icmp_proto=socket.getprotobyname("icmp")
        my_socket=socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
        my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    except PermissionError:
        print("Permission error, try sudo")
        return

    success_count=0
    for i in range(count):
        my_id=(id(i) & 0xffff)
        packet=create_packet(my_id)
        
        send_time=time.time()
        my_socket.sendto(packet, (dest_ip, 1))
        
        if receive_ping(my_socket, my_id, 2.0, send_time):
            success_count+=1
            if not limit:
                break

        time.sleep(1)

    my_socket.close()
    print(f"Statistics: Send = {i+1}, Received = {success_count}")

if __name__ == "__main__":
    main()