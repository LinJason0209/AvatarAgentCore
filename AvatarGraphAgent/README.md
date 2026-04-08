## Curl Test
curl -X POST "http://127.0.0.1:8000/soulmoon/v1/stage/chat_stream" ^
     -H "Content-Type: application/json" ^
     -d "{\"message\": \"你好靈月，請自我介紹\", \"user_id\": \"lin_hong_test\"}"

## Start Server
uvicorn app.api.v1.router:app --reload --port 8000