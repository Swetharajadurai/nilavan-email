@app.route("/send-email", methods=["POST"])
def send_email():
    try:
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
            to_emails=email,
            subject="New Contact Form Submission",
            plain_text_content=f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
        )

        response = sg.send(mail)
        
        # Debugging information
        print("SendGrid Response Status Code:", response.status_code)
        print("SendGrid Response Headers:", response.headers)

        return jsonify({"message": "Email sent successfully!", "status": response.status_code}), 200

    except Exception as e:
        print("SendGrid Error:", str(e))
        return jsonify({"error": str(e)}), 500
