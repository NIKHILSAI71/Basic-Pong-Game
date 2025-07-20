# Adaptive Pong Game

A simple, responsive Pong game built with Flask, Socket.IO, and HTML5 Canvas that adapts to any screen size.

## Features

- **Fully Responsive**: Adapts to any screen size from mobile phones to large desktops
- **Touch Support**: Touch controls for mobile devices
- **Real-time Gameplay**: Uses WebSockets for smooth, real-time gameplay
- **AI Opponent**: Simple AI that adapts to ball movement
- **Clean Design**: Minimalist black and white aesthetic
- **Cross-Platform**: Works on all modern browsers and devices

## Project Structure

```
Basic-Pong-Game/
│
├── app.py              # Flask server with game logic
├── requirements.txt    # Python dependencies
├── README.md          # This file
│
├── templates/
│   └── index.html     # HTML template with responsive canvas
│
└── static/
    └── style.css      # Responsive CSS styling
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

4. **Click "START GAME" to begin playing!**

## Controls

- **Desktop**: Use Arrow Keys (↑↓) or W/S keys to control the right paddle
- **Mobile**: Touch and drag on the game area to control the paddle
- **Start Game**: Click "START GAME" button

## Game Rules

- First player to reach 5 points wins
- Left paddle is controlled by AI
- Right paddle is controlled by the player
- Ball bounces off paddles and top/bottom walls
- Points scored when ball passes the opponent's paddle

## How It Works

### Backend (Python)
- **Flask**: Web server framework
- **Flask-SocketIO**: Real-time bidirectional communication with optimized timing
- **Game Logic**: Improved collision detection with proper ball-paddle interaction
- **Game Loop**: Optimized 60 FPS with delta timing to prevent lag
- **AI**: Simple but responsive AI that follows the ball

### Frontend (HTML/CSS/JavaScript)
- **Canvas**: Hardware-accelerated rendering with FPS throttling
- **Socket.IO**: Throttled real-time updates to prevent lag
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Performance**: Optimized drawing loop with requestAnimationFrame

### Key Features
- **Lag-Free**: Optimized game loop and rendering for smooth gameplay
- **Accurate Collision**: Improved ball-paddle collision detection
- **Creator Credit**: Attribution preserved as requested
- **Mobile Support**: Touch controls with proper throttling

## Technical Improvements Made

- Fixed ball-paddle collision detection with proper hit zones
- Added FPS throttling to prevent lag on slower devices
- Optimized Socket.IO communication with update limiting
- Improved AI responsiveness and accuracy
- Added proper creator attribution
- Enhanced mobile touch controls with better sensitivity

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
