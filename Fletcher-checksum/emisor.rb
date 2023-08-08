require 'webrick'

server = WEBrick::HTTPServer.new :Port => 3000

server.mount_proc '/' do |req, res|
    res.body = "Laboratorio 2.1 - Emissor"
end

server.mount_proc '/fletcher-emit' do |req, res|
    res.body = fletcherCheckSumEmissor(req.query["data"])
end

def fletcherCheckSumEmissor(data)
    # data: string/
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

trap("INT") { server.shutdown }
server.start