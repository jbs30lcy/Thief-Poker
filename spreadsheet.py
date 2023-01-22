import gspread
from oauth2client.service_account import ServiceAccountCredentials
from obj import Card
class SP:
    def __init__(self, num = 0): # num : 반 번호
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
        ]

        json_file_name = 'thief-poker-346a3342e123.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
        gc = gspread.authorize(credentials)

        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1l7bGqQjoqhLUXDCAhGzFqPZHfkKuFDiO7b7UYIaFOh0/edit?usp=sharing'

        self.doc = gc.open_by_url(spreadsheet_url)
        self.ws = self.doc.worksheet(f'player{num}')
        
        self.rows = {}
        i = "A"
        while True:
            word = self.ws.get(f"{i}1")
            if word == [] : break
            word = word[0][0]
            #print(word)
            self.rows[word] = i
            i = chr(ord(i)+1)

    def num_players(self):
        return len(self.worksheet.get_all_values()) - 1 

    def get_hand(self):  #return hand cards as list from spreadsheet
        row = self.rows['hand']
        team += 1
        hand = []
        while True:
            card = self.ws.get(f'{self.row_add(row+i)}{team}')
            if card == "" : break
            hand.append(Card(card, fromcell=True))
        return hand

    def upload_hand(self, team = 0, hand_cards = []): #플레이어의 번호와 카드 리스트를 받아서 스프레드시트에 업로드
        row = self.rows['hand']
        team += 1
        for i, card in enumerate(hand_cards):
            self.ws.update_acell(f'{self.row_add(row,i)}{team}', card.tocell())
        else:
            self.ws.update_acell(f'{self.row_add(row,i+1)}{team}', "")
    
    def row_add(self, row, n): #코드 간결화를 위한 보조 함수
        return chr(ord(row)+n)


# 위는 놔두고 아래부터 수정, json 파일 수정 금지

# worksheet에 업로드 하는 코드
# worksheet.update_acell('B2', 'novels')

# worksheet 상의 모든 텍스트 다 가져오는 코드
# value_all = worksheet.get_all_values()

# worksheet 상의 특정 셀의 텍스트를 가져오는 코드
# cell1 = worksheet.get('B1')


if __name__ == '__main__': #테스트
    sp = SP()
    a = ['11', '21', '31', '41']
    cards = []
    for i in a:
        cards.append(Card(i, fromcell=True))
    sp.upload_hand(1, cards)