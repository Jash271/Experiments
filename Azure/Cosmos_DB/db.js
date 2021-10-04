require('dotenv').config();

const mongoose = require('mongoose');

const Connect_DB = async () => {
  try {
    console.log(process.env.COSMOSDB_USER);
    await mongoose.connect(
      'mongodb://' +
        process.env.COSMOSDB_HOST +
        ':' +
        process.env.COSMOSDB_PORT +
        '/' +
        process.env.COSMOSDB_DBNAME +
        '?ssl=true&replicaSet=globaldb',
      {
        auth: {
          username: process.env.COSMOSDB_USER,
          password: process.env.COSMOSDB_PASSWORD,
        },
        useNewUrlParser: true,
        useUnifiedTopology: true,
        retryWrites: false,
      }
    );
    console.log('Connected to CosmosDB');
  } catch (err) {
    console.log(err);
    process.exit(1);
  }
};
module.exports = Connect_DB;
