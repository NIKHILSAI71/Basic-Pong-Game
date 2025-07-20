from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pong_game_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Game state - clean and simple percentage-based coordinates
game_state = {
    'ball': {'x': 50, 'y': 50, 'dx': 0.8, 'dy': 0.5},
    'left_paddle': {'y': 42.5, 'target_y': 42.5},
    'right_paddle': {'y': 42.5, 'target_y': 42.5},
    'left_score': 0,
    'right_score': 0,
    'game_started': False,
    'game_over': False,
    'paddle_speed': 2.0,
    'ball_base_speed': 0.8,
    'rally_count': 0,
    'paddle_smoothing': 0.2
}

def reset_ball():
    """Reset ball to center with random direction"""
    game_state['ball']['x'] = 50
    game_state['ball']['y'] = 50 + random.uniform(-10, 10)  # Add slight vertical randomness
    game_state['rally_count'] = 0
    
    # Set ball direction and speed
    direction_x = 1 if random.random() > 0.5 else -1
    direction_y = random.uniform(-0.5, 0.5)
    
    game_state['ball']['dx'] = game_state['ball_base_speed'] * direction_x
    game_state['ball']['dy'] = direction_y

def update_game():
    """Clean game update logic with proper physics"""
    if not game_state['game_started'] or game_state['game_over']:
        return

    # Smooth paddle interpolation
    smoothing = game_state['paddle_smoothing']
    game_state['left_paddle']['y'] += (game_state['left_paddle']['target_y'] - game_state['left_paddle']['y']) * smoothing
    game_state['right_paddle']['y'] += (game_state['right_paddle']['target_y'] - game_state['right_paddle']['y']) * smoothing

    # Move ball
    game_state['ball']['x'] += game_state['ball']['dx']
    game_state['ball']['y'] += game_state['ball']['dy']

    # Ball collision with top/bottom walls
    if game_state['ball']['y'] <= 0 or game_state['ball']['y'] >= 100:
        game_state['ball']['dy'] = -game_state['ball']['dy']
        game_state['ball']['y'] = max(0, min(100, game_state['ball']['y']))

    # Paddle dimensions
    paddle_width = 2
    paddle_height = 15
    ball_x, ball_y = game_state['ball']['x'], game_state['ball']['y']
    
    # Left paddle collision (AI)
    if (ball_x <= paddle_width and game_state['ball']['dx'] < 0 and
        ball_y >= game_state['left_paddle']['y'] and 
        ball_y <= game_state['left_paddle']['y'] + paddle_height):
        
        game_state['rally_count'] += 1
        
        # Simple speed increase (max 1.5x)
        speed_mult = min(1.0 + (game_state['rally_count'] * 0.03), 1.5)
        
        # Reverse and increase speed
        game_state['ball']['dx'] = game_state['ball_base_speed'] * speed_mult
        game_state['ball']['x'] = paddle_width + 0.1  # Push ball away
        
        # Add spin based on where ball hits paddle
        hit_pos = (ball_y - game_state['left_paddle']['y']) / paddle_height - 0.5
        game_state['ball']['dy'] += hit_pos * 0.3

    # Right paddle collision (Player)
    elif (ball_x >= 100 - paddle_width and game_state['ball']['dx'] > 0 and
          ball_y >= game_state['right_paddle']['y'] and 
          ball_y <= game_state['right_paddle']['y'] + paddle_height):
        
        game_state['rally_count'] += 1
        
        # Simple speed increase (max 1.5x)
        speed_mult = min(1.0 + (game_state['rally_count'] * 0.03), 1.5)
        
        # Reverse and increase speed
        game_state['ball']['dx'] = -game_state['ball_base_speed'] * speed_mult
        game_state['ball']['x'] = 100 - paddle_width - 0.1  # Push ball away
        
        # Add spin based on where ball hits paddle
        hit_pos = (ball_y - game_state['right_paddle']['y']) / paddle_height - 0.5
        game_state['ball']['dy'] += hit_pos * 0.3

    # Limit vertical speed
    if abs(game_state['ball']['dy']) > 1.2:
        game_state['ball']['dy'] = 1.2 if game_state['ball']['dy'] > 0 else -1.2

    # Scoring
    if ball_x < -1:
        game_state['right_score'] += 1
        reset_ball()
    elif ball_x > 101:
        game_state['left_score'] += 1
        reset_ball()

    # AI paddle movement
    paddle_center = game_state['left_paddle']['y'] + paddle_height/2
    ball_target = ball_y + (game_state['ball']['dy'] * 10)  # Predict ball position
    
    if paddle_center < ball_target - 1:
        game_state['left_paddle']['target_y'] = min(85, game_state['left_paddle']['target_y'] + 1.5)
    elif paddle_center > ball_target + 1:
        game_state['left_paddle']['target_y'] = max(0, game_state['left_paddle']['target_y'] - 1.5)

    # Win condition
    if game_state['left_score'] >= 5 or game_state['right_score'] >= 5:
        game_state['game_over'] = True
        game_state['game_started'] = False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    emit('game_state', game_state)

@socketio.on('start_game')
def start_game():
    game_state['game_started'] = True
    game_state['game_over'] = False
    game_state['left_score'] = 0
    game_state['right_score'] = 0
    game_state['left_paddle']['y'] = 42.5
    game_state['right_paddle']['y'] = 42.5
    game_state['left_paddle']['target_y'] = 42.5
    game_state['right_paddle']['target_y'] = 42.5
    reset_ball()
    socketio.start_background_task(target=game_loop)

@socketio.on('move_paddle')
def move_paddle(data):
    """Handle player paddle movement"""
    if data['direction'] == 'up':
        game_state['right_paddle']['target_y'] = max(0, game_state['right_paddle']['target_y'] - game_state['paddle_speed'])
    elif data['direction'] == 'down':
        game_state['right_paddle']['target_y'] = min(85, game_state['right_paddle']['target_y'] + game_state['paddle_speed'])

def game_loop():
    """Main game loop - 60 FPS"""
    import time
    frame_time = 1.0 / 60
    last_time = time.time()
    
    while game_state['game_started']:
        current_time = time.time()
        if current_time - last_time >= frame_time:
            update_game()
            socketio.emit('game_state', game_state)
            last_time = current_time
        socketio.sleep(0.01)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
