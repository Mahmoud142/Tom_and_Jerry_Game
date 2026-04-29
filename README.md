# Tom & Jerry Game

Welcome to the **Tom & Jerry Game**, a procedural grid-based puzzle and chase game! Play as Jerry and navigate through a procedurally generated maze to reach your mouse hole before Tom catches you.

This project uses a modern **2D Pygame graphical version**.

---

## Key Features

- **Procedural Map Generation**: Every single match is unique. Maps randomly generate obstacles, spawn points, and exits based on your selected difficulty.
- **A\* Pathfinding AI**: Tom uses A\* search to hunt Jerry down by finding the shortest path around obstacles.
- **Graphical Gameplay**: Play the fully graphical Pygame version with mouse and keyboard menus, sprite assets, and smooth movement.

---

## Project Architecture

### The Graphical Engine (Pygame)

- **`AppGui.py`**
  The interactive GUI entry point. It paints a sleek, modern starting menu with full mouse-hover support, dynamic button color highlighting, and handles routing the selected difficulty over to the graphical engine.
- **`GameGui.py`**
  The fully visual game loop. It dynamically loads PNG sprites, translates rigid grid coordinates into smooth graphical character interpolation (sliding), and uses an advanced `heapq` Priority Queue A\* algorithm so Tom can chase you at 60 FPS natively without lag.
- **`App.py`**
  A simple launcher that starts the graphical version.

### Core Utilities & Assets

- **`Maps.py`**
  The procedural level generator engine. Utilizing calculating Manhattan Distances, it ensures a fair spawn distance between Tom, Jerry, and the Exit, while randomly scattering brick wall obstacles across the grid.
- **`assets/`**
  The directory holding all custom-generated `.png` sprites. It contains the textures for Tom, Jerry, a highly detailed realistic mouse hole exit, and the boundary brick walls.
- **`.gitignore`**
  Protects the repository from bloat. It explicitly ignores Python cache files (`__pycache__`) and the large `.venv` virtual environment folder so the Git repository remains clean and light.

---

## How to Play

1. **Setup your environment:**
   Make sure you have `pygame` installed. If using the project's virtual environment:

    ```bash
    source .venv/bin/activate
    pip install pygame
    ```

2. **Play the game:**

    ```bash
    python App.py
    ```
