# Set up SongID
# github.com/smcclennon/SongID


import os, json


# If you're deploying locally (not with Heroku), then uncomment
# these environment variable declarations and replace the values
# with your own bot token, telegram user ID, telegram username,
# and your own ACR Cloud API keys and secrets

# The current values are randomly generated strings, and will not work

# Example values (change this)
'''
os.environ['telegram_token'] = '1000000000:CwdERilvbzQIBShDtFfOfiPXwvmoGjgxiHQ'
os.environ['telegram_devid'] = '000000000'
os.environ['telegram_devusername'] = '@username'

os.environ['acr_clear_access_key'] = 'OyswaLrqexEuTJmBVBFdzxuvECziwYvb'
os.environ['acr_clear_access_secret'] = 'cVNYZoIhEVjsekkeZUyMKBwICnsGGkFTTHdwecnx'

os.environ['acr_noisy_access_key'] = 'NGoKAAnwrLzxyyJLPvPYZLdSRarqMFoj'
os.environ['acr_noisy_access_secret'] = 'iePWlMXjDwYTakSDBQNXqcJcDSuFiiFSZbVAsuEs'

os.environ['acr_hum_access_key'] = 'OyswaLrqexEuTJmBVBFdzxuvECziwYvb'
os.environ['acr_hum_access_secret'] = 'cVNYZoIhEVjsekkeZUyMKBwICnsGGkFTTHdwecnx'
'''


# Required variables (don't change this)
required_vars = [  # Environment variables required
    'telegram_token',
    'telegram_devid',
    'telegram_devusername',
    'acr_clear_access_key',
    'acr_clear_access_secret',
    'acr_noisy_access_key',
    'acr_noisy_access_secret',
    'acr_hum_access_key',
    'acr_hum_access_secret',
    'heroku_enabled',
    'heroku_webhook'
]


# Keep track
environment_variables = {
    'success': {},  # keep track of successful import names
    'failed': [],  # keep track of failed import names
    'current_env_var': {}  # keep track of current env var name
}


print('Retrieving required environment variables')
for variable_name in required_vars:
    print('\n    '+variable_name+'...', end='')
    environment_variables['current_env_var'][variable_name] = os.getenv(variable_name)

    if environment_variables['current_env_var'][variable_name] == None:
        print('Failed!\n        [!] Environment variable does not exist!')
        environment_variables["failed"].append(variable_name)
    else:
        print('Success!')
        environment_variables["success"][variable_name] = environment_variables['current_env_var'][variable_name]


print(f'\n\nSuccessfully imported {len(environment_variables["success"])} environment variables')
for item in environment_variables["success"]:
    print('    '+str(item))

if len(environment_variables["failed"]) > 0:
    print(f'\nFailed to import {len(environment_variables["failed"])} environment variables')
    for item in environment_variables["failed"]:
        print('\n    '+item)
        print('    Please manually enter a value for '+item)
        environment_variables["success"][item] = str(input('        '+item+' = '))


print('\n\nLoading token example json file...')
with open('data/token_example.json', 'r') as f:
    tokens = json.load(f)
print('Overwriting example tokens with environment variables...')
tokens["telegram"]["token"] = environment_variables["success"]["telegram_token"]
tokens["telegram"]["devid"] = environment_variables["success"]["telegram_devid"]
tokens["telegram"]["devusername"] = environment_variables["success"]["telegram_devusername"]
tokens["acr"]["clear"]["access_key"] = environment_variables["success"]["acr_clear_access_key"]
tokens["acr"]["clear"]["access_secret"] = environment_variables["success"]["acr_clear_access_secret"]
tokens["acr"]["noisy"]["access_key"] = environment_variables["success"]["acr_noisy_access_key"]
tokens["acr"]["noisy"]["access_secret"] = environment_variables["success"]["acr_noisy_access_secret"]
tokens["acr"]["hum"]["access_key"] = environment_variables["success"]["acr_hum_access_key"]
tokens["acr"]["hum"]["access_secret"] = environment_variables["success"]["acr_hum_access_secret"]
if str(environment_variables["success"]["heroku_enabled"]).upper() in ['1', 'true', 'y', 'yes']:
    tokens["heroku"]["enabled"] = 'True'
tokens["heroku"]["webhook"] = environment_variables["success"]["heroku_webhook"]


print('Dumping tokens to token json file...')
with open('data/token.json', 'w') as f:
    json.dump(tokens, f, indent=4)


if not os.path.isfile('data/userdata.json'):
    print('\nCreating userdata json file...')
    with open('data/userdata.json', 'w') as f:
        f.write('{}')


print('\nClearing all variables (preparing for running SongID)...')
import sys
sys.modules[__name__].__dict__.clear()

print('Now importing SongID. If you have provided any invalid tokens,\
SongID will crash.')
print('Importing SongID...\n\n\n')
try:
    import SongID
    exit()
except ImportError as e:
    print('ImportError: '+str(e))
except Exception as e:
    if str(e) == "Unauthorized":
        print('Unauthorized bot token. Does it exist? Please double check your environment variables,\n\
and if you haven\'t set any, re-run this setup script and enter the correct value.')
    elif str(e) == "Invalid Token":
        print('Invalid Telegram bot token. Please double check your environment variables,\n\
and if you haven\'t set any, re-run this setup script and enter the correct value.')
    else:
        raise(e)

input('\nPress enter to exit')