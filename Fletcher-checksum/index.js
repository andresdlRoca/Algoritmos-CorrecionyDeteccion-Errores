const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Laboratorio 2');
});

app.get('/fletcher-emit', (req, res) => {
    const data = req.query.data;
    
    const checksum = fletcherChecksumEmissor(data);
    console.log("Sent data: ", data + checksum.toString(16));
    res.send(data + checksum.toString(16));
});

app.get('/fletcher-receive', (req, res) => {
    const data = req.query.data;

    const receivedChecksum = parseInt(data.slice(-1));
    const receivedData = data.slice(0, -1);
    console.log('receivedChecksum', receivedChecksum);
    console.log('receivedData', receivedData);
    const detectError = fletcherChecksumReceptor(receivedData, receivedChecksum);
    console.log(detectError);
    res.send(detectError);
});

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});

// Emisor
function fletcherChecksumEmissor(data) {
    let sum1 = 0;
    let sum2 = 0;

    for (let i = 0; i < data.length; i++) {
        sum1 = (sum1 + data[i]) % 2;
        sum2 = (sum2 + sum1) % 2;
    }

    //Calculamos el checksum
    const checksum = sum2;
    return checksum;
}

// //Testeo emisor
// const data = "100110001";
// const checksum = fletcherChecksumEmissor(data);
// console.log('Sent checksum', checksum.toString(16));



// Receptor
function fletcherChecksumReceptor(data, receivedChecksum) {
    let sum1 = 0;
    let sum2 = 0;

    for (let i = 0; i < data.length; i++) {
        sum1 = (sum1 + data[i]) % 2;
        sum2 = (sum2 + sum1) % 2;
    }

    //Calculamos el checksum
    const checksum = sum2;
    
    const isValid = checksum === receivedChecksum;

    if(isValid) {
        return "Data received is valid: " + data;
    } else {
        return "Checksum is invalid";
    }

}

// receivedData = "100110001";
// console.log(fletcherChecksumReceptor(receivedData, checksum));