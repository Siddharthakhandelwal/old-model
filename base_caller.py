
import os
import requests
from datetime import datetime
from data_manager import CallDataManager
import logging

class BaseCaller:
    def __init__(self, model_type):
        self.model_type = model_type
        self.auth_token = os.getenv(f'VAPI_AUTH_TOKEN_{model_type.upper()}')
        self.phone_number_id = os.getenv(f'PHONE_NUMBER_ID_{model_type.upper()}')
        
        if not self.auth_token or not self.phone_number_id:
            raise ValueError(f"Missing required environment variables for {model_type}")
            
        self.data_manager = CallDataManager()

    def send_call_request(self, headers, data):
        response = requests.post(
            'https://api.vapi.ai/call',
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def make_call(self, name, number, mail, callback_time=None):
        try:
            if not all([name, number]):
                raise ValueError("Name and number are required")

            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json',
            }

            now = datetime.now()
            data = self.prepare_call_data(name, number, now)
            
            response = self.send_call_request(headers, data)
            call_id = response.get('id')
            
            if call_id:
                summary = self.process_call_result(call_id, mail, number, name)
                self.data_manager.add_call_record(
                    name, number, mail, callback_time, summary, self.model_type
                )
            
            return response

        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            logging.error(error_msg)
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Error in {self.model_type} call: {str(e)}"
            logging.error(error_msg)
            return {"error": error_msg}

    def prepare_call_data(self, name, number, now):
        raise NotImplementedError
        
    def process_call_result(self, call_id, mail, number, name):
        raise NotImplementedError
