const redis = require('redis');
const REDIS_PORT = process.env.PORT || 6379;

const client = redis.createClient(REDIS_PORT);

client.setex('username', 3600, 'Jash10');
