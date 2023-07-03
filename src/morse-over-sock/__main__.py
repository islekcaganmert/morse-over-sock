from datetime import datetime
import socket

def morse(mode, text):
    abc = {
        'a': '.-',
        'b': '-...',
        'c': '-.-.',
        'd': '-..',
        'e': '.',
        'f': '..-.',
        'g': '--.',
        'h': '....',
        'i': '..',
        'j': '.---',
        'k': '-.-',
        'l': '.-..',
        'm': '--',
        'n': '-.',
        'o': '---',
        'p': '.--.',
        'q': '--.-',
        'r': '.-.',
        's': '...',
        't': '-',
        'u': '..-',
        'v': '...-',
        'w': '.--',
        'x': '-..-',
        'y': '-.--',
        'z': '--..',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        '.': '.-.-.-',
        ',': '--..--',
        '?': '..--..',
        "'": '.----.',
        '!': '-.-.--',
        '/': '-..-.',
        '(': '-.--.',
        ')': '-.--.-',
        '&': '.-...',
        ':': '---...',
        ';': '-.-.-.',
        '=': '-...-',
        '+': '.-.-.',
        '-': '-....-',
        '_': '..--.-',
        '"': '.-..-.',
        '$': '...-..-',
        '@': '.--.-.',
        ' ': '/'
    }
    if mode == 'to_text':
        text = text.lower().split(' ')
        result = ''
        for char in text:
            for key, value in abc.items():
                if value == char:
                    result += key
                    break
        return result
    elif mode == 'to_morse':
        result = ''
        for char in text:
            if char.lower() in abc:
                result += abc[char.lower()] + ' '
        return result.strip()

    else:
        return text

mode = input('Reciever or Sender (R/S): ')
if mode.upper() == 'R':
    host = input('Sender: ')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, 8942))
    server_socket.listen(1)
    print(f'Listening {host}')
    try:
        client_socket, client_address = server_socket.accept()
        while True:
            request_data = morse('to_text', client_socket.recv(1024).decode())
            print(f'[{str(datetime.utcnow())}] {request_data}')
    except KeyboardInterrupt: pass
elif mode.upper() == 'S':
    s = None
    for res in socket.getaddrinfo(input('Reciever: '), 8942, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('Could not connect')
    with s:
        try:
            while True:
                s.sendall(morse('to_morse', input('Message: ')).encode('UTF-8'))
        except KeyboardInterrupt: s.close()