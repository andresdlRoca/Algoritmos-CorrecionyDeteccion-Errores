import requests 
import random
import string
import time
import matplotlib.pyplot as plt

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
    if isValid:
        print("Integridad: OK: " + data)
        return True
    else:
        print("Integridad: ERROR")
        return False
    
def fletcherChecksumReceptorNoPrints(data, receivedChecksum):
    sum1 = 0
    sum2 = 0
    for i in range(len(data)):
        sum1 = (sum1 + int(data[i])) % 2
        sum2 = (sum2 + sum1) % 2
    checksum = sum2
    isValid = str(checksum) == str(receivedChecksum)
    if isValid:
        return True
    else:
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
        decoded_data = ''.join([encoded_data[i - 1] for i in range(1, n + 1) if (i & (i - 1)) != 0])
        return decoded_data, error_pos
    except IndexError:
        print("Error: Encoded data length is not consistent with expected Hamming encoding.")
        return None, None
    
def hamming_decodeNoPrints(encoded_data):
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
        decoded_data = ''.join([encoded_data[i - 1] for i in range(1, n + 1) if (i & (i - 1)) != 0])
        return decoded_data, error_pos
    except IndexError:
        return None, None

def main():
    run = True
    while run:
        print("\n-- Menu --")
        print("1. Fletcher")
        print("2. Hamming")
        print("3. Automated Testing")
        print("4. Salir")
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
            for char in mensaje_recibido:
                decoded_data, error_pos = hamming_decode(char)
                if error_pos != 0:
                    print("Integridad: ERROR")
                    chequeIntegridad.append(False)
                else:
                    print("Integridad: OK: " + decoded_data)
                    chequeIntegridad.append(True)
                mensaje_sinChecksum.append(decoded_data)
            if False in chequeIntegridad:
                print("Mensaje recibido con errores")
            else:
                print("Mensaje recibido sin errores")
                print("Mensaje decodificado: ", decodificarMensaje(''.join(mensaje_sinChecksum)))

        elif opcion == "3":
            print('Automated Test')

            # Prompt user for number of runs, character length and initialize time lists
            num_runs = int(input("\nEnter the number of times to run each method: "))
            char_length = int(input("Enter the character length of the data to test: "))
            fletcher_times = []
            fletcher_errors = []
            hamming_times = []
            hamming_errors = []
            

            # for _ in range(num_runs):
            #     # Generate random data of specified length

            #     data = ''.join(random.choice(string.ascii_letters) for _ in range(char_length))

            #     # Measure time for Fletcher method

            #     start_time = time.time()
            #     mensaje_recibido = recibirInformacion("http://localhost:3000/fletcher-emit", {'data': data})
            #     fletcherChecksumReceptor(mensaje_recibido[:-1], mensaje_recibido[-1])
            #     fletcher_times.append(time.time() - start_time)

            #     # Measure time for Hamming method
            #     start_time = time.time()
            #     mensaje_recibido = recibirInformacion("http://localhost:3000/hamming-emit", {'data': data})
            #     hamming_decode(mensaje_recibido)
            #     hamming_times.append(time.time() - start_time)

            for i in range(num_runs):
                chequeIntegridad = []
                mensaje_sinChecksum = []
                mensaje = ''.join(random.choice(string.ascii_letters) for _ in range(char_length))
                start_time = time.time()
                mensaje_recibido = recibirInformacion("http://localhost:3000/fletcher-emit", {'data': mensaje})
                mensaje_recibido = mensaje_recibido.split('.')
                for char in mensaje_recibido:
                    chequeIntegridad.append(fletcherChecksumReceptorNoPrints(char[:-1], char[-1]))
                    mensaje_sinChecksum.append(char[:-1])
                fletcher_times.append(time.time() - start_time)
                if False in chequeIntegridad:
                    fletcher_errors.append(1)
                else:
                    fletcher_errors.append(0)

            for i in range(num_runs):
                chequeIntegridad = []
                mensaje_sinChecksum = []
                start_time = time.time()
                mensaje_recibido = recibirInformacion("http://localhost:3000/hamming-emit", {'data': mensaje})
                mensaje_recibido = mensaje_recibido.split('.')
                for char in mensaje_recibido:
                    decoded_data, error_pos = hamming_decodeNoPrints(char)
                    if error_pos != 0:
                        chequeIntegridad.append(False)
                    else:
                        chequeIntegridad.append(True)
                    mensaje_sinChecksum.append(decoded_data)
                hamming_times.append(time.time() - start_time)
                if False in chequeIntegridad:
                    hamming_errors.append(1)
                else:
                    hamming_errors.append(0)


            # Calculate error percentages
            fletcher_error_percentage = (sum(fletcher_errors) / len(fletcher_errors)) * 100
            hamming_error_percentage = (sum(hamming_errors) / len(hamming_errors)) * 100
            # Plotting error percentages
            labels = ['Fletcher', 'Hamming']
            error_percentages = [fletcher_error_percentage, hamming_error_percentage]
            plt.figure(figsize=(8, 6))
            plt.bar(labels, error_percentages, color=['blue', 'red'], alpha=0.7)
            plt.ylabel('Error Percentage (%)')
            plt.title('Error Percentage for Fletcher and Hamming Algorithms')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            # Display the percentages on top of the bars
            for i, v in enumerate(error_percentages):
                plt.text(i, v + 1, f"{v:.2f}%", ha='center', va='bottom', fontweight='bold')
            plt.show()

            # BoxPlot for runtime
            # data = [fletcher_times, hamming_times]
            # labels = ['Fletcher', 'Hamming']
            # plt.boxplot(data, vert=True, patch_artist=True, labels=labels)
            # plt.title('Comparison of Algorithm Runtimes')
            # plt.ylabel('Runtime (seconds)')
            # plt.grid(axis='y')

            # plt.show()


        elif opcion == "4":
            print("Saliendo...")
            run = False
        else:
            print("Opcion invalida")

if __name__ == "__main__":
    main()
