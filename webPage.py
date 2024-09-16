
def webPage():
    html = """<html>
<script type="text/javascript">
    function saveCredentials(event) {
        event.preventDefault();
        var ssid = document.getElementById("ssid").value;
        var password = document.getElementById("password").value;
        
        var credentials = {
            "ssid": ssid,
            "password": password
        };
        
        var jsonString = JSON.stringify(credentials);
        
        var serverRequest = new XMLHttpRequest();
        serverRequest.open("POST", "/save_credentials", true);
        serverRequest.setRequestHeader("Content-Type", "application/json");
        
        serverRequest.send(jsonString);
        
        document.getElementById("ssid").value = "";
        document.getElementById("password").value = "";
        
        return false;
    }
</script>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body{
           font-size: 16px;
        }
        .title-box{
            text-align: center;
            margin-top: 1em  
        }
        .title-box h1{
            font-size: 2em;
            margin: 1em;
            padding: 0;
        }
        .form form{
            display: flex;
            flex-direction: column;
            margin: 0 auto;
            width: 80%;
            height: 25vh;
            max-width: 500px;
            border: 1px solid #d1c1c1;
            box-shadow: 0 15px 10px -10px rgba(0, 0, 0, 0.3);
            padding: 1em;
            border-radius: 1em;
        }
        .form form label{
            margin-top: 10px;
            font-size: 1.2em;
            font-weight: bold;
        }

        .button{
            background-color: #094181;
            border: none;
            color: white;
            padding: 0.5em;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 1em;
            font-weight: bold;
            margin: auto auto;
            width: 50%;
            border-radius: 1em;
        }
        .button:hover{
            background-color: #346392;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="title-box">
        <h1>Wifi Credentials</h1>
    </div>
    <div class="form">
        <form action="/save_credentials" onsubmit="return saveCredentials()" method="POST">
            <label for="ssid">SSID:</label>
            <input type="text" id="ssid" name="ssid" placeholder="ssid" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <input class="button" type="submit" value="Connect">
        </form>  
    </div>  
</body>
</html>"""
    return html

def initializeWebPage():
    try:
        import usocket as socket
    except:
        import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(4096).decode("utf-8")
            print('Content = %s' % str(request))

            if "POST /save_credentials" in request:
                try:
                    # Encuentra el índice de inicio de los datos POST
                    post_start = request.find("\r\n\r\n") + 4

                    # Lee los datos POST
                    post_data = request[post_start:]
                    print("POST data:", post_data)

                    # Procesa los datos POST en formato x-www-form-urlencoded
                    post_data_parts = post_data.split("&")
                    data = {}
                    for part in post_data_parts:
                        key, value = part.split("=")
                        data[key] = value

                    # Guarda en el archivo
                    try:
                        with open("data.txt", "w") as file:
                            file.write(f"SSID: {data.get('ssid', '')}\nPassword: {data.get('password', '')}\n")
                            print("Credentials saved")
                        response = "Credentials saved"
                    except Exception as e:
                        print("Error saving credentials:", e)
                        response = "Error saving credentials"
                except Exception as e:
                    print("Error processing POST data or saving credentials:", e)
                    print("Request:", request)
                    response = "Error saving credentials"
            else:
                response = webPage()

            # Envia la respuesta al cliente
            conn.sendall('HTTP/1.1 200 OK\n')
            conn.sendall('Content-Type: text/html\n')
            conn.sendall('Connection: close\n\n')
            conn.sendall(response.encode("utf-8")) 
            conn.close()
        except OSError:
            print("Error in HTTP server")
