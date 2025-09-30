import pygame
import serial

pygame.init()

# Window
win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Joystick Game")
# Character
character_size = 50
character_color = (0, 255, 0)
character_x, character_y = win_width//2, win_height//2
character_speed = 5

# Serial
arduino_port = 'COM3'
ser = serial.Serial(arduino_port, 9600)

running = True
prev_x, prev_y = character_x, character_y

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read serial data
    if ser.in_waiting > 0:
        data = ser.readline().decode(errors='ignore').strip().split(',')
        if len(data) == 3:
            joy_x, joy_y, button_state = map(int, data)
            new_x = character_x + int((joy_x - 512)/100 * character_speed)
            new_y = character_y + int((joy_y - 512)/100 * character_speed)

            new_x = max(character_size//2, min(win_width - character_size//2, new_x))
            new_y = max(character_size//2, min(win_height - character_size//2, new_y))

            if (new_x, new_y) != (prev_x, prev_y):
                character_x, character_y = new_x, new_y
                character_color = (0, 0, 255) if button_state == 1 else (255, 0, 0)
                prev_x, prev_y = character_x, character_y

    # Draw
    win.fill((255, 255, 255))
    pygame.draw.circle(win, character_color, (character_x, character_y), character_size//2)
    pygame.display.flip()

# Cleanup
ser.close()
pygame.quit()
