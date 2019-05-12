# With this template, 
# we are building an AI that will apply 
# combinatorial game theory tools against a greedy opponent.

# Unless you know what you are doing, 
# you should use this template with a very limited number of pieces of cheese, 
# as it is very demanding in terms of computations.

# The first thing you should do is copy this file (tp3.py) to the AIs folder of pyrat, example:
# cp -r ~/IntroToAI/session4/tp3.py ~/pyrat/AIs/

# A typical use would be:
# python pyrat.py -d 0 -md 0 -p 7 --rat AIs/tp3.py --python AIs/manh.py --nonsymmetric

# If enough computation time is allowed, 
# it is reasonable to grow the number of pieces of cheese up to around 15.
# For example:

# python pyrat.py -d 0 -md 0 -p 13 --rat AIs/tp3.py --python AIs/manh.py --synchronous --tests 100 --nodrawing --nonsymmetric

# In this example, we can obtain scores in the order of: "win_python": 0.07 "win_rat": 0.93

from heapq import heappush, heappop
from time import time
from itertools import permutations
import heapq as h 



MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

############ GLOBAL VARIABLES ############
moves = []
mouvements_exhaustif = 0
eatenCheese = []
numberOfmoves = 1
piecesOfCheesePrems = []
cheese_1 = 0
m = 0
n = 0
k = 0
j = 0
###############################

# This function returns the move that can lead the mouse from a first location to a neighbor location
def aboveOf(location):
    return((location[0],location[1]+1))

# Function that returns the location below#
def belowOf(location):
    return((location[0],location[1]-1))

# Function that returns the location at left#
def leftOf(location):
    return((location[0]-1,location[1]))

# Function that returns the location at right#
def rightOf(location):
    return((location[0]+1,location[1]))

'''def GetMove_(sourceLocation, targetLocation) : 
    difference = tuple(numpy.subtract(targetLocation, sourceLocation))
    if difference == (0, -1) :
        return MOVE_DOWN
    elif difference == (0, 1) :
        return MOVE_UP
    elif difference == (1, 0) :
        return MOVE_RIGHT
    elif difference == (-1, 0) :
        return MOVE_LEFT
    else:
        return('error')'''
def GetMove(fromLocation,toLocation):
    
      if toLocation==aboveOf(fromLocation):
          return MOVE_UP
      elif toLocation==belowOf(fromLocation):
          return MOVE_DOWN
      elif toLocation==leftOf(fromLocation):
          return MOVE_LEFT
      elif toLocation==rightOf(fromLocation):
          return MOVE_RIGHT
      else:
          return None

# This function tests if two cells are neighbors
        
def CanMove(source,target,mazeMap):
    if source in mazeMap[target]:
        return True
    else:
        return False     




# This function gives the mouse the shortest path to follow in order to reach a cell that contains a piece of cheese in a weighted maze

def djikstra(mazeMap, playerLocation) :
    priorityQueue = []   #the heapqueue that contains the nodes and distances to them from playerloc as tulpes
    visitedCells = {} #a dictionnary that contains cells and the minimum distances to them
    neighbors_queue = [] #a list that contains the same nodes as priority queue but without the values ; it helps us know the index of a tulpe containing the desired node in priorityQueue even if we don't know it's value 
    moves = {}    #a dictionnary which keys are all the cells of the maze and their values being the moves that lead to them starting from the player location (ready for use by the pyRat Program)
    
    moves[playerLocation] = []    
    for neighbor in mazeMap[playerLocation] :  
        moves[neighbor] = [GetMove(playerLocation,neighbor)]
    heappush(priorityQueue,(0, playerLocation))
    
    while priorityQueue != [] :
        minDistance, minElement = heappop(priorityQueue)
        visitedCells[minElement] = minDistance
        neighbors_distances = mazeMap[minElement].items()
        for neighbor, distance in neighbors_distances : #FOR EACH NODE WE UPDATE OUR HEAPQUEUE ( adding a new couple (node,distance) or keeping the one with smallest distance)
            if neighbor not in neighbors_queue:
                #this means the neighbor is not in the heapqueue so we add it there while updating the moves dict as well
                heappush(priorityQueue, (distance + minDistance, neighbor))
                neighbors_queue.append(neighbor)
                moves[neighbor] = moves[minElement] + [GetMove(minElement, neighbor)]
            elif neighbor not in visitedCells : # If the neighbor is in visitedCells, it means that we've already found a path from the playerLocation to it      
                k=0       
                while priorityQueue[k][1] != neighbor :
                    k+=1     
                if distance + minDistance < priorityQueue[k][0]:
                    priorityQueue[k] = (distance + minDistance, neighbor)
    return moves,visitedCells


