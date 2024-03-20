import selectors
import socket
import sys
from message.client_message import ClientMessage
from message.server_message import ServerMessage

ANTHILL_HOST = '127.0.0.1'
ANTHILL_PORT = 0
DISCOVERY_HOST = '127.0.0.1'
DISCOVERY_PORT = 0
DEBUG = True


def main():
    register()
    game()


def register():
    """
    register this anthill service with the discovery service
    :return: None
    """
    # TODO
    message = {'action': 'register', 'ip': ANTHILL_HOST, 'port': ANTHILL_PORT, 'type': 'hive'}
    sel = selectors.DefaultSelector()
    request = create_request(message)
    start_connection(sel, DISCOVERY_HOST, DISCOVERY_PORT, request)

    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(f'Error: Exception for {message.ipaddr}')
                    message.close()
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print('Caught keyboard interrupt, exiting')
    finally:
        sel.close()


def game():
    """
    process the rounds of the game
    :return:
    """
    # TODO
    sel = selectors.DefaultSelector()
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((ANTHILL_HOST, ANTHILL_PORT))
    lsock.listen()
    print(f'Discovery: listening on {(ANTHILL_HOST, ANTHILL_PORT)}')
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

def process_action(message):
    """
    process the action from the game service
    :param message:
    :return:
    """
    # TODO
    if DEBUG:
        print(f'Discovery/process_action: event={message.event}')
    if message.event == 'READ':
        action = message.request['action']
        if action == 'round':
            service_uuid = '["N", "S"]'
            print(service_uuid)
            message.response = service_uuid
        if action == 'quit':
            return True

        message.set_selector_events_mask('w')




def create_request(action_item):
    """
    creates the body of the request
    :param action_item:
    :return:
    """
    return dict(
        type='text/json',
        encoding='utf-8',
        content=action_item,
    )


def start_connection(sel, host, port, request):
    """
    starts the connection to a remote socket
    :param sel:
    :param host:
    :param port:
    :param request:
    :return:
    """
    addr = (host, port)
    if DEBUG: print(f'Hive1: Starting connection to {addr}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = ClientMessage(sel, sock, addr, request)
    sel.register(sock, events, data=message)




def accept_wrapper(sel, sock):
    """
    Wrapper for the recieved messages
    :param sel:
    :param sock:
    :return:
    """
    conn, addr = sock.accept()  # Should be ready to read
    if DEBUG: print(f'Hive1: Accepted connection from {addr}')
    conn.setblocking(False)
    message = ServerMessage(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Script needs two arguments')
        exit(2)
    else:
        DISCOVERY_PORT = int(sys.argv[1])
        ANTHILL_PORT = int(sys.argv[2])
        main()
