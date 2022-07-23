class Utilities:

    def post_req(self, req_type, data):
        return 'POST HTTP/1.1 \r\nContent-Type: text/html\r\nContent-Length: %d\r\nReq-Type: %s\r\n\r\n%s' %(len(data), req_type, data)

    def post_res(self, res_type, data):
        return 'POST HTTP/1.1 \r\nContent-Type: text/html\r\nContent-Length: %d\r\nRes-Type: %s\r\n\r\n%s' %(len(data), res_type, data)

    def send_ack(self, socket):
        socket.send('GET HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nRes-Type: ack'.encode())