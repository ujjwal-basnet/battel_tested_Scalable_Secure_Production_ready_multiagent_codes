When building APIs, we   need  to ensure that  only authorized users can access our services 

one way of acheving this is using API key authentication using a header. 
``` 
from fastapi.security import APIKeyHeader 
 
 ```

so what is a this? 

when   you click a send button on chatgpt.com then ,  your browser sends an **HTTP request** to their server.

this request includes some information  basically “labels” telling the server about you and what you’re sending , and where it should go. etc .  which is called **HTTP headers**


Realistic HTTP header examples 
```
POST /v1/chat/completions HTTP/1.1    # "I want to send a message."

Host: api.openai.com                   # "Which server should handle this?"

Authorization: Bearer sk-aBcDeFgHiJkLmNoPqRsTuVwXyZ...  # "Here’s my secret key to prove I’m allowed"

Content-Type: application/json         # "I’m sending JSON data"

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...  # "This is my browser/app"

Accept: application/json               # "I expect JSON back from the server"
``` 