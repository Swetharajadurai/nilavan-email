
from flask import Flask, request, jsonify
import sendgrid
from sendgrid.helpers.mail import Mail
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
AUTHORIZED_BEARER_TOKEN =os.getenv("BEARER_TOKEN")

@app.route("/send-email", methods=["POST"])
def send_email():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401
    
    token = auth_header.split("Bearer ")[1]
    if token != AUTHORIZED_BEARER_TOKEN:
        return jsonify({"error": "Invalid token"}), 403

    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    if not (name and email and message):
        return jsonify({"error": "Missing required fields"}), 400

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    mail = Mail(
        from_email="swetha@leadtap.ai",
        to_emails="swetha@leadtap.ai",
        subject="New Contact Form Submission",
        plain_text_content=f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
    )

    try:
        sg.send(mail)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)



