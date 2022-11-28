from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image 
import json
import urllib.request
import urllib.response
import requests
from urllib.request import urlopen
import base64
from io import BytesIO


root = Tk()
root.geometry("1920x1080")
playerImg = []
playerLabel = []
dealerImg = []
dealerLabel = []
for i in range(7):
    response = requests.get("https://deckofcardsapi.com/static/img/3D.png")
    img = ImageTk.PhotoImage((Image.open(BytesIO(response.content)).resize((150, 200), Image.ANTIALIAS)))
    playerImg.append(img)
    playerLabel.append(Label(root, bg='black', image=playerImg[i], width=150, height=200))
for i in range(7):
    response = requests.get("https://deckofcardsapi.com/static/img/3D.png")
    img = ImageTk.PhotoImage((Image.open(BytesIO(response.content)).resize((150, 200), Image.ANTIALIAS)))
    dealerImg.append(img)
    dealerLabel.append(Label(root, bg='black', image=dealerImg[i], width=150, height=200))

class Window(Frame):

    playercardsTot = []
    playeramountTot = 0

    dealerCardsTot = []
    dealeramountTot = 0

    deckId = 'nothing'

    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()
        self.main()
    

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("BLACK JACK")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=2)

        # creating a button instance
        hitButton = Button(self, text="   HIT   ", command=self.hit)
        passButton = Button(self, text="STAND", command=self.stand)

        # placing the button on my window
        hitButton.place(x=10, y=10)
        passButton.place(x=10, y=50)
    
    def main(self):
        print("MAIN METHOD")
        req = urllib.request.Request('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6', headers={'User-Agent' : "Magic Browser"})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())

        self.deckId = str(data.get('deck_id'))

        temp = urllib.request.Request('https://deckofcardsapi.com/api/deck/' + self.deckId + '/draw/?count=2', headers={'User-Agent' : "Magic Browser"})
        playerjson = urllib.request.urlopen(temp)
        playercards = json.loads(playerjson.read())
        self.playercardsTot.append(playercards.get('cards')[0])
        self.playercardsTot.append(playercards.get('cards')[1])

        print(self.playercardsTot)
        self.printPlayerCards()

        tempTwo = urllib.request.Request('https://deckofcardsapi.com/api/deck/' + self.deckId + '/draw/?count=2', headers={'User-Agent' : "Magic Browser"})
        dealerjson = urllib.request.urlopen(tempTwo)
        dealercards = json.loads(dealerjson.read())

        self.dealerCardsTot.append(dealercards.get('cards')[0])
        self.dealerCardsTot.append(dealercards.get('cards')[1])

        self.checkIfBust(self.dealerCardsTot, "DEALER")
        self.checkIfBust(self.playercardsTot, "PLAYER")

        print("END OF MAIN METHOD")
    
    def printPlayerCards(self):
        for i in range(len(self.playercardsTot)):
            response = requests.get(self.playercardsTot[i]['image'])
            img = ImageTk.PhotoImage((Image.open(BytesIO(response.content)).resize((150, 200), Image.ANTIALIAS)))
            playerImg[i] = img
            playerLabel[i] = Label(self, bg='black', image=playerImg[i], width=150, height=200)
            playerLabel[i].place(x=100+i*100, y=300)
    
    def printDealerCards(self):
        for i in range(len(self.dealerCardsTot)):
            response = requests.get(self.dealerCardsTot[i]['image'])
            img = ImageTk.PhotoImage((Image.open(BytesIO(response.content)).resize((150, 200), Image.ANTIALIAS)))
            dealerImg[i] = img
            dealerLabel[i] = Label(self, bg='black', image=dealerImg[i], width=150, height=200)
            dealerLabel[i].place(x=100+i*100, y=600)
    
    def checkIfBust(self, dictionary, pers):
        tot = 0
        ace = 0
        for x in dictionary:
            temp = str(x.get('value'))

            if temp == '2':
                tot = tot+2
            elif temp == '3':
                tot = tot+3
            elif temp == '4':
                tot = tot+4
            elif temp == '5':
                tot = tot+5
            elif temp == '6':
                tot = tot+6
            elif temp == '7':
                tot = tot+7
            elif temp == '8':
                tot = tot+8
            elif temp == '9':
                tot = tot+9
            elif temp == '10':
                tot = tot+10
            elif temp == 'JACK' or temp == 'QUEEN' or temp == 'KING':
                tot = tot+10
            elif temp == 'ACE':
                ace = ace+1
        if ace>0:
            for x in range(0, ace):
                if tot+11 < 21:
                    tot = tot + 11
                else:
                    tot = tot + 1

        if tot > 21:
            if pers == "PLAYER":
                messagebox.showinfo("BLACKJACK", "BUST-DEALER WINS")
            elif pers == "DEALER":
                messagebox.showinfo("BLACKJACK", "BUST-PLAYER WINS")

    def checkTot(self, dictionary):
        tot = 0
        ace = 0
        for x in dictionary:
            temp = str(x.get('value'))

            if temp == '2':
                tot = tot+2
            elif temp == '3':
                tot = tot+3
            elif temp == '4':
                tot = tot+4
            elif temp == '5':
                tot = tot+5
            elif temp == '6':
                tot = tot+6
            elif temp == '7':
                tot = tot+7
            elif temp == '8':
                tot = tot+8
            elif temp == '9':
                tot = tot+9
            elif temp == '10':
                tot = tot+10
            elif temp == 'JACK' or temp == 'QUEEN' or temp == 'KING':
                tot = tot+10
            elif temp == 'ACE':
                ace = ace+1
        
        if ace>0:
            for x in range(0, ace):
                if tot+11>21:
                    tot = tot+1
                else:
                    tot = tot+11
        
        return tot

        
    def hit(self):
        print('HIT')
        temp = urllib.request.Request('https://deckofcardsapi.com/api/deck/' + self.deckId + '/draw/?count=1', headers={'User-Agent' : "Magic Browser"})
        playerjson = urllib.request.urlopen(temp)
        playercards = json.loads(playerjson.read())

        self.playercardsTot.append(playercards.get('cards')[0])
        print("PLAYER CARDS")
        print(self.playercardsTot)
        self.printPlayerCards()
        self.checkIfBust(self.playercardsTot, "PLAYER")

    def stand(self):
        while True:
            tempTwo = urllib.request.Request('https://deckofcardsapi.com/api/deck/' + self.deckId + '/draw/?count=1', headers={'User-Agent' : "Magic Browser"})
            dealerjson = urllib.request.urlopen(tempTwo)
            dealercards = json.loads(dealerjson.read())
            
            self.dealerCardsTot.append(dealercards.get('cards')[0])
            print("DEALER CARDS")
            print(self.dealerCardsTot)
            self.printDealerCards()
            deal = self.checkTot(self.dealerCardsTot)
            self.dealeramountTot=deal
            if deal>17:
                break
        player = self.checkTot(self.playercardsTot)
        self.playeramountTot = player
        self.checkhigheramount()
    
    def checkhigheramount(self):
        if self.playeramountTot > 21:
            messagebox.showinfo("BLACKJACK", "BUST-DEALER WINS")
        elif self.dealeramountTot > 21:
            messagebox.showinfo("BLACKJACK", "BUST-PLAYER WINS")
        elif self.dealeramountTot > self.playeramountTot:
            messagebox.showinfo("BLACKJACK", "DEALER WINS")
        elif self.playeramountTot > self.dealeramountTot:
            messagebox.showinfo("BLACKJACK", "PLAYER WINS")
        elif self.playeramountTot == self.dealeramountTot:
            messagebox.showinfo("BLACKJACK", "PLAYER AND DEALER TIE")

app = Window(root)

root.mainloop()  