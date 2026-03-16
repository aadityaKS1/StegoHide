bits_withmessage=['10010110',
'01101101',
'11100010',
'01011011']

message=""
for row in range(len(bits_withmessage)):
    message=message+bits_withmessage[row][-1]
    
print(message)