import requests
import random


class Service:
    def __init__(self):
        self.urlEmitFletcher = "localhost:3000/fletcher-emit"
        self.urlReceiveFletcher = "localhost:3001/fletcher-receive"
        self.urlEmitHamming = "localhost:3002/hamming-emit"
        self.urlReceiveHamming = "localhost:3003/hamming-receive"

        self.mensaje= ""
        self.mensaje_binario = []

    def solicitarMensaje(self, mensaje):
        self.message = mensaje
    
    def codificarMensaje(self, mensaje):
        binary_strings = []

        for char in mensaje:
            ascii_value = ord(char)
            binary_string = bin(ascii_value)[2:]
            binary_strings.append(binary_string)
        
        return binary_strings

    def calculcarIntegridad(self, metodo): # Emisores
        if metodo == "Hamming":
            pass # TODO: Implementar
        elif metodo == "Fletcher":
            pass # TODO: Implementar

    def aplicarRuido(self):
        strings_con_ruido = []
        for i in range(len(self.mensaje_binario)):
            string_con_ruido = self.mensaje_binario[i]
            binario_con_ruido = ""
            for bit in string_con_ruido:
                if random.random() < 0.1:
                    binario_con_ruido += '1' if bit == '0' else '0'
                else:
                    binario_con_ruido += bit
            strings_con_ruido.append(binario_con_ruido)
        return strings_con_ruido

    def verificarIntegridad(self, metodo): # Receptores
        if metodo == "Hamming":
            pass
        elif metodo == "Fletcher":
            pass
    
    def corregirMensaje(self): # Exclusivo para Hamming
        pass

    def enviarMensaje(self):
        pass

    def mostrarMensaje(self):
        pass

run = True

while run:

    print("\n--- Menu ---")
    print("1. Hamming")
    print("2. Fletcher")
    print("3. Salir")

    option = input("Ingrese una opcion: ")

    if option == "1":
        print('Handle Hamming')
    elif option == "2":
        print('Handle Fletcher')
    elif option == "3":
        run = False
    else:
        print("Opcion invalida\n")

