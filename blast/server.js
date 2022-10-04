const http = require('http');
const fs = require('fs')
const express = require('express');

const app = express();
const hostname = '127.0.0.1';
const port = 3000;

app.use(express.static('dest'));

app.get('/', function(req, res) {
    res.statusCode = 200;
    res.writeHead(200, { 'content-type': 'text/html' })
    fs.createReadStream('dest/index.html').pipe(res)
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})