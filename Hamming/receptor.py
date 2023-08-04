import requests

def hamming_decode(encoded_data):
    try:
        n = len(encoded_data)
        r = 0
        while 2**r < n - r + 1:
            r += 1

        error_pos = 0
        for i in range(r):
            parity = 0
            for j in range(1, n + 1):
                if j & (1 << i) != 0:
                    parity ^= int(encoded_data[j - 1])
            if parity != 0:
                error_pos += 2**i

        if error_pos != 0:
            encoded_data = encoded_data[:error_pos - 1] + str(1 - int(encoded_data[error_pos - 1])) + encoded_data[error_pos:]

        decoded_data = ''.join([encoded_data[i - 1] for i in range(1, n + 1) if (i & (i - 1)) == 0])
        return decoded_data, error_pos
    except IndexError:
        print("Error: Encoded data length is not consistent with expected Hamming encoding.")
        return None, None

url = 'http://localhost:3000/hamming-emit'
params = {'data': '100010001'}

response = requests.get(url, params=params)
encoded_data = response.text

# Uncomment the following line to introduce a single-bit error (e.g., flip the last bit)
# encoded_data = '1011110'

result = hamming_decode(encoded_data)

if result is not None:
    decoded_data, error_pos = result
    print("Encoded data:", encoded_data)
    print("Decoded data:", decoded_data)
    if error_pos != 0:
        print(f"Corrected error at position {error_pos}")
    else:
        print("No errors detected")
