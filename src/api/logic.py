from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()

        api_key = os.environ.get("OPENROUTER_API_KEY")
        
        if not api_key:
            self.wfile.write(json.dumps({"reply": "Error: Key not found in Vercel Env."}).encode())
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            user_message = json.loads(body).get("message", "")

            url = "https://openrouter.ai/api/v1/chat/completions"
            
            # UPDATED TO GPT-4O-MINI
            payload = {
                "model": "openai/gpt-4o-mini", 
                "messages": [
                    {"role": "system", "content": "You are Bliss AI, a helpful assistant."},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7
            }

            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'))
            req.add_header("Authorization", f"Bearer {api_key}")
            req.add_header("Content-Type", "application/json")
            # OpenRouter needs these to stay active
            req.add_header("HTTP-Referer", "http://bliss-ai-local") 

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Double check the response structure
                if 'choices' in result:
                    ai_reply = result['choices'][0]['message']['content']
                else:
                    ai_reply = f"API Error: {result.get('error', {}).get('message', 'Unknown error')}"
                
                self.wfile.write(json.dumps({"reply": ai_reply}).encode())

        except Exception as e:
            self.wfile.write(json.dumps({"reply": f"Python Error: {str(e)}"}).encode())
            
