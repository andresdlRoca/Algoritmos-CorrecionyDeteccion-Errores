# Algoritmo de Hamming Code (Corrección)

## Emisor (Ruby)
[Archivo Emisor](./emisor.rb)

#### Prerequisitos
- Ruby (3.2.2^)

#### Dependencias/Librerias
- webrick

#### Uso
```
ruby emisor.rb
```


## Receptor (Python)
[Archivo Receptor](./receptor.py)

#### Prerequisitos
- Python (3.10.5^)

#### Dependencias/Librerias
- Requests

#### Uso
Dentro del programa:
```
# Ejemplo de trama:
params = {'data': '100110001'} # Cambiar este parametro
```

En consola
```
python receptor.py
```