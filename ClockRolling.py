import utime
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# Create a GalacticUnicorn object and initialize graphics
gu = GalacticUnicorn()
picoboard = PicoGraphics(DISPLAY)

# Set font e.g., bitmap6, bitmap8, sans
picoboard.set_font("bitmap6")

# Define a function to display a single digit
def show_digit(display_number, x_pos, y_pos):
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.rectangle(x_pos, y_pos, 5, 6)
    
    picoboard.set_pen(picoboard.create_pen(255, 105, 0))
    picoboard.text(str(display_number), x_pos, y_pos, -1, 0.5)

# Define a function to scroll a single digit
def scroll_digit(reverse, top_number, bottom_number, x_pos, y_pos, loop_num):
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.rectangle(x_pos, y_pos, 5, 6)
    
    picoboard.set_clip(x_pos, y_pos, 5, 6)

    picoboard.set_pen(picoboard.create_pen(255, 105, 0))
    picoboard.text(str(top_number), x_pos, y_pos - 1 - loop_num, -1, 0.5)
    picoboard.text(str(bottom_number), x_pos, y_pos + 5 - loop_num, -1, 0.5)
    
    picoboard.remove_clip()

current_time = utime.localtime() # puts hours in current_time[3], minutes in current_time[4], seconds in current_time[5]
# Set initial values for an initial display without any scrolling
old_h1, old_h2 = divmod(current_time[3], 10)
old_m1, old_m2 = divmod(current_time[4], 10)
old_s1, old_s2 = divmod(current_time[5], 10)

old_values = [old_h1, old_h2, old_m1, old_m2, old_s1, old_s2] # h1, h2, m1, m2, s1, s2

while True:
    # Set X across the display for time components
    x_positions = [7, 7 + 1 * 5, 7 + (2 * 5) + 2, 7 + (3 * 5) + 2, 7 + (4 * 5) + 5, 7 + (5 * 5) + 5]
    all_y = 3
    
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    
    current_time = utime.localtime()
    
    # Split time components HH:MM:SS into two digits
    h1, h2 = divmod(current_time[3], 10)
    m1, m2 = divmod(current_time[4], 10)
    s1, s2 = divmod(current_time[5], 10)
    
    values = [h1, h2, m1, m2, s1, s2]
    
    # Initialize a list to track which digits need scrolling
    tick_flags = [values[i] != old_values[i] for i in range(6)]
    
    for i in range(6): # Loop for vertical lines of a digit (6)   
        for j in range(6): # Loop for each of the time variables in HH:MM:SS
            if tick_flags[j]:
                scroll_digit(0, old_values[j], values[j], x_positions[j], all_y, i)
            else:
                show_digit(old_values[j], x_positions[j], all_y)


        # Add colons
        if current_time[5] % 2 == 0:
            picoboard.set_pen(picoboard.create_pen(255, 105, 0))
            picoboard.text(":", 7 + (2 * 5), all_y, -1, 0.5)  # HH:MM
            picoboard.text(":", 7 + (4 * 5) + 3, all_y, -1, 0.5)  # MM:SS  
        
        # Update display
        gu.update(picoboard)
        utime.sleep(0.05)

    utime.sleep(1 - (6 * 6 * 0.05))
    
    # Update old values
    old_values = values.copy()

