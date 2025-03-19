from base_caller import BaseCaller
from searching import to_check_querr
from datetime import datetime

class DoctorCaller(BaseCaller):
    def __init__(self):
        super().__init__('DOCTOR')

    def prepare_call_data(self, name, number, now):
        current_time = now.strftime("%H:%M:%S")
        return {
            'assistant': {
                "firstMessage": "Hello, This is simran, thank you for calling Apollo Hospitals, Banglore. How can I assist you today?",
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-2-general",
                    "language": "en-IN",
                },
                "model": {
                    "provider": "openai",
                    "model": "gpt-4",
                    "knowledgeBaseId": "ded9fb19-5d4e-41a7-9110-77dd51655d52",
                    "messages": [
                        {
                            "role": "system",
                            "content": f'''You are simran a front desk at Apollo hospital, currently the time is {current_time} and date is {now}. user's name is {name}. Ask questions one by one after taking the user response don't ask all the questions at once. Your task is to clear the user query, book appointments and give recommendations in the medical field. If the user asks any question other than the medical field or hospital just say that you called at Apollo hospital please check the number. Don't say redundantly sorry even if it is your mistake or anything else. Give intuitive answers, act like a human receptionist don't say that you are an AI or live in the digital world. Don't talk about anything other than the medical field or apollo hospital. Keep your answers short. Don't say sorry or apologize redundantly or again and again. Take help from external context also.'''
                        }
                    ]
                },
                "voice": {
                    "provider": '11labs',
                    "voiceId": "ftDdhfYtmfGP0tFlBYA1",
                },
                "backgroundSound": 'office',
            },
            'phoneNumberId': self.phone_number_id,
            'type': 'outboundPhoneCall',
            'customer': {
                'number': number,
                'name': name
            },
        }

    def process_call_result(self, call_id, mail, number, name):
        return to_check_querr(call_id, mail, number, name)

def doctor_call(name, number, mail):
    caller = DoctorCaller()
    return caller.make_call(name, number, mail)