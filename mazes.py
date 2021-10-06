import os
import cv2
import glob
import shutil
import random
import imageio
from PIL import Image
from queue import Queue
from time import perf_counter


class MazeSolver :
    """
    Solve a 2-color(wall color and path color) maze using several algorithm choices:
    - Breadth-First Search Algorithm(BFS).
    """

    def __init__ ( self ,
                   maze_path ,
                   marking_color ,
                   start_end = None ,
                   solution_size = (500 , 500) ,
                   downsize = (150 , 150) ,
                   ) :
        """
        Initialize maze image, mark start and end points.
        maze_path: a string (path to maze image).
        marking_color: RGB tuple of color to use for drawing the solution path.
        solution_size: a tuple (height, width) of the solved version size.
        start_end: a tuple of x, y coordinates of maze start and x, y coordinates of maze end or
        'a' for automatic mode.
        """
        self.path = input (
            "Enter folder path to save images and GIF frames: "
        ).rstrip ( )
        while not os.path.exists ( self.path ) :
            print ( f"Invalid folder path {self.path}" )
            self.path = input (
                "Enter folder path to save images and gifs: "
            ).rstrip ( )
        self.maze = Image.open ( maze_path ).resize ( downsize )
        self.downsize = downsize
        self.height , self.width = self.maze.size
        self.maze_path = maze_path
        self.marking_color = marking_color
        if start_end == "a" :
            self.initial_coordinates = [ ]
            self._automatic_start_end ( )
            self.start , self.end = self.initial_coordinates
        if start_end and start_end != "a" :
            self.start , self.end = start_end
        if not start_end :
            self.initial_coordinates = [ ]
            self.titles = [ "(End)" , "(Start)" ]
            self._set_start_end ( )
            self.start , self.end = self.initial_coordinates
        self.path_color = self.maze.getpixel (
            (self.start [ 0 ] , self.start [ 1 ])
        )
        self.wall_color = self.maze.getpixel ( (0 , 0) )
        self.solution_name = (
                str ( random.randint ( 10 ** 6 , 10 ** 8 ) )
                + " Maze solution"
        )
        self.output_image_size = solution_size
        self.configurations = {
            "bfs" : self._breadth_first_search ( )
        }
        self.algorithm_names = {
            "bfs" : "BREADTH-FIRST SEARCH "
        }

    def _automatic_start_end ( self ) :
        """Determine start and end automatically"""
        start = 0
        end_rows , end_columns = (
            self.height - 1 ,
            self.width - 1 ,
        )
        border_color = self.maze.getpixel ( (0 , 0) )
        while (
                self.maze.getpixel ( (start , start) )
                == border_color
        ) :
            start += 1
        while (
                self.maze.getpixel ( (end_rows , end_columns) )
                == border_color
        ) :
            end_rows -= 1
            end_columns -= 1
        self.initial_coordinates.append ( (start , start) )
        self.initial_coordinates.append (
            (end_rows , end_columns)
        )

    def _set_start_end ( self ) :
        """
        Show maze image to determine coordinates.
        You will be shown the maze, click twice, first to indicate the starting point
        and second to indicate ending point and then press any key to proceed.
        """
        maze_image = cv2.imread ( self.maze_path )
        resized_image = cv2.resize (
            maze_image , self.downsize
        )
        cv2.namedWindow ( "Maze to solve" )
        cv2.setMouseCallback (
            "Maze to solve" , self._get_mouse_click
        )
        cv2.imshow ( "Maze to solve" , resized_image )
        cv2.waitKey ( 0 )
        cv2.destroyAllWindows ( )
        if len ( self.initial_coordinates ) != 2 :
            raise ValueError (
                f"Expected 2 clicks for start and end "
                f"respectively, got {len ( self.initial_coordinates )}"
            )

    def _get_mouse_click ( self , event , x , y , flags , param ) :
        """Get x, y coordinates for mouse clicks on maze image."""
        if event == cv2.EVENT_LBUTTONDOWN :
            self.initial_coordinates.append ( (x , y) )
            print (
                f"Clicked on coordinates {x , y} {self.titles.pop ( )} color: {self.maze.getpixel ( (x , y) )}"
            )

    def _get_neighbor_coordinates ( self , coordinates ) :
        """
        Return a list of adjacent pixel coordinates that represent a path."""
        x , y = coordinates
        north = (x - 1 , y)
        if north [ 0 ] < 0 :
            north = None
        if (
                north
                and self.maze.getpixel ( north ) == self.wall_color
        ) :
            north = None
        south = (x + 1 , y)
        if south [ 0 ] > self.height :
            south = None
        if (
                south
                and self.maze.getpixel ( south ) == self.wall_color
        ) :
            south = None
        east = (x , y + 1)
        if east [ 1 ] > self.width :
            east = None
        if (
                east
                and self.maze.getpixel ( east ) == self.wall_color
        ) :
            east = None
        west = (x , y - 1)
        if west [ 1 ] < 0 :
            west = None
        if (
                west
                and self.maze.getpixel ( west ) == self.wall_color
        ) :
            west = None
        return [
            neighbor
            for neighbor in (north , south , east , west)
            if neighbor
        ]

    def _breadth_first_search ( self ) :
        """Return path and visited pixels solved by a breadth-first search algorithm."""
        check = Queue ( )
        check.put ( [ self.start ] )
        visited = [ ]
        while not check.empty ( ) :
            path = check.get ( )
            last = path [ -1 ]
            if last == self.end :
                return path , visited
            if last not in visited :
                neighbor_coordinates = self._get_neighbor_coordinates (
                    last
                )
                valid_coordinates = [
                    neighbor
                    for neighbor in neighbor_coordinates
                    if neighbor not in visited
                ]
                for valid_coordinate in valid_coordinates :
                    new_path = list ( path )
                    new_path.append ( valid_coordinate )
                    check.put ( new_path )
                visited.append ( last )
        raise ValueError (
            f"Too low downsize rate {self.downsize}"
        )

    def produce_path_image ( self , configuration ) :
        """
        Draw path in maze and return solved maze picture.
        configuration: a string representing the algorithm:
        - 'bfs': solve using breadth-first search algorithm.
        """
        start_time = perf_counter ( )
        os.chdir ( self.path )
        if configuration not in self.configurations :
            raise ValueError (
                f"Invalid configuration {configuration}"
            )
        path , visited = self.configurations [ configuration ]
        for coordinate in path :
            self.maze.putpixel (
                coordinate , self.marking_color
            )
        if "Solutions" not in os.listdir ( self.path ) :
            os.mkdir ( "Solutions" )
        os.chdir ( "Solutions" )
        maze_name = "".join (
            [
                self.algorithm_names [ configuration ] ,
                self.solution_name ,
                ".png" ,
            ]
        )
        resized_maze = self.maze.resize (
            self.output_image_size
        )
        resized_maze.save ( maze_name )
        end_time = perf_counter ( )
        print ( f"Time: {end_time - start_time} seconds." )
        return resized_maze

    def produce_maze_solving_visualization (
            self , configuration , frame_speed , new_size = None
    ) :
        """
        Generate GIF for the solution of the maze by the selected algorithm:
        configuration: a string:
        - 'bfs': Breadth-first search algorithm.
        frame_speed: frame speed in ms
        new_size: a tuple containing new (height, width)
        """
        start_time = perf_counter ( )
        initial_image = Image.open ( self.maze_path ).resize (
            self.downsize
        )
        os.chdir ( self.path )
        if configuration not in self.configurations :
            raise ValueError (
                f"Invalid configuration {configuration}"
            )
        path , visited = self.configurations [ configuration ]
        count = 1
        for coordinate in visited :
            self.maze.putpixel (
                coordinate , self.marking_color
            )
            if new_size :
                resized = self.maze.resize ( new_size )
                resized.save ( str ( count ) + ".png" )
            else :
                self.maze.save ( str ( count ) + ".png" )
            count += 1
        if new_size :
            resized = initial_image.resize ( new_size )
            resized.save ( str ( count ) + ".png" )
        else :
            initial_image.save ( str ( count ) + ".png" )
        count += 1
        for coordinate in path [ : :-1 ] :
            initial_image.putpixel (
                coordinate , self.marking_color
            )
            if new_size :
                resized = initial_image.resize ( new_size )
                resized.save ( str ( count ) + ".png" )
            else :
                initial_image.save ( str ( count ) + ".png" )
            count += 1
        os.mkdir ( self.solution_name )
        for file in os.listdir ( self.path ) :
            if file.endswith ( ".png" ) :
                shutil.move ( file , self.solution_name )
        os.chdir ( self.solution_name )
        frames = glob.glob ( "*.png" )
        frames.sort ( key = lambda x : int ( x.split ( "." ) [ 0 ] ) )
        frames = [ imageio.imread ( frame ) for frame in frames ]
        imageio.mimsave (
            self.path + str ( self.solution_name ) + ".gif" ,
            frames ,
            "GIF" ,
            duration = frame_speed ,
        )
        end_time = perf_counter ( )
        print ( f"Time: {end_time - start_time} seconds." )


if __name__ == "__main__" :
    test = MazeSolver ( "test.png" , (255 , 0 , 0) , "a" )
    test.produce_path_image ( "bfs" ).show ( )