#this function returns the metamap associated with our mazemap                

def MetaMaze(mazeMap,piecesOfCheese,playerLocation):
    metaMap={}
    movesMap={} 
    Nodes=piecesOfCheese+[playerLocation]    
    for Node in Nodes: #FOR EACH OF THE CELLS WE'RE INTERESTED IN WE USE DJIKSTRA TO CALCULATE THE MINIMAL DISTANCES THAT WILL SERVE AS WEIGHTS FOR OUR NEW MAP
        moves={}
        neighbors={}        
        moves_toall,allneighbors=djikstra(mazeMap,Node)
        #DJISKTRA LOADS THE DISTANCES TO ALL THE NODES IN THE ORIGINAL MAP BUT WE ONLY WANT THOSE IN THE LIST NODES SO WE "FILTER" THEM
        for node in Nodes : 
            
            if node!=Node :
                moves[node] = moves_toall[node]
                neighbors[node]= allneighbors[node]
        
        metaMap[Node]=neighbors
        movesMap[Node]=moves
    
    return metaMap,movesMap


# THIS FUNCTION RETURNS ALL THE PERMUTATIONS OF THE LIST Liste[0:i+1]

def Permutations(Liste): 
       p = permutations(Liste)
       return [list(i) for i in p]

#THIS FUNCTION CALCULATES THE LENGHT OF A GIVEN PATH IN A GIVEN MAP
def PathLength(Order,MetaMaze,CurrentDistance):
    L = 0
    i = 0
    while i < len(Order)-1:
        L += MetaMaze[Order[i]][Order[i+1]]
        i += 1
        if L > CurrentDistance :
            return CurrentDistance
    return L

 
#THIS FUNCTION SELECTS THE SHORTEST PATH IN A COMPLETE GRAPH BY TRYING ALL THE POSSIBLE WAYS
def exhaustif(MetaMaze,piecesOfCheese,playerLocation):
    
    #WE CREATE A LIST OF ALL THE POSSIBLE PATHS BEGINNING BY THE PLAYERLOCATION AND PASSING THROUGH ALL THE PIECES OF CHEESE 
    list_permutations = Permutations(piecesOfCheese)    
    CheeseReorders = [ playerLocation + permutation  for permutation in list_permutations]   

    #THIS LOOP COMPARES THE LENGHTS OF ALL THE PREVIOUS PATHS TO RETURN THE SHORTEST ONE    
    FinalOrder = CheeseReorders[0]
    CurrentDistance = 1000
    FinalDistance = PathLength(FinalOrder,MetaMaze,CurrentDistance)
    
    for Path in CheeseReorders[1:] : 
        CurrentDistance = PathLength(Path,MetaMaze,FinalDistance)
        
        if CurrentDistance < FinalDistance:
                FinalOrder    = Path
                FinalDistance = CurrentDistance

    return FinalOrder

#THIS FUNCTIONS GIVES A PATH WHERE THE LENGTH FROM Am -= 1 PIECE TO THE NEXT ONE IS THE SHORTEST WITHOUT ANY GUARANTEE THAT THE GLOBAL PATH IS THE SHORTEST

