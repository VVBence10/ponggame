import sys, pygame, random

# general setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# main window
screen_width = 960
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# colors
bg_color = pygame.Color("grey12")
light_grey = pygame.Color(200, 200, 200)
lighter_grey = pygame.Color(240, 240, 240)

# game rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 44, 10, 88)
opponent = pygame.Rect(10, screen_height / 2 - 44, 10, 88)

# game variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 0
level = 0
players = None
start1 = False
start2 = False
score_time = None
player_score = 0
opponent_score = 0
current_time = 0
number_two = None
number_one = None
number_three = None

# text variables
game_font = pygame.font.Font("freesansbold.ttf", 30)

# sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")


# functions
def ball_animation():
    global ball_speed_x, ball_speed_y, opponent_score, player_score, score_time
    # move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height or ball.top <= 0:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1


def player_animation():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height
    player.y += player_speed


def opponent_animation():
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height
    opponent.y += opponent_speed


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed

    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0

    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_start():
    global ball_speed_x, ball_speed_y, current_time, level, score_time, number_two, number_one, number_three

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    if current_time - score_time < 300:
        number_three = game_font.render("3", False, lighter_grey)
        screen.blit(number_three, (screen_width / 2 - 8, screen_height / 2 + 20))
    if 300 < current_time - score_time < 600:
        number_two = game_font.render("2", False, lighter_grey)
        screen.blit(number_two, (screen_width / 2 - 8, screen_height / 2 + 20))
    if 600 < current_time - score_time < 900:
        number_one = game_font.render("1", False, lighter_grey)
        screen.blit(number_one, (screen_width / 2 - 8, screen_height / 2 + 20))
    if current_time - score_time < 900:
        ball_speed_x = 0
        ball_speed_y = 0
    else:
        if level == 1:
            ball_speed_y = 7 * random.choice((1, -1))
            ball_speed_x = 7 * random.choice((1, -1))
            score_time = None
        elif level == 2:
            ball_speed_y = 9 * random.choice((1, -1))
            ball_speed_x = 11 * random.choice((1, -1))
            score_time = None
        elif level == 3:
            ball_speed_y = 12 * random.choice((1, -1))
            ball_speed_x = 14 * random.choice((1, -1))
            score_time = None


def get_level():
    global start1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_1:
                return 1
            if event.key == pygame.K_2:
                return 2
            if event.key == pygame.K_3:
                return 3


def set_level(n):
    global player_speed, opponent_speed, level, score_time, start1

    screen.fill(bg_color)
    level_text = game_font.render(
        "Choose a level on your keyboard (1, 2 or 3)", False, light_grey
    )
    screen.blit(level_text, (175, screen_height / 2))

    level = n
    if level == 1:
        player_speed = 0
        opponent_speed = 7
        start1 = True

    elif level == 2:
        player_speed = 0
        opponent_speed = 12
        start1 = True

    elif level == 3:
        player_speed = 0
        opponent_speed = 13
        start1 = True


def get_players():
    global players, start2, score_time, player_speed, opponent_speed

    screen.fill(bg_color)
    start_text = game_font.render(
        "Type in how many players there are (1 or 2)", False, light_grey
    )
    screen.blit(start_text, (175, screen_height / 2))

    players = None
    score_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_1:
                players = 1
                start2 = True
                ball_start()
            if event.key == pygame.K_2:
                players = 2
                start2 = True
                player_speed = 0
                opponent_speed = 0
                ball_start()


def main():
    global start1, start2, score_time, player_score, opponent_score, player_speed, opponent_speed

    while True:
        if start1 == True and start2 == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_DOWN:
                        player_speed += 7
                    if event.key == pygame.K_UP:
                        player_speed -= 7
                    if event.key == pygame.K_s and players == 2:
                        opponent_speed += 7
                    if event.key == pygame.K_w and players == 2:
                        opponent_speed -= 7
                    if event.key == pygame.K_r:
                        opponent_score = 0
                        player_score = 0
                        score_time = pygame.time.get_ticks()
                        start1 = False
                        start2 = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        player_speed -= 7
                    if event.key == pygame.K_UP:
                        player_speed += 7
                    if event.key == pygame.K_s and players == 2:
                        opponent_speed -= 7
                    if event.key == pygame.K_w and players == 2:
                        opponent_speed += 7

            # game logics
            ball_animation()
            player_animation()
            if players == 1:
                opponent_ai()
            elif players == 2:
                opponent_animation()

            # visuals
            screen.fill(bg_color)
            pygame.draw.ellipse(screen, light_grey, ball)
            pygame.draw.rect(screen, light_grey, player)
            pygame.draw.rect(screen, light_grey, opponent)
            pygame.draw.aaline(
                screen,
                light_grey,
                (screen_width / 2, 0),
                (screen_width / 2, screen_height),
            )

            if score_time:
                ball_start()

            player_text = game_font.render(f"{player_score}", False, light_grey)
            opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
            screen.blit(player_text, (500, 20))

            if opponent_score < 10:
                screen.blit(opponent_text, (445, 20))
            else:
                screen.blit(opponent_text, (425, 20))

        # level choosing
        elif start1 == False and start2 == False:
            set_level(get_level())

        elif start1 == True and start2 == False:
            get_players()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
