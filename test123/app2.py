from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Sample data to simulate sales data
data = [
    {
        "SuperId": "S001",
        "CustomerInfo": "John Doe<br>john.doe@example.com<br>1234567890<br>123 Street, City",
        "CompanyInfo": "XYZ Corp<br>contact@xyz.com<br>0987654321<br>456 Avenue, City",
        "InvoiceId": "SL0199",
        "PaymentStatus": "Paid<br>Completed"
    },
    {
        "SuperId": "S002",
        "CustomerInfo": "Jane Smith<br>jane.smith@example.com<br>2345678901<br>789 Boulevard, City",
        "CompanyInfo": "ABC Inc<br>info@abc.com<br>1234567890<br>321 Road, City",
        "InvoiceId": "SL0999",
        "PaymentStatus": "Pending<br>Not Completed"
    },
    # Add more sales records as needed
]

@app.route('/')
def index():
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
