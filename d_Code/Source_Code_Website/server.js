const express = require('express');
const fs = require('fs');
const cors = require('cors');
const mqtt = require('mqtt');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

app.get('/data', (req, res) => {
    fs.readFile('data.csv', 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Error reading data file');
            return;
        }
        res.send(data);
    });
});

const client = mqtt.connect('mqtt://broker.hivemq.com:1883');

client.on('connect', function () {
    console.log('Connected to MQTT broker');
});

app.post('/run-motor', (req, res) => {
    client.publish('cmpe244', 'run', {}, (error) => {
        if (error) {
            console.error('Failed to publish message:', error);
            res.status(500).send('Error sending message to MQTT broker');
        } else {
            res.send('Message sent to MQTT broker');
        }
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
