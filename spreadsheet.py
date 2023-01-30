import gspread
from oauth2client.service_account import ServiceAccountCredentials
from obj import Card
import pymysql
class SP:
    def __init__(self, num = 0, team=0): # num : 반 번호
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
        self.team = team

    def ck_players(self, num_players=8):
        teams = self.get_cell_range(self.cols['team'], 1, 2, num_players)
        for team in teams: 
            if self.cell_is_empty(team):
                return False
        return True

    def get_start_permission(self, match=0):
        cell = self.get_acell(col='match_permission', row=self.team+1, use_player_sheet=False)
        if self.cell_is_empty(cell) :
            return False
        else:
            return int(cell) == match

    def enroll_player(self):
        team = self.team
        self.update_cell(1, team+1, team)
        self.update_cell(1, team+1, team, False)
        for i in range(2,10):
            self.update_cell(i, team+1, "")

    def num_players(self):
        cells = self.get_cell_range('team', 1, 2, self.num_players)
        i = 0
        for c in cells:
            if c != "" :
                i += 1
        return i == self.num_players

    def get_hand(self, team = 0):  #return hand cards as list from spreadsheet
        if team == 0 : team = self.team
        col = self.cols['hand']
        team += 1
        hand = []
        cards = self.get_acell('hand', team).split('|')
        for card in cards:
            if self.cell_is_empty(card):break
            hand.append(Card(card, fromcell=True))

        return hand

    def upload_hand(self, team = 0, hand_cards = []): #플레이어의 번호와 카드 리스트를 받아서 스프레드시트에 업로드
        if team == 0 : 
            team = self.team
        team += 1
        text = "|".join(map(str,hand_cards))
        self.update_cell('hand', team, text)
        #self.update_cell_range('hand', len(hand_cards)+1, team, 1, hand_cards+[''] )

    def upload_playing(self, team=0, hand_cards = [], match=0, round=0, phase=1):
        if team == 0 : team = self.team
        col = self.cols[f'phase{phase}']
        team += 1
        hand_cards = [str(x) for x in hand_cards]
        card_text = "|".join(hand_cards)
        self.update_cell(col, team, card_text)
        self.update_cell_range('match', 3, team, 1, [match, round, phase], use_player_sheet=False)

    def upload_step(self, step="round", text = "", team = 0):
        if team==0 : team=self.team
        team += 1
        col = self.cols_dir[step]
        self.update_cell(col, team, text)

    def get_common(self, round=1):
        cell = self.get_acell(f"common{round}", self.team+1, use_player_sheet=True)
        #print(cell)
        #print(Card(cell, fromcell=True))
        return Card(cell, fromcell=True)
    
    def clear_phase(self):
        self.update_cell_range('phase1', 2, self.team+1, 1, ["" for x in range(2)])

    def get_playing(self, team=0, phase=1):
        if team == 0 : team = self.team
        col = self.cols[f'phase{phase}']
        team += 1
        
        cards = self.get_acell(col, team)
        if cards == "" : return [] #혹시나 비어있을 경우 에러 처리

        cards = cards.split("|")
        print(f"get_playing : {cards}")
        cards = [Card(x, fromcell=True) for x in cards]

        return cards
        
    def has_conducted(self, team = 0, round = 0, phase=1) -> bool : #해당 팀이 해당 라운드 및 페이즈를 진행했는지 확인. eg. sp.has_conducted(1,1,1) : 1팀이 1라운드 첫 조합을 냈는 지 확인
        if team == 0 : team = self.team
        r, p = map(int, self.get_cell_range('round', 2, team + 1, 1, use_player_sheet=False))
        
        return r == round and p == phase

    def get_match(self, team = 0) -> int:
        # ValueError: invalid literal for int() with base 10: '' 
        # 위 에러가 뜨면 빈 셀을 읽은 것
        if team == 0 : team = self.team
        cell = self.get_acell( self.cols_dir['match'], team+1, use_player_sheet=False )
        return 0 if self.cell_is_empty(cell) else int(cell)

    def get_opponent(self, match, team=0) :
        if team == 0 : team = self.team

        cell = self.get_acell( 'opponents', team+1, use_player_sheet=False)
        opponent = int(cell.split("|")[match-1])

        return opponent

    

    def get_round(self, team = 0) -> int:
        # ValueError: invalid literal for int() with base 10: '' 
        # 위 에러가 뜨면 빈 셀을 읽은 것
        if team == 0 : team = self.team
        cell = self.get_acell( 'round', team+1, use_player_sheet=False )
        return 0 if self.cell_is_empty(cell) else int(cell)


    def get_phase(self, team = 0) : 
        if team == 0 : team = self.team
        cell = self.get_acell( 'phase', team+1, use_player_sheet=False )
        return 0 if self.cell_is_empty(cell) else int(cell)
    # 보조 메소드들
    
    def get_cell_range(self, col_start, num_cols, row_start, num_rows, use_player_sheet=True):
        if type(col_start) == type(1):
            col_start = self.num_to_col(col_start)
        if len(col_start) > 2:
            col_start = self.cols[col_start] if use_player_sheet else self.cols_dir[col_start]

        table_range = f"{col_start}{row_start}:{self.col_add(col_start, num_cols-1)}{row_start+num_rows-1}"
        
        table = self.ws.range(table_range) if use_player_sheet else self.ws_dir.range(table_range)
        #print(table)
        table = [x.value for x in table]
        #print(table)
        res = []
        for i in range(num_rows):
            res.append([])
            for j in range(num_cols):
                res[i].append(table[num_cols*i + j])
        if num_cols == 1:
            res = [x[0] for x in res]
        if num_rows == 1:
            res = res[0]
        return res
    def update_cell_range(self, col_start, num_cols, row_start, num_rows, texts, use_player_sheet=True):
        
        if type(col_start) == type(1):
            col_start = self.num_to_col(col_start)
        if len(col_start) > 2:
            col_start = self.cols[col_start] if use_player_sheet else self.cols_dir[col_start]

        table_range = f"{col_start}{row_start}:{self.col_add(col_start, num_cols-1)}{row_start+num_rows-1}"
        
        if num_cols == 1:
            texts = [[x] for x in texts]
        if num_rows == 1:
            texts = [texts]
        
        texts = [self.cards_to_texts(x) for x in texts]

        self.ws.update(table_range, texts) if use_player_sheet else self.ws_dir.update(table_range, texts)


    def update_cell(self, col, row, text, use_player_sheet=True):
        if type(col) == type(1):
            col = self.num_to_col(col)
        if len(col) > 2:
            col = self.cols[col] if use_player_sheet else self.cols_dir[col]

        text = str(text)

        self.ws.update_acell(f"{col}{row}", text) if use_player_sheet else self.ws_dir.update_acell(f"{col}{row}", text)

    def get_acell(self, col, row, use_player_sheet = True):
        if type(col) == type(1): # 열 값으로 숫자로 받아도 되게 처리 eg. 28 -> AA
            col = self.num_to_col(col)
        if len(col) > 2:
            col = self.cols[col] if use_player_sheet else self.cols_dir[col]

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

    def col_to_num(self, col):
        res = 0
        for c in col:
            res *=26
            res += ord(c) - ord('A') + 1
        return res
    
    def col_add(self, col, n): #코드 간결화를 위한 보조 함수 - 행 알파벳 연산
        return self.num_to_col(self.col_to_num(col)+n)

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
    def cards_to_texts(self, cards=[]):
        return [str(x) for x in cards]

