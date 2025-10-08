# AI-Powered Othello Game: Neural Network & MCTS Implementation

An  Othello (Reversi) game implementation featuring neural network-enhanced Monte Carlo Tree Search (MCTS) agents capable of learning and playing at a competitive level.

##  Project Overview

This project combines classical AI search algorithms with modern deep learning techniques to create intelligent Othello players. The system features two types of AI agents: traditional MCTS and neural network-enhanced MCTS, allowing for sophisticated gameplay and learning capabilities.

### Neural Network Design (My Contribution)
I was responsible for designing, implementing, and training the neural network component:

- **Custom CNN Architecture**: 3-layer convolutional network optimized for 8x8 board states
- **Dual-Channel Input**: Separate channels for black and white pieces representation
- **Advanced Training Pipeline**: Implemented with class weighting, early stopping, and learning rate scheduling
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

The trained neural network demonstrates:
- Significant improvement over random play
- Competitive performance against traditional MCTS
- Efficient learning from self-play data
- Robust evaluation of complex board positions

## 👥 Team Contributions

**Iván Fernández Limárquez (Me)**: Neural Network Architecture, Training Pipeline, Data Preprocessing, Model Optimization, Game Logic, User Interface

**Eloy Sancho Cebrero**: MCTS Implementation, Game Logic, User Interface, Project Integration

## 📚 Documentation

Complete project documentation available in `docs/documentacion.pdf`

---

*This project showcases the successful integration of deep learning with traditional AI search algorithms, demonstrating how neural networks can enhance classical game-playing techniques.*
