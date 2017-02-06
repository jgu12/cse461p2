import socket
import sys
import threading
import os


def handle(conn_tcp, addr_tcp):

    # print "a new connection is created, ", addr_tcp 

    request = conn_tcp.recv(4096)
    ###get web server and port (host line)
    if len(request) > 0:
        request_lines = request.split("\n");    #split each line
        server_str = ''
        port = 80
        for lines in request_lines:
            temp = lines
            temp = temp.replace(" ", "").lower()
            host_index = temp.find("host:")
            if host_index != -1:
                host_index += 5
                server_str = '%s' % temp[host_index:]
                port_index = server_str.find(':')
                if port_index != -1: 
                    port = server_str[port_index+1:]   
                    server_str = server_str[0:port_index]
                break

        port = int(port)

        if port == 80 and request_lines[0].lower().find("https://") > 0:
            port = 443

            
        print request_lines[0]

        ###Turning off keep-alive
        request = request.replace("Connection: keep-alive", "Connection: close")

        
        ###establish tcp connection to server
        try:
            server_str = server_str[0:(len(server_str) - 1)]
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((server_str, port))
            tcp.send(request)

            while 1:
                requestedData = tcp.recv(4096)
                if len(requestedData) > 0:
                    # print requestedData
                    conn_tcp.sendall(requestedData)
                else:
                    break
            tcp.close()
            conn_tcp.close()

        except socket.error, (value, message):
            # print "Some error"
            sys.exit(1)





if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print "usage: proxy <port>"
        sys.exit(1)


    host = ''
    port = int (sys.argv[1])
    # print "successful user input"
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((host, port))
    tcp_socket.listen(100)
    print 'Proxy listening on 0.0.0.0:', port


    while True:
        conn_tcp, addr_tcp = tcp_socket.accept()
        # print "connection established"
        tcp_thread = threading.Thread(target=handle, args=(conn_tcp, addr_tcp))
        tcp_thread.daemon = True
        tcp_thread.start()





# ref:  http://luugiathuy.com/2011/03/simple-web-proxy-python/

# question: when opening one site, multiple connections are created. 





# POST http://clients1.google.com/ocsp HTTP/1.1
# Host: clients1.google.com
# User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Content-Length: 75
# Content-Type: application/ocsp-request
# Connection: keep-alive
