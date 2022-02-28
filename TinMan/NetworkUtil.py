import socket
import struct
from Log import Log
import time

class NetworkUtil:
    _log = Log.create()

    def write_string_with_32_bit_length_prefix(client, msg):

        payload = msg.encode('ascii')
        prefix = struct.pack('!I', len(payload))
        print(prefix+payload)
        client.send(prefix + payload)

    def get_length(client, timeout):
        c_time = time.time()
        try:
            while time.time() - c_time < timeout:
                prefix = client.recv(4)
                if prefix != b"":
                    break
                elif time.time() - c_time >= timeout:
                    NetworkUtil._log.warn('No response recieved within time limit')
                    return None
        except socket.timeout:
            NetworkUtil._log.warn('No response recieved within time limit')
            return None
        if not prefix:
            NetworkUtil._log.warn('No response recieved within time limit')
            return None
        
        return struct.unpack('!I', prefix)[0]

    def read_response_string(client, timeout):
        
        payload_length = NetworkUtil.get_length(client, timeout)
        
        if payload_length == None:
            return None
        raw_payload = client.recv(payload_length)
        payload = raw_payload.decode('ascii')
        print(payload)
        return payload







