# Personal Finance Tracker

A privacy-first, local-first budgeting application with encryption at rest and optional cloud sync.

## Features

- **CSV Import**: Import bank transactions from CSV files
- **Column Mapping**: Intelligent column detection and manual mapping UI
- **Transaction Categorization**: Automatic categorization with ML (coming soon)
- **Visualizations**: Monthly reports with Chart.js/D3 (coming soon)
- **Privacy-First**: Data encrypted at rest, stored locally
- **Optional Cloud Sync**: Secure cloud synchronization (coming soon)

## Project Structure

```
Financial-tracker-/
├── frontend/          # React frontend application
├── backend/           # Python Flask backend
└── sample_transactions.csv  # Sample CSV file for testing
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## Using the CSV Import Feature

1. Open the application in your browser
2. Click "Choose CSV File" and select a CSV file containing transactions
3. Click "Continue" to upload and parse the file
4. Map the CSV columns to transaction fields:
   - **Date** (required): The transaction date
   - **Description** (required): Transaction description
   - **Amount** (required): Transaction amount
   - **Category** (optional): Transaction category
5. Click "Preview Transactions" to see the parsed data
6. Review the transactions and click "Import" to complete

### Sample CSV Format

The application works with most bank CSV formats. Here's an example:

```csv
Date,Description,Amount,Type
2025-01-15,Grocery Store,-85.50,Shopping
2025-01-16,Salary Deposit,3500.00,Income
```

A sample CSV file is included as `sample_transactions.csv` for testing.

## Tech Stack

- **Frontend**: React with Vite
- **Backend**: Python Flask
- **Data Processing**: Pandas
- **Database**: SQLite (coming soon)
- **Visualization**: Chart.js/D3 (coming soon)

## Development

### Linting

Frontend:
```bash
cd frontend
npm run lint
```

### Building

Frontend:
```bash
cd frontend
npm run build
```

## License

MIT