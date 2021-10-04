const mongoose = require('mongoose');
const Car = require('./Car');

const DriverSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  vehicles: [
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: Car,
    },
  ],
});
module.exports = mongoose.model('Driver', DriverSchema);
