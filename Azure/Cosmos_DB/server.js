var mongoose = require('mongoose');
var env = require('dotenv').config();

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const Connect_DB = require('./db');
const Car = require('./models/Car');

// mongoose
//   .connect(
//     'mongodb://' +
//       process.env.COSMOSDB_HOST +
//       ':' +
//       process.env.COSMOSDB_PORT +
//       '/' +
//       process.env.COSMOSDB_DBNAME +
//       '?ssl=true&replicaSet=globaldb',
//     {
//       auth: {
//         user: process.env.COSMOSDB_USER,
//         password: process.env.COSMOSDB_PASSWORD,
//       },
//       useNewUrlParser: true,
//       useUnifiedTopology: true,
//       retryWrites: false,
//     }
//   )
//   .then(() => console.log('Connection to CosmosDB successful'))
//   .catch((err) => console.error(err));

Connect_DB();

//Add a new Car to Database

const add_new_car = async (car_name, model) => {
  try {
    let new_car = new Car({
      name: car_name,
      model: model,
    });
    car_result = await new_car.save();
    console.log(car_result);
  } catch (err) {
    console.log(err);
  }
};

add_new_car((car_name = 'Mercedes'), (model = 'C class'));
