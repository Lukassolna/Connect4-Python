# Evaluating AI Performance and Adaptability in Connect-4
This project implements and compares different AI approaches for playing Connect-4

• Minimax with alpha-beta pruning

• Reinforcement learning, specifically Q-learning with an epsilon-greedy exploration strategy
## Features
- Multiple AI Agents:
  - Q-learning agent with reinforcement learning
  - Minimax agent with alpha-beta pruning (configurable depth)
  - Random agent (baseline)
  - Player agent (human interaction)
- Configurable game environments:
  - Adjustable board sizes
  - Variable winning conditions (Connect-3, Connect-4, Connect-5)

## Bonus Feature
- Combining Q-learning and Minimax: Agent consults Minimax algorithm for unknown game states
- Best of both worlds
- Faster learning
- Instant results
## Installation
```bash
git clone https://github.com/Lukassolna/Connect4-Python.git
cd Connect4-Python
```
## Usage
Run the main program:
```bash
python main.py
```
### Modifying Game Parameters
In `main.py`, you can adjust:
- Board dimensions (ROW_COUNT, COLUMN_COUNT)
- Win condition (WIN_COUNT)
- Agent matchups
### Example: Playing Against AI
To play against a Minimax agent with depth 4:
```python
start_game(user, mini4, True)  # Human vs Minimax depth 4
```
### Training Q-Learning Agent
To train the Q-learning agent, use the `qlrn.train` method ( Takes a long time, beware)
## Performance
- Minimax agent performs consistently well, especially at higher depths
  
- Q-learning agent achievements:
  - 91.2% win rate vs random agent after 1M games
  - 100% win ratio vs minimax depth 3 after 1M games
  - Can adapt to different board sizes and win conditions
  - Shows improved performance with Minimax helper feature
## Credits
Special thanks to:
- Keith Galli (Game environment and initial alpha-beta pruning implementation)
- Simplilearn Team (Q-learning walkthrough and learning material)
