from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Setup CORS & Headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # Allow UI to talk to API
        self.end_headers()

        try:
            # 2. Get User Input
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            user_message = json.loads(body).get("message", "")

            # 3. OpenRouter Configuration
            # Note: Ensure OPENROUTER_API_KEY is set in Vercel Environment Variables
            api_key = os.environ.get("OPENROUTER_API_KEY", "YOUR_KEY_HERE")
            url = "https://openrouter.ai/api/v1/chat/completions"

            data = json.dumps({
                "model": "nvidia/nemotron-3-super-free",
                "messages": [
                    {"role": "system", "content": "You are Bliss AI, a minimalist and efficient assistant."},
                    {"role": "user", "content": user_message}
                ]
            }).encode('utf-8')

            # 4. Built-in urllib Request (Zero Pip Packages!)
            req = urllib.request.Request(url, data=data)
            req.add_header("Content-Type", "application/json")
            req.add_header("Authorization", f"Bearer {api_key}")
            req.add_header("HTTP-Referer", "http://localhost:3000") # Required by OpenRouter

            with urllib.request.urlopen(req) as response:
                api_response = json.loads(response.read().decode('utf-8'))
                # Extract text from OpenRouter response format
                ai_reply = api_response['choices'][0]['message']['content']
                
                output = json.dumps({"reply": ai_reply})
                self.wfile.write(output.encode('utf-8'))

        except Exception as e:
            error_msg = json.dumps({"reply": f"System Error: {str(e)}"})
            self.wfile.write(error_msg.encode('utf-8'))
          
