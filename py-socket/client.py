from websocket import create_connection

ws = create_connection()
ws.send('hello world')
