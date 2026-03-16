from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PIL import Image
import base64


# Create your views here.
#converting password to key
def password_to_key(password):
    key=0
    for char in password:
        key+=ord(char)
    return key % 256



#encrypting the message using XOR operation with a key
def encrypt_message(message,key):
    encrypted_message=[]
    for  char in message:
        encrypted=ord(char)^key
        encrypted_message.append(encrypted)
    message_len=len(encrypted_message)
    return encrypted_message,message_len

#decrypting the message using XOR operation with a passord-derived key
def decrypt_message(encrypted_message, key):
    message = ""
    for num in encrypted_message:
        char = chr(num ^ key)
        message += char
    return message 

# extract first 32 bits (message length)
def get_message_length(img):

    bits = ""

    for y in range(img.height):
        for x in range(img.width):

            r,g,b = img.getpixel((x,y))

            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

            if len(bits) >= 32:
                return int(bits[:32],2)
            
#converitng encrypted message to binary
def to_binary(encrypted_message):
    binary=""
    for num in encrypted_message:
        binary+=format(num,'08b')
    return binary

#extracting the encrypted message from the image
def extract_message(enc_img, message_len):

    binary_message = ""
    encrypted_message = []

    skipped = 0
    bits_to_skip = 32   # skip header

    for y in range(enc_img.height):
        for x in range(enc_img.width):

            r,g,b = enc_img.getpixel((x,y))

            for bit in [r & 1, g & 1, b & 1]:

                # skip first 32 bits
                if skipped < bits_to_skip:
                    skipped += 1
                    continue

                binary_message += str(bit)

                if len(binary_message) >= 8:
                    byte = binary_message[:8]
                    binary_message = binary_message[8:]

                    encrypted_message.append(int(byte,2))

                    if len(encrypted_message) >= message_len:
                        return encrypted_message

    return encrypted_message

@api_view(['POST'])
def encode_image(request):
    image=request.FILES['image']
    message=request.data['message']
    password=request.data['password']  
    
    img=Image.open(image)
    key=password_to_key(password)
    encrypted_message,message_len=encrypt_message(message,key)
    binary_message=to_binary(encrypted_message)
    length_bits = format(message_len,'032b')
    payload = length_bits + binary_message


    
    #adding the binary message to the least significant bits of the image pixels

    pixels=img.load()

    bit_index=0
    for y in range(img.height):
        for x in range(img.width):
            if bit_index>=len(payload):
                break
            r,g,b=pixels[x,y]
            if bit_index<len(payload):
                r=(r & ~1) | int(payload[bit_index]) #clearing and adding message bit
                bit_index+=1
            if bit_index<len(payload):
                g=(g & ~1) | int(payload[bit_index]) 
                bit_index+=1     
            if bit_index<len(payload):
                b=(b & ~1) | int(payload[bit_index])
                bit_index+=1    
            pixels[x,y]=(r,g,b)
        if bit_index>=len(payload):
            break
    
    img.save("encoded.png")
    
    with open("encoded.png","rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return Response({"encoded_image":encoded})

@api_view(['POST'])
def decode_message(request):

    image = request.FILES['image']
    password = request.data['password']

    img = Image.open(image)

    # STEP 1: get message length
    message_len = get_message_length(img)

    # STEP 2: extract encrypted message
    encrypted_numbers = extract_message(img, message_len)

    # STEP 3: decrypt message
    key = password_to_key(password)
    message = decrypt_message(encrypted_numbers, key)

    return Response({
        "decoded_message": message
    })