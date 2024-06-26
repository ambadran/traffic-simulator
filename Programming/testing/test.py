# Handle HTTP requests
def handle_request(conn):
    request = conn.recv(1024)
    request = str(request)
    print('Request:', request)
    
    # Parse HTTP request
    if 'GET /capture' in request:
        img_data = capture_image()
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n')
        conn.sendall(img_data)
    elif 'POST /led' in request:
        content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
        body = conn.recv(content_length)
        data = json.loads(body)
        color = data['color']
        state = data['state']
        
        if color == 'red':
            red_led.value(state)
        elif color == 'yellow':
            yellow_led.value(state)
        elif color == 'green':
            green_led.value(state)
        
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
        conn.send(json.dumps({'status': 'OK'}))
    elif 'GET /proximity' in request:
        prox_value = prox_sensor.read()
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
        conn.send(json.dumps({'value': prox_value}))
    else:
        # Serve index.html
        if 'GET / ' in request or 'GET /index.html' in request:
            response = ''
            with open('index.html', 'r') as file:
                response = file.read()
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            conn.sendall(response)
        else:
            conn.send('HTTP/1.1 404 Not Found\r\n\r\n')
    
    conn.close()

# Setup server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(5)
print('Listening on', addr)

while True:
    conn, addr = s.accept()
    print('Connection from', addr)
    handle_request(conn)
