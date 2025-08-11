# Examples

Sample payloads to try against the Sentiment Analysis API.

## Files
- `payloads/single.json` — single text classification request
- `payloads/batch.json` — batch classification request

## Usage
```bash
# Single
curl -s http://127.0.0.1:8000/predict \
  -H 'content-type: application/json' \
  -d @examples/payloads/single.json | jq .

# Batch
curl -s http://127.0.0.1:8000/predict/batch \
  -H 'content-type: application/json' \
  -d @examples/payloads/batch.json | jq .
```
