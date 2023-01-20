import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

json_file_name = 'thief-poker-346a3342e123.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1l7bGqQjoqhLUXDCAhGzFqPZHfkKuFDiO7b7UYIaFOh0/edit?usp=sharing'

doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('시트1')

#worksheet.update_acell('B2', 'novels')
value_all = worksheet.get_all_values()
print(value_all)