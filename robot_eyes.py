import pygame
import time
import random



def run_eyes() -> None:

    # Initialize screen
    pygame.display.init()

    # Hide the mouse cursor
    pygame.mouse.set_visible(False)

    # Screen dimensions
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SRCALPHA)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Robotic eyes")

    # Colors
    BLACK = (0, 0, 0)
    BLUE = (75, 170, 200)
    WHITE = (255, 255, 255)

    # Eye properties
    eye_width, eye_height = 600, 850
    eye_spacing = 150    # Space between the eyes
    corner_radius = 50  # Radius of the eye corners

    # Pupil properties
    pupil_width, pupil_height = 200, 300
    pupil_move_interval = random.uniform(10, 15)  # Time in seconds between movements
    pupil_speed = 2  # Speed of pupil movement
    next_pupil_move_time = time.time() + pupil_move_interval
    margin = 50 # Margin from the edges of the eyes

    # Eye positions
    left_eye_pos = (WIDTH // 2 - eye_width - eye_spacing // 2, HEIGHT // 2 - eye_height // 2)
    right_eye_pos = (WIDTH // 2 + eye_spacing // 2, HEIGHT // 2 - eye_height // 2)

    # Pupil positions (initially centered)
    left_pupil_pos = [left_eye_pos[0] + (eye_width - pupil_width) // 2, left_eye_pos[1] + (eye_height - pupil_height) // 2]
    right_pupil_pos = [right_eye_pos[0] + (eye_width - pupil_width) // 2, right_eye_pos[1] + (eye_height - pupil_height) // 2]

    # Target positions for smooth movement
    left_pupil_target = left_pupil_pos[:]
    right_pupil_target = right_pupil_pos[:]

    # Blink settings
    blink_duration = 0.15
    blink_interval = random.uniform(10, 20)
    next_blink_time = time.time() + blink_interval
    blinking = False

    # Main loop
    running = True
    clock = pygame.time.Clock()

    while running:

        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to quit
                    running = False

        screen.fill(BLACK)

        # Blinking
        current_time = time.time()
        if blinking:
            if current_time >= blink_end_time:
                blinking = False
                next_blink_time = current_time + blink_interval
        elif current_time >= next_blink_time:
            blinking = True
            blink_end_time = current_time + blink_duration

        # Pupil movement
        if current_time >= next_pupil_move_time:
            move_x = random.randint(-eye_width + margin + pupil_width, eye_width - margin - pupil_width)
            move_y = random.randint(-eye_height + margin + pupil_height, eye_height - margin - pupil_height)

            left_pupil_target = [
                max(left_eye_pos[0] + margin, min(left_eye_pos[0] + eye_width - pupil_width - margin, left_pupil_pos[0] + move_x)),
                max(left_eye_pos[1] + margin, min(left_eye_pos[1] + eye_height - pupil_height - margin, left_pupil_pos[1] + move_y))
            ]

            right_pupil_target = [
                max(right_eye_pos[0] + margin, min(right_eye_pos[0] + eye_width - pupil_width - margin, right_pupil_pos[0] + move_x)),
                max(right_eye_pos[1] + margin, min(right_eye_pos[1] + eye_height - pupil_height - margin, right_pupil_pos[1] + move_y))
            ]

            next_pupil_move_time = current_time + pupil_move_interval

        # Smooth movement
        for i in range(2):  # x and y
            if left_pupil_pos[i] < left_pupil_target[i]:
                left_pupil_pos[i] = min(left_pupil_pos[i] + pupil_speed, left_pupil_target[i])
            elif left_pupil_pos[i] > left_pupil_target[i]:
                left_pupil_pos[i] = max(left_pupil_pos[i] - pupil_speed, left_pupil_target[i])

            if right_pupil_pos[i] < right_pupil_target[i]:
                right_pupil_pos[i] = min(right_pupil_pos[i] + pupil_speed, right_pupil_target[i])
            elif right_pupil_pos[i] > right_pupil_target[i]:
                right_pupil_pos[i] = max(right_pupil_pos[i] - pupil_speed, right_pupil_target[i])

        # Draw eyes
        if not blinking:
            pygame.draw.rect(screen, BLUE, (*left_eye_pos, eye_width, eye_height), border_radius=corner_radius)
            pygame.draw.rect(screen, BLUE, (*right_eye_pos, eye_width, eye_height), border_radius=corner_radius)

            # Draw pupils
            pygame.draw.rect(screen, WHITE, (*left_pupil_pos, pupil_width, pupil_height), border_radius=corner_radius // 2)
            pygame.draw.rect(screen, WHITE, (*right_pupil_pos, pupil_width, pupil_height), border_radius=corner_radius // 2)

        else:
            pygame.draw.rect(screen, BLUE, (left_eye_pos[0], HEIGHT // 2 - eye_height // 16, eye_width, eye_height // 8), border_radius=corner_radius)
            pygame.draw.rect(screen, BLUE, (right_eye_pos[0], HEIGHT // 2 - eye_height // 16, eye_width, eye_height // 8), border_radius=corner_radius)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.display.quit()
