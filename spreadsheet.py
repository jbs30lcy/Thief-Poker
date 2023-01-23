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
        self.ws_dir = self.doc.worksheet(f'director{num}')
        self.cols = self.update_cols_dict(True)
        self.cols_dir = self.update_cols_dict(False)
        # i = "A"
        # while True:
        #     word = self.get_acell(i, 1)
        #     if word == "" : break
        #     self.cols[word] = i
        #     i = chr(ord(i)+1)

    def num_players(self):
        return len(self.worksheet.get_all_values()) - 1 

    def get_hand(self):  #return hand cards as list from spreadsheet
        col = self.cols['hand']
        team += 1
        hand = []
        while True:
            card = self.ws.get(f'{self.col_add(col+i)}{team}')
            if self.cell_is_empty(card) : break
            hand.append(Card(card, fromcell=True))
        return hand

    def upload_hand(self, team = 0, hand_cards = []): #플레이어의 번호와 카드 리스트를 받아서 스프레드시트에 업로드
        col = self.cols['hand']
        team += 1
        for i, card in enumerate(hand_cards):
            self.update_cell(self.col_add(col,i),team, str(card))
        else:
            self.update_cell(self.col_add(col,i+1),team, "")
    
    def upload_playing(self, team=0, hand_cards = [], phase=1):
        col = self.cols[f'phase{phase}']
        team += 1
        hand_cards = [str(x) for x in hand_cards]
        card_text = "|".join(hand_cards)
        self.update_cell(col, team, card_text)

    def get_playing(self, team=0, phase=1):
        col = self.cols[f'phase{phase}']
        team += 1
        
        cards = self.get_acell(col, team)
        if cards == "" : return [] #혹시나 비어있을 경우 에러 처리

        cards = cards.split("|")

        cards = [Card(x, fromcell=True) for x in cards]

        return cards
        
    def has_conducted(self, team = 0, round = 0, phase=1) -> bool : #해당 팀이 해당 라운드 및 페이즈를 진행했는지 확인. eg. sp.has_conducted(1,1,1) : 1팀이 1라운드 첫 조합을 냈는 지 확인
        return self.get_round(team) == round and self.get_phase(team) == phase

    def get_round(self, team = 0) -> int:
        # ValueError: invalid literal for int() with base 10: '' 
        # 위 에러가 뜨면 빈 셀을 읽은 것
        return int(self.get_acell( self.cols_dir['round'], team+1, use_player_sheet=False ))


    def get_phase(self, team = 0) : 
        return int(self.get_acell(self.cols_dir['phase'], team+1, use_player_sheet=False))
    
    # 보조 메소드들
    
    def update_cell(self, col, row, text):
        if type(col) == type(1):
            col_txt = ""
            while col > 0:
                col_txt = col_txt + chr(col%26 + ord("A") - 1) 
                col = col // 26
            col = col_txt
        
        self.ws.update_acell(f"{col}{row}", text)

    def get_acell(self, col, row, use_player_sheet = True):
        if type(col) == type(1): # 열 값으로 숫자로 받아도 되게 처리 eg. 28 -> AA
            col = self.num_to_col(col)
        data = self.ws.get(f"{col}{row}") if use_player_sheet else self.ws_dir.get(f"{col}{row}")
        
        if self.cell_is_empty(data):
            data = ""
        else:
            data = data[0][0]

        return data

    def num_to_col(self, col): #열번호를 숫자로 받아서 알파벳으로 변환 
        col_txt = ""
        while col > 0:
            col_txt = chr(col%26 + ord("A") - 1) + col_txt 
            col = col // 26
        return  col_txt


    def col_add(self, col, n): #코드 간결화를 위한 보조 함수 - 행 알파벳 연산
        return chr(ord(col)+n)

    def cell_is_empty(self, cell):
        return cell==[] or cell == ""

    def update_cols_dict(self, use_player_sheet=True):
        cols = {}
        i = "A"
        while True:
            word = self.get_acell(i, 1, use_player_sheet)
            if word == "" : break
            cols[word] = i
            i = self.col_add(i, 1)

        return cols


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
    sp.upload_playing(1, [Card('11', fromcell=True),'22'], 1)
    print(sp.get_playing(1,1))
    print(sp.get_round(1))
    print(sp.get_phase(1))
    print(sp.has_conducted(1,1,2))
    print(sp.has_conducted(1,2,2))
    
