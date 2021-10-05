var redis = require('redis');
var bluebird = require('bluebird');
require('dotenv').config();
// Convert Redis client API to use promises, to make it usable with async/await syntax
bluebird.promisifyAll(redis.RedisClient.prototype);
bluebird.promisifyAll(redis.Multi.prototype);

var cacheConnection = redis.createClient(6380, process.env.REDISCACHEHOSTNAME, {
  auth_pass: process.env.REDISCACHEKEY,
  tls: { servername: process.env.REDISCACHEHOSTNAME },
});

const get_val = async () => {
  var reply = await cacheConnection.getAsync('Message');
  console.log(reply);
};

get_val();
