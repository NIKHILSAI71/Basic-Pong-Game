import math
import random
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pong_game_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Game Constants
GAME_WIDTH = 1200
GAME_HEIGHT = 700
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
PADDLE_SPEED = 8
BALL_SPEED_INITIAL = 6

# Game State
game_state = {
    'ball': {'x': GAME_WIDTH / 2, 'y': GAME_HEIGHT / 2, 'dx': BALL_SPEED_INITIAL, 'dy': BALL_SPEED_INITIAL},
    'player_paddle': {'y': GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2},
    'ai_paddle': {'y': GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2},
    'player_score': 0,
    'ai_score': 0,
    'game_started': False,
    'game_over': False
}

def reset_ball():
    game_state['ball']['x'] = GAME_WIDTH / 2
    game_state['ball']['y'] = GAME_HEIGHT / 2
    game_state['ball']['dx'] = BALL_SPEED_INITIAL * (1 if random.random() > 0.5 else -1)
    game_state['ball']['dy'] = BALL_SPEED_INITIAL * (1 if random.random() > 0.5 else -1)

def update_game_state():
    if not game_state['game_started'] or game_state['game_over']:
        return

    # Move Ball
    game_state['ball']['x'] += game_state['ball']['dx']
    game_state['ball']['y'] += game_state['ball']['dy']

    # Ball collision with top/bottom walls
    if game_state['ball']['y'] - BALL_RADIUS <= 0:
        game_state['ball']['y'] = BALL_RADIUS
        game_state['ball']['dy'] *= -1
    elif game_state['ball']['y'] + BALL_RADIUS >= GAME_HEIGHT:
        game_state['ball']['y'] = GAME_HEIGHT - BALL_RADIUS
        game_state['ball']['dy'] *= -1

    # Ball collision with paddles
    # AI Paddle (right)
    if (game_state['ball']['x'] + BALL_RADIUS >= GAME_WIDTH - PADDLE_WIDTH and
            game_state['ball']['dx'] > 0 and
            game_state['ball']['y'] >= game_state['ai_paddle']['y'] and
            game_state['ball']['y'] <= game_state['ai_paddle']['y'] + PADDLE_HEIGHT):
        game_state['ball']['x'] = GAME_WIDTH - PADDLE_WIDTH - BALL_RADIUS
        game_state['ball']['dx'] *= -1.05  # Slightly increase speed
        # Add spin based on where ball hits paddle
        hit_pos = (game_state['ball']['y'] - game_state['ai_paddle']['y']) / PADDLE_HEIGHT - 0.5
        game_state['ball']['dy'] += hit_pos * 2

    # Player Paddle (left - AI controlled)
    if (game_state['ball']['x'] - BALL_RADIUS <= PADDLE_WIDTH and
            game_state['ball']['dx'] < 0 and
            game_state['ball']['y'] >= game_state['player_paddle']['y'] and
            game_state['ball']['y'] <= game_state['player_paddle']['y'] + PADDLE_HEIGHT):
        game_state['ball']['x'] = PADDLE_WIDTH + BALL_RADIUS
        game_state['ball']['dx'] *= -1.05  # Slightly increase speed
        # Add spin based on where ball hits paddle
        hit_pos = (game_state['ball']['y'] - game_state['player_paddle']['y']) / PADDLE_HEIGHT - 0.5
        game_state['ball']['dy'] += hit_pos * 2

    # Score points
    if game_state['ball']['x'] < 0:
        game_state['ai_score'] += 1
        reset_ball()
    elif game_state['ball']['x'] > GAME_WIDTH:
        game_state['player_score'] += 1
        reset_ball()

    # Simple AI Logic to follow the ball
    # Left Paddle
    if game_state['player_paddle']['y'] + PADDLE_HEIGHT / 2 < game_state['ball']['y']:
        game_state['player_paddle']['y'] += PADDLE_SPEED
    elif game_state['player_paddle']['y'] + PADDLE_HEIGHT / 2 > game_state['ball']['y']:
        game_state['player_paddle']['y'] -= PADDLE_SPEED

    # Right Paddle
    if game_state['ai_paddle']['y'] + PADDLE_HEIGHT / 2 < game_state['ball']['y']:
        game_state['ai_paddle']['y'] += PADDLE_SPEED
    elif game_state['ai_paddle']['y'] + PADDLE_HEIGHT / 2 > game_state['ball']['y']:
        game_state['ai_paddle']['y'] -= PADDLE_SPEED

    # Keep paddles on screen
    game_state['player_paddle']['y'] = max(0, min(game_state['player_paddle']['y'], GAME_HEIGHT - PADDLE_HEIGHT))
    game_state['ai_paddle']['y'] = max(0, min(game_state['ai_paddle']['y'], GAME_HEIGHT - PADDLE_HEIGHT))

    # Check for game over (first to 5 points)
    if game_state['player_score'] >= 5 or game_state['ai_score'] >= 5:
        game_state['game_over'] = True
        game_state['game_started'] = False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('game_state', game_state)

@socketio.on('start_game')
def start_game():
    if not game_state['game_started']:
        game_state['game_started'] = True
        game_state['game_over'] = False
        game_state['player_score'] = 0
        game_state['ai_score'] = 0
        reset_ball()
        
        print("Game started with simple AI!")
        socketio.start_background_task(target=game_loop)

def game_loop():
    while game_state['game_started']:
        update_game_state()
        socketio.emit('game_state', game_state)
        socketio.sleep(0.016)  # Update every 16ms (60 FPS)

if __name__ == '__main__':
    print("Starting Simple AI Pong Game...")
    print("AI will try to follow the ball")
    print("Open your browser and go to: http://127.0.0.1:5000")
    socketio.run(app, debug=True, port=5000)
