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

cacheConnection.setex(
  'Message',
  300,
  'Hello! The cache is working from Node.js!'
);

cacheConnection.get('Message', function (err, reply) {
  console.log('This is fetched value', reply);
});
