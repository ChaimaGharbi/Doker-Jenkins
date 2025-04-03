from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
  return jsonify({
    "message": "Bienvenue sur mon application Devops!!",
    "version": "1.0.5" 
  })
  
  
@app.route("/health")
def health_check():
  return jsonify({"status": "healthy"})


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)