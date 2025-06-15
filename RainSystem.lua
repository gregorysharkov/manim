-- RainSystem.lua
-- Script for creating rain items and managing their lifecycle

local RainSystem = {}

-- Configuration
local MAX_RAIN_ITEMS = 100 -- Maximum number of rain items allowed
local RAIN_INTERVAL = 0.5 -- Time between rain drops in seconds
local RAIN_LIFETIME = 10 -- How long each rain item exists before being eligible for deletion
local CLEANUP_INTERVAL = 2 -- How often to check for cleanup (seconds)
local FADE_OUT_TIME = 0.5 -- Time to fade out rain drops before removal (seconds)

-- Storage for rain items
local rainItems = {}
local cleanupRunning = false
local rainRunning = false

-- Function to create a new rain item
function RainSystem:CreateRainItem()
    -- Create a new part to represent rain
    local rainPart = Instance.new("Part")
    rainPart.Name = "RainDrop"
    rainPart.Size = Vector3.new(0.2, 0.6, 0.2)
    rainPart.Material = Enum.Material.SmoothPlastic
    rainPart.Transparency = 0.3
    rainPart.Color = Color3.fromRGB(110, 153, 202) -- Light blue color
    rainPart.Anchored = false
    rainPart.CanCollide = true
    
    -- Random position above the play area
    local randomX = math.random(-100, 100)
    local randomZ = math.random(-100, 100)
    rainPart.Position = Vector3.new(randomX, 100, randomZ) -- High in the sky
    
    -- Add physics properties
    local bodyVelocity = Instance.new("BodyVelocity", rainPart)
    bodyVelocity.MaxForce = Vector3.new(0, 0, 0) -- No force initially
    
    -- Store creation time with the rain item
    local rainItemData = {
        part = rainPart,
        creationTime = os.time()
    }
    
    -- Add to our tracking table
    table.insert(rainItems, rainItemData)
    
    -- Parent to workspace to make it visible
    rainPart.Parent = workspace
    
    return rainPart
end

-- Function to fade out and remove a rain item
function RainSystem:FadeOutAndRemove(rainItem)
    if not rainItem or not rainItem.part or not rainItem.part.Parent then
        return
    end
    
    -- Create a tween to fade out the rain drop
    local tweenService = game:GetService("TweenService")
    local tweenInfo = TweenInfo.new(FADE_OUT_TIME, Enum.EasingStyle.Linear)
    local properties = {Transparency = 1}
    
    local tween = tweenService:Create(rainItem.part, tweenInfo, properties)
    tween:Play()
    
    -- Wait for the tween to complete, then destroy the part
    spawn(function()
        wait(FADE_OUT_TIME)
        if rainItem.part and rainItem.part.Parent then
            rainItem.part:Destroy()
        end
    end)
end

-- Function to clean up old rain items when we have too many
function RainSystem:CleanupRainItems()
    -- If cleanup is already running, don't start another one
    if cleanupRunning then
        return
    end
    
    cleanupRunning = true
    
    spawn(function()
        while rainRunning do
            local currentTime = os.time()
            local itemsToRemove = {}
            
            -- First, identify items to remove based on age
            for i, item in ipairs(rainItems) do
                if currentTime - item.creationTime >= RAIN_LIFETIME then
                    table.insert(itemsToRemove, i)
                end
            end
            
            -- Remove identified items (starting from the end to avoid index issues)
            for i = #itemsToRemove, 1, -1 do
                local index = itemsToRemove[i]
                local item = table.remove(rainItems, index)
                if item and item.part then
                    self:FadeOutAndRemove(item)
                end
            end
            
            -- If we still have too many items, remove the oldest ones
            if #rainItems > MAX_RAIN_ITEMS then
                -- Sort rain items by creation time (oldest first)
                table.sort(rainItems, function(a, b)
                    return a.creationTime < b.creationTime
                end)
                
                -- Calculate how many to remove
                local removeCount = #rainItems - MAX_RAIN_ITEMS
                
                -- Remove oldest items
                for i = 1, removeCount do
                    local oldestItem = table.remove(rainItems, 1)
                    if oldestItem and oldestItem.part then
                        self:FadeOutAndRemove(oldestItem)
                    end
                end
            end
            
            -- Wait before checking again
            wait(CLEANUP_INTERVAL)
        end
        
        cleanupRunning = false
    end)
end

-- Function to start the rain system
function RainSystem:StartRain()
    if rainRunning then
        return -- Already running
    end
    
    rainRunning = true
    
    -- Start the cleanup process
    self:CleanupRainItems()
    
    -- Create a loop that spawns rain at intervals
    spawn(function()
        while rainRunning do
            self:CreateRainItem()
            wait(RAIN_INTERVAL)
        end
    end)
end

-- Function to stop the rain and clean up all rain items
function RainSystem:StopRain()
    rainRunning = false
    
    -- Remove all rain items with a fade effect
    for i = #rainItems, 1, -1 do
        local item = table.remove(rainItems, i)
        if item and item.part then
            self:FadeOutAndRemove(item)
        end
    end
end

return RainSystem 