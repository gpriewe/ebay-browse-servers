import requests, csv, base64
from dotenv import dotenv_values

# Define the CSV file names
csv_file = 'ebaydump.csv'
search_file = 'cpulist.csv'

first_pass = True

prd_keys = dotenv_values('.prd-env')
encoded_keys = base64.b64encode((prd_keys['APP_ID'] + ':' + prd_keys['CERT_ID']).encode('utf-8')).decode('utf-8')
search_value = '5118'

def generate_oauth_token(encoded_keys):
    urloauth = 'https://api.ebay.com/identity/v1/oauth2/token'
    payloadoauth = { 'grant_type': 'client_credentials', 'scope': 'https://api.ebay.com/oauth/api_scope'}
    headersoauth = { 'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic ' + encoded_keys}
    responseoauth = requests.post(urloauth, data=payloadoauth, headers=headersoauth)
    #print(responseoauth.json()['access_token'])
    if responseoauth.status_code == 200:
        tokenoauth = responseoauth.json()['access_token']
    else:
        print(str(responseoauth.status_code) + ' ' + responseoauth.text)
        exit()
    #tokenoauth = 'v^1.1#i^1#I^3#p^1#r^0#f^0#t^H4sIAAAAAAAAAOVYW2wUVRjebbdIW7pERLnIw3a4GMW57ezs7ky6i0svdKWlS3dpobFp5nKmHbo7s86Zoa0hZGmwiRdqhIQQcJM+AA/wAiYikIixJgiGiJJ4iSKakCgPPmCE8IKJZ6ZL2VbCrZvYxH3ZzH/+85/v+87/nxuVm1P50kjzyO0a91NlYzkqV+Z209VU5ZyK1d7ysqUVLqrIwT2WW5HzDJdfr4NCJp3l2wHM6hoEvsFMWoO8Y4xglqHxugBVyGtCBkDelPhkrLWF9xMUnzV0U5f0NOaLN0QwWWYVRaIVILEKB5gwsmp3Y6b0CMaKbDAYFgWGDsiMKEioHUILxDVoCpoZwfyUP4DTNE5zKYrhKZZnAkQgGO7CfB3AgKquIReCwqIOXN7paxRhfTBUAUJgmCgIFo3HmpJtsXhD44ZUHVkUK1rQIWkKpgWnftXrMvB1CGkLPHgY6HjzSUuSAIQYGZ0YYWpQPnYXzBPAd6RWaC7MAdEvM4BTuDBdEimbdCMjmA/GYVtUGVccVx5opmoOPUxRpIa4FUhm4WsDChFv8Nl/Gy0hrSoqMCJY49rYllgigUXXGYhBwlDxJBAMqQ9PtDfgnEgHw1wwQOMsRTF+jhMLw0zEKog8bZx6XZNVWzLo26CbawHCDKYq4+fZImWQU5vWZsQU08ZT7MdOKkh32VM6MYeW2afZswoySAaf8/lw/Sd7m6ahipYJJiNMb3AEimBCNqvK2PRGJxMLyTMII1ifaWZ5khwYGCAGGEI3ekk/RdHk5taWpNQHMgLm+Nq1bvurD++Aqw4VCaCeUOXNoSzCMogyFQHQerEoSwUZlinoPhVWdLr1X4YizuTUeihVfXD+IED1wXCiKAVCglKK+ogWUpS0cQBRGMIzgtEPzGxakAAuoTyzMsBQZZ5hFT8TVgAuBzkFD3CKgousHMTRyggoABAkLvz/KZNHTfQkkAxglijTS5Tl4U4uSa0z5AG2vaGvMym1kpssGG6jyaTV2UT1vr76DeZVNRHq6Cd7I49aC/clX59WkTIpNH6pBLBrvTQiNOvQBPKM6CUlPQsSelqVhmbXBDOGnBAMcygJ0mlkmBHJWDYbL9VKXSJ6j7VIPBnrUu5P/8nedF9W0E7Y2cXK7g9RACGrEvbuQ0h6htQFdOwg7VpH5h4H9Yx4q+jMOqtYI5ITbFV54rBJOJQJuE0iDAB1y0DnbKLNPn2l9H6god3MNPR0Ghgd9IyrOZOxTEFMg9lW1iVIcFWYZVstHWLQnYZlmcCMeEnORtoz25ak0i3EnjWPeaAmp17uoy7nRw+7x6lh99kyt5uqo1bSy6naOeWbPOXzlkLVBIQqKARUezV0ZzUA0Q+GsoJqlD3juuRtkXc2t9zKidbHnTfXhF01RW8LY93U4snXhcpyurroqYFadq+lgp6/qMYfoGmaoxgKzXgXtfxeq4d+zrNQTS1r+XpXVwB4TyZePoyPJnbczlM1k05ud4XLM+x2vXl4sKf+80u/pKwP42fz4V0S/f3YX3krfi337oWvLj+9sf3OD/OXrwLN+z/L+1Z/Odpdpby14tzbiaOL15+u8v62aMuVnYtOdRNbvYtNvfyyK9RdK92uvLBg//i+1uOndm/+deD0qfyV3Ufeee3YwRtXT/98gg+5m/aenHtj/NjmeesPVR3I4X/v3f378KpYrKZj9PzIndodZ744f/y9Pa3VNy+sr1m54MAL46Hsj1usa8z5W/lQbE/8yKbrvovVz//U803dyqo/Ao0LlWfz51o8d5Qz5078eTAmrr1ZqV5advTsttoX9x3e1d3lfv+TQyPbgx8tIJZ4v418t72xnP1gSfzoRa/n6rbMp3NfmZjLfwCqRFNd9REAAA=='
    return tokenoauth

