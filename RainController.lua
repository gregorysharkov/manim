-- RainController.lua
-- Script that demonstrates how to use the RainSystem

-- Load the RainSystem module
local RainSystem = require(script.Parent:WaitForChild("RainSystem"))

-- Example of how to use the rain system in a Roblox game

-- Create a simple button to toggle rain
local function createRainToggleButton()
    local button = Instance.new("Part")
    button.Name = "RainToggleButton"
    button.Size = Vector3.new(4, 1, 4)
    button.Position = Vector3.new(0, 1, 0)
    button.Anchored = true
    button.CanCollide = true
    button.BrickColor = BrickColor.new("Bright blue")
    
    -- Add a ClickDetector to the button
    local clickDetector = Instance.new("ClickDetector")
    clickDetector.Parent = button
    
    -- Add a label to the button
    local buttonLabel = Instance.new("BillboardGui")
    buttonLabel.Size = UDim2.new(0, 100, 0, 40)
    buttonLabel.Adornee = button
    buttonLabel.Parent = button
    
    local textLabel = Instance.new("TextLabel")
    textLabel.Size = UDim2.new(1, 0, 1, 0)
    textLabel.BackgroundTransparency = 1
    textLabel.TextScaled = true
    textLabel.Font = Enum.Font.SourceSansBold
    textLabel.TextColor3 = Color3.new(1, 1, 1)
    textLabel.Text = "Toggle Rain"
    textLabel.Parent = buttonLabel
    
    button.Parent = workspace
    
    return button, clickDetector
end

-- Create a variable to track if rain is active
local isRainActive = false

-- Create the button
local rainButton, clickDetector = createRainToggleButton()

-- Connect the button to toggle rain
clickDetector.MouseClick:Connect(function()
    if isRainActive then
        -- Stop the rain
        RainSystem:StopRain()
        isRainActive = false
    else
        -- Start the rain
        RainSystem:StartRain()
        isRainActive = true
    end
end)

-- Print instructions to the output
print("Click the blue button to toggle rain!")
print("The system will automatically delete the oldest rain drops when there are more than 100.") 