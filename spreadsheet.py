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

# 위는 놔두고 아래부터 수정, json 파일 수정 금지

# worksheet에 업로드 하는 코드
# worksheet.update_acell('B2', 'novels')

# worksheet 상의 모든 텍스트 다 가져오는 코드
# value_all = worksheet.get_all_values()

# worksheet 상의 특정 셀의 텍스트를 가져오는 코드
# cell1 = worksheet.get('B1')