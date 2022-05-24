import pygame
from pygame import mixer

pygame.init()

WIDTH = 1200
HEIGHT = 700

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('The Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 23)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range (instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)

# Load in sounds
hi_hat = mixer.Sound('sounds/hi_hat.wav')
snare = mixer.Sound('sounds/snare.wav')
kick = mixer.Sound('sounds/kick.wav')
cymbal = mixer.Sound('sounds/cymbal.wav')
clap = mixer.Sound('sounds/clap.wav')
tom = mixer.Sound('sounds/tom.wav')
pygame.mixer.set_num_channels(instruments * 3)

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                cymbal.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()

def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 1)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 1)
    boxes = []
    colors = [gray, white, gray]

    hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (30, 20))

    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30, 100))

    kick_text = label_font.render('Bass Drum', True, colors[actives[2]])
    screen.blit(kick_text, (30, 180))

    cymbal_text = label_font.render('Cymbal', True, colors[actives[3]])
    screen.blit(cymbal_text, (30, 260))

    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (30, 340))

    floor_text = label_font.render('Floor Tom', True, colors[actives[5]])
    screen.blit(floor_text, (30, 420))

    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, ( i * 80)), (200, ( i * 80)), 1)

    for i in range(beats):
        for j in range(instruments):
            if clicked[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray

            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205, (j * 80) + 5, ((WIDTH - 200) // beats) - 10, ((HEIGHT - 200) // instruments) - 10], 0, 3)

            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, (j * 80), ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 3, 3)

            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, (j * 80), ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 2, 3)

            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 80], 5, 3)

    return boxes

def draw_save_menu():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))

    return exit_btn

def draw_load_menu():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    
    return exit_btn

run = True
while run:
    timer.tick(fps)

    screen.fill(black)
    
    boxes = draw_grid(clicked, active_beat, active_list) 

    # Lower menu
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))

    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
         play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))

    # bpm stuff
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 3, 3)
    bpm_text = medium_font.render('Beats per minute', True, white)
    screen.blit(bpm_text, (305, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
    add_text = medium_font.render('+5', True, white)
    sub_text = medium_font.render('-5', True, white)
    screen.blit(add_text, (520, HEIGHT - 140))
    screen.blit(sub_text, (520, HEIGHT - 90))

    # beats stuff
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 200, 100], 3, 3)
    beats_text = medium_font.render('Beats in loop', True, white)
    screen.blit(beats_text, (615, HEIGHT - 130))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (680, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, white)
    sub_text2 = medium_font.render('-1', True, white)
    screen.blit(add_text2, (820, HEIGHT - 140))
    screen.blit(sub_text2, (820, HEIGHT - 90))

    # instruments rects
    instruments_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instruments_rects.append(rect)

    # Save and load stuff
    save_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 150, 200, 48], 0, 5)
    save_text = label_font.render('Save Beat', True, white)
    screen.blit(save_text, (920, HEIGHT - 140))
    load_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 100, 200, 48], 0, 5)
    load_text = label_font.render('Load Beat', True, white)
    screen.blit(load_text, (920, HEIGHT - 90))

    # Cler board
    clear_button = pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = label_font.render('Clear board', True, white)
    screen.blit(clear_text, (1160, HEIGHT - 120))
    
    if save_menu:
        exit_button = draw_save_menu()
    if load_menu:
        exit_button = draw_load_menu()


    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range (instruments)]
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True
            for i in range(len(instruments_rects)):
                if instruments_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True


    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats -1:
                active_beat += 1
                beat_changed = True
            else: 
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.QUIT