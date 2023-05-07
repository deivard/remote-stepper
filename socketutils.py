HEADER_LEN = 10

def send_data(s, data):
    data_len = len(data)
    header = f"{data_len:<{HEADER_LEN}}"
    data = bytes(header + data, "utf8")
    totalsent = 0
    while totalsent < data_len:
        sent = s.send(data[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    return totalsent

def receive_data(s):
    chunks = []
    bytes_recd = 0
    try:
        msg_len = int(s.recv(HEADER_LEN).decode("utf8"))
    except:
        return b''
    while bytes_recd < msg_len:
        chunk = s.recv(min(msg_len - bytes_recd, 2048))
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)