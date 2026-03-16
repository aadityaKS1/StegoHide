from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PIL import Image
import base64
import Crypto.Hash.SHA256 as SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

#converitng encrypted message to binary
def to_binary(encrypted_message):
    binary=""
    for num in encrypted_message:
        binary+=format(num,'08b')
    return binary

#converting password to key using SHA256 hashing algorithm
def password_to_key(password):
    password=str(password)
    return SHA256.new(password.encode()).digest()

#encrypting the message using AES encryption algorithm in CBC mode
def encrypt_message_AES(message, password):
    key = password_to_key(password)
    cipher=AES.new(key, AES.MODE_CBC) 
    ciphertext = cipher.encrypt(pad(message.encode(),16))
    iv = cipher.iv
    full_cipher = iv + ciphertext
    return list(full_cipher), len(full_cipher) # return list of integers and length of the ciphertext easy to store in image


#decrypting the message using AES decryption algorithm in CBC mode
def decrypt_message_AES(encrypted_message, password):
    key = password_to_key(password)
    encrypted_bytes = bytes(encrypted_message)
    iv = encrypted_bytes[:16]
    ciphertext = encrypted_bytes[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(ciphertext),16)
    return decrypted.decode()

# extract first 32 bits (message length)
def get_message_length(img):
    capacity = img.width * img.height * 3

    if len(payload) > capacity:
        return Response({
            "error": "Message too large for this image"
        })
    bits = ""

    for y in range(img.height):
        for x in range(img.width):

            r,g,b = img.getpixel((x,y))

            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

            if len(bits) >= 32:
                return int(bits[:32],2)
    return 0
#embedding the encrypted message into the image using least significant bit (LSB) steganography
def embed_payload(img,payload):

    pixels = img.load()

    bit_index = 0

    for y in range(img.height):
        for x in range(img.width):

            if bit_index >= len(payload):
                return img

            r,g,b = pixels[x,y]

            if bit_index < len(payload):
                r = (r & ~1) | int(payload[bit_index])
                bit_index += 1

            if bit_index < len(payload):
                g = (g & ~1) | int(payload[bit_index])
                bit_index += 1

            if bit_index < len(payload):
                b = (b & ~1) | int(payload[bit_index])
                bit_index += 1

            pixels[x,y] = (r,g,b)

    return img

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
    
    img=Image.open(image).convert("RGB")
    encrypted_message,message_len=encrypt_message_AES(message,password)
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
    
    import os

    filename = image.name
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_encoded{ext}"

    img.save(new_filename,format="PNG")
    
    with open(new_filename,"rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return Response({"encoded_image":encoded})

@api_view(['POST'])
def decode_message(request):

    image = request.FILES['image']
    password = request.data['password']

    img = Image.open(image).convert("RGB")

    # STEP 1: get message length
    message_len = get_message_length(img)

    # STEP 2: extract encrypted message
    encrypted_numbers = extract_message(img, message_len)

    # STEP 3: decrypt message
    message = decrypt_message_AES(encrypted_numbers, password)

    return Response({
        "decoded_message": message
    })