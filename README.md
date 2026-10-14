# Genius Arcade

> **An educational arcade game combining kinematic projectile physics, reactive obstacle evasion, and rapid mental math agility.**

---

##  Purpose & The OOP Journey

> *"I built Genius Arcade as an intensive, ground-up deep dive to master Object-Oriented Programming (OOP) in Python, state management and real-time software architecture and also to have an insight on how production grade softwares are written."*

Rather than following a surface-level tutorial, this project was designed from scratch to put core computer science and OOP design patterns into practical, working software:

* **Encapsulation & Single Responsibility:** Every domain in the game lives in its own dedicated, decoupled class ranging from kinematic sprites (`Ball`, `Barrier`, `Spike`) to persistence (`DataManager`) and audio (`SoundManager`).
* **Inheritance & Polymorphism:** Extending Pygame's `Sprite` hierarchy to manage lifecycles, group collision matrices, and clean updates.
* **Component-Based UI Architecture:** Building reusable GUI widgets (`MenuPanel`, `MenuBar`, `FormField`) with dynamic alignment, text rendering, and event handlers rather than hardcoded UI coordinates.
* **The State Pattern (Finite State Machine):** Eliminating spaghetti flags by decomposing 8 distinct game screens (`login`, `create`, `reset`, `welcome`, `menu`, `playing`, `pause`, `game_over`) into isolated state drawers and event listeners.
* **Defensive Engineering & Persistence:** Architecting a 4-guard validation ladder and 3-phase password recovery system backed by clean JSON serialization.

---

## 📖 Overview & Gameplay

**Genius Arcade** is a fast-paced arcade game where players solve arithmetic equations under pressure to survive bouncing balls and moving spikes.

To pop balls and survive, players must solve procedurally generated math puzzles under intense time pressure while managing player health, moving obstacles, and dynamic difficulty scaling.

### Core Mechanics
- **Two-Stage Kinematics & Ball Trapping:** Balls enter via horizontal burst acceleration ($a_x$) before transitioning into gravitational freefall ($a_y$) upon hitting the boundary. Ricochets are governed by kinematic impulse velocities ($v_y = \sqrt{2 \cdot a_y \cdot h}$) and a horizontally oscillating barrier that traps balls in play.
* **Procedural Hazard Chains:** Moving spikes cycle continuously across the bottom frame. If a ball or barrier strikes a spike, damage occurs.
* **Heart & Damage System:** Players start with 3 hearts. Losing a ball or having the barrier strike a spike deducts health. Reaching 0 hearts triggers Game Over.
* **Dynamic Math Engine:** Dynamically generates arithmetic equations at the bottom bar. Submitting correct answers pops trapped balls and awards points ($+50\text{ pts}$).
* **Difficulty Scaling:**
  * **Easy:** Low bar velocity, 3 balls.
  * **Medium:** Faster barrier oscillation, increased ball density.
  * **Hard:** High-speed barriers and dense ball counts requiring rapid cognitive response.

---

## 🏛️ Project Architecture
```
Genius-Arcade/
├── main.py              # Central engine, state dispatcher, and game loop
├── settings.py          # Global constants, colors, timing, and physics scales
├── game_stats.py        # Score tracking and persistent record synchronizer
├── data_manager.py      # Secure credential store and multi-tier high scores
├── sound_manager.py     # Event-driven audio player and volume mixer
├── generate_sounds.py   # Procedural mathematical 16-bit PCM audio synthesizer
├── ball.py              # Sprite kinematics, impulses, and boundary snapping
├── barrier.py           # Oscillating platform physics and boundary updates
├── spike.py             # Hazard sprite generation and procedural chaining
├── questions.py         # Arithmetic equation and answer generator
├── input_block.py       # Dynamic user input box and text renderer
├── form_field.py        # Reusable UI text input component with cursor logic
├── menu_panel.py        # Universal dialog card, button, and typography renderer
├── menu_bar.py          # Docked HUD elements and right-aligned buttons
├── heart.py             # Player life-gauge sprite renderer
└── user_data.json       # Local JSON persistence store
```

---

### Key Technical Highlights
1. **Freeze-Frame Veil (`screen_veil`):** Captures live display snapshots, downsamples by $10\times$, upscales via bilinear interpolation (`smoothscale`), and applies a $60\%$ dark alpha overlay (`(0, 0, 0, 160)`) to render modern blurred pause and dialog backdrops.
2. **Adaptive Welcome Dashboard:** Evaluates user play history on login—presenting a **"HOW TO PLAY"** tutorial card for first-time players, and a 3-column personal records dashboard for returning players.
3. **Procedural 16-Bit Audio Engine:** [`generate_sounds.py`](generate_sounds.py) programmatically synthesizes standard 16-bit PCM Mono `.wav` files using Python's built-in `wave`, `math`, and `struct` modules.

---

## ⌨️ Controls Reference

| Action | Input | Available State |
| :--- | :--- | :--- |
| **Type Numbers / Answers** | `0` – `9` | Playing, Forms |
| **Submit Answer / Confirm** | `ENTER` / `KP_ENTER` | Playing, Forms, Welcome |
| **Backspace / Delete** | `BACKSPACE` | Playing, Forms |
| **Pause Game** | `ESC` or Click **Pause** | Playing |
| **Resume Game** | `ESC` or Click **Resume** | Pause |
| **Emergency Quit** | `Q` | Any State |
| **UI Navigation** | `Left Mouse Click` | Menus, Dialogs |

---

## Installation & Quickstart

### Prerequisites
* Python 3.10+ (Tested on Python 3.12)
* `pygame` (v2.5.0+)

### Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Mechluid/Genius-Arcade.git](https://github.com/Mechluid/Genius-Arcade.git)
   cd Genius-Arcade

2. **Install dependencies:**
   ```bash
   pip install pygame
   ```

3. **Launch the game:**
   ```bash
   python main.py
   ```

*(Optional) Regenerate audio assets:*
```bash
python generate_sounds.py
```