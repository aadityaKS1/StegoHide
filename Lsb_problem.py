Pixel="01101100"
Message_bit="1"
Result="10110111"

def repace_lsb(Pixel,Message_bit):
    return Pixel[:-1]+Message_bit

result=repace_lsb(Pixel,Message_bit)
print(Pixel)
print(result)