def Glouton(playerLocation,piecesOfCheese,mazeMap):
    L=[]
    moves=[]
    metaMap,movesMap = MetaMaze(mazeMap,piecesOfCheese,playerLocation)
    Nodes = [playerLocation] + piecesOfCheese  #Nodes is a list that will contain all the nodes to be reached
    CurrentNode = Nodes.pop(0) 
    
    while Nodes != []:   #THIS LOOP POPS THE CURRENT NODE AND FINDS THE CLOSEST NEXT ONE TO IT USING THE METAMAP AND STOPS WHEN THERE ARE NO MORE NODES TO REACH
        
        neighbors,distance = list(metaMap[CurrentNode].keys()), list(metaMap[CurrentNode].values())
        #indice=distance.index(min(distance))          
        indice = neighbors.index(Nodes[0])       
        for i in range(0,len(distance)): 
            if (distance[i] < distance[indice]) and (neighbors[i] in Nodes) : #WE MAKE SURE THAT THE NEXT NODE IS THE CLOSEST ONE THAT HAS NOT BEEN VISITED YET
                indice = i
        ClosestNeighbor = neighbors[indice] 
        Nodes.remove(ClosestNeighbor) #WE CHANGE THE NODES LIST TOO SO THAT IT ONLY KEEPS THE NODES THAT HAS NOT BEEN VISITED YET
        moves += movesMap[CurrentNode][ClosestNeighbor] #THE GLOBAL MOVES LIST GETS UPDATED IN EACH LEAP FROM NODE TO NODE
        CurrentNode = ClosestNeighbor
        L.append(CurrentNode)
    return moves, L, metaMap
        
        
def intersection(liste_1, liste_2) : 
    for i in liste_1 :
        if i in liste_2 :
            return True
    return False    


nbTurn = 0
chemin = []

###############################
# Preprocessing function
# Function that returns the location above#
def aboveOf(location):
    return((location[0],location[1]+1))

# Function that returns the location below#
def belowOf(location):
    return((location[0],location[1]-1))

# Function that returns the location at left#
def leftOf(location):
    return((location[0]-1,location[1]))

# Function that returns the location at right#
def rightOf(location):
    return((location[0]+1,location[1]))
    
CheminToCheese= []

def dijikstra(graph,sourcenode):
        file=[]#on initialise le tas-mine
        h.heappush(file,(0,sourcenode))#avec le sourcenode en plus
        distances={}#initialisation dictionnaire des distances
        for i in graph.keys(): #on initialise la distance 1 to * par une distance très grande 
                distances[i]=100000
                
        distances[sourcenode]=0 #la distance d'un noeud vers lui meme est nulle
        routage={}#on initialise la table de routage
        while file: #tant que la file est non vide
            (distance,sommet_courant)=h.heappop(file)#on note la distance de l'origine par rapport au sommet courant
            for neighbor in graph.get(sommet_courant).keys():#on parcours les voisins du sommet courant
                dist_c=distance+graph.get(sommet_courant).get(neighbor)#on calcule la distance par rapport a l'origine
                if distances.get(neighbor)>dist_c:#on ecrase la valeur dans la matrice de  distance si on trouve un chemin plus court et decide de passer par ce noeud                                    
                    distances[neighbor]=dist_c
                    h.heappush(file,(dist_c,neighbor))
                    routage[neighbor]=sommet_courant #Pour aller a neighbor il faudra passer par le sommet courant
                    
        return routage, distances
    
def Chemin(Parcours,cheese,sommet_départ):

    Chemin = [cheese]
    position = cheese
    while position != sommet_départ:
        Chemin = [Parcours[position]]+Chemin
        position = Parcours[position]
    return Chemin

     
# This function is calldjikstra(mazeMap, opponentLocation)[1][ClosestTreat]ed at the beginnig of the game
     
# Useful utility functions to obtain new location after a move
def move(location, move):
    if move == MOVE_UP:
        return (location[0], location[1] + 1)
    if move == MOVE_DOWN:
        return (location[0], location[1] - 1)
    if move == MOVE_LEFT:
        return (location[0] - 1, location[1])
    if move == MOVE_RIGHT:
        return (location[0] + 1, location[1])

# The first things we do is we program the AI of the opponent, so that we know exactly what will be its decision in a given situation
def distance(la, lb):
    ax,ay = la
    bx,by = lb
    return abs(bx - ax) + abs(by - ay)

def turn_of_opponent(opponentLocation, piecesOfCheese):    
    closest_poc = (-1,-1)
    best_distance = -1
    for poc in piecesOfCheese:
        if distance(poc, opponentLocation) < best_distance or best_distance == -1:
            best_distance = distance(poc, opponentLocation)
            closest_poc = poc
    ax, ay = opponentLocation
    bx, by = closest_poc
    if bx > ax:
        return MOVE_RIGHT
    if bx < ax:
        return MOVE_LEFT
    if by > ay:
        return MOVE_UP
    if by < ay:
        return MOVE_DOWN
    pass

