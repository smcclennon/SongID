# SongID Data parse
# smcclennon.github.io
# Parse the SongID userdata json file and display statistics about usage


import json

total_users = 0
total_api_calls = 0
api_calls_above_0 = 0
api_calls_at_0 = 0

# Load user data json
with open('data/userdata.json', 'r') as f:
    userdata = json.load(f)

# Parse all user data
for user in userdata:
    total_users += 1  # Count how many users there are

    if 'api_calls' in userdata[user]:
        user_api_calls = int(userdata[user]['api_calls'])  # Extract api call count from users data
        total_api_calls += user_api_calls  # Increment the total api call variable
        if user_api_calls > 0:
            api_calls_above_0 += 1  # Count how many users have used SongID
        del user_api_calls

api_calls_at_0 = total_users - api_calls_above_0  # Determine how many users haven't tried to identify a song
percent_users_used = api_calls_above_0 / total_users * 100


# Print results
# variable:, = add commas to numbers
# eg 30000 -> 30,000
print(f'Total users: {total_users:,}')
print(f'Total songs processed: {total_api_calls:,}')
print(f'\nUsers who have used SongID: {api_calls_above_0:,}')
print(f'Users who have not used SongID: {api_calls_at_0:,}')
print(f'Percentage of users who have used SongID: {round(percent_users_used, 2)}%')  # Round to 2 decimal places