# 위는 놔두고 아래부터 수정, json 파일 수정 금지

# worksheet에 업로드 하는 코드
# worksheet.update_acell('B2', 'novels')

# worksheet 상의 모든 텍스트 다 가져오는 코드
# value_all = worksheet.get_all_values()

# worksheet 상의 특정 셀의 텍스트를 가져오는 코드
# cell1 = worksheet.get('B1')


class SP_DB(SP):
    def __init__(self, group = 0, team = 0):
        
        '''
        self.ws = self.doc.worksheet(f'player{num}')
        self.ws_dir = self.doc.worksheet(f'director{num}')
        self.cols = self.update_cols_dict(True)
        self.cols_dir = self.update_cols_dict(False)
        self.team = team
        '''

        self.host = 'jeonsaegi23.c5hjdgv5b9uj.ap-northeast-2.rds.amazonaws.com'
        self.port = 3306
        self.user = 'jeonsaegi23'
        self.password = 'jeonsaegi23' # host, password는 보안 문제가 있어서, 나중에 파일을 따로 빼자
        self.database = 'player_info'
        self.conn = pymysql.connect(host = self.host, port = self.port, user = self.user, password = self.password, database = self.database)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.conn.autocommit(True)
        
        self.group = group
        self.team = team
        
        self.cur.execute("DESC player")
        fetch = self.cur.fetchall()
        self.cols_db = [x['Field'] for x in fetch ]
        self.cols = dict(zip( self.cols_db, map(self.num_to_col, range(len(fetch))) ))
        
        self.cur.execute("DESC director")
        fetch = self.cur.fetchall()
        self.cols_db_dir = [ x['Field'] for x in fetch ]
        self.cols_dir = dict(zip( self.cols_db_dir, map(self.num_to_col, range(len(fetch))) ))
        

        print(self.cols)
        print(self.cols_dir)
        
    def get_acell(self, col, row, use_player_sheet=True):
        table = 'player' if use_player_sheet else "director"
        mykey = self.group * 100 + row - 1
        col = self.col_to_num_db(col, use_player_sheet)
        fetch = self.execute(f"SELECT {col} FROM {table} WHERE mykey={mykey};")
        return fetch[0][col]

    def update_cell(self, col, row, text, use_player_sheet=True):
        mykey = self.group * 100 + row - 1 
        table = 'player' if use_player_sheet else "director"
        col = self.col_to_num_db(col, use_player_sheet)
        print(col)
        q = f"UPDATE {table} SET {col}=%s WHERE mykey={mykey};"
        print("UPDATE_CELL")
        print(q)
        self.execute(q , [text])

    def update_cell_range(self, col_start, num_cols, row_start, num_rows, texts, use_player_sheet=True):
        if num_cols == 1:
            texts = [ [x] for x in texts ]
        if num_rows == 1:
            texts = [  texts  ]
        
        print("UPDATE_CELL_RANGE")
        mykey = self.group * 100 + row_start - 1
        table = 'player' if use_player_sheet else "director"
        print(col_start, use_player_sheet)
        col_start = self.col_to_num_db(col_start, use_player_sheet)
        print(col_start)
        insert = self.col_to_num_db(col_start,use_player_sheet, num_cols)
        print(insert)
        middle_text = [" {} = %s ".format(x) for x in insert] 
        print("UPDATE_CELL_RANGE")
        print(middle_text)
        for mk in range(num_rows):
            q = f"UPDATE {table} SET " + " , ".join(middle_text) + f"WHERE mykey={mk+mykey}"
            print(q)
            print(texts[mk])
            self.execute(q, texts[mk] )


    def get_cell_range(self, col_start, num_cols, row_start, num_rows, use_player_sheet=True):
        table = table = 'player' if use_player_sheet else "director"
        mykey = self.group * 100 + row_start - 1
        ins = self.col_to_num_db(col_start, use_player_sheet, num_cols)
        q = "SELECT "
        middle_text = " , ".join([f"{x}" for x in ins ]) 
        q += middle_text + f" FROM {table} "
        q += f" WHERE mykey BETWEEN {mykey-1} AND {mykey+num_rows}" if num_rows > 1 else f" WHERE mykey = {mykey}" 
        print("GET_CELL_RANGE_QUERY | ",q, ins)
        fetch = self.execute(q)
        print(fetch)
        ret = [ [ row[r] for r in row ] for row in fetch  ]
        print(ret)
        if num_cols == 1:
            ret = [ x[0] for x in ret ] 
        if num_rows == 1:
            ret = ret[0]
        return ret

    def col_to_num_db(self, col, use_player_sheet=True, num_cols = 1):
        print('col_to_num_db' + "-"*19)
        print("COL : ", col)
        if num_cols == 1:
            print("NOT RANGE")
            if type(col) == type(1):
                print("IF INT")
                ret = self.cols_db[col] if use_player_sheet else self.cols_db_dir[col]
                print(ret)
                return ret
            print("INPUT WAS STRING")
            if len(col) > 2: 
                print("INPUT WAS LONG")
                ret = col + ("" if use_player_sheet or col[-1] == '_' else "_" )
                print(ret)
                return ret
            if not use_player_sheet or col[-1] == '_' : col = col + "_"

            #col = self.cols[col] if use_player_sheet else self.cols_dir[col]
            print(col)
            col = self.col_to_num(col)
            print(col)
            ret = self.cols_db[col] if use_player_sheet else self.cols_db_dir[col]
            print(ret)
            return ret
        else:
            print("CALL WAS RANGE")
            print(col)
            if type(col) == type("a"):
                print("INPUT WAS STRING")
                if len(col) > 2 :
                    print("INPUT WAS LONG")
                    col +=  "" if use_player_sheet or col[-1] == '_'else "_"
                    col = self.cols[col] if use_player_sheet else self.cols_dir[col]
                col = self.col_to_num(col)
                print(col)
            print(col)
            ret =  self.cols_db[col:col+num_cols] if use_player_sheet else self.cols_db_dir[col:col+num_cols] 
            print(ret)
            return ret
    def execute(self, query, insert=""):
        if insert=="":
            self.cur.execute(query)
        else:
            self.cur.execute(query,insert) #insert 시엔 인수를 받음
        return self.cur.fetchall()




if __name__ == '__main__': #테스트
    sp = SP_DB(1,1)
    #exit(1)

    #sp = SP()
    a = ['11', '21', '31', '41']
    cards = []
    for i in a:
        cards.append(Card(i, fromcell=True))
    sp.upload_hand(1, cards)
    sp.upload_playing(1, [Card('11', fromcell=True),'22'], 1)
    print(sp.get_hand(1))
    print(sp.get_playing(1,1))
    print(sp.get_round(1))
    print(sp.get_phase(1))
    print(sp.has_conducted(1,1,2))
    print(sp.has_conducted(1,2,2))
    print(sp.get_cell_range(1,3,2,4))
    print(sp.get_cell_range("B",3,2,4))    
    sp.update_cell_range(4,4,2,2, [a,a])