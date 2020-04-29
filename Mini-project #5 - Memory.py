# implementation of card game - Memory

import simplegui
import random

global FONT_SIZE

FONT_SIZE = 50

# helper function to initialize globals
def new_game():
    global numbers_list
    global exposed_list
    global cell_width
    global frame_width
    global frame_height
    global first_click_index
    global second_click_index
    global attempts
    global label
    
    numbers_list = [number for number in range(8)]
    first_click_index = '' #variables to compare numbers in mouseclock(pos)
    second_click_index = '' #variables to compare numbers in mouseclock(pos)
    attempts = 0
    numbers_list *= 2
    random.shuffle(numbers_list)
    exposed_list = [0 for i in range(len(numbers_list))]
    cell_width = len(str(numbers_list[-1])) * FONT_SIZE #cell_width = %max count of digits in number% * %width of one digit% = %max count of digits in number% * %FONT_SIZE% 
    frame_width = cell_width * len(numbers_list)
    frame_height = cell_width
    
    # create frame and add a button and labels
    frame = simplegui.create_frame("Memory", frame_width, frame_height)
    label = frame.add_label('') #draw empty line on canvas to avoid interface elemets overlaping for some values of FONT_SIZE
    label = frame.add_label('') #draw empty line on canvas to avoid interface elemets overlaping for some values of FONT_SIZE
    label = frame.add_label('') #draw empty line on canvas to avoid interface elemets overlaping for some values of FONT_SIZE
    label = frame.add_label('') #draw empty line on canvas to avoid interface elemets overlaping for some values of FONT_SIZE
    frame.add_button("Reset", new_game)
    label = frame.add_label('Turns = ' + str(attempts))
    
    # register event handlers
    frame.set_mouseclick_handler(mouseclick)
    frame.set_draw_handler(draw)
    
    # get things rolling
    frame.start()

# define event handlers
def mouseclick(pos):
    global first_click_index
    global second_click_index
    global attempts

    number_index = pos[0] / cell_width
    if exposed_list[number_index] == 0:
        if first_click_index != '' and second_click_index != '': #check if two cells has been opened already + open current cell
            attempts += 1
            if numbers_list[first_click_index] == numbers_list[second_click_index]: #if numbers in opened cells are even, we keep these cells opened permanently (state=2)
                exposed_list[first_click_index] = 2
                exposed_list[second_click_index] = 2
            else: #if numbers are differ, hide these cells (state=0)
                exposed_list[first_click_index] = 0
                exposed_list[second_click_index] = 0
            exposed_list[number_index] = 1 #temp open current cell (state=1)
            first_click_index = number_index
            second_click_index = ''
        elif first_click_index != '':
            second_click_index = number_index
            exposed_list[second_click_index] = 1
        elif first_click_index == '':
            attempts += 1
            first_click_index = number_index
            exposed_list[first_click_index] = 1
        else:
            print 'Unexpected if/else output in mouseclick(pos)'
    label.set_text('Turns = ' + str(attempts))
                        
def draw(canvas):
    text_x_pos = cell_width * 1/4
    text_y_pos = cell_width * 7/8
    polygon_positing = 0
    number_index = 0
    for number in numbers_list:
        if exposed_list[number_index] == 0:
            canvas.draw_polygon([[polygon_positing, 0], [polygon_positing+cell_width, 0], [polygon_positing+cell_width, cell_width], [polygon_positing, cell_width]], 2, 'white', 'blue')
        elif exposed_list[number_index] == 1:
            canvas.draw_polygon([[polygon_positing, 0], [polygon_positing+cell_width, 0], [polygon_positing+cell_width, cell_width], [polygon_positing, cell_width]], 2, 'white')        
            canvas.draw_text(str(number), [text_x_pos, text_y_pos], FONT_SIZE, 'white')
        elif exposed_list[number_index] == 2:
            canvas.draw_polygon([[polygon_positing, 0], [polygon_positing+cell_width, 0], [polygon_positing+cell_width, cell_width], [polygon_positing, cell_width]], 2, 'white')  
            canvas.draw_text(str(number), [text_x_pos, text_y_pos], FONT_SIZE, 'white')
        else:
            print 'Unexprected value of exposed_list: ', exposed_list[number_index]
        text_x_pos += cell_width
        polygon_positing += cell_width
        number_index += 1

new_game()


# Always remember to review the grading rubric
