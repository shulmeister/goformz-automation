import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from goformz_client import GoFormzClient
from shiftcare_automation import ShiftcareAutomation
from pdf_parser import PDFParser

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
goformz_client = GoFormzClient(
    client_id=os.getenv('GOFORMZ_CLIENT_ID'),
    client_secret=os.getenv('GOFORMZ_CLIENT_SECRET')
)

shiftcare_automation = ShiftcareAutomation(
    username=os.getenv('SHIFTCARE_USERNAME'),
    password=os.getenv('SHIFTCARE_PASSWORD')
)

pdf_parser = PDFParser()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "GoFormz-Shiftcare Integration API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "forms": "/forms",
            "process_packets": "/process-packets"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/process-packets', methods=['POST'])
def process_packets():
    try:
        # Get form IDs from request or fetch all recent forms
        form_ids = request.json.get('form_ids', [])
        
        if not form_ids:
            # Fetch recent forms from GoFormz
            forms = goformz_client.get_recent_forms()
            form_ids = [form['id'] for form in forms]
        
        results = []
        
        for form_id in form_ids:
            try:
                # Download PDF from GoFormz
                pdf_data = goformz_client.download_form_pdf(form_id)
                
                # Parse PDF to extract data
                parsed_data = pdf_parser.parse_pdf(pdf_data)
                
                # Determine if it's a client or employee packet
                packet_type = pdf_parser.determine_packet_type(parsed_data)
                
                # Create in Shiftcare
                if packet_type == 'client':
                    result = shiftcare_automation.create_client_with_care_plan_sync(parsed_data)
                elif packet_type == 'employee':
                    result = shiftcare_automation.create_employee_sync(parsed_data)
                else:
                    result = {"error": "Unknown packet type"}
                
                results.append({
                    "form_id": form_id,
                    "packet_type": packet_type,
                    "result": result
                })
                
            except Exception as e:
                logger.error(f"Error processing form {form_id}: {str(e)}")
                results.append({
                    "form_id": form_id,
                    "error": str(e)
                })
        
        return jsonify({"results": results})
        
    except Exception as e:
        logger.error(f"Error in process_packets: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/forms', methods=['GET'])
def get_forms():
    try:
        forms = goformz_client.get_recent_forms()
        return jsonify({"forms": forms})
    except Exception as e:
        logger.error(f"Error fetching forms: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
