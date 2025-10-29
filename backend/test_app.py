import unittest
import json
import io
from app import app, detect_columns
import pandas as pd


class TestCSVImporter(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
    
    def test_detect_columns(self):
        """Test column detection logic"""
        # Create a sample dataframe
        df = pd.DataFrame({
            'Date': ['2025-01-01', '2025-01-02'],
            'Description': ['Purchase', 'Payment'],
            'Amount': [-100.0, 200.0],
            'Category': ['Shopping', 'Income']
        })
        
        detected = detect_columns(df)
        
        # Check that columns are detected
        self.assertIn('date', detected)
        self.assertIn('description', detected)
        self.assertIn('amount', detected)
        self.assertIn('category', detected)
        
        # Check that correct columns are mapped
        self.assertEqual(detected['date'], 'Date')
        self.assertEqual(detected['description'], 'Description')
        self.assertEqual(detected['amount'], 'Amount')
        self.assertEqual(detected['category'], 'Category')
    
    def test_csv_parse(self):
        """Test CSV parsing endpoint"""
        # Create a sample CSV content
        csv_content = "Date,Description,Amount,Type\n2025-01-01,Test,-100.0,Shopping\n"
        
        # Create a file-like object
        data = {
            'file': (io.BytesIO(csv_content.encode()), 'test.csv')
        }
        
        response = self.client.post(
            '/api/csv/parse',
            data=data,
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        
        # Check response structure
        self.assertIn('columns', result)
        self.assertIn('sample_data', result)
        self.assertIn('detected_mapping', result)
        self.assertIn('total_rows', result)
        
        # Check data
        self.assertEqual(len(result['columns']), 4)
        self.assertEqual(result['total_rows'], 1)
    
    def test_csv_parse_no_file(self):
        """Test CSV parsing with no file"""
        response = self.client.post('/api/csv/parse')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_csv_import(self):
        """Test CSV import endpoint"""
        csv_content = "Date,Description,Amount,Type\n2025-01-01,Test Purchase,-100.50,Shopping\n2025-01-02,Salary,3000.00,Income\n"
        
        payload = {
            'file_content': csv_content,
            'mapping': {
                'date': 'Date',
                'description': 'Description',
                'amount': 'Amount',
                'category': 'Type'
            }
        }
        
        response = self.client.post(
            '/api/csv/import',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        
        # Check response
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 2)
        self.assertIn('transactions', result)
        
        # Check transactions
        transactions = result['transactions']
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['amount'], -100.50)
        self.assertEqual(transactions[1]['amount'], 3000.00)
    
    def test_csv_import_missing_mapping(self):
        """Test CSV import with missing required fields"""
        csv_content = "Date,Description,Amount\n2025-01-01,Test,-100.0\n"
        
        payload = {
            'file_content': csv_content,
            'mapping': {
                'date': 'Date',
                # Missing description and amount
            }
        }
        
        response = self.client.post(
            '/api/csv/import',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
