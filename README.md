# URL Shortener — Serverless on AWS

A serverless URL shortening service built on AWS. Paste a long URL, get a short code back, and share it — the short link redirects anyone who clicks it to the original URL.

![screenshot](https://raw.githubusercontent.com/kbharat1210/url-shortener/main/url-shortener/demo/screenshot.png)

![demo](https://raw.githubusercontent.com/kbharat1210/url-shortener/main/url-shortener/demo/demo.gif)

---

## Architecture

```
User → API Gateway → Lambda → DynamoDB
                         ↓
                     301 Redirect
```

| Layer | Service |
|---|---|
| Frontend | S3 Static Hosting |
| API | AWS API Gateway (HTTP API) |
| Business Logic | AWS Lambda (Python 3.12) |
| Database | AWS DynamoDB |
| Security | AWS IAM |

---

## Features

- Shorten any valid `http://` or `https://` URL
- Short code redirects via HTTP 301
- Collision-safe short code generation with retry logic
- Input validation and error handling
- Request throttling to prevent abuse
- Clean frontend hosted on S3

---

## Project Structure

```
url-shortener/
├── lambdas/
│   ├── create_url.py      # POST /urls — generates short code, stores in DynamoDB
│   └── get_url.py         # GET /urls/{short_code} — looks up and redirects
├── frontend/
│   └── index.html         # Static frontend hosted on S3
├── demo/
│   ├── screenshot.png
│   └── demo.gif
└── README.md
```

---

## API Reference

### Create a short URL
```
POST /urls
```
Request body:
```json
{
  "long_url": "https://www.example.com/very/long/url"
}
```
Response:
```json
{
  "short_code": "DDVTtr",
  "message": "Short URL created successfully"
}
```

### Redirect to original URL
```
GET /urls/{short_code}
```
Returns a `301` redirect to the original URL.

---

## How to Deploy

**Prerequisites**
- AWS account
- AWS CLI configured

**1. Create DynamoDB table**
- Table name: `url-shortener`
- Partition key: `short_code` (String)
- Billing: On-demand

**2. Create Lambda functions**
- Runtime: Python 3.12
- Create two functions using the code in `/lambdas`
- Attach an IAM role with `dynamodb:PutItem` and `dynamodb:GetItem` permissions

**3. Create API Gateway**
- HTTP API
- Routes:
  - `POST /urls` → create_url Lambda
  - `GET /urls/{short_code}` → get_url Lambda
- Enable CORS
- Deploy to `prod` stage

**4. Host the frontend**
- Create an S3 bucket with static website hosting enabled
- Update `API_BASE` in `frontend/index.html` with your API Gateway URL
- Upload `index.html` and make it public

---

## Author

**Bharat Reddy K**  
[GitHub](https://github.com/kbharat1210) · [LinkedIn](https://linkedin.com/in/bharatreddyk)
