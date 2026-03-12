R = "11001000"
G = "10101010"
B = "01100100"
Message_bit = "101"

def hide_message_in_Lsb(R, G,B,Message_bit):
    R=R[:-1]+Message_bit[0]
    G=G[:-1]+Message_bit[1]
    B=B[:-1]+Message_bit[2]
    return R, G, B
R, G, B = hide_message_in_Lsb(R, G, B, Message_bit)
print(R)
print(G)
print(B)