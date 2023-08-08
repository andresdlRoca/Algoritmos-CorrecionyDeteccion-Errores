import requests 

def fletcherChecksumReceptor(data, receivedChecksum):

    sum1 = 0
    sum2 = 0

    for i in range(len(data)):
        sum1 = (sum1 + int(data[i])) % 2
        sum2 = (sum2 + sum1) % 2
    
    checksum = sum2

    isValid = str(checksum) == str(receivedChecksum)

    if isValid:
        return 'Valid data: ' + data
    else:
        return 'Invalid data'


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