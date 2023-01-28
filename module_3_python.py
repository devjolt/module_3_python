"""
our assignment is to code, in python 3, a program to plot routes
for a simple drone guidance system.

The program should be able to plot the routes by following the
instructions from a series of route guidance files.

The program should either display the route (and print the coordinates of the route),
or state that the route is not valid (e.g., outside of the grid).

The program should continue to ask for the next route until requested to stop.

We require that the program you write does some things in a very specific way
so please follow the bullet points below to the letter
otherwise your program will be automatically failed.

The program must run in Python3 without error.
The size of the grid to display is 12 x 12
The following route instruction files are provided: (
these are provided in docx, you will need to convert these to txt files
(using the Save As option in Word, and save as Plain Text (*.txt) )
Route001.txt, Route002.txt and Route003.txt

The format of the route instructions file is as follows:
Item 1: X-Coordinate of start of route
Item 2: Y-Coordinate of start of route
Item 3 onwards: N, S, E, or W

The program must output the completed route plot grid and the route coordinates,
or the reason why the grid cannot be plotted
(i.e., “Error: The route is outside of the grid”).

The route instruction files must be stored in the same path
(as a .txt file not docx) as the program code and when the file is loaded,
do not include the path (i.e. “open(‘Route001.txt’, …)”).

Refer to the Route Plot Guidance Notes for more details
and example of the type of output format that is expected
for the grid layout and coordinates.

The program must only stop to ask for the filename of the next route instructions file,
or when the instruction STOP is entered
(ie. “Enter the next route instructions file or enter STOP to finish:”).

There should be no menus or other user input.
"""

def blank_grid(size:int=12)->'size*size array to be used as a grid, default 12':
    return [['   ' for i in range(size)] for i in range(size)]

def make_grid_number(i:int)->str:
    return (' '+str(i+1).zfill(2))

def print_grid(new_grid:list):
    grid_text = '\n'

    row_num = len(new_grid)-1
    for row in new_grid[::-1]:# reverse new_grid, so last row is first
        grid_text+=make_grid_number(row_num)
        for square in row:
            grid_text+=square
        grid_text+='\n'
        row_num-=1

    grid_text+='  '
    for i in range(len(new_grid[0])):
        grid_text+=make_grid_number(i)
    
    print(grid_text+'\n')


def populate_grid_and_get_coordinates(x:int, y:int, bearings:list):
    coordinates = [(x,y)]

    new_grid = blank_grid()
    new_grid[y-1][x-1] = ' S '

    direction_indicators = {
        'N':'^',
        'E':'>',
        'S':'v',
        'W':'<'
    }


    for bearing in bearings: # assume that bearing is a letter NESW plus \n
        
        if bearing == 'N':
            y+=1
        elif bearing == 'S':
            y-=1
        elif bearing == 'E':
            x+=1
        elif bearing == 'W':
            x-=1
        else:
            pass
        old_bearing = bearing

        if x<1 or y<1 or x>len(new_grid) or x>len(new_grid):
            print(f'\n>>> ERROR: Drone path leaves grid attempting to go {bearing} from {old_x},{old_y}')

            print('\nKey: S = Start')
            print('     E = Drone path leaves grid')

            new_grid[old_y-1][old_x-1] = ' E ' 
            
            coordinates.append(('ERROR'))
            
            print_grid(new_grid)
            print(coordinates)   
            return

        # new_grid[y-1][x-1] = ' x '
        new_grid[y-1][x-1] = f' {direction_indicators[bearing]} '
        coordinates.append((x,y))
        old_x,old_y = x,y

    new_grid[y-1][x-1] = ' F '
    
    print('\nkey: S = Start')
    print('     F = Finish')
    print_grid(new_grid)
    print(coordinates)
    return

while True:
    prompt_text = "Enter the next route instructions file or enter STOP to finish:"
    instruction = input(prompt_text)
    
    if instruction == 'STOP':
        print('Ending program')
        break # stop searching for new orders
    
    try: # validate filename
        f = open(instruction, 'r')
    except FileNotFoundError as e:
        print(e)
        print(f'>>> {instruction} was not found.\n    Please check it exists or check your input!')
        continue

    lines = f.read().split('\n')
    
    try: # validate starting coordinates for drone
        x,y = int(lines[0]), int(lines[1])
        print(f'starting at: {x},{y}')
    except ValueError as e: # if first or second line do not contain an integer
        print(e)
        print(f'>>> The first two lines of file {instruction} should each contain one integer e.g. 4')
        print(f'    Please review {instruction} and correct!')
        continue
    
    populate_grid_and_get_coordinates(x, y, lines[2:])

