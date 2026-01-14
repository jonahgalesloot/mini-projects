# Electron Space Invaders Demo

## Purpose  
A demo built in Electron for teaching my classmatesJS, showing possibilities with more advanced coding. Features a charge-shot system (quick/charged/overload), sprite animations (7 states), sprite preprocessing (rotation/trimming/scaling), fullscreen toggle (F/ESC), and particle effects.

## How It Works  
- **Electron desktop app** with IPC for fullscreen control (F=enter, ESC=exit)  
- **Sprite pipeline**: Loads PNG sprite sheets → trims transparent pixels → rotates 90° → scales responsively  
- **Responsive canvas**: Scales to container size, maintains 30FPS cap  
- **Audio**: 3 explosion types (quick/charged/overload) with preload  

## Included Files  
- `main.js`: Electron window + fullscreen IPC handlers  
- `game.js`: Game loop, player physics, projectile/explosion systems, sprite processing  
- `index.html`: Start screen → game canvas toggle  
- `Sprites/`: Player animations (idle/turn/shoot/charge/damage/death), projectiles, effects  
- `Sounds/`: Explosion SFX  

## Prerequisites  
```bash
npm init -y
npm install electron --save-dev
```

## Usage
```
npm start  # Launches Electron app
# F = Fullscreen, ESC = Exit fullscreen
# A/D = Move, Space = Charge shot (hold longer = more power!)
# L = Damage animation, K = Death animation (debug)
```