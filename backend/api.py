from flask import Flask, request, jsonify
import sendgrid
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
# 🔥 ALLOW YOUR FRONTEND DOMAIN (Replace with your actual Vercel domain)
CORS(app, resources={r"/send-email": {"origins": "*"}})

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    if not (name and email and message):
        return jsonify({"error": "Missing required fields"}), 400

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    mail = Mail(
        from_email="info@leadtap.ai",  # Corrected from 'ifo@'
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
