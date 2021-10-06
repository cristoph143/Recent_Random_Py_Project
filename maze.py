import sys


class Node :
    def __init__ ( self , state , parent , action ) :
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier :
    def __init__ ( self ) :
        self.frontier = [ ]  # list of nodes

    def add ( self , node ) :
        self.frontier.append ( node )

    def contain_state ( self , state ) :
        return any ( node.state == state for node in self.frontier )

    def empty ( self ) :
        return len ( self.frontier ) == 0

    def remove ( self ) :
        if self.empty ( ) :
            raise Exception ( 'Empty Frontier' )
        else :
            node = self.frontier [ -1 ]
            self.frontier = self.frontier [ :-1 ]
            return node


class QueueFrontier ( StackFrontier ) :
    def remove ( self ) :
        if self.empty ( ) :
            raise Exception ( 'Empty Frontier' )
        else :
            node = self.frontier [ 0 ]
            self.frontier = self.frontier [ 1 : ]
            return node


class Maze :
    def __init__ ( self , filename ) :
        # read file and set height and width of Maze
        with open ( filename ) as f :
            contents = f.read ( )
        # validate start and goal
        if contents.count ( 'A' ) != 1 :
            raise Exception ( 'Maze must have Exactly one Start Point' )
        if contents.count ( 'B' ) != 1 :
            raise Exception ( 'Maze must have Exactly one One Goal' )
        # determine height and width of Maze
        contents = contents.splitlines ( )
        self.height = len ( contents )
        self.width = max ( len ( line ) for line in contents )
        # keep tracks of walls
        self.walls = [ ]
        for i in range ( self.height ) :
            row = [ ]
            for j in range ( self.width ) :
                try :
                    if contents [ i ] [ j ] == 'A' :
                        self.start = (i , j)
                        row.append ( False )
                    elif contents [ i ] [ j ] == 'B' :
                        self.goal = (i , j)
                        row.append ( False )
                    elif contents [ i ] [ j ] == ' ' :
                        row.append ( False )
                    else :
                        row.append ( True )
                except IndexError :
                    row.append ( False )
            self.walls.append ( row )

        self.solution = None

    def print ( self ) :
        solution = self.solution [ 1 ] if self.solution is not None else None
        print ( )
        for i , row in enumerate ( self.walls ) :
            for j , col in enumerate ( row ) :
                if col :
                    print ( '#' , end = '' )
                elif (i , j) == self.start :
                    print ( 'A' , end = '' )
                elif (i , j) == self.goal :
                    print ( 'B' , end = '' )
                elif solution is not None and (i , j) in solution :
                    print ( '*' , end = '*' )
                else :
                    print ( ' ' , end = '' )
            print (' ')
        print ( )

    def neighbors ( self , state ) :
        row , col = state
        candidates = [  # Possible Actions
            ('up' , (row - 1 , col)) ,
            ('down' , (row + 1 , col)) ,
            ('left' , (row , col - 1)) ,
            ('right' , (row , col + 1)) ,
        ]
        result = [ ]  # ensure actions are validate
        for action , (r , c) in candidates :
            try :
                if not self.walls [ r ] [ c ] :
                    result.append ( (action , (r , c)) )
            except IndexError :
                continue
        return result

    def solve ( self ) :
        """Finds a Solution to Maze, if one Exists"""
        # keep track of number of states explored
        self.num_explored = 0
        # initialized an empty explored set
        start = Node ( state = self.start , parent = None , action = None )
        frontier = StackFrontier ( )
        frontier.add ( start )
        # initialize an empty explored set
        self.explored = set ( )
        # keep looping until solution found
        while True :
            if frontier.empty ( ) :  # if nothing left in frontier then no path
                raise Exception ( 'no solution' )
            node = frontier.remove ( )  # choose a node from StackFrontier
            self.num_explored += 1
            if node.state == self.goal :
                actions = [ ]
                cells = [ ]
                # follow parent nodes to find solution
                while node.parent is not None :
                    actions.append ( node.action )
                    cells.append ( node.state )
                    node = node.parent
                actions.reverse ( )
                cells.reverse ( )
                self.solution = (actions , cells)
                return
            # mark node as num_explored
            self.explored.add ( node.state )
            # add neighbors to frontier
            for action , state in self.neighbors ( node.state ) :
                if not frontier.contain_state ( state ) and state not in self.explored :
                    child = Node ( state = state , parent = node , action = action )
                    frontier.add ( child )

    def output_image ( self , filename , show_explored = False ) :

        from PIL import Image , ImageDraw
        show_solution = True
        cell_size = 50
        cell_border = 2
        img = Image.new ( 'RGBA' , (self.width * cell_size , self.height * cell_size) , 'black' )  # create blank canvas
        draw = ImageDraw.draw(img)
        solution = self.solution [ 1 ] if self.solution is not None else None
        for i , row in enumerate ( self.walls ) :
            for j , col in enumerate ( row ) :
                if col :
                    fill = (40 , 40 , 40)
                elif (i , j) == self.start :
                    fill = (250 , 0 , 0)
                elif (i , j) == self.goal :
                    fill = (0 , 171 , 28)
                elif solution is not None and show_solution and (i , j) in solution :
                    fill = (220 , 235 , 113)
                elif solution is not None and show_explored and (i , j) in self.neighbors :
                    fill = (212 , 97 , 85)
                else:
                    fill = (237 , 97 , 85)
                draw.rectangle (
                    ([ (j * cell_size + cell_border , i * cell_size + cell_border) ,
                       ((j + 1) * cell_size - cell_border , (i + 1) * cell_size - cell_border) ]) ,
                    fill = fill
                )
                img.save ( filename )
                if len ( sys.argv ) != 2 :
                    sys.exit ( 'Usage.python maze.py maze1.txt' )

if __name__ == "__main__":
    m = Maze('maze.txt')
    print('Maze: ')
    m.print ( )
    print ( 'Solving...' )
    m.solve ( )
    print ( 'States Explored: ' , m.num_explored )
    print ( 'solution' )
    #m.output_image ( 'maze.png' , show_explored = True )
