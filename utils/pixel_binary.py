pixel=(42,65,210)
r_bin=format(pixel[0],'08b')
print(r_bin)
r=int(r_bin,2)
print(r)
g_bin=bin(pixel[1])[2:]
print(g_bin)

def bin_to_dec(bin_str):
    dec=0
    for i in range(len(bin_str)):
        if bin_str[i]=='0':
            i+=1
        else:
            dec=dec+2**(len(bin_str)-1-i)
    return dec

print(bin_to_dec("00101010"))