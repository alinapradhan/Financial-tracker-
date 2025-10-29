import { useState } from 'react';
import './CsvImporter.css';

const API_URL = 'http://localhost:5000';

function CsvImporter() {
  const [file, setFile] = useState(null);
  const [csvData, setCsvData] = useState(null);
  const [mapping, setMapping] = useState({
    date: '',
    description: '',
    amount: '',
    category: ''
  });
  const [transactions, setTransactions] = useState([]);
  const [step, setStep] = useState(1); // 1: upload, 2: mapping, 3: preview
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'text/csv') {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Please select a valid CSV file');
      setFile(null);
    }
  };

  const handleFileUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/api/csv/parse`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Failed to parse CSV file');
      }

      const data = await response.json();
      setCsvData(data);

      // Set detected mappings
      if (data.detected_mapping) {
        setMapping({
          date: data.detected_mapping.date || '',
          description: data.detected_mapping.description || '',
          amount: data.detected_mapping.amount || '',
          category: data.detected_mapping.category || ''
        });
      }

      setStep(2);
    } catch (err) {
      setError(err.message || 'Error uploading file');
    } finally {
      setLoading(false);
    }
  };

  const handleMappingChange = (field, value) => {
    setMapping(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePreview = async () => {
    // Validate required fields
    if (!mapping.date || !mapping.description || !mapping.amount) {
      setError('Please map all required fields (Date, Description, Amount)');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Read file content
      const fileContent = await file.text();

      const response = await fetch(`${API_URL}/api/csv/import`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          file_content: fileContent,
          mapping: mapping
        })
      });

      if (!response.ok) {
        throw new Error('Failed to import transactions');
      }

      const data = await response.json();
      setTransactions(data.transactions);
      setStep(3);
    } catch (err) {
      setError(err.message || 'Error previewing transactions');
    } finally {
      setLoading(false);
    }
  };

  const handleImport = () => {
    // In a real app, this would save to database
    alert(`Successfully imported ${transactions.length} transactions!`);
    // Reset to start
    setFile(null);
    setCsvData(null);
    setMapping({ date: '', description: '', amount: '', category: '' });
    setTransactions([]);
    setStep(1);
  };

  const handleReset = () => {
    setFile(null);
    setCsvData(null);
    setMapping({ date: '', description: '', amount: '', category: '' });
    setTransactions([]);
    setStep(1);
    setError('');
  };

  return (
    <div className="csv-importer">
      <h1>Import Transactions from CSV</h1>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Step 1: File Upload */}
      {step === 1 && (
        <div className="upload-section">
          <div className="upload-card">
            <h2>Step 1: Select CSV File</h2>
            <p>Upload a CSV file containing your bank transactions</p>
            
            <div className="file-input-wrapper">
              <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                id="csv-file-input"
              />
              <label htmlFor="csv-file-input" className="file-label">
                {file ? file.name : 'Choose CSV File'}
              </label>
            </div>

            {file && (
              <button
                className="btn btn-primary"
                onClick={handleFileUpload}
                disabled={loading}
              >
                {loading ? 'Processing...' : 'Continue'}
              </button>
            )}
          </div>
        </div>
      )}

      {/* Step 2: Column Mapping */}
      {step === 2 && csvData && (
        <div className="mapping-section">
          <div className="mapping-card">
            <h2>Step 2: Map CSV Columns</h2>
            <p>Match your CSV columns to transaction fields</p>

            <div className="mapping-form">
              <div className="mapping-field">
                <label>
                  Date <span className="required">*</span>
                </label>
                <select
                  value={mapping.date}
                  onChange={(e) => handleMappingChange('date', e.target.value)}
                >
                  <option value="">Select column...</option>
                  {csvData.columns.map(col => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
              </div>

              <div className="mapping-field">
                <label>
                  Description <span className="required">*</span>
                </label>
                <select
                  value={mapping.description}
                  onChange={(e) => handleMappingChange('description', e.target.value)}
                >
                  <option value="">Select column...</option>
                  {csvData.columns.map(col => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
              </div>

              <div className="mapping-field">
                <label>
                  Amount <span className="required">*</span>
                </label>
                <select
                  value={mapping.amount}
                  onChange={(e) => handleMappingChange('amount', e.target.value)}
                >
                  <option value="">Select column...</option>
                  {csvData.columns.map(col => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
              </div>

              <div className="mapping-field">
                <label>Category (Optional)</label>
                <select
                  value={mapping.category}
                  onChange={(e) => handleMappingChange('category', e.target.value)}
                >
                  <option value="">Select column...</option>
                  {csvData.columns.map(col => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="sample-preview">
              <h3>Sample Data Preview</h3>
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      {csvData.columns.map(col => (
                        <th key={col}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {csvData.sample_data.map((row, idx) => (
                      <tr key={idx}>
                        {csvData.columns.map(col => (
                          <td key={col}>{row[col]}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="sample-info">
                Showing {csvData.sample_data.length} of {csvData.total_rows} rows
              </p>
            </div>

            <div className="button-group">
              <button className="btn btn-secondary" onClick={handleReset}>
                Cancel
              </button>
              <button
                className="btn btn-primary"
                onClick={handlePreview}
                disabled={loading}
              >
                {loading ? 'Processing...' : 'Preview Transactions'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Step 3: Preview & Import */}
      {step === 3 && transactions.length > 0 && (
        <div className="preview-section">
          <div className="preview-card">
            <h2>Step 3: Preview & Import</h2>
            <p>Review your transactions before importing</p>

            <div className="transactions-preview">
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Description</th>
                      <th>Amount</th>
                      <th>Category</th>
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.slice(0, 10).map((transaction, idx) => (
                      <tr key={idx}>
                        <td>{transaction.date}</td>
                        <td>{transaction.description}</td>
                        <td className={transaction.amount < 0 ? 'negative' : 'positive'}>
                          ${Math.abs(transaction.amount).toFixed(2)}
                        </td>
                        <td>{transaction.category}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="preview-info">
                Showing 10 of {transactions.length} transactions
              </p>
            </div>

            <div className="button-group">
              <button className="btn btn-secondary" onClick={handleReset}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={handleImport}>
                Import {transactions.length} Transactions
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CsvImporter;
