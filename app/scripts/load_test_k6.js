import http from 'k6/http';
import { sleep } from 'k6';
export let options = { vus: 10, duration: '30s' };
export default function () {
  http.post('http://localhost:8000/predict', JSON.stringify({ text: 'I love this!' }), { headers: { 'Content-Type': 'application/json' } });
  sleep(1);
}
