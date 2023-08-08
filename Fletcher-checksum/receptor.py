import requests

# Receive data from this endpoint
url = 'http://localhost:3000/fletcher-emit'
params = {'data': '1010110001'} # Cambiar este parametro para enviar datos

response = requests.get(url, params=params) 
# print('Response', response.json())

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
    
# print(type(response.json()))

receivedData = str(response.json())
receivedChecksum = receivedData[-1]
receivedData = receivedData[:-1]

print("Trama utilizada:", params["data"])
receivedData = "0101001110"
print("Modficicacion trama:", receivedData)
print(fletcherChecksumReceptor(receivedData, receivedChecksum))