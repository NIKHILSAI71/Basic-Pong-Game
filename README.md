# AI-Controlled Pong Game

An exciting AI vs AI Pong game built with Python (Flask + SocketIO) for the backend AI logic and HTML/CSS/JavaScript for the frontend UI.

## Features

- Two AI players competing against each other
- Real-time game updates via WebSocket
- Beautiful gradient UI with glowing effects
- Responsive design for different screen sizes
- 50 FPS smooth gameplay
- First to 5 points wins

## Project Structure

```
Basic-Pong-Game/
│
├── app.py              # Main Python server with AI logic
├── requirements.txt    # Python dependencies
├── README.md          # This file
│
├── templates/
│   └── index.html     # HTML template
│
└── static/
    └── style.css      # CSS styling
```

## Installation & Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python app.py
   ```

3. **Open your browser and go to:**
   ```
   http://127.0.0.1:5000
   ```

4. **Click "Start Game" to watch the AI players compete!**

## How It Works

### Backend (Python)
- **Flask**: Web server framework
- **Flask-SocketIO**: Real-time bidirectional communication
- **AI Logic**: Simple "follow the ball" algorithm with slight differences between left and right AI
- **Game Loop**: Runs at 50 FPS, updating ball physics and AI decisions

### Frontend (HTML/CSS/JavaScript)
- **Canvas**: Renders the game graphics
- **Socket.IO**: Receives real-time game state updates
- **Responsive Design**: Works on desktop and mobile devices

### AI Strategy
- **Left AI**: Slightly less responsive (80% speed) to create competitive gameplay
- **Right AI**: More responsive and accurate
- **Ball Physics**: Realistic collision detection with random variation after paddle hits

## Game Rules

- First player to reach 5 points wins
- Ball bounces off top and bottom walls
- Ball resets to center after each score
- AI paddles automatically track and hit the ball

## Customization

You can modify these constants in `app.py`:
- `PADDLE_SPEED`: How fast paddles move
- `BALL_SPEED_INITIAL`: Initial ball speed
- `GAME_WIDTH/HEIGHT`: Court dimensions
- Score limit (currently 5 points to win)

## Future Enhancements

- Sound effects
- Different AI difficulty levels  
- Machine learning-based AI players
- Tournament mode
- Particle effects
- Power-ups

Enjoy watching the AI battle it out in this classic game!
