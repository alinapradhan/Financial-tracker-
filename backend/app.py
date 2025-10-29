from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Common bank CSV formats
COMMON_FORMATS = {
    'generic': {
        'date': ['date', 'transaction_date', 'posted_date', 'trans_date'],
        'description': ['description', 'desc', 'memo', 'transaction_description'],
        'amount': ['amount', 'transaction_amount', 'value'],
        'category': ['category', 'type', 'transaction_type']
    }
}

def detect_columns(df):
    """Detect likely column mappings based on common patterns"""
    columns = df.columns.tolist()
    detected = {}
    
    # Normalize column names for detection
    normalized_cols = {col: col.lower().strip() for col in columns}
    
    # Detect date column
    for col, norm in normalized_cols.items():
        if any(pattern in norm for pattern in ['date', 'posted', 'trans']):
            if 'date' not in detected:
                detected['date'] = col
                
    # Detect description column
    for col, norm in normalized_cols.items():
        if any(pattern in norm for pattern in ['description', 'desc', 'memo', 'details']):
            if 'description' not in detected:
                detected['description'] = col
                
    # Detect amount column
    for col, norm in normalized_cols.items():
        if any(pattern in norm for pattern in ['amount', 'value', 'debit', 'credit']):
            # Check if column contains numeric data
            try:
                pd.to_numeric(df[col].head(10), errors='coerce')
                if 'amount' not in detected:
                    detected['amount'] = col
            except:
                pass
    
    # Detect category column
    for col, norm in normalized_cols.items():
        if any(pattern in norm for pattern in ['category', 'type']):
            if 'category' not in detected:
                detected['category'] = col
    
    return detected

@app.route('/api/csv/parse', methods=['POST'])
def parse_csv():
    """Parse CSV file and return structure info"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read CSV file
        content = file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(content))
        
        # Get column information
        columns = df.columns.tolist()
        
        # Detect likely column mappings
        detected_mapping = detect_columns(df)
        
        # Get sample data (first 5 rows)
        sample_data = df.head(5).to_dict('records')
        
        # Convert numpy types to native Python types for JSON serialization
        for row in sample_data:
            for key, value in row.items():
                if pd.isna(value):
                    row[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    row[key] = value.isoformat()
                elif hasattr(value, 'item'):  # numpy types
                    row[key] = value.item()
        
        return jsonify({
            'columns': columns,
            'sample_data': sample_data,
            'detected_mapping': detected_mapping,
            'total_rows': len(df)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/csv/import', methods=['POST'])
def import_csv():
    """Import CSV with user-provided column mappings"""
    try:
        data = request.get_json()
        
        if 'file_content' not in data or 'mapping' not in data:
            return jsonify({'error': 'Missing file content or mapping'}), 400
        
        # Parse the CSV content
        df = pd.read_csv(io.StringIO(data['file_content']))
        
        mapping = data['mapping']
        
        # Validate mapping
        required_fields = ['date', 'description', 'amount']
        for field in required_fields:
            if field not in mapping or not mapping[field]:
                return jsonify({'error': f'Missing required field mapping: {field}'}), 400
        
        # Create standardized transaction list
        transactions = []
        for _, row in df.iterrows():
            transaction = {
                'date': str(row[mapping['date']]) if mapping.get('date') else None,
                'description': str(row[mapping['description']]) if mapping.get('description') else None,
                'amount': float(row[mapping['amount']]) if mapping.get('amount') else 0.0,
                'category': str(row[mapping['category']]) if mapping.get('category') and mapping['category'] else 'Uncategorized'
            }
            transactions.append(transaction)
        
        return jsonify({
            'success': True,
            'transactions': transactions,
            'count': len(transactions)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
