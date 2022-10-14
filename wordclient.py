import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s):
    """
    * Return the next word packet from the stream.
    * The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.
    * Returns None if there are no more words, i.e. the server has hung
    up.
    """
    global packet_buffer
    packet = b''

    while True:
        end_of_packet = packet_buffer.find(b'\r\n\r\n')   # Check for double blank space
        # end_of_packet = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], 'big')
        
        if end_of_packet != -1:        # indicating the packet is not incomplete
            packet = packet_buffer[:end_of_packet + WORD_LEN_SIZE]       # extract packet data
            packet_buffer = packet_buffer[end_of_packet + WORD_LEN_SIZE:]    # strip off front
            # print(packet_buffer)
            # print(packet)
            break

        chunk = s.recv(5)

        if chunk == b'':    # if our recv'd bytestring is 0
            break

        packet_buffer += chunk      # add the recv'd data to the buffer
        # print(packet_buffer)

    return packet_buffer

def extract_word(word_packet):
    """
    * Extract a word from a word packet.
    * word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.
    * Returns the word decoded as a string.
    """
    encoded_word = word_packet[2:]
    decoded = encoded_word.decode('UTF-8')
    return decoded
    # print(decoded)

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            print("packet is none ERROR")
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))