from dotenv import load_dotenv
import os


class Config():

    def __init__(self):
        load_dotenv()

    def load_env_variables(self):
        self.CONNECTION_STRING = os.environ.get('CONNECTION_STRING')
        self.OTEL_SERVICE_NAME = os.environ.get('OTEL_SERVICE_NAME')