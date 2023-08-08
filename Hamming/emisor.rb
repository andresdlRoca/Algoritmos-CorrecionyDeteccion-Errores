require 'webrick'

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

server = WEBrick::HTTPServer.new(Port: 3000)
server.mount_proc '/hamming-emit' do |req, res|
  data = req.query['data']
  encoded_data = hamming_encode(data)
  res.body = encoded_data
end

trap 'INT' do server.shutdown end
server.start
