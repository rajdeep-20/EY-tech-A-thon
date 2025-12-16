from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(filename, content):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    
    y = height - 50
    for line in content:
        c.drawString(50, y, line)
        y -= 20
        
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    if not os.path.exists("samples"):
        os.makedirs("samples")
        
    # Accepted Profile
    accepted_content = [
        "CONFIDENTIAL - LOAN APPLICATION DOCUMENT",
        "----------------------------------------",
        "Name: Rajdeep Ghosh",
        "Employment Type: Salaried",
        "Annual Income: INR 12,00,000",
        "Credit Score: 820",
        "Status: Good Standing",
        "Bank: HDFC Bank",
        "Account Number: XXXXXX1234"
    ]
    create_pdf("samples/Accepted_Loan_Profile.pdf", accepted_content)
    
    # Rejected Profile
    rejected_content = [
        "CONFIDENTIAL - LOAN APPLICATION DOCUMENT",
        "----------------------------------------",
        "Name: John Doe",
        "Employment Type: Self-Employed",
        "Annual Income: INR 1,50,000",
        "Credit Score: 550",
        "Status: High Risk",
        "Bank: SBI",
        "Account Number: XXXXXX5678",
        "Notes: Multiple defaults in past 12 months."
    ]
    create_pdf("samples/Rejected_Loan_Profile.pdf", rejected_content)
