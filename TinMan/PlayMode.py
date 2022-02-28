from enum import Enum
class PlayMode(Enum):
    unknown = -1
    before_kick_off = 0
    kick_off_left = 1
    kick_off_right = 2
    play_on = 3
    kick_in_left = 4
    kick_in_right = 5
    corner_kick_left = 6
    corner_kick_right = 7
    goal_kick_left = 8
    goal_kick_right = 9
    offside_left = 10
    offside_right = 11
    game_over = 12
    goal_left = 13
    goal_right = 14
    free_kick_left = 15
    free_kick_right = 16
    none = 17

class PlayModeUtil1:
    _play_mode_by_string_code = {'before_kick_off': PlayMode.before_kick_off,
        'kick_off_left': PlayMode.kick_off_left, 'kick_off_right': PlayMode.kick_off_right,
        'play_on': PlayMode.play_on, 'kick_in_left': PlayMode.kick_in_left, 'kick_in_right': PlayMode.kick_in_right,
        'corner_kick_left' : PlayMode.corner_kick_left, 'corner_kick_right': PlayMode.corner_kick_right,
        'goal_kick_left': PlayMode.goal_kick_left, 'goal_kick_right': PlayMode.goal_kick_right,
        'offside_left': PlayMode.offside_left, 'offside_right': PlayMode.offside_right,
        'game_over': PlayMode.game_over, 'goal_left': PlayMode.goal_left, 'goal_right': PlayMode.goal_kick_right,
        'free_kick_left': PlayMode.free_kick_left, 'free_kick_right': PlayMode.free_kick_right,
        'unknown': PlayMode.none}

    _string_code_by_play_mode = {{'before_kick_off': PlayMode.before_kick_off,
        'kick_off_left': PlayMode.kick_off_left, 'kick_off_right': PlayMode.kick_off_right,
        'play_on': PlayMode.play_on, 'kick_in_left': PlayMode.kick_in_left, 'kick_in_right': PlayMode.kick_in_right,
        'corner_kick_left' : PlayMode.corner_kick_left, 'corner_kick_right': PlayMode.corner_kick_right,
        'goal_kick_left': PlayMode.goal_kick_left, 'goal_kick_right': PlayMode.goal_kick_right,
        'offside_left': PlayMode.offside_left, 'offside_right': PlayMode.offside_right,
        'game_over': PlayMode.game_over, 'goal_left': PlayMode.goal_left, 'goal_right': PlayMode.goal_kick_right,
        'free_kick_left': PlayMode.free_kick_left, 'free_kick_right': PlayMode.free_kick_right,
        'unknown': PlayMode.none}[i]:i for i in {'before_kick_off': PlayMode.before_kick_off,
        'kick_off_left': PlayMode.kick_off_left, 'kick_off_right': PlayMode.kick_off_right,
        'play_on': PlayMode.play_on, 'kick_in_left': PlayMode.kick_in_left, 'kick_in_right': PlayMode.kick_in_right,
        'corner_kick_left' : PlayMode.corner_kick_left, 'corner_kick_right': PlayMode.corner_kick_right,
        'goal_kick_left': PlayMode.goal_kick_left, 'goal_kick_right': PlayMode.goal_kick_right,
        'offside_left': PlayMode.offside_left, 'offside_right': PlayMode.offside_right,
        'game_over': PlayMode.game_over, 'goal_left': PlayMode.goal_left, 'goal_right': PlayMode.goal_kick_right,
        'free_kick_left': PlayMode.free_kick_left, 'free_kick_right': PlayMode.free_kick_right,
        'unknown': PlayMode.none}}

    def try_parse(mode_str):
        if mode_str in PlayModeUtil1._play_mode_by_string_code:
            return PlayModeUtil1._play_mode_by_string_code[mode_str]
        return None
    
    def get_server_string(play_mode):
        try:
            string = PlayModeUtil1._string_code_by_play_mode[play_mode]
        except KeyError:
            raise(BaseException('Unexpected PlayMode enum value: ' + play_mode))
        return string
        




