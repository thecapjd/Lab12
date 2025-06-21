# chat_client.py
import socket
import threading
import sys

HOST = '127.0.0.1'  # La misma dirección IP que el servidor
PORT = 65432        # El mismo puerto que el servidor

def recibir_mensajes(s):
    while True:
        try:
            mensaje = s.recv(1024).decode('utf-8')
            if not mensaje:
                print("\n[DESCONEXIÓN] El servidor se ha desconectado.")
                break
            print(f"\n{mensaje}\nTu mensaje: ", end='')
        except OSError:  # Posiblemente el socket se cerró
            break
        except Exception as e:
            print(f"Error al recibir: {e}")
            break

def enviar_mensajes(s):
    while True:
        try:
            mensaje = input("Tu mensaje: ")
            s.sendall(mensaje.encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar: {e}")
            break

def iniciar_cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Conectado al servidor en {HOST}:{PORT}")
        except ConnectionRefusedError:
            print("No se pudo conectar al servidor. Asegúrate de que el servidor esté ejecutándose.")
            sys.exit()

        recibir_thread = threading.Thread(target=recibir_mensajes, args=(s,))
        recibir_thread.start()

        enviar_thread = threading.Thread(target=enviar_mensajes, args=(s,))
        enviar_thread.start()

        recibir_thread.join() # Esperar a que el hilo de recepción termine (e.g., si el servidor se desconecta)
        enviar_thread.join() # Asegurarse de que el hilo de envío también termine si el de recepción lo hace

if __name__ == "__main__":
    iniciar_cliente()