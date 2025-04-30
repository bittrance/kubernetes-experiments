import { Client, StatusOK } from 'k6/net/grpc';
import { check } from 'k6';

const endpoint = __ENV.HELLO_GRPC_ENDPOINT || "localhost:8080";

export const options = {
  scenarios: {
    receive_greeting: {
      executor: "constant-arrival-rate",
      rate: 100,
      duration: "60s",
      timeUnit: "1s",
      preAllocatedVUs: 60,
    }
  },
  summaryTrendStats: ['min', 'med','p(80)', 'p(99)', 'max', 'count'],
}

const client = new Client();
client.load([], 'greetings.proto');

export default function receive_greeting() {
  if(__ITER == 0) {
    const options = {
      plaintext: !!__ENV.HELLO_GRPC_PLAINTEXT,
    }
    client.connect(endpoint, options);
  }
  const data = { name: 'Bert' };
  const res = client.invoke('greetings.GreetMe/Send', data);
  if (res.status != StatusOK) {
    console.log(res);
  }
  check(res, {
    'status is OK': (r) => r && r.status === StatusOK,
  });
}
