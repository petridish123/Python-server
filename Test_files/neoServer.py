import json
import socket


url :str= "localhost"
PORT :int= 8765

connected_clients = {}
connected_set = set()

def handle_message(message) -> None:
    message_str : str = json.loads(message)
    print(message_str)
    return message_str

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((url, PORT))
    server_socket.listen(12)

    while True:
        print("Starting ANother loop")
        client_socket, client_address = server_socket.accept()
        connected_clients[client_socket] = client_address
        connected_set.add(client_socket)
        
        message = client_socket.recv(1024)

        try:
            recieved_message = handle_message(message.decode())

            response = {
                "RESPONSE" : "accepted"
            }
            
            response = json.dumps(response).encode()
            client_socket.send(response)
        except json.JSONDecodeError as e:
            print("Had a tough time decoding there")
        

if __name__ == "__main__":
    try:
        run()  
    except KeyboardInterrupt:
        print("Killed")