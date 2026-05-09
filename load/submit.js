import http from "k6/http";
import { sleep } from "k6";

export const options = {
  stages: [
    { duration: "1m", target: 20 },
    { duration: "3m", target: 100 },
    { duration: "2m", target: 250 },
    { duration: "3m", target: 250 },
    { duration: "2m", target: 0 },
  ],
};

export default function () {
  const payload = JSON.stringify({
    type: "image_resize",
    input: Math.random().toString(36),
  });

  http.post(`${__ENV.API_URL}/submit`, payload, {
    headers: { "Content-Type": "application/json" },
  });

  sleep(0.1);
}