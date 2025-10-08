# AI-Powered Othello Game: Neural Network & MCTS Implementation

An advanced Othello (Reversi) game implementation featuring neural network-enhanced Monte Carlo Tree Search (MCTS) agents capable of learning and playing at a competitive level.

## 🎯 Project Overview

This project combines classical AI search algorithms with modern deep learning techniques to create intelligent Othello players. The system features two types of AI agents: traditional MCTS and neural network-enhanced MCTS, allowing for sophisticated gameplay and learning capabilities.

## 🧠 Key Features

- **Neural Network Integration**: Custom CNN architecture for board position evaluation
- **Monte Carlo Tree Search**: Optimized MCTS implementation with neural network guidance
- **Interactive Gameplay**: Human vs AI and AI vs AI game modes
- **Real-time Visualization**: Pygame-based graphical interface
- **Training Data Generation**: Automated dataset creation from MCTS gameplay
- **Performance Analytics**: Comprehensive game statistics and visualizations

## 🏗️ Architecture

### Neural Network Design (My Contribution)
I was responsible for designing, implementing, and training the neural network component:

- **Custom CNN Architecture**: 3-layer convolutional network optimized for 8x8 board states
- **Dual-Channel Input**: Separate channels for black and white pieces representation
- **Advanced Training Pipeline**: Implemented with class weighting, early stopping, and learning rate scheduling
- **Data Preprocessing**: Channel-based encoding system for optimal neural network performance
- **Model Optimization**: Adam optimizer with cosine decay and regularization techniques

```python
# Neural Network Architecture
Input Layer: 8x8x2 (board state with separate channels)
Conv2D: 64 filters, 3x3 kernel, ReLU activation
Conv2D: 128 filters, 3x3 kernel, ReLU activation  
Conv2D: 128 filters, 3x3 kernel, ReLU activation
Dense: 256 neurons, ReLU activation, Dropout 0.5
Output: 1 neuron, Tanh activation (win probability)
```

### MCTS Integration
- Traditional MCTS implementation for baseline performance
- Neural network-enhanced MCTS for improved position evaluation
- Configurable simulation parameters and exploration strategies

## 🚀 Getting Started

### Prerequisites
```bash
pip install keras tensorflow numpy pandas matplotlib pygame
```

### Running the Game

**Human vs AI:**
```bash
python otelo.py
```

**AI vs AI Demo:**
```bash
python otelo_ia_vs_ia.py
```

## 📊 Training Process

The neural network training involves:

1. **Data Generation**: MCTS agents play thousands of games to generate training data
2. **Feature Engineering**: Board states converted to dual-channel representation
3. **Balanced Training**: Class weighting to handle imbalanced win/loss/draw outcomes
4. **Validation**: 10% validation split with early stopping to prevent overfitting
5. **Model Persistence**: Trained model saved as `othello_neuronal_entrenada.h5`

## 📁 Project Structure

```
otelo/
├── red_neuronal/           # Neural Network Implementation (My Work)
│   ├── othello_net.py     # NN architecture & training pipeline
│   └── othello_neuronal_entrenada.h5  # Trained model
├── mcts/                  # Monte Carlo Tree Search
│   ├── agente_mcts.py     # Traditional MCTS agent
│   ├── agente_mcts_red_neuronal.py  # NN-enhanced MCTS
│   ├── motor_mcts.py      # MCTS engine
│   └── motor_mcts_neuronal.py       # NN-integrated MCTS
├── utiles/                # Game utilities
│   ├── tablero.py         # Board representation
│   └── fichas.py          # Game logic
├── datos/                 # Training datasets
├── docs/                  # Documentation & analysis
└── otelo.py              # Main game interface
```

## 🔬 Technical Highlights

### Neural Network Innovation
- **Channel-based Encoding**: Revolutionary approach to represent game pieces as separate channels rather than integer values, preventing the network from learning incorrect piece hierarchies
- **Balanced Training**: Sophisticated class weighting system to handle the natural imbalance in game outcomes
- **Robust Architecture**: Careful balance of model complexity and regularization to prevent overfitting

### Performance Optimization
- **Efficient Data Pipeline**: Optimized numpy operations for fast batch processing
- **Memory Management**: Strategic use of data types (int32, float32) for optimal performance
- **Callback Integration**: Early stopping and learning rate reduction for optimal convergence

## 📈 Results

The trained neural network demonstrates:
- Significant improvement over random play
- Competitive performance against traditional MCTS
- Efficient learning from self-play data
- Robust evaluation of complex board positions

## 👥 Team Contributions

**Iván Fernández Limárquez (Me)**: Neural Network Architecture, Training Pipeline, Data Preprocessing, Model Optimization

**Eloy Sancho Cebrero**: MCTS Implementation, Game Logic, User Interface, Project Integration

## 📚 Documentation

Complete project documentation available in `docs/documentacion.pdf`

---

*This project showcases the successful integration of deep learning with traditional AI search algorithms, demonstrating how neural networks can enhance classical game-playing techniques.*
