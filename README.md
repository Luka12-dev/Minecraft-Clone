# Minecraft Clone

A Python-based Minecraft clone built with Pyglet and OpenGL, featuring voxel-based terrain generation, chunk management, and classic Minecraft gameplay mechanics.

## Features

### Core Gameplay
- **Voxel-based world** with 32x256x32 chunk system
- **Enhanced terrain generation** with hills, valleys, and natural tree placement
- **Block placement and breaking** mechanics
- **Flying and walking modes** with physics and collision detection
- **93+ texture support** covering a wide range of Minecraft blocks

### World Management
- **Chunk-based rendering** for optimized performance
- **World save/load system** for persistent gameplay
- **Dynamic chunk loading** and unloading
- **Efficient subchunk meshing** for rendering optimization

### Block Types
Supports numerous block types including:
- Natural blocks (stone, dirt, grass, sand, gravel)
- Ores (coal, iron, gold, diamond, redstone)
- Construction blocks (wood, planks, bricks, glass)
- Decorative blocks (flowers, mushrooms, leaves, torches)
- Interactive blocks (doors, ladders, buttons, levers)
- Special blocks (TNT, furnaces, mob spawners, and more)

## Controls

### Movement
- **W/A/S/D** - Move forward/left/backward/right
- **Space** - Jump (or ascend in fly mode)
- **Left Shift** - Descend (in fly mode)
- **Left Ctrl** - Sprint

### Gameplay
- **Left Click** - Break block
- **Right Click** - Place block
- **Middle Click** - Pick block (copies block to hand)
- **F** - Toggle fly mode
- **F11** - Toggle fullscreen
- **G** - Select random block
- **R** - Random teleport within the world
- **O** - Save world
- **ESC** - Release mouse cursor

## Requirements

- Python 3.7+
- Pyglet
- OpenGL 3.3+
- NumPy (for matrix operations)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Luka12-dev/Minecraft-Clone
cd Minecraft-Clone
```

2. Install dependencies:
```bash
pip install pyglet numpy
```

3. Run the game:
```bash
python main.py
```

## Project Structure

```
minecraft-clone/
├── main.py                 # Main game window and event handling
├── world.py                # World management and chunk coordination
├── chunk.py                # Chunk generation and management
├── subchunk.py             # Subchunk meshing for optimized rendering
├── player.py               # Player physics and movement
├── collider.py             # Collision detection system
├── entity.py               # Base entity class
├── block_type.py           # Block type definitions and properties
├── texture_manager.py      # Texture loading and management
├── shader.py               # OpenGL shader compilation and management
├── matrix.py               # Matrix operations for 3D transformations
├── hit.py                  # Raycasting for block interaction
├── save.py                 # World save/load functionality
├── vert.glsl               # Vertex shader
├── frag.glsl               # Fragment shader
├── data/
│   └── blocks.mcpy         # Block configuration data
├── models/                 # Block model definitions
│   ├── cube.py             # Standard cube blocks
│   ├── plant.py            # Plant-like blocks
│   ├── liquid.py           # Water and lava
│   ├── stairs.py           # Stair blocks
│   ├── door.py             # Door blocks
│   └── ...                 # Additional model types
└── textures/               # Block textures (PNG files)
```

## Technical Details

### Rendering
- Uses OpenGL 3.3 core profile
- Implements frustum culling for chunk visibility
- Vertex buffer objects (VBOs) for efficient mesh rendering
- Texture array for all block textures
- Custom GLSL shaders for vertex and fragment processing

### World Generation
- Perlin-like noise for terrain height maps
- Biome-based generation with temperature and moisture values
- Procedural tree generation
- Cave and ore vein generation

### Performance Optimizations
- Subchunk-based mesh building (16x16x16 sections)
- Greedy meshing to reduce vertex count
- Frustum culling to avoid rendering off-screen chunks
- Lazy chunk generation and loading
- Face culling for hidden block faces

## Development

### Adding New Blocks
1. Add texture file to `textures/` directory
2. Define block properties in `data/blocks.mcpy`
3. Create model in `models/` if needed (for non-cube blocks)
4. Update `block_type.py` if new properties are required

### Modifying Terrain Generation
Edit the generation logic in `chunk.py` to adjust:
- Terrain height and variation
- Ore placement and frequency
- Structure generation (trees, caves, etc.)
- Biome distribution

## Known Limitations

- World size is limited by memory
- No multiplayer support
- Limited redstone functionality
- Simplified physics compared to Minecraft

## License

This project is a learning implementation and is not affiliated with Mojang or Microsoft.

## Acknowledgments

Built as an educational project to explore voxel-based rendering, procedural generation, and game development with Python and OpenGL.
