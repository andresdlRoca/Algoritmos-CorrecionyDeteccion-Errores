import requests 


def recibirInformacion(url, params):
    response = requests.get(url, params=params)
    return response.text

def fletcherChecksumReceptor(data, receivedChecksum):

    sum1 = 0
    sum2 = 0

    for i in range(len(data)):
        sum1 = (sum1 + int(data[i])) % 2
        sum2 = (sum2 + sum1) % 2
    
    checksum = sum2

    isValid = str(checksum) == str(receivedChecksum)

    # Verificacion integridad
    if isValid:
        print("Integridad: OK: " + data)
        return True
    else:
        print("Integridad: ERROR")
        return False


def decodificarMensaje(data):
    ascii_list = []

    for i in range(0, len(data), 7):
        ascii_list.append(chr(int(data[i:i+7], 2)))
    
    return ''.join(ascii_list)

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

def main():
    run = True

    while run:
        print("\n-- Menu --")
        print("1. Fletcher")
        print("2. Hamming")
        print("3. Salir")

        opcion = input("Ingrese una opcion: ")

        if opcion == "1":
            print('Fletcher')
            chequeIntegridad = []
            mensaje_sinChecksum = []
            mensaje = str(input("\nIngrese el mensaje: "))
            mensaje_recibido = recibirInformacion("http://localhost:3000/fletcher-emit", {'data': mensaje})
            print("Mensaje codificado recibido: ", mensaje_recibido)
            mensaje_recibido = mensaje_recibido.split('.')
            for char in mensaje_recibido:
                chequeIntegridad.append(fletcherChecksumReceptor(char[:-1], char[-1]))
                mensaje_sinChecksum.append(char[:-1])

            if False in chequeIntegridad:
                print("Mensaje recibido con errores")
            else:
                print("Mensaje recibido sin errores")
                print("Mensaje decodificado: ", decodificarMensaje(''.join(mensaje_sinChecksum)))

                
        elif opcion == "2":
            print('Hamming')
            chequeIntegridad = []
            mensaje_sinChecksum = []
            mensaje = str(input("\nIngrese el mensaje: "))
            mensaje_recibido = recibirInformacion("http://localhost:3000/hamming-emit", {'data': mensaje})
            print("Mensaje codificado recibido: ", mensaje_recibido)
            mensaje_recibido = mensaje_recibido.split('.')

            # TODO: Adaptar para que funcione con la correccion de errores
            for char in mensaje_recibido:
                chequeIntegridad.append(hamming_decode(char))
                mensaje_sinChecksum.append(char[:-1])
            
            if False in chequeIntegridad:
                print("Mensaje recibido con errores")
            else:
                print("Mensaje recibido sin errores")
                print("Mensaje decodificado: ", decodificarMensaje(''.join(mensaje_sinChecksum)))

        elif opcion == "3":
            print("Saliendo...")
            run = False
        else:
            print("Opcion invalida")

if __name__ == "__main__":
    main()