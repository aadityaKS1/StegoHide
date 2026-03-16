def text_to_binary(text):

    
    binary=[format(ord(char), '08b' )for char in text]
    binary_string=''.join (binary)
    return binary_string

def bytes_to_binary(bytes):

    
    binary=[format(byte, '08b' )for byte in bytes]
    binary_string=''.join (binary)
    return binary_string

print(bytes_to_binary(b"hi")) 
print(text_to_binary("hI")) 