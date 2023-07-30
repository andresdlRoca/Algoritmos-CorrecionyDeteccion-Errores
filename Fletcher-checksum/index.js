const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.get('/fletcher', (req, res) => {
    const data = req.query.data;
    const checksum = fletcherChecksumEmissor(data);
    res.send(checksum.toString(16));
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
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
    const checksum = (sum2 << 1) | sum1;
    return checksum;
}

//Testeo emisor
const data = [1, 0, 0, 1, 1, 0, 0, 0];
const checksum = fletcherChecksumEmissor(data);
console.log('Sent checksum', checksum.toString(16));



// Receptor
function fletcherChecksumReceptor(data, receivedChecksum) {
    let sum1 = 0;
    let sum2 = 0;

    for (let i = 0; i < data.length; i++) {
        sum1 = (sum1 + data[i]) % 2;
        sum2 = (sum2 + sum1) % 2;
    }

    //Calculamos el checksum
    const checksum = (sum2 << 1) | sum1;
    
    return checksum === receivedChecksum;
}

errorData = [1, 1, 0, 1, 1, 0, 0, 0];

console.log('Checksum is valid?', fletcherChecksumReceptor(errorData, checksum));