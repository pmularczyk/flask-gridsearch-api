# Standard library imports
from functools import reduce

# Third party imports
import numpy as np

# Local application imports
from queue import Queue

class SearchSquareGrid:
    """ SearchSquareGrid(data, size)

    Parameters:
    -----------
    data : list
        the grid that gets searched in form of a list
        e.g. ['p--','x-x','x-m']

    size : integer
        the size of the grid in the case of three list 
        elements would be 3


    Returns:
    --------
    list : stdout
        depending on which method is used it returns a list
        of tuples, list of strings or list of lists

    Examples:
    ---------
    >>> data = ['p--','x-x','x-m']
    >>> size = 3
    >>> grid = SearchSquareGrid(data, size)

    >>> grid.breadth_first_search()
    [(2, 2), (2, 1), (1, 1), (0, 1), (0, 0)]

    >>> grid.get_path()
    ['Left', 'Up', 'Up', 'Left']

    >>> grid.get_grid()
    [['p' '-' '-']
    ['x' '-' 'x']
    ['x' '-' 'm']]

    >>> grid.get_walls()
    [(1, 0), (1, 2), (2, 0)]
    """

    def __init__(self, data, size):
        self.data = data
        self.size = size
        self.error_flag = False
        
        self._grid = self._validate_and_create_grid()
        self._walls = self._create_walls_from_grid()

    def _validate_and_create_grid(self):

        # check if data input is of type list or array
        if type(self.data) != type([]) and type(self.data) != type(np.array([])):
            self.error_flag = True
            return self.error_flag

        try:
            grid = list(reduce(lambda a, b: a + b, self.data))
            grid = np.array(grid).reshape(self.size, self.size)
        except (ValueError, TypeError):
            self.error_flag = True
            return self.error_flag

        return grid

    def _create_walls_from_grid(self):

        # get grid to create walls
        self._grid = self._validate_and_create_grid()

        # get position of wall elements
        # convert it to list of tuples
        wall_elems = np.where(self._grid == "x")
        walls = np.array(wall_elems).transpose()
        walls = [tuple(element) for element in walls]

        return walls

    
    def _get_start_end_position(self, char):

        if self.error_flag:
            return self.error_flag
        
        try:
            x, y = np.where(self._grid == char)
            position = x[0], y[0]
            return position
        except IndexError:
            # print("You have to provide a start and a goal")
            self.error_flag = True
            return self.error_flag
        

    def _within_bounds(self, position):

        # check the position tuple it within the grid
        x, y = position

        return 0 <= x < self.size and 0 <= y < self.size
    
    def _traversable(self, position):

        # check if position tuple is a wall or not
        return position not in self._walls
    
    def _neighbors(self, position):

        x, y = position

        results = [(x + 1, y),  # next below neigbor
                   (x, y - 1),  # next left
                   (x - 1, y),  # next above
                   (x, y + 1)]  # next right

        if (x + y) % 2 == 0:
            results.reverse()

        results = filter(self._within_bounds, results)
        results = filter(self._traversable, results)

        return results


    def get_grid(self):

        return self._grid

    def get_walls(self):

        return self._walls

    def breadth_first_search(self):

        if self.error_flag:
            return self.error_flag

        start = self._get_start_end_position("m")
        end = self._get_start_end_position("p")

        border = Queue()
        border.put(start)
        origin = {}
        origin[start] = None
    
        while not border.empty():
    
            current = border.get()
    
            if current == end:
                break
    
            for next in self._neighbors(current):
                if next not in origin:
                    border.put(next)
                    origin[next] = current
    
        current = end
        path = []

        # if there is no way to the princess
        if next == start:
            return []

        else:
            while current != start: 
                path.append(current)
                current = origin[current]
            path.append(start)
            path.reverse()
    
        return path

    @staticmethod
    def tuple_diff(tpl_1, tpl_2):
    
        if len(tpl_1) > 2 or len(tpl_1) < 2:
            raise ValueError("Not correct number of values (expected 2)")
            
        if len(tpl_2) > 2 or len(tpl_2) < 2:
            raise ValueError("Not correct number of values (expected 2)")
        
        row_elem_tpl_1, col_elem_tpl_1 = tpl_1
        row_elem_tpl_2, col_elem_tpl_2 = tpl_2
        
        row_result = row_elem_tpl_1 - row_elem_tpl_2
        col_result = col_elem_tpl_1 - col_elem_tpl_2
        
        return row_result, col_result
    
    def get_path(self):

        if self.error_flag:
            return self.error_flag

        path_list = self.breadth_first_search()
        
        path = []
    
        for i in range(len(path_list)):
            try:
                current = path_list[i]
                at_next = path_list[i + 1]
    
                diff = SearchSquareGrid.tuple_diff(current, at_next)
                row_diff = diff[0]
                col_diff = diff[1]
    
                # Check row results
                if row_diff > 0:
                    path.append("Up")
                elif row_diff < 0:
                     path.append("Down")
                elif col_diff > 0:
                    path.append("Left")
                elif col_diff < 0:
                    path.append("Right")
    
            except IndexError:
                pass
            
        return path