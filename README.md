# Roblox Rain System

A simple rain system for Roblox games that creates rain items and automatically manages cleanup of old items.

## Features

- Creates realistic rain drops that fall from the sky
- Automatically cleans up rain drops based on age and quantity
- Smooth fade-out effect when removing rain drops
- Easy to integrate into any Roblox game
- Configurable settings for rain density and maximum number of rain items

## Installation

1. In Roblox Studio, create two Script objects in ServerScriptService:
   - Name the first one `RainSystem` and paste the contents of `RainSystem.lua`
   - Name the second one `RainController` and paste the contents of `RainController.lua`

2. Make sure the `RainSystem` script is set as a ModuleScript (right-click and change to ModuleScript)

3. The `RainController` should be a regular Script

## Usage

Once installed, a blue button will appear in your game. Players can click this button to toggle the rain on and off.

### Customizing the Rain System

You can modify the following variables in the `RainSystem.lua` file to customize the rain:

```lua
-- Configuration
local MAX_RAIN_ITEMS = 100 -- Maximum number of rain items allowed
local RAIN_INTERVAL = 0.5 -- Time between rain drops in seconds
local RAIN_LIFETIME = 10 -- How long each rain item exists before being eligible for deletion
local CLEANUP_INTERVAL = 2 -- How often to check for cleanup (seconds)
local FADE_OUT_TIME = 0.5 -- Time to fade out rain drops before removal (seconds)
```

- `MAX_RAIN_ITEMS`: Controls how many rain drops can exist before the oldest ones get deleted
- `RAIN_INTERVAL`: Controls how frequently new rain drops are created (lower = more rain)
- `RAIN_LIFETIME`: How long each rain drop exists before being automatically removed
- `CLEANUP_INTERVAL`: How often the system checks for rain drops to clean up
- `FADE_OUT_TIME`: How long it takes for a rain drop to fade out before being removed

### Using the Rain System in Your Own Scripts

You can also use the RainSystem module in your own scripts:

```lua
-- Load the module
local RainSystem = require(game.ServerScriptService.RainSystem)

-- Start the rain
RainSystem:StartRain()

-- Later, stop the rain
RainSystem:StopRain()
```

## How It Works

### Rain Creation
The system creates rain drops at regular intervals. Each rain drop is tracked with its creation time.

### Rain Despawning
The system uses two methods to despawn rain items:

1. **Age-based cleanup**: Rain drops older than `RAIN_LIFETIME` seconds are automatically removed
2. **Quantity-based cleanup**: When the number of rain drops exceeds `MAX_RAIN_ITEMS`, the oldest ones are removed first

### Cleanup Process
1. The cleanup process runs at regular intervals (defined by `CLEANUP_INTERVAL`)
2. It first removes any rain drops that have exceeded their lifetime
3. If there are still too many rain drops, it removes the oldest ones
4. When removing rain drops, it uses a smooth fade-out effect before destroying them

This dual cleanup approach ensures that your game's performance remains stable even with continuous rain effects, while the fade-out effect makes the removal visually appealing.