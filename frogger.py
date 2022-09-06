import pgzrun
from pgzero.builtins import Actor, keys, sounds, clock, music #, screen
from random import randint

# PGZero Window settings.
WIDTH = 800
HEIGHT = 600
TITLE = "Frogger"
ICON = "images/frog-1.png"

game_music = "jump-8bit"
frog = Actor("frog-1")
cars = []

game_state = "intro"
mute_music = False
seconds = 0
jumps = 0
frog.x = WIDTH / 2
frog.y = HEIGHT - 35
movex = 0
movey = 0
move_count = 0
move_delay = 0
jumping = False
car_speed = 2


def setup_cars():
    global cars
    cars = []
    for lane in range(0, 5):
        for traffic in range(0, 3):
            car = Actor("car" + str(randint(1, 5)))
            car.pos = (266 * traffic) + randint(80, 186), 70 * lane + 215
            if (lane % 2) == 0:
                car.angle = 180
            cars.append(car)

setup_cars()

def update_cars():
    for car in cars:
        if car.y == 285 or car.y == 425:
            car.x += car_speed
            if car.x > WIDTH + 80:
                car.x -= WIDTH + 160
        else:
            car.x -= car_speed
            if car.x + 80 < 0:
                car.x += WIDTH + 160


def set_move(direction):
    global movex, movey, jumping, move_count, move_delay, jumps
    jumping = True
    move_count = 0
    move_delay = 0
    movex = 0
    movey = 0
    jumps += 1
    sounds.super.play()
    if direction == "up":
        frog.angle = 0
        movey = -17.5
    elif direction == "down":
        frog.angle = 180
        movey = 17.5
    elif direction == "left":
            frog.angle = 90
            movex = -17.5
    elif direction == "right":
            frog.angle = 270
            movex = 17.5


def update_move():
    global move_count, jumping, movex, movey, move_delay, game_state
    if jumping:
        move_delay += 1
        if move_delay > 2:
            move_delay = 0
            move_count += 1
            frog.x += movex
            frog.y += movey
            angle = frog.angle
            if move_count == 1:
                frog.image = "frog-2"
            elif move_count == 2:
                frog.image = "frog-3"
            elif move_count == 3:
                frog.image = "frog-2"
            elif move_count > 3:
                frog.image = "frog-1"
                jumping = False
                if frog.y == 145:
                    clock.unschedule(update_seconds)
                    game_state = "win"
                    music.pause()
                    sounds.win.play()
                    clock.schedule_unique(game_reset, 15.0)
            frog.angle = angle


def update_seconds():
    global seconds
    seconds += 1


def game_reset():
    global jumping, jumps, seconds, game_state
    clock.unschedule(game_reset)
    game_state = "intro"
    frog.x = WIDTH / 2
    frog.y = HEIGHT - 35
    frog.image = ("frog-1")
    jumping = False
    jumps = 0
    seconds = 0
    setup_cars()
    if not mute_music:
        music.unpause()


def on_key_down(key):
    global game_state, jumping, mute_music, jumps, seconds
    if key == keys.ESCAPE:
        exit()
    if key == keys.M:
        if music.is_playing(game_music):
            music.pause()
            mute_music = True
        else:
            music.unpause()
            mute_music = False
    if game_state == "play":
        if not jumping:
            if key == keys.UP or key == keys.W:
                if frog.y > 145:
                    set_move("up")
            elif key == keys.DOWN or key == keys.S:
                if frog.y < HEIGHT - 35:
                    set_move("down")
            elif key == keys.LEFT or key == keys.A:
                if frog.x > 50:
                    set_move("left")
            elif key == keys.RIGHT or key == keys.D:
                if frog.x < WIDTH - 50:
                    set_move("right")
    else:
        if key == keys.SPACE:
            game_reset()
            game_state = "play"
            clock.schedule_interval(update_seconds, 1.0)
    

def check_collide():
    global game_state
    for car in cars:
        if frog.colliderect(car):
            clock.unschedule(update_seconds)
            game_state = "over"
            music.pause()
            sounds.over.play()
            clock.schedule_unique(game_reset, 15.0)


def update():
    if not game_state == "over":
        update_cars()
    if game_state == "play":
        update_move()
        check_collide()        


def draw():
    screen.blit("background", (0, 0))
    screen.draw.text("Jumps: " + str(jumps), midleft=(20, 53), color="white", fontsize=50)
    screen.draw.text("Frogger", center=(WIDTH / 2, 53), owidth=1.5, ocolor="green", color="black", fontsize=100)
    screen.draw.text("Seconds: " + str(seconds), midright=(WIDTH - 20, 53), color="white", fontsize=50)

    for car in cars:
        car.draw()
    frog.draw()

    if game_state == "over":
        screen.draw.text("Game Over :-(", center=(WIDTH / 2, HEIGHT / 2), owidth=1.5, ocolor="green", color="black", fontsize=150)
    elif game_state == "win":
        screen.draw.text("Winner :-)", center=(WIDTH / 2, HEIGHT / 2), owidth=1.5, ocolor="green", color="black", fontsize=150)
    if not game_state == "play":
        screen.draw.text("Press SPACE", center=(WIDTH / 2, HEIGHT * 0.75), owidth=1.5, ocolor="white", color="black", fontsize=100)


music.play(game_music)

pgzrun.go()