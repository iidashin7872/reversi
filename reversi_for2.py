import tkinter
import tkinter.messagebox
from enum import Enum

FS = ("Times New Roman", 20)
FL = ("Times New Roman", 80)

BOARD_SIZE = 8 # 盤面の大きさ
CANVAS_WIDTH = 560 # 盤面の横幅(px)
CANVAS_HEIGHT = 560 # 盤面の縦幅(px)
SQUARE_WIDTH = CANVAS_WIDTH // BOARD_SIZE # マスの横幅(px)
SQUARE_HEIGHT = CANVAS_HEIGHT // BOARD_SIZE # マスの縦幅(px)

BLACK = 1 # 黒い石
WHITE = 2 # 白い石
COLOR_LIST = [BLACK, WHITE] # プレイヤーの駒の色を管理する配列

class Phase(Enum):
    STANDBY = 0
    MAIN = 1
    END = 2
    RESULT = 3

mx = 0 # クリックしたマスのX座標
my = 0 # クリックしたマスのY座標
mc = 0 # クリックしたかどうかを判別する変数
proc = Phase.STANDBY # 進行を管理する変数
turn = 0 # 手番を管理する変数
who = ["BLACK", "WHITE"] # プレイヤーの手番を管理する配列
msg = "" # メッセージ

board = [] # 盤面の状況を管理する2次元配列
back = [] # 現在の盤面の状況を保存する2次元配列
back_2 = [] # 2ターン前の盤面の状況を保存する2次元配列
placeable_square_X = [] # 配置可能なマスのX座標
placeable_square_Y = [] # 配置可能なマスのX座標

for y in range(BOARD_SIZE): # board, back, back_2を初期化
    board.append([0] * BOARD_SIZE)
    back.append([0] * BOARD_SIZE)
    back_2.append([0] * BOARD_SIZE)

def click(e): # クリックされた時に呼び出し
    global mx, my, mc
    mx = int(e.x / SQUARE_WIDTH) # クリックしたマスのX座標を判定
    my = int(e.y / SQUARE_HEIGHT) # クリックしたマスのY座標を判定
    mc = 1 # クリック判定

def display_board(): # 盤面を表示する関数
    cvs.delete("all")
    cvs.create_text(SQUARE_WIDTH*4, CANVAS_HEIGHT+30, text=msg, fill="silver", font=FS) # 下部にメッセージを表示
    
    for i in range(BOARD_SIZE):
        X = i * SQUARE_WIDTH
        Y = i * SQUARE_HEIGHT
        # 線を引く
        cvs.create_line(0, Y+SQUARE_HEIGHT, CANVAS_WIDTH, Y+SQUARE_HEIGHT, fill="black", width=2)
        cvs.create_line(X+SQUARE_WIDTH, 0, X+SQUARE_WIDTH, CANVAS_HEIGHT, fill="black", width=2)
    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            X = x * SQUARE_WIDTH
            Y = y * SQUARE_HEIGHT
            
            # マスに円を描写
            if board[y][x] == BLACK:
                cvs.create_oval(X+10, Y+10, X+SQUARE_WIDTH-10, Y+SQUARE_HEIGHT-10, fill="black", width=0)
            elif board[y][x] == WHITE:
                cvs.create_oval(X+10, Y+10, X+SQUARE_WIDTH-10, Y+SQUARE_HEIGHT-10, fill="white", width=0)
            
            # ヒントを描写
            if placeable_square_num(x, y, COLOR_LIST[turn]) > 0 and mc == 0:
                if proc == Phase.MAIN:
                    cvs.create_oval(X+30, Y+30, X+SQUARE_WIDTH-30, Y+SQUARE_HEIGHT-30, fill="gold", width=0)
    cvs.update()

def init_board(): # 盤面を初期化する関数
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            board[y][x] = 0
        board[3][4] = BLACK
        board[4][3] = BLACK
        board[3][3] = WHITE
        board[4][4] = WHITE

