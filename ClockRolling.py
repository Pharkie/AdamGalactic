import utime
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# Create a GalacticUnicorn object and initialize graphics
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

# Set font e.g., bitmap6, bitmap8, sans
graphics.set_font("bitmap6")

# Define the vertical position to start
y_position = 5

while True:
    graphics.set_pen(graphics.create_pen(0,0,0))
    graphics.clear()
    
    graphics.set_pen(graphics.create_pen(255, 105, 0))
    # Display numbers 0 to 9 in a vertical strip
    for num in range(20):
        number_text = str(num % 10)
        graphics.text(number_text, 20, y_position + num * 6, -1, 0.5)
    
    # Update the display
    gu.update(graphics)
    
    # Pause briefly before scrolling
    utime.sleep(0.1)
    
    # Scroll the numbers upwards
    y_position -= 1
    
    # Reset the vertical position when it reaches the top
    if y_position < -48:
        y_position = 5

