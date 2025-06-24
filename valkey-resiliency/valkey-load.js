import redis from 'k6/experimental/redis';
import { check } from "k6";

const host = __ENV.REDIS_HOSTNAME || 'localhost';
const port = __ENV.REDIS_PORT || 26379;
const primaryset = __ENV.REDIS_PRIMARYSET;
const username = __ENV.REDIS_USERNAME;
const password = __ENV.REDIS_PASSWORD;
const vus = 40;

export const options = {
   scenarios: {
       load: {
           executor: "constant-arrival-rate",
           rate: 2,
           duration: "300s",
           timeUnit: "1s",
           preAllocatedVUs: vus,
       }
    },
    summaryTrendStats: ['min', 'med','p(80)', 'p(99)', 'max', 'count'],
};
    
const client = new redis.Client({
  socket: {
    host,
    port,
  },
  username,
  password,
  masterName: primaryset,
  sentinelUsername: username,
  sentinelPassword: password,
});

const key = `key-${__VU}`;
let expected = 0;

export async function setup() {
  for(let n = 0; n < 100000; n++) {
    await client.set(`dummy-${n}`, 'some large string');
  }
  for(let n = 0; n < vus; n++) {
    await client.del(`key-${n + 1}`);
  }
}

export default async function() {
  await client.incrBy(key, 1);
  expected += 1;
  const actual = await client.get(key);
  check(actual, { "value updated": (v) => v == expected});
  if (actual != expected) {
    console.log(`Difference ${expected} != ${actual}`);
    expected = actual;
  }
}