tokenoauth = generate_oauth_token(encoded_keys)

# Read from CSV
def read_csv(search_file):
    with open(search_file, mode='r', encoding='utf-8') as file: 
        reader = csv.DictReader(file)
        #for row in reader:
            #print(row)
        search_file_processed = [row for row in reader]
    print(f'Data read from {search_file}')
    return search_file_processed

def get_results(tokenoauth, url):
    headers = { 'Accept-Lanuage': 'en-US', 'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US', 'Authorization': 'Bearer ' + tokenoauth }
    response = requests.get(url, headers=headers).json()
    #print(response)
    return response

fieldnames = ['itemId', 'title', 'price_value', 'seller_username', 'seller_feedbackPercentage', 'seller_feedbackScore', 
                'condition', 'shippingOptions_shippingCostType', 'shippingOptions_shippingCost_value', 'buyingOptions', 'itemWebUrl', 
                'itemLocation_postalCode', 'itemCreationDate']

fieldname_mapping = {
    'itemId': ['itemId'],
    'title': ['title'],
    'price_value': ['price', 'value'],
    'seller_username': ['seller', 'username'],
    'seller_feedbackPercentage': ['seller', 'feedbackPercentage'],
    'seller_feedbackScore': ['seller', 'feedbackScore'],
    'condition': ['condition'],
    'shippingOptions_shippingCostType': ['shippingOptions', 0, 'shippingCostType'],
    'shippingOptions_shippingCost_value': ['shippingOptions', 0, 'shippingCost', 'value'],
    'buyingOptions': ['buyingOptions', 0],
    'itemWebUrl': ['itemWebUrl'],
    'itemLocation_postalCode': ['itemLocation', 'postalCode'],
    'itemCreationDate': ['itemCreationDate']
}

# Function to retrieve nested values, handling lists as well
def get_nested_values(record, path):
    value = record
    for key in path:
        if isinstance(value, list): # Check if the value is a list
            if value: # If the list is not empty, access the first element
                value = value[0] # Get the first element of the list
            else:
                value = '' # If the list is empty, return a default value
        elif isinstance(value, dict):
            value = value.get(key, '')
        else:
            return ''
    return value

# Transform the data so that it matches the custom fieldnames
def get_mapped_data(response):
    mapped_data = [
        {custom_field: get_nested_values(record, original_key) for custom_field, original_key in fieldname_mapping.items()}
        for record in response
    ]
    return mapped_data

# Write to CSV
def write_csv(csv_file, mapped_data, fieldnames, response, first_pass, tokenoauth):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file: 
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Write the header
        if first_pass == True:
            writer.writeheader()
            first_pass = False

        # Write the data
        writer.writerows(mapped_data)

        try:
            while response['next']:
                response = get_results(tokenoauth, response['next'])
                writer.writerows(get_mapped_data(response['itemSummaries']))
        except KeyError:
            pass
    print(f'Data written to {csv_file}')
    return first_pass

search_file_processed = read_csv(search_file)
for row in search_file_processed:
    search_value = row['name']
    url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?q=1u ' + search_value + '&category_ids=11211&filter=price:[..1000],priceCurrency:USD,itemLocationCountry:US,searchInDescription:true'
    response = get_results(tokenoauth, url)
    if response['total'] == 0:
        print(search_value + ' Empty')
        continue
    first_pass = write_csv(csv_file, get_mapped_data(response['itemSummaries']), fieldnames, response, first_pass, tokenoauth)
