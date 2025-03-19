
import pandas as pd
from datetime import datetime
import os
import re
import logging

logging.basicConfig(
    filename='calls.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CallDataManager:
    def __init__(self, excel_path='data.xlsx'):
        self.excel_path = excel_path
        self.create_if_not_exists()
    
    def create_if_not_exists(self):
        try:
            if not os.path.exists(self.excel_path):
                df = pd.DataFrame(columns=[
                    'name', 'phone_number', 'email', 'callback_time',
                    'call_summary', 'model_type', 'call_date'
                ])
                df.to_excel(self.excel_path, index=False)
                logging.info(f"Created new Excel file at {self.excel_path}")
        except Exception as e:
            logging.error(f"Error creating Excel file: {str(e)}")
            raise

    def validate_phone_number(self, number):
        # Basic phone number validation
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, number))

    def validate_email(self, email):
        if not email:
            return True
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def add_call_record(self, name, number, email, callback_time, summary, model_type):
        try:
            if not name or not number:
                raise ValueError("Name and phone number are required")
            
            if not self.validate_phone_number(number):
                raise ValueError("Invalid phone number format")
            
            if email and not self.validate_email(email):
                raise ValueError("Invalid email format")

            df = pd.read_excel(self.excel_path)
            new_record = {
                'name': name.strip(),
                'phone_number': number,
                'email': email if email else 'Not provided',
                'callback_time': callback_time or 'Not specified',
                'call_summary': summary,
                'model_type': model_type,
                'call_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            df.to_excel(self.excel_path, index=False)
            logging.info(f"Added new call record for {name}")
            
        except Exception as e:
            logging.error(f"Error adding call record: {str(e)}")
            raise
