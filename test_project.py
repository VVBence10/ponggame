import pygame
from unittest import TestCase
import unittest
import project


class TestPongGame(TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.NOFRAME)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        project.ball_speed_x = 0
        project.ball_speed_y = 0
        project.player_speed = 0
        project.opponent_speed = 0
        project.level = 0
        project.players = None
        project.start1 = False
        project.start2 = False
        project.score_time = None
        project.player_score = 0
        project.opponent_score = 0
        project.current_time = 0
        project.number_two = None
        project.number_one = None
        project.number_three = None

    def test_ball_animation(self):
        project.ball_speed_y = -5
        project.ball.y = 50
        project.ball_animation()
        self.assertEqual(project.ball.y, 45)

        project.ball.y = 0
        project.ball_animation()
        self.assertEqual(project.ball_speed_y, 5)

    def test_player_animation(self):
        project.player_speed = -7
        project.player.y = 100
        project.player_animation()
        self.assertEqual(project.player.y, 93)

        project.player.y = 0
        project.player_animation()
        self.assertEqual(project.player.y, -7)

    def test_opponent_ai(self):
        project.ball.y = 50
        project.opponent.y = 100
        project.opponent_speed = 7
        project.opponent_ai()
        self.assertEqual(project.opponent.y, 93)

        project.ball.y = 200
        project.opponent.y = 100
        project.opponent_ai()
        self.assertEqual(project.opponent.y, 107)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    unittest.main()
