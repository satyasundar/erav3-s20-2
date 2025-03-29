# Self-Driving Car Simulation

A Kivy-based simulation environment for training a self-driving car using reinforcement learning. The project implements a Q-learning neural network that learns to navigate through a custom map while avoiding obstacles.

## Features

- Real-time simulation of a self-driving car
- Neural network-based reinforcement learning (Q-learning)
- Interactive environment with customizable maps
- Three sensors for obstacle detection
- Dynamic goal-based navigation system
- Drawing tools to create custom obstacles
- Save/Load functionality for trained models

## Requirements

- Python 3.x
- PyTorch
- Kivy
- NumPy
- Matplotlib
- PIL (Python Imaging Library)


## Project Structure

- `map.py` - Main simulation environment and game logic
- `ai.py` - Neural network architecture and Q-learning implementation
- `images/` - Contains map assets and masks
  - `car.png` - Car sprite
  - `mgroad_map_only_mask_base.png` - Base map mask
  - `mgroad_map_only_mask_hw.png` - Highway map mask

## Usage

1. Run the simulation:
```bash
python map.py
```

2. Controls:
- The car moves automatically based on the AI
- Use the mouse to draw obstacles (left click and drag)
- Clear button: Removes all drawn obstacles
- Save button: Saves the current state of the AI
- Load button: Loads the previously saved AI state

## How It Works

### Car Sensors
- The car has three sensors:
  - Front sensor (30° forward)
  - Right sensor (30° right)
  - Left sensor (30° left)

### Learning System
- Uses a Deep Q-Network (DQN) with:
  - 5 input neurons (3 sensors + 2 orientation values)
  - 3 possible actions (straight, right turn, left turn)
  - Reward system based on:
    - Negative reward for hitting obstacles
    - Positive reward for reaching goals
    - Small negative reward for regular movements

### Goals System
The car navigates between four predefined goals:
1. (504, 930)
2. (471, 50)
3. (1690, 550)
4. (2676, 380)

