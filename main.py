#coding=utf-8
import socket
import argparse
from sys import exit
from time import time
from threading import Thread

def scanning(num: int, start: int, end: int):
    global PortNum
    if num % PartProgress == 0:
        print("█", end='', flush=True)
    try:
        for port in range(start, end):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                print("[ info ] 线程 " + str(num) + " 检测到 " + "Port {} Open".format(port))
                PortNum += 1
                f.write("\n" + str(port))
            sock.close()
    except Exception as e:
        print("[ info ] 线程 " + str(num) + " 出现错误: " + str(e))
        exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="一个基于命令行的端口扫描器")
    parser.add_argument('host', type=str)
    parser.add_argument('threads', type=int)
    parser.add_argument('timeout', type=float)
    args = parser.parse_args()

    if not 65536 % args.threads == 0:
        print("[ Error ] 请确认 65536 能被您指定的线程数 " + str(args.threads) + " 整除.")
        exit()
    else:
        PartThreads = int(65536 / args.threads)
    host = args.host
    timeout = float(args.timeout)
    start = time()

    threads = []
    PartNum = 0
    f = open("LastScanResults.txt","w")
    f.write("地址 " + host + " 的所有 开放端口 扫描结果如下\n")

    PartProgress = args.threads / 16
    if PartProgress < 0:
        PartProgress = 1

    PortNum = 0
    print("正在启动线程")
    print("进度 | ", end="")

    for ThreadNum in range(1, args.threads + 1):
        threads.append(Thread(target=scanning, args=(ThreadNum, (ThreadNum - 1) * PartThreads, ThreadNum * PartThreads)))

    for thread in threads:
        thread.start()
    print(" | [ Success ] 所有线程 (" + str(args.threads) + " 个) 均已启动完毕.")
    print("每个线程需扫描 " + str(PartThreads) + " 个端口 | 预计耗时 " + str(PartThreads * timeout) + "s+ 结束扫描.\n")

    for thread in threads:
        thread.join()

    end = time()
    EndMessage = f"扫描完成 | 耗时 {end - start:.3f}s | 总开放端口数 " + str(PortNum)
    print(EndMessage)
    f.write("\n\n" + EndMessage)
    f.close()
    exit()
