import chess
import chess.polyglot
import random
import time
import chess.svg

from IPython.display import SVG, display_svg

board = chess.Board()
print(board)

def startGame():

    isGameOn = True
    white = True

    while isGameOn:
        
  
       
        with chess.polyglot.open_reader('../data/performance.bin') as reader:
                        
            entries = []
            
            for entry in reader.find_all(board):
                entries.append(entry.move)
            
            if entries:                          
                entry = random.randint(0, len(entries) - 1)
                coup = entries[entry]
            else:
                
                l = []
                
                for moves in board.legal_moves:
                    l.append(moves)
                
                r = random.randint(0, len(l) - 1)
                
                coup = l[r]
                print("MEILLEUR COUP")
                

            print(coup)
            
            board.push(chess.Move.from_uci(str(coup)))

        
        
        """  coup = input('Jouez un coup \n')
        
        if white == True:
            
            while isLegal(coup) == False :            
                coup = input('Jouez un coup \n')
                
            board.push(chess.Move.from_uci(coup))
            white = False
       
        else :
            
            while isLegal(coup) != True : 
                coup = input('Jouez un coup \n')
            board.push(chess.Move.from_uci(coup))"""
        white = True
         
        time.sleep(0.01)
        print("\n")    
        #print(board.fen())
        print("\n") 
        print(board)
        
        print("\n")
        
        if isEnded():
            display_svg(SVG(chess.svg.board(board=board,size=400)))
            showResult()
            break
        
           
            
        
        
def isLegal(coup) :
      
   try:
       move = chess.Move.from_uci(coup)
              
       if move in board.legal_moves:
           return True
       else:
           print("Coup Illégal !")
           return False
       
   except ValueError:
       print("Coup Illégal !")
       return False
           
   
def isEnded():
    
    
    if board.outcome(claim_draw = True) != None:
        return True
    
def showResult():
    
    if board.result() == "1-0":
        print("Victoire des blancs")
    elif board.result() == "0-1":
        print("Victoire des noirs")  
    else:
        print("Egalité")

startGame()

