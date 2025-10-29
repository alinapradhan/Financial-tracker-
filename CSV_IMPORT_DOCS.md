# CSV Import Feature Documentation

## Overview

The CSV Import feature allows users to import bank transactions from CSV files with intelligent column detection and user-friendly mapping.

## Architecture

### Backend (Python/Flask)

**File**: `backend/app.py`

#### Key Functions

1. **`detect_columns(df)`**
   - Automatically detects likely column mappings based on common patterns
   - Checks for date, description, amount, and category columns
   - Returns a dictionary of detected mappings

2. **API Endpoints**

   - **`GET /api/health`**
     - Health check endpoint
     - Returns: `{"status": "ok"}`

   - **`POST /api/csv/parse`**
     - Parses uploaded CSV file
     - Input: CSV file (multipart/form-data)
     - Returns:
       ```json
       {
         "columns": ["Date", "Description", "Amount", "Type"],
         "sample_data": [...],
         "detected_mapping": {
           "date": "Date",
           "description": "Description",
           "amount": "Amount",
           "category": "Type"
         },
         "total_rows": 10
       }
       ```

   - **`POST /api/csv/import`**
     - Imports transactions with user-provided mappings
     - Input:
       ```json
       {
         "file_content": "Date,Description,Amount\n...",
         "mapping": {
           "date": "Date",
           "description": "Description",
           "amount": "Amount",
           "category": "Type"
         }
       }
       ```
     - Returns:
       ```json
       {
         "success": true,
         "transactions": [...],
         "count": 10
       }
       ```

### Frontend (React)

**File**: `frontend/src/CsvImporter.jsx`

#### Component Structure

The CSV Importer is a multi-step wizard with three stages:

1. **Step 1: File Upload**
   - User selects a CSV file
   - File is validated (must be .csv)
   - Click "Continue" to upload and parse

2. **Step 2: Column Mapping**
   - Shows detected column mappings
   - User can manually adjust mappings using dropdowns
   - Required fields: Date, Description, Amount
   - Optional field: Category
   - Displays sample data preview (first 5 rows)
   - Click "Preview Transactions" to continue

3. **Step 3: Preview & Import**
   - Shows formatted transaction list
   - Displays first 10 transactions
   - User reviews and clicks "Import" to complete

#### State Management

```javascript
const [file, setFile] = useState(null);           // Selected file
const [csvData, setCsvData] = useState(null);     // Parsed CSV data
const [mapping, setMapping] = useState({});       // Column mappings
const [transactions, setTransactions] = useState([]); // Imported transactions
const [step, setStep] = useState(1);              // Current step (1-3)
const [loading, setLoading] = useState(false);    // Loading state
const [error, setError] = useState('');           // Error message
```

## CSV Format Support

The system supports common bank CSV formats with the following columns:

### Required Columns
- **Date**: Transaction date (various formats supported)
- **Description**: Transaction description/memo
- **Amount**: Transaction amount (positive for credits, negative for debits)

### Optional Columns
- **Category/Type**: Transaction category

### Example CSV Formats

**Format 1: Generic Bank Statement**
```csv
Date,Description,Amount,Type
2025-01-15,Grocery Store Purchase,-85.50,Shopping
2025-01-16,Salary Deposit,3500.00,Income
```

**Format 2: Credit Card Statement**
```csv
Transaction Date,Merchant,Debit,Credit,Category
01/15/2025,Amazon.com,99.99,,Shopping
01/16/2025,Payroll,,3500.00,Income
```

**Format 3: Minimal Format**
```csv
Date,Description,Amount
2025-01-15,Purchase,-85.50
2025-01-16,Deposit,3500.00
```

## Column Detection Algorithm

The system uses pattern matching to detect columns:

1. **Date Columns**: Matches keywords like "date", "posted", "trans"
2. **Description Columns**: Matches "description", "desc", "memo", "details"
3. **Amount Columns**: Matches "amount", "value", "debit", "credit" (validates numeric data)
4. **Category Columns**: Matches "category", "type"

Column names are normalized (lowercase, trimmed) for matching.

## Error Handling

### Backend Errors
- File not uploaded: `400 Bad Request`
- Invalid CSV format: `500 Internal Server Error`
- Missing required field mapping: `400 Bad Request`
- Invalid data in columns: `500 Internal Server Error`

### Frontend Errors
- Invalid file type: "Please select a valid CSV file"
- Upload failure: "Error uploading file"
- Missing required mappings: "Please map all required fields"
- Import failure: "Error previewing transactions"

## Testing

### Unit Tests

Run backend tests:
```bash
cd backend
source venv/bin/activate
python -m unittest test_app.py -v
```

Tests include:
- Health check endpoint
- Column detection logic
- CSV parsing endpoint
- CSV import endpoint
- Error handling for missing files and mappings

### Manual Testing

1. Use the provided `sample_transactions.csv` file
2. Start both servers
3. Navigate to the frontend
4. Upload the CSV file
5. Verify column mappings are detected correctly
6. Preview and import transactions

## Future Enhancements

- [ ] Support for multi-currency transactions
- [ ] Date format detection and parsing
- [ ] Duplicate transaction detection
- [ ] Transaction validation rules
- [ ] Bulk import from multiple files
- [ ] Import history and rollback
- [ ] Custom column mapping templates
- [ ] Support for Excel files (.xlsx)
