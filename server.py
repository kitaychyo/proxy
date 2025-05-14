import socket
import threading
import sys


def handle_client(client_socket, target_host, target_port):
    try:
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.settimeout(5)  # Таймаут для операций с сокетом

        try:
            target_socket.connect((target_host, target_port))
            print(f"[*] Подключено к целевому серверу {target_host}:{target_port}")
        except ConnectionRefusedError:
            print(f"[-] Целевой сервер {target_host}:{target_port} недоступен")
            client_socket.close()
            return
        except Exception as e:
            print(f"[-] Ошибка подключения: {e}")
            client_socket.close()
            return

        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break

                target_socket.sendall(data)  # sendall вместо send для полной отправки

                response = target_socket.recv(4096)
                if not response:
                    break

                client_socket.sendall(response)
            except socket.timeout:
                print("[!] Таймаут при ожидании данных")
                break
            except ConnectionResetError:
                print("[!] Соединение разорвано")
                break
            except Exception as e:
                print(f"[!] Ошибка при передаче данных: {e}")
                break

    finally:
        client_socket.close()
        target_socket.close()
        print(f"[*] Соединение с клиентом закрыто")


def start_proxy(server_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Переиспользование порта

    try:
        server.bind(('0.0.0.0', server_port))
        server.listen(5)
        print(f"[*] Прокси слушает порт {server_port} -> {target_host}:{target_port}")

        while True:
            client_socket, addr = server.accept()
            print(f"[+] Подключение от {addr[0]}:{addr[1]}")

            proxy_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, target_host, target_port)
            )
            proxy_thread.daemon = True  # Демонизированный поток
            proxy_thread.start()

    except KeyboardInterrupt:
        print("\n[*] Остановка прокси...")
    except Exception as e:
        print(f"[!] Критическая ошибка: {e}")
    finally:
        server.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python proxy.py [LOCAL_PORT] [TARGET_HOST] [TARGET_PORT]")
        print("Пример: python proxy.py 3391 localhost 3389")
        sys.exit(1)

    try:
        local_port = int(sys.argv[1])
        target_host = sys.argv[2]
        target_port = int(sys.argv[3])
        start_proxy(local_port, target_host, target_port)
    except ValueError:
        print("Ошибка: Порт должен быть числом")
    except Exception as e:
        print(f"Ошибка: {e}")