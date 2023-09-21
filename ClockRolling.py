import utime
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# Create a GalacticUnicorn object and initialize graphics
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

# Set font e.g., bitmap6, bitmap8, sans
graphics.set_font("bitmap6")


def display_number(number_for_display, x, y):
    graphics.set_pen(graphics.create_pen(0,0,0))
    graphics.clear()
        
    graphics.set_pen(graphics.create_pen(255, 105, 0))
    graphics.text(str(number_for_display), x, y, -1, 0.5)
    
    gu.update(graphics)

def scroll_number(from_number, to_number, x, y):
    num_loops = 7
    
    graphics.set_clip(x, y, 10, 6)
    
    while num_loops > 0:
        graphics.set_pen(graphics.create_pen(0,0,0))
        graphics.clear()
        
        graphics.set_pen(graphics.create_pen(255, 105, 0))
        graphics.text(str(from_number), x, y, -1, 0.5)
        graphics.text(str(to_number), x, y+6, -1, 0.5)
        
        gu.update(graphics)
        utime.sleep(0.05)
        
        y -= 1
        num_loops -= 1
    
# Define the vertical position to start
y_position = -1

while True:
    x_position = 20
    y_position = 3
    
    graphics.set_pen(graphics.create_pen(0,0,0))
    graphics.clear()
    
    for current_num in range(10):
        display_number(current_num, x_position, y_position)
        utime.sleep(1 - (7*0.05))
        if current_num == 9:
            target_num = 0
        else:
            target_num = current_num + 1
        scroll_number(current_num, target_num, x_position, y_position)

   
#     graphics.set_pen(graphics.create_pen(255, 105, 0))
#     # Display numbers 0 to 9 in a vertical strip
#     for num in range(12):
#         number_text = str(num % 10)
#         graphics.text(number_text, 20, y_position + num * 6, -1, 0.5)
#     
#     # Update the display
#     gu.update(graphics)
#     
#     # Pause briefly before scrolling
#     utime.sleep(0.05)
#     
#     # Scroll the numbers upwards
#     y_position -= 1
#     
#     # Reset the vertical position when it reaches the top
#     if y_position < -((10*6)): # 10 digits x 6 pixels high
#         y_position = -1

