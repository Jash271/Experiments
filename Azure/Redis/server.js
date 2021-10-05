const conn = require('./create_conn');
const Conn = require('./create_conn');

const set_cache_value = async () => {
  conn.setex('Jash', 300, 'Hi there I am Jash');
  console.log('Data Written to Redis');
};

set_cache_value();

const fetch_cache_data = async () => {
  const value = await conn.get('Jash');
  console.log('This is the Fetched Value', value);
};

fetch_cache_data();
