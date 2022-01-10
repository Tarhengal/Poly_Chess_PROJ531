import chess

board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 4")
print(board)

def startGame():

    isGameOn = True
    white = True

    while isGameOn:
        
        coup = input('Jouez un coup \n')
        
        if white == True:
            
            while isLegal(coup) == False :            
                coup = input('Jouez un coup \n')
                
            board.push(chess.Move.from_uci(coup))
            white = False
       
        else :
            
            while isLegal(coup) != True : 
                coup = input('Jouez un coup \n')
            board.push(chess.Move.from_uci(coup))
            white = True
            
        print(board)
        print("\n")
        
        if isEnded():
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
    print(board.result())        

startGame()

