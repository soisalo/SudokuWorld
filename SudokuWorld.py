"""
SudokuWorld! GUI-project
Comp.cs.100
Eemil Soisalo
150353416
eemil.soisalo@tuni.fi

Tämä projekti on sudokun ratkaisija "SudokuWorld!", joka pystyy 
luomaan uniikin ratkaistavan sudokun käyttäjälle kolmella eri vaikeustasolla.

Käyttäjä voi ratkaista sudokun itse tai antaa ohjelman ratkaista sen hänen puolesta.
Käyttäjä voi myös antaa omia sudokujaan ja ohjelma pystyy ratkaisemaan ne.
Peli sisältää myös ohjeet ohjelman toimintaan ja sudokun ratkaisemiseen.

Ohjelma koostuu kahdesta luokasta: SudokuSolver ja SudokuUI.
SudokuSolver-luokka ratkaisee sudokun ja luo uuden sudokun.
SudokuUI-luokka taas luo Sudoku-ratkaisijan käyttöliittymän.

Onnea peliin!
"""

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random



class SudokuSolver:
    """
    Tämä luokka käsittelee sudokun ratkaisemista ja sudokun luomista. (Äly)
    """
    def ratkaise_sudoku_algo(self, board):
            """
            Tämä metodi ratkaisee sudokun rekursiivisesti.

            Param: board: 9x9 matriisi, joka sisältää sudokun
            """

            #Etsitään tyhjät ruudut käyttäen find_empty metodia
            empty = self.find_empty(board)

            #Jos tyhjiä ruutuja ei ole, sudoku on ratkaistu.
            if not empty:
                return True
            else:
                row, col = empty

            #Käydään läpi numerot 1-10 ja tarkistetaan onko numero oikea ratkaisu
            #käyttäen is_valid metodia.
            for i in range(1, 10):
                
                if self.is_valid(board, i, (row, col)):
                    board[row][col] = i

                    #Tarkistetaan onko ratkaisu oikea
                    if self.ratkaise_sudoku_algo(board):
                        return True
                    
                    #Jos ratkaisua ei löydy, laitetaan ruudun arvoksi 0.
                    board[row][col] = 0

            return False

    def find_empty(self, board):
            """
            Tämä metodi etsii ja tarkistaa onko ruutu
            tyhjä matriisissa, jos on, se palauttaa sen koordinaatit.

            Param: board: 9x9 matriisi, joka sisältää sudokun
            """
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        return (i, j)
                    
            return None
            
    def is_valid(self, board, num=None, pos=None):
        """
        Tämä metodi tarkistaa onko annettu numero oikea ratkaisu
        annettulle koordinaatille.
        
        Param: board: 9x9 matriisi, joka sisältää sudokun
        Param: num: int, numero joka tarkistetaan
        Param: pos: tuple, koordinaatti johon numero lisätään
        """

        #Määritetään uniikki funktio, 
        #joka tarkistaa onko annetussa listassa
        #kaikki arvot uniikkeja.      
        def uniikki(values):
            ei_nollia = [v for v in values if v!=0]
            return len(ei_nollia) == len(set(ei_nollia))

        #Tarkistetaan onko numero ja koordinaatti annettu
        if num is not None and pos is not None:
            row, col = pos

            #Käydään läpi rivi ja sarake ja tarkistetaan onko numero
            #oikea ratkaisu.
            if any(board[row][i] == num for i in range(9) if i !=col):
                return False
            if any(board[i][col] == num for i in range(9) if i !=row):
                return False

            #Laskee 3x3 ruudun koordinaatit sijainnille pos
            box_x, box_y  = col //3, row //3
            for i in range(box_y*3, box_y*3+3):
                for j in range(box_x*3, box_x*3+3):
                    if board[i][j] == num and (i,j) != pos:
                        return False

            return True

        #Tarkistetaan onko matriisi oikein
        for i in range(9):

            if not uniikki(board[i]) or not uniikki([board[j][i] for j in range(9)]):
                return False

        #Käydään läpi 3x3 ruudukko ja tarkistetaan
        #sopiiko numero siihen
        for box_x in range(3):
            for box_y in range(3):
                if not uniikki([board[i][j] for i in range(box_y*3, box_y*3+3) 
                                            for j in  range(box_x*3, box_x*3+ 3)]):
                    
                    return False
                

        #Tarkistetaan vielä että kaikki ruudut on täytetty
        for row in board:
            if any(cell == 0 for cell in row):
                return False
            
            
        return True

    def vaikeus(self):
            """
            Tämä metodi kysyy käyttäjältä sudokun vaikeusastetta ja 
            palauttaa sen mukaan kuinka monta numeroa sudokusta poistetaan.
            """
            difficulty = simpledialog.askstring(
                "Valitse vaikeusaste", 
                "__________________Vaikeusaste:___________________\n1. Helppo\n2. Keskiverto\n3. Vaikea\n"
            )   

            if difficulty is None:
                return 0
            elif difficulty == "1":
                return 50
            elif difficulty == "2":
                return 60
            elif difficulty == "3":
                return 70
            else:
                return 0
            
    def luo_valmis_sudoku(self):
        """
        Luo valmiiksi täytetyn ja ratkaistavan uniikin sudoku-matriisin.
        Tätä käytetään pohjana ratkaistavan sudokun luomisessa.
        """
        
        #Luodaan tyhjä 9x9 matriisi
        board = [[0 for _ in range(9)] for _ in range(9)]

        # Täytetään matriisi 10 satunnaisella numerolla
        numero = 0
        while numero < 10:
            i = random.randint(0,8)
            j = random.randint(0,8)
            num = random.randint(1,9)

            # Tarkistetaan onko numero oikea ratkaisu
            if board[i][j] ==0 and self.is_valid(board, num, (i,j)):
                board[i][j] =num
                numero +=1

        # Tarkistetaan, voidaanko sudoku ratkaista
        if self.ratkaise_sudoku_algo(board):
            # Jos voidaan ratkaista, palautetaan matriisi
            return board
        else:
            # Muuten aloitetaan alusta
            return self.luo_valmis_sudoku()
                
    def luo_ratkaistava_sudoku(self, vaikeus):
        """
        Tämä metodi luo vaikeusasteeltaan pienen, keskisuuren 
        tai vaikean sudokun, jonka käyttäjä voi ratkaista.

        Param: vaikeus: int, sudokun vaikeusaste
        """

        #Luodaan valmis sudoku ja haetaan vaikeustaso
        board = self.luo_valmis_sudoku()

        #Poistetaan vaikeustason verran
        #numeroita sudokusta ja korvataan ne tyhjillä
        soluja_poistetaan = set()
        while len(soluja_poistetaan) < vaikeus:
            i, j = random.randint(0, 8), random.randint(0, 8)

            if (i, j) not in soluja_poistetaan:
                soluja_poistetaan.add((i, j))
                board[i][j] = 0

        return board
    
    

