# chat_server.py
import socket
import threading

HOST = '127.0.0.1'  # Dirección IP local
PORT = 65432        # Puerto para la conexión

clientes = []

def manejar_cliente(conn, addr):
    print(f"[CONEXIÓN] {addr} conectado.")
    clientes.append(conn)
    try:
        while True:
            mensaje = conn.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(f"[{addr}] {mensaje}")
            # Reenviar mensaje a todos los clientes
            for cliente in clientes:
                if cliente != conn:
                    try:
                        cliente.sendall(f"[{addr}] {mensaje}".encode('utf-8'))
                    except:
                        # Manejo de clientes desconectados
                        clientes.remove(cliente)
                        cliente.close()
    except Exception as e:
        print(f"Error con el cliente {addr}: {e}")
    finally:
        print(f"[DESCONEXIÓN] {addr} desconectado.")
        if conn in clientes:
            clientes.remove(conn)
        conn.close()

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor de chat escuchando en {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
            thread.start()
            print(f"[ACTIVO] Número de conexiones: {threading.active_count() - 1}")

if __name__ == "__main__":
    iniciar_servidor()