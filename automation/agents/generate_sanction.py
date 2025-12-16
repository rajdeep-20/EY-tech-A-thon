import sys
import json
import os
import ast
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_pdf(data):
    name = data.get("name", "Customer")
    amount = data.get("amount", 0)
    date = data.get("date", "2024-01-01")
    # Calculate interest rate based on risk score if available, else default
    risk_score = data.get("risk_score", 0.8)
    interest_rate = 10.5 if risk_score > 0.7 else 14.0
    
    filename = f"Sanction_Letter_{name.replace(' ', '_')}.pdf"
    output_path = os.path.join(os.getcwd(), filename)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Header
    header_text = '<font size=18 color="darkblue"><b>Tata Capital Financial Services</b></font>'
    story.append(Paragraph(header_text, styles['Title']))
    story.append(Spacer(1, 20))
    
    # Date
    story.append(Paragraph(f"<b>Date:</b> {date}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Salutation
    story.append(Paragraph(f"Dear <b>{name}</b>,", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Body
    body_text = (
        f"We are pleased to inform you that your loan application has been reviewed and <b>APPROVED</b> based on your credit profile. "
        f"Tata Capital is committed to helping you achieve your financial goals."
    )
    story.append(Paragraph(body_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Loan Details Table
    table_data = [
        ["Description", "Details"],
        ["Sanctioned Amount", f"INR {amount:,.2f}"],
        ["Interest Rate", f"{interest_rate}% p.a."],
        ["Tenure", "36 Months"],
        ["Processing Fee", "INR 2,000"]
    ]
    
    table = Table(table_data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 40))
    
    # Terms
    story.append(Paragraph("<b>Terms and Conditions:</b>", styles['Normal']))
    story.append(Paragraph("1. This sanction is valid for 30 days.", styles['Normal']))
    story.append(Paragraph("2. Disbursal is subject to final verification of documents.", styles['Normal']))
    story.append(Spacer(1, 40))
    
    # Signature
    story.append(Paragraph("Authorized Signatory", styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<i>(Digitally Signed)</i>", styles['Normal']))
    story.append(Paragraph("<b>Tata Capital Loans Division</b>", styles['Normal']))
    
    doc.build(story)
    
    res = {
        "status": "SUCCESS",
        "file_path": output_path,
        "message": "Sanction letter generated successfully."
    }
    
    with open("debug_sanction.json", "w") as f:
        json.dump(res, f)
        
    return res

if __name__ == "__main__":
    try:
        input_str = ""
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if os.path.exists(arg) and os.path.isfile(arg):
                with open(arg, 'r') as f:
                    input_str = f.read().strip()
            else:
                input_str = ' '.join(sys.argv[1:])
        else:
            input_str = sys.stdin.read().strip()
            
        if input_str:
            try:
                data = json.loads(input_str)
            except:
                data = ast.literal_eval(input_str)
                
            result = generate_pdf(data)
            print(json.dumps(result))
        else:
            print(json.dumps({"error": "No input provided"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
