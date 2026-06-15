import socket
import threading
import json

HOST = "127.0.0.1"
PORT_CLIENT  = 6000
PORT_MONITOR = 6001

monitors = []

def monitor_dinle(conn):
    monitors.append(conn)
    try:
        while True:
            if not conn.recv(16):
                break
    except:
        pass
    monitors.remove(conn)
    conn.close()

def client_dinle(conn):
    buffer = ""
    try:
        while True:
            veri = conn.recv(1024).decode()
            if not veri:
                break
            buffer += veri
            while "\n" in buffer:
                satir, buffer = buffer.split("\n", 1)
                if satir.strip():
                    mesaj = json.loads(satir)
                    print(f"[SERVER] Mesaj alındı: {mesaj}")
                    for mon in monitors:
                        try:
                            mon.sendall((json.dumps(mesaj) + "\n").encode())
                        except:
                            pass
    except:
        pass
    conn.close()

def sunucu_baslat(port, handler):
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, port))
    srv.listen(10)
    print(f"[SERVER] Port {port} dinleniyor.")
    while True:
        conn, addr = srv.accept()
        print(f"[SERVER] Bağlantı: {addr}")
        threading.Thread(target=handler, args=(conn,), daemon=True).start()

threading.Thread(target=sunucu_baslat, args=(PORT_CLIENT, client_dinle), daemon=True).start()
threading.Thread(target=sunucu_baslat, args=(PORT_MONITOR, monitor_dinle), daemon=True).start()

print("Server çalışıyor.")
import time
while True:
    time.sleep(1)