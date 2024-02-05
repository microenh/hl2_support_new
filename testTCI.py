from websockets.sync.client import connect

def main():
    with connect("ws://localhost:50001") as websocket:
        while True:
            message = websocket.recv()
            # print(f"Received: {message}")
            if message == 'ready;':
                break
        # websocket.send('start;')
        # websocket.send('SPOT:N8ME,LSB,3816000,4294967295,Mark;')
        # websocket.send('SPOT:WA8KKN,LSB,3816000,4294967295,Mark;')
        websocket.send('RX_CHANNEL_ENABLE:true,1000;')
        while True:
            message = websocket.recv()
            print (message)

if __name__ == '__main__':
    main()
