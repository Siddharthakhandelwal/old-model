
import pandas as pd
from datetime import datetime
import os

class CallDataManager:
    def __init__(self, excel_path='data.xlsx'):
        self.excel_path = excel_path
        self.create_if_not_exists()
    
    def create_if_not_exists(self):
        if not os.path.exists(self.excel_path):
            df = pd.DataFrame(columns=[
                'name', 'phone_number', 'email', 'callback_time',
                'call_summary', 'model_type', 'call_date'
            ])
            df.to_excel(self.excel_path, index=False)
    
    def add_call_record(self, name, number, email, callback_time, summary, model_type):
        df = pd.read_excel(self.excel_path)
        new_record = {
            'name': name,
            'phone_number': number,
            'email': email,
            'callback_time': callback_time or 'Not specified',
            'call_summary': summary,
            'model_type': model_type,
            'call_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        df.to_excel(self.excel_path, index=False)
