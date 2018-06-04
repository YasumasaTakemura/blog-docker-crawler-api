import os
from env import settings
pwd = os.getcwd()
env_dir_list = os.listdir('{}/env'.format(pwd))
assert '.env' in env_dir_list , 'No .env file. perform "bash ./bin/kms.sh" first.'
print(env_dir_list)
settings.load_dotenv()
