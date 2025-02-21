const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const cors = require('cors');
const morgan = require('morgan');
const path = require('path');

dotenv.config();
const app = express();
app.use(express.json());
app.use(cors());
app.use(morgan('dev'));
app.use(express.static(__dirname)); 
app.use(express.static(path.join(__dirname, 'public')));
app.get('/login.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/profile.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'profile.html'));
});

mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.log('MongoDB connection error:', err));

app.listen(7000, () => {
  console.log('Server is running on http://localhost:7000');
});