# With this template, we are building an AI that will apply combinatorial game theory tools against a greedy opponent
TEAM_NAME = "combinatorialGameTheory"


# We do not need preprocessing, so we let this function empty
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    temps = time() 
    
    global moves    
    global mouvements_exhaustif
    global lastLocation
    global piecesOfCheesePrems
    global cheese_1
    global j
    
     

    
    #
    tkhrbiqa,CheeseOrder,metaMap = Glouton(playerLocation,piecesOfCheese,mazeMap)
    Distances = [metaMap[CheeseOrder[i]][CheeseOrder[i+1]] for i in range(len(piecesOfCheese) - 1)]
    Distances_5 = [Distances[i] + Distances[i+1] + Distances[i+2] + Distances[i+3] for i in range(len(piecesOfCheese) - 4)]
    j = Distances_5.index(min(Distances_5))
    cheese_1 = piecesOfCheese[0]   
    moves += djikstra(mazeMap, playerLocation)[0][cheese_1]
    #
    print(time()-temps)

# This function is expected to return a move

# We use a recursive function that goes through the trees of possible plays
# It takes as arguments a given situation, and return a best target piece of cheese for the player, such that aiming to grab this piece of cheese will eventually lead to a maximum score. It also returns the corresponding score
def best_target(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese):

    # First we should check how many pieces of cheese each player has to see if the play is over. It is the case if no pieces of cheese are left, or if playerScore or opponentScore is more than half the total number playerScore + opponentScore + piecesOfCheese
    totalPieces = len(piecesOfCheese) + playerScore + opponentScore
    if playerScore > totalPieces / 2 or opponentScore > totalPieces / 2 or len(piecesOfCheese) == 0:
        return (-1,-1), playerScore

    # If the play is not over, then the player can aim for any of the remaining pieces of cheese
    # So we will simulate the game to each of the pieces, which will then by recurrence test all
    # the possible trees.

    best_score_so_far = -1
    best_target_so_far = (-1,-1)
    for target in piecesOfCheese:
        end_state = simulate_game_until_target(
            target,playerLocation,opponentLocation,
            playerScore,opponentScore,piecesOfCheese.copy())
        _, score = best_target(*end_state)
        if score > best_score_so_far:
            best_score_so_far = score
            best_target_so_far = target

    return best_target_so_far, best_score_so_far

### FUNCTION TO COMPLETE, 
# Move the agent on the labyrinth using function move from aux and the different directions
# It suffices to move in the direction of the target. 
# You should only run function move once and you can't move diagonally.
## Without loss of generality, we can suppose it gets there moving vertically first then horizontally

def updatePlayerLocation(target,playerLocation):
    if playerLocation[1] != target[1]:
        if target[1] < playerLocation[1]:
            playerLocation = move(playerLocation, MOVE_DOWN)
        else:
            playerLocation = move(playerLocation, MOVE_UP)
    elif target[0] < playerLocation[0]:
        playerLocation = move(playerLocation, MOVE_LEFT)
    else:
        playerLocation = move(playerLocation, MOVE_RIGHT)
    return playerLocation

#FUNCTION TO COMPLETE, 
#CHECK IF EITHER/BOTH PLAYERS ARE ON THE SAME SQUARE OF A CHEESE. 
#If that is the case you have to remove the cheese from the piecesOfCheese list and 
#add points to the score. The players get 1 point if they are alone on the square with a cheese.
#If both players are in the same square and there is a cheese on the square each player gets 0.5 points.
def checkEatCheese(playerLocation,opponentLocation,playerScore,opponentScore,piecesOfCheese):
    if playerLocation in piecesOfCheese and playerLocation == opponentLocation:
        playerScore = playerScore + 0.5
        opponentScore = opponentScore + 0.5
        piecesOfCheese.remove(playerLocation)
    else:
        if playerLocation in piecesOfCheese:
            playerScore = playerScore + 1
            piecesOfCheese.remove(playerLocation)
        if opponentLocation in piecesOfCheese:
            opponentScore = opponentScore + 1
            piecesOfCheese.remove(opponentLocation)
    return playerScore,opponentScore


