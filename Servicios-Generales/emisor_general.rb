require 'webrick'

server = WEBrick::HTTPServer.new :Port => 3000

server.mount_proc '/' do |req, res|
    res.body = "Laboratorio 2.2 - General Emissor"
end

# -- Enviar Informacion -- #
server.mount_proc '/fletcher-emit' do |req, res|
    res.body = useFletcher(req.query["data"])
end

server.mount_proc '/hamming-emit' do |req, res|
    res.body = useHamming(req.query["data"])
end

def useFletcher(data)
  binary_msg = codificarMensaje(data)
  for i in 0..binary_msg.length-1
    binary_msg[i] = fletcherCheckSumEmissor(binary_msg[i])
  end
  for i in 0..binary_msg.length-1
    binary_msg[i] = aplicarRuido(binary_msg[i])
  end
  mensaje_a_enviar = binary_msg.join('.')
  return mensaje_a_enviar
end

def useHamming(data)
  binary_msg = codificarMensaje(data)
  for i in 0..binary_msg.length-1
    binary_msg[i] = hamming_encode(binary_msg[i])
  end
  for i in 0..binary_msg.length-1
    binary_msg[i] = aplicarRuido(binary_msg[i])
  end
  mensaje_a_enviar = binary_msg.join('.')
  return mensaje_a_enviar
end


def codificarMensaje(data)
    binary_strings = []

    data.each_char do |char|
      ascii_value = char.ord  
      binary_string = ascii_value.to_s(2)
      binary_strings << binary_string
    end

    return binary_strings
    
end

def aplicarRuido(mensaje_binario , probabilidad = 1)
  mensaje_binario.chars.map do |bit|
    if rand(100) < probabilidad
      bit == '0' ? '1' : '0'
    else
      bit
    end
  end.join
end



def fletcherCheckSumEmissor(data)
    # data: string
    # return: string

    sum1 = 0
    sum2 = 0

    # Recorremos el string
    data.each_char do |byte|
        sum1 = (sum1 + byte.to_i) % 2
        sum2 = (sum2 + sum1) % 2
    end 

    checksum = sum2
    return data.to_s + checksum.to_s
end

def hamming_encode(data)
    m = data.length
    r = 0
    while 2**r < m + r + 1
      r += 1
    end
  
    encoded = ''
    j = 0
    for i in 0...(m + r)
      if (i & (i + 1)).zero?
        encoded += '0'
      else
        encoded += data[j]
        j += 1
      end
    end
  
    for i in 0...r
      parity_pos = 2**i
      parity = 0
      encoded.each_char.with_index do |bit, index|
        next if index + 1 == parity_pos || bit == '0'
        parity ^= 1 if (index + 1) & parity_pos != 0
      end
      encoded[parity_pos - 1] = parity.to_s
    end
  
    encoded
  end


trap("INT") { server.shutdown }
server.start