def place_disc(x, y, color):
    board[y][x] = color
    
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            k = 0
            sx = x
            sy = y
            while True:
                sx += dx
                sy += dy
                if sx < 0 or BOARD_SIZE <= sx or sy < 0 or BOARD_SIZE <= sy:
                    break
                if board[sy][sx] == 0:
                    break
                if board[sy][sx] == 3-color:
                    k += 1
                if board[sy][sx] == color:
                    for i in range(k):
                        sx -= dx
                        sy -= dy
                        board[sy][sx] = color
                    break

def placeable_square_num(x, y, color):
    if board[y][x] > 0:
        return -1
    
    total = 0
    
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            k = 0
            sx = x
            sy = y
            while True:
                sx += dx
                sy += dy
                if sx < 0 or BOARD_SIZE <= sx or sy < 0 or BOARD_SIZE <= sy:
                    break
                if board[sy][sx] == 0:
                    break
                if board[sy][sx] == 3-color:
                    k += 1
                if board[sy][sx] == color:
                    total += k
                    break
    
    return total

def placeable_square_existence(color):
    placeable_square_X.clear()
    placeable_square_Y.clear()
    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if placeable_square_num(x, y, color) > 0:
                placeable_square_X.append(x)
                placeable_square_Y.append(y)
    
    if len(placeable_square_X) >= 1:
        return True
    return False

def count_discs():
    black_disc_num = 0
    white_disc_num = 0
    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == BLACK:
                black_disc_num += 1
            elif board[y][x] == WHITE:
                white_disc_num += 1
    
    return black_disc_num, white_disc_num

def main():
    global proc, turn, mc, msg
    display_board()

    if proc == Phase.STANDBY:
        cvs.create_text(SQUARE_WIDTH*4, SQUARE_HEIGHT*3, text="Reversi", fill="gold", font=FL)
        cvs.create_text(SQUARE_WIDTH*4, SQUARE_HEIGHT*5+35, text="Start", fill="silver", font=FS)
        if mc == 1:
            mc = 0
            if (mx == 3 or mx == 4) and my == 5:
                init_board()
                proc = Phase.MAIN
    
    elif proc == Phase.MAIN:
        if turn == 0:
            msg = "BLACK's Turn"
        else:
            msg = "WHITE's Turn"
        if mc == 1:
            if placeable_square_num(mx, my, COLOR_LIST[turn]) > 0:
                place_disc(mx, my, COLOR_LIST[turn])
                proc = Phase.END
            mc = 0
        
    elif proc == Phase.END:
        msg = ""
        turn = 1 - turn
        if placeable_square_existence(BLACK) == False and placeable_square_existence(WHITE) == False:
            space = 0
            for y in range(BOARD_SIZE):
                for x in range(BOARD_SIZE):
                    if board[y][x] == 0:
                        space += 1
            if space > 0:
                tkinter.messagebox.showinfo("", "どちらも打つ手がないため，終了します")
            proc = Phase.RESULT
        elif placeable_square_existence(COLOR_LIST[turn]) == False:
            tkinter.messagebox.showinfo("", who[turn]+"は打つ手がありません")
        else:
            proc = Phase.MAIN
    elif proc == Phase.RESULT:
        black_disc_num, white_disc_num = count_discs()
        
        tkinter.messagebox.showinfo("終了", "BLACK={} / WHITE={}".format(black_disc_num, white_disc_num))
        
        if black_disc_num > white_disc_num:
            tkinter.messagebox.showinfo("", "BLACK WIN!")
        elif white_disc_num > black_disc_num:
            tkinter.messagebox.showinfo("", "WHITE WIN!")
        else:
            tkinter.messagebox.showinfo("", "DRAW")
        
        proc = Phase.STANDBY
    
    root.after(100, main)

root = tkinter.Tk() # ウィンドウオブジェクト
root.title("Reversi") # ウィンドウタイトル
root.resizable(False, False) # ウィンドウのサイズ変更不可
root.bind("<Button>", click) # マウスをクリックしたときにクリック関数を呼び出し
cvs = tkinter.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT+60, bg="green") #キャンバス(640x700, green)
cvs.pack() # ウィンドウにキャンバスを設置
root.after(100, main)
root.mainloop() # ウィンドウを表示