#FUNCTION TO COMPLETE
#In this function we simulate what will happen until we reach the target
#You should use the two functions defined before
def simulate_game_until_target(target,playerLocation,opponentLocation,playerScore,opponentScore,piecesOfCheese):
    
    #While the target cheese has not yet been eaten by either player
    #We simulate how the game will evolve until that happens    
    while target in piecesOfCheese:
        #Update playerLocation (position of your player) using updatePlayerLocation
        playerLocation = updatePlayerLocation(target,playerLocation)
        #Every time that we move the opponent also moves. update the position of the opponent using turn_of_opponent and move
        opponentLocation = move(opponentLocation, turn_of_opponent(opponentLocation, piecesOfCheese))
        #Finally use the function checkEatCheese to see if any of the players is in the same square of a cheese.
        playerScore, opponentScore = checkEatCheese(
            playerLocation,opponentLocation,playerScore,opponentScore,piecesOfCheese)
    return playerLocation,opponentLocation,playerScore,opponentScore,piecesOfCheese
    

# During our turn we continue going to the next target, unless the piece of cheese it originally contained has been taken
# In such case, we compute the new best target to go to
current_target = (-1,-1)
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):

    if len(piecesOfCheese) > 9 : 

       global moves
       global numberOfmoves # it counts the number of moves that have been followed
       global lastLocation
       global eatenCheese  
       global mouvements_exhaustif
       global piecesOfCheesePrems
       global m
       global k
       global cheese_1
       global j
       temps = time()
       if playerLocation == cheese_1 :
           cheese_1 = (-1,-1)
     
         
           
       if cheese_1 in piecesOfCheese :
           if m <= 0 :
               items_distances = []
               items_moves = {}
               move, visitedCells = djikstra (mazeMap, playerLocation)
               for key in piecesOfCheese :
                   items_moves[key] = move[key]
               for key in piecesOfCheese :
                   heappush(items_distances,(visitedCells[key],key))
               min_tuple = heappop(items_distances)
               if min_tuple[0] < 6 : 
                   moves = items_moves[min_tuple[1]] + djikstra(mazeMap,min_tuple[1])[0][cheese_1]
                   m = len(items_moves[min_tuple[1]])
           m -= 1    
       

       else :
           
           proutage ,pdistances= dijikstra(mazeMap, opponentLocation)
           routage,distances = dijikstra(mazeMap,playerLocation)
           
           ClosestTreatp,ClosestDistancep = piecesOfCheese[0], pdistances[piecesOfCheese[0]]
           for i in range(1,len(piecesOfCheese)):
               if pdistances[piecesOfCheese[i]] < ClosestDistancep:
                   ClosestTreatp,ClosestDistancep = piecesOfCheese[i], pdistances[piecesOfCheese[i]]
                   
                   
           ClosestTreat,ClosestDistance = piecesOfCheese[0], distances[piecesOfCheese[0]]
           ClosestTreat2 = piecesOfCheese[0]
           for i in range(1,len(piecesOfCheese)):
               if distances[piecesOfCheese[i]] < ClosestDistance:
                   ClosestTreat2 = ClosestTreat
                   ClosestTreat,ClosestDistance = piecesOfCheese[i], distances[piecesOfCheese[i]]


           if pdistances[ClosestTreat] < ClosestDistance :
                 return GetMove(playerLocation,Chemin(routage,ClosestTreat2,playerLocation)[1])
           
           elif distances[ClosestTreatp] < pdistances[ClosestTreatp]:
                 return GetMove(playerLocation,Chemin(routage,ClosestTreatp,playerLocation)[1])
               
           
           else :
                 return GetMove(playerLocation,Chemin(routage,ClosestTreat,playerLocation)[1])
              
       if moves != [] :  
           return moves.pop(0)








    else:
        global current_target
        if current_target not in piecesOfCheese:
            current_target, score = best_target(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese)
            print("My new target is " + str(current_target) + " and I will finish with " + str(score) + " pieces of cheese")
            
        if current_target[1] > playerLocation[1]:
            return MOVE_UP
        if current_target[1] < playerLocation[1]:
            return MOVE_DOWN
        if current_target[0] > playerLocation[0]:
            return MOVE_RIGHT
        return MOVE_LEFT
