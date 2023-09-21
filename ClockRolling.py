import utime
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# Create a GalacticUnicorn object and initialize graphics
gu = GalacticUnicorn()
picoboard = PicoGraphics(DISPLAY)

# Set font e.g., bitmap6, bitmap8, sans
picoboard.set_font("bitmap6")

# display.text(text, x, y, wordwrap, scale, angle, spacing)
    # text - the text string to draw
    # x - the destination X coordinate
    # y - the destination Y coordinate
    # wordwrap - number of pixels width before trying to break text into multiple lines
    # scale - size
    # angle - rotation angle (Vector only!)
    # spacing - letter spacing
    # fixed_width - space all characters equal distance apart (monospace)


def show_digit(display_number, x_pos, y_pos):
    # Clear character space to black
    picoboard.set_pen(picoboard.create_pen(0,0,0))
    picoboard.rectangle(x_pos, y_pos, 6, 10)
    
    picoboard.set_pen(picoboard.create_pen(255, 105, 0))
    picoboard.text(str(display_number), x_pos, y_pos, -1, 0.5)

def scroll_digit_1row(reverse, top_number, bottom_number, x_pos, y_pos, loop_num):
    # Clear character space to black
    picoboard.set_pen(picoboard.create_pen(0,0,0))
    picoboard.rectangle(x_pos, y_pos, 6, 10)
    
    picoboard.set_clip(x_pos, y_pos, 6, 6)

    picoboard.set_pen(picoboard.create_pen(255, 105, 0))
    picoboard.text(str(top_number), x_pos, y_pos+1-loop_num, -1, 0.5)
    picoboard.text(str(bottom_number), x_pos, y_pos+7-loop_num, -1, 0.5)
    
    picoboard.remove_clip()
    
old_h1 = old_h2 = old_m1 = old_m2 = old_s1 = old_s2 = 0;

current_time = utime.localtime() # puts hours in current_time[3], minutes in current_time[4], seconds in current_time[5]
# Set initial values for an initial display without any scrolling
old_h1, old_h2 = divmod(current_time[3], 10)
old_m1, old_m2 = divmod(current_time[4], 10)
old_s1, old_s2 = divmod(current_time[5], 10)

while True:
    # Set X across the display for time components
    h1_x = 7
    h2_x = 7+(1*6)
    m1_x = 7+(2*6)
    m2_x = 7+(3*6)
    s1_x = 7+(4*6)
    s2_x = 7+(5*6)
    all_y = 3
    
    picoboard.set_pen(picoboard.create_pen(0,0,0))
    picoboard.clear()
    
    current_time = utime.localtime() # puts hours in current_time[3], minutes in current_time[4], seconds in current_time[5]
    # Split time components HH:MM:SS into two digits
    h1, h2 = divmod(current_time[3], 10)
    m1, m2 = divmod(current_time[4], 10)
    s1, s2 = divmod(current_time[5], 10)
    
    if h1 != old_h1:
        tick_h1 = True
    else:
        tick_h1 = False
        
    if h2 != old_h2:
        tick_h2 = True
    else:
        tick_h2 = False
        
    if m1 != old_m1:
        tick_m1 = True
    else:
        tick_m1 = False
        
    if m2 != old_m2:
        tick_m2 = True
    else:
        tick_m2 = False
        
    if s1 != old_s1:
        tick_s1 = True
    else:
        tick_s1 = False
        
    if s2 != old_s2:
        tick_s2 = True
    else:
        tick_s2 = False
         
    picoboard.set_pen(picoboard.create_pen(0,0,0))
    picoboard.clear()
    picoboard.set_pen(picoboard.create_pen(255, 105, 0))
    
    loop_num = 1
    
    while loop_num <= 5: # Digits are 5 px high
        #print(h1, old_h1, h1 != old_h1, tick_h1)
        if tick_h1:
            scroll_digit_1row(0, old_h1, h1, h1_x, all_y, loop_num)
        else:
            show_digit(old_h1, h1_x, all_y)
        
        if tick_h2:
            scroll_digit_1row(0, old_h2, h2, h2_x, all_y, loop_num)
        else:
            show_digit(old_h2, h2_x, all_y)
            
        if tick_m1:
            scroll_digit_1row(0, old_m1, m1, m1_x, all_y, loop_num)
        else:
            show_digit(old_m1, m1_x, all_y)
            
        if tick_m2:
            scroll_digit_1row(0, old_m2, m2, m2_x, all_y, loop_num)
        else:
            show_digit(old_m2, m2_x, all_y)

        if tick_s1:
            scroll_digit_1row(0, old_s1, s1, s1_x, all_y, loop_num)

        else:
            show_digit(old_s1, s1_x, all_y)
            
        if tick_s2:
            scroll_digit_1row(0, old_s2, s2, s2_x, all_y, loop_num)

        else:
            show_digit(old_s2, s2_x, all_y)

        gu.update(picoboard)
        
        utime.sleep(0.05)

        loop_num += 1
     
    old_h1 = h1
    old_h2 = h2
    old_m1 = m1
    old_m2 = m2
    old_s1 = s1
    old_s2 = s2

    utime.sleep(1 - (5*0.05))
