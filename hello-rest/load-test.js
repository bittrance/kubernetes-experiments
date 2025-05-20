import http from "k6/http";
import { b64encode } from "k6/encoding";
import { check } from "k6";

const endpoint = __ENV.HELLO_REST_ENDPOINT || "http://localhost:8080/";

export const options = {
   scenarios: {
       // Assuming delay=0.8, worerks=4
       load: {
           executor: "constant-arrival-rate",
           rate: 20,
           duration: "300s",
           timeUnit: "1s",
           preAllocatedVUs: 40,
       }
    },
    summaryTrendStats: ['min', 'med','p(80)', 'p(99)', 'max', 'count'],
}

export default function load() {
    let res = http.get(endpoint);
    if (res.status == 0 || res.status > 299) {
        console.log(new Date().toISOString(), res.status);
    }
    check(res, { "status is 200": (r) => r.status == 200 });
}
