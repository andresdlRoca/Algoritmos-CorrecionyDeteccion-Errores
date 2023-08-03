import requests

def hamming_decode(encoded_data):
    n = len(encoded_data)
    r = 0
    while 2**r <= n:
        r += 1
    m = n - r

    parity_bits = [int(encoded_data[2**i - 1]) for i in range(r)]
    calculated_parity = []
    for i in range(r):
        parity = 0
        for j, bit in enumerate(encoded_data):
            if j + 1 != 2**i and (j + 1) & 2**i != 0:
                parity ^= int(bit)
        calculated_parity.append(parity)

    error_pos = 0
    for i in range(r):
        if parity_bits[i] != calculated_parity[i]:
            error_pos += 2**i

    if error_pos != 0:
        encoded_data = encoded_data[:error_pos - 1] + str(1 - int(encoded_data[error_pos - 1])) + encoded_data[error_pos:]

    decoded_data = ''.join([encoded_data[i] for i in range(n) if (i & (i + 1)) != 0])
    return decoded_data, error_pos

url = 'http://localhost:3000/hamming-emit'
params = {'data': '1101010'}

response = requests.get(url, params=params)
encoded_data = response.text


encoded_data = '11101011011' #introduce a single-bit error

decoded_data, error_pos = hamming_decode(encoded_data)

print("Encoded data:", encoded_data)
print("Decoded data:", decoded_data)
if error_pos != 0:
    print(f"Corrected error at position {error_pos}")
else:
    print("No errors detected")