class SudokuUI:
    """
    Tämä luokka luo Sudoku-ratkaisijan käyttöliittymän.
    """

    def __init__(self):
        """
        Luo Sudoku-ratkaisijan käyttöliittymän ja alustaa arvot.
        """

        #Pääikkuna
        self.__mainwindow = Tk()
        #9x9 ruudukko
        self.__entries = []

        #Nappulat
        self.__ilmoitus_label = None

        #Tällä luodaan SudokuSolver-olio
        self.solver = SudokuSolver()

        #Luo käyttöliittymän
        self.create_ui()

    def create_ui(self):

        #Asetetaan ikkunan otsikko
        self.__mainwindow.title("SudokuWorld!")

        #Luodaan 9x9 ruudukko käyttöliittymään käyttäen Canvas-elementtiä
        canvas = Canvas(self.__mainwindow, width=450, height=450)
        canvas.grid(row=0, column=0, columnspan=9, rowspan=9)

        #Piirretään viivat 50 pikselin välein,
        #jotta 3x3 ruudukko tulee esiin paremmin
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            canvas.create_line(50 * i, 0, 50 * i, 450, width=line_width)
            canvas.create_line(0, 50 * i, 450, 50 * i, width=line_width)

        #Rakennetaan 9x9 ruudukko for-loopilla
        for i in range(9):
            row = []
            for j in range(9):
                frame = Frame(self.__mainwindow)
                frame.grid(row=i, column=j)
                entry = Entry(self.__mainwindow, width=3, font=("Helvetica", 15))
                entry.grid(row=i, column=j)
                row.append(entry)

            #Lisätään rivit listaan
            self.__entries.append(row)

        #Lisätään nappulat käyttöliittymään
        #sekä määritetään mitä ne tekevät
        self.__solve_button = Button(self.__mainwindow, text="Ratkaise", command=self.solve_sudoku)
        self.__solve_button.grid(row=9, column=0, columnspan=9, pady=5)

        self.__clear_button = Button(self.__mainwindow, text="Tyhjennä", command=self.clear)
        self.__clear_button.grid(row=10, column=0, columnspan=9, pady=5)

        self.__ohjeet_button = Button(self.__mainwindow, text="Ohjeet", command=self.ohjeet)
        self.__ohjeet_button.grid(row=11, column=4, columnspan=9, pady=5)

        self.__luo_sudoku = Button(self.__mainwindow, text="Luo Sudoku", command=self.luo_sudoku)
        self.__luo_sudoku.grid(row=9, column=4, columnspan=9, pady=5)

        self._tarkista_sudoku = Button(self.__mainwindow, text="Tarkista Sudoku", command=self.tarkista_sudoku)
        self._tarkista_sudoku.grid(row=10, column=4, columnspan=9, pady=5)

        self.__quit_button = Button(self.__mainwindow, text="Lopeta", command=self.__mainwindow.quit)
        self.__quit_button.grid(row=11, column=0, columnspan=9, pady=5)
        
        #Lisätään "ilmoitustaulu" käyttöliittymään
        self.__ilmoitus_label = Label(self.__mainwindow, text="", font=("Helvetica", 15))
        self.__ilmoitus_label.grid(row=12, column=0, columnspan=9, pady=5)

    def start(self):
        """
        Käynnistää ruudukon
        """
        self.__mainwindow.mainloop()

    def clear(self):
        """
        Tämä metodi tyhjentää ruudukon.
        """
        for i in range(9):
            for j in range(9):
                self.__entries[i][j].delete(0, END)

        self.__ilmoitus_label.config(text="")
    
    def luo_sudoku(self):
        """
        Tämä metodi luo vaikeusasteeltaan pienen, keskisuuren 
        tai vaikean sudokun, jonka käyttäjä voi ratkaista.
        """
        vaikeus = self.solver.vaikeus()
        if vaikeus == 0 or vaikeus is None:
            self.clear()
        else:
            board = self.solver.luo_ratkaistava_sudoku(vaikeus)
            self.display_board(board)
      
    def solve_sudoku(self):
        """
        Tämä metodi ratkaisee sudokun käyttäjän syötteiden perusteella.
        """
        if self.tarkista_merkki(self.__entries):
                
                #Haetaan matriisi käyttäjän syötteiden perusteella
                board = self.hae_board_matrix()

                #Tarkistetaan onko sudoku ratkaistavissa
                if self.solver.ratkaise_sudoku_algo(board):
                    self.display_board(board)
                    self.show_message("Sudoku ratkaistu!")
                else:
                    self.show_message("Sudokua ei voi ratkaista!")
              
    def hae_board_matrix(self):
        """
        Tämä metodi luo 9x9 matriisin käyttäjän syötteiden perusteella.
        """

        #Luodaan tyhjä 9x9 matriisi
        board = []

        for i in range(9):
            row = []
            for j in range(9):

                #Haetaan käyttäjän syöte tietyssä koordinaatissa
                entry = self.__entries[i][j].get()

                #Tarkistetaan onko syöte tyhjä, jos on, 
                #tulkitaan että se on 0
                row.append(int(entry) if entry else 0)
                
            #Lisätään rivit matriisiin
            board.append(row)

        return board

    def display_board(self, board):
        """
        Tämä metodi näyttää sudokun
        matriisin perusteella.

        Param: board: 9x9 matriisi
        """
        for i in range(9):
            for j in range(9):

                #Poistetaan vanha syöte "" ja lisätään oikea syöte.
                self.__entries[i][j].delete(0, END)

                if board[i][j] != 0:
                    self.__entries[i][j].insert(0, str(board[i][j])) 

    def show_message(self, message):
        """
        Tämä metodi näyttää viestin käyttäjälle.

        Param: message: str, viesti
        """
        self.__ilmoitus_label.config(text=message)

    def ohjeet(self):
        """
        Tämä metodi näyttää käyttäjälle ohjeet ohjelman toimintaan
        ja sudokun ratkaisemiseen popup-ikkunassa.
        """
        ohjeet = """
        Tervetuloa käyttämään Sudoku Worldiä!

        1. Syötä ruudukkoon numeroita 1-9.
        2. Tyhjät ruudut tulkitaan nolliksi.
        3. Paina 'Luo sudoku' jos haluat luoda ratkaistavan 
           sudokun.
        4. Paina 'Tarkista sudoku' jos haluat tarkistaa onko 
           syöttämäsi sudoku oikein.
        5. Paina 'Ratkaise' nappulaa ratkaistaksesi sudokun.
        6. Paina 'Tyhjennä' nappulaa tyhjentääksesi ruudukon.
        7. Paina 'Lopea' lopettaaksesi ohjelman.


        Sudokun säännöt:

        1. Jokaisessa rivissä on oltava numerot 1-9, ilman toistoa.
        2. Jokaisessa sarakkeessa on oltava numerot 1-9,
           ilman toistoa.
        3. Jokaisessa 3x3 ruudukossa on oltava numerot 1-9, 
           ilman toistoa.
        """

        messagebox.showinfo("Ohjeet:", ohjeet)
    
    def tarkista_sudoku(self):
        """
        Tämä metodi tarkistaa onko käyttäjän syöttämä sudoku oikein.
        """
        
        if self.tarkista_merkki(self.__entries):

            board = self.hae_board_matrix()
            
            if self.solver.is_valid(board):

                self.display_board(board)

                self.show_message("Sudoku on oikein!")
            else:
                self.show_message("Täytä sudoku kokonaan!")

    def tarkista_merkki(self, entries):
        """
        Tarkistaa onko merkki positiivinen numero väliltä 1-9.

        Param: entries: 9x9 matriisi, joka sisältää käyttäjän syötteet
        """
        
        #Käydään läpi 9x9 matriisi ja tarkistetaan onko se
        #positiivinen numero välillä 1-9.
        for i in range(9):
            for j in range(9):

                entry = entries[i][j].get()
                
                if entry and (not entry.isdigit() or not (1 <= int(entry) <= 9)):
                    messagebox.showinfo("Virhe:", "Syötä numero 1-9!")

                    return False
        return True
    
def main():
    """
    Käynnistää SudokuWorld! käyttöliittymän.
    """
    sudoku_ui = SudokuUI()
    sudoku_ui.start()

if __name__ == "__main__":
    main()
