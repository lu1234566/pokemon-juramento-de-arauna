-- Arauna QA bridge for mGBA 0.10.x+
-- Start tools/arauna_qa/arauna_qa.py first, then load this script from
-- Tools -> Scripting in mGBA.

local HOST = "127.0.0.1"
local PORT = 8765

local client, connectErr = socket.connect(HOST, PORT)
if not client then
    console:error("Arauna QA: failed to connect to " .. HOST .. ":" .. PORT .. ": " .. tostring(connectErr))
    return
end

local rxBuffer = ""
local press = {
    active = false,
    id = nil,
    mask = 0,
    frames = 0,
    releaseFrame = false,
}

local function cleanField(value)
    value = tostring(value or "")
    value = value:gsub("[\r\n\t]", " ")
    return value
end

local function sendResponse(id, status, payload)
    local line = cleanField(id) .. "\t" .. cleanField(status)
    if payload ~= nil then
        line = line .. "\t" .. cleanField(payload)
    end
    local _, err = client:send(line .. "\n")
    if err then
        console:error("Arauna QA: send failed: " .. tostring(err))
    end
end

local function toHex(data)
    local out = {}
    for i = 1, #data do
        out[#out + 1] = string.format("%02x", string.byte(data, i))
    end
    return table.concat(out)
end

local function splitTabs(line)
    local fields = {}
    local startPos = 1
    while true do
        local tabPos = string.find(line, "\t", startPos, true)
        if not tabPos then
            fields[#fields + 1] = string.sub(line, startPos)
            break
        end
        fields[#fields + 1] = string.sub(line, startPos, tabPos - 1)
        startPos = tabPos + 1
    end
    return fields
end

local function parseNumber(text)
    if not text then
        return nil
    end
    if string.sub(text, 1, 2) == "0x" or string.sub(text, 1, 2) == "0X" then
        return tonumber(string.sub(text, 3), 16)
    end
    return tonumber(text)
end

local function handleCommand(line)
    local fields = splitTabs(line)
    local id = fields[1]
    local command = fields[2]

    if not id or not command then
        return
    end

    if command == "PING" then
        sendResponse(id, "OK", "PONG")
    elseif command == "INFO" then
        local payload = string.format(
            "%s|%s|%u",
            cleanField(emu:getGameTitle()),
            cleanField(emu:getGameCode()),
            emu:currentFrame()
        )
        sendResponse(id, "OK", payload)
    elseif command == "READ8" then
        local address = parseNumber(fields[3])
        if not address then
            sendResponse(id, "ERR", "bad address")
            return
        end
        sendResponse(id, "OK", tostring(emu:read8(address)))
    elseif command == "READ16" then
        local address = parseNumber(fields[3])
        if not address then
            sendResponse(id, "ERR", "bad address")
            return
        end
        sendResponse(id, "OK", tostring(emu:read16(address)))
    elseif command == "READ32" then
        local address = parseNumber(fields[3])
        if not address then
            sendResponse(id, "ERR", "bad address")
            return
        end
        sendResponse(id, "OK", tostring(emu:read32(address)))
    elseif command == "READRANGE" then
        local address = parseNumber(fields[3])
        local length = parseNumber(fields[4])
        if not address or not length or length < 0 or length > 65536 then
            sendResponse(id, "ERR", "bad range")
            return
        end
        sendResponse(id, "OK", toHex(emu:readRange(address, length)))
    elseif command == "SETKEYS" then
        local mask = parseNumber(fields[3])
        if not mask then
            sendResponse(id, "ERR", "bad key mask")
            return
        end
        if press.active then
            sendResponse(id, "ERR", "press busy")
            return
        end
        emu:setKeys(mask)
        sendResponse(id, "OK", tostring(mask))
    elseif command == "PRESS" then
        local mask = parseNumber(fields[3])
        local frames = parseNumber(fields[4])
        if not mask or not frames or frames < 1 or frames > 600 then
            sendResponse(id, "ERR", "bad press")
            return
        end
        if press.active then
            sendResponse(id, "ERR", "press busy")
            return
        end
        press.active = true
        press.id = id
        press.mask = mask
        press.frames = frames
        press.releaseFrame = false
    elseif command == "SCREENSHOT" then
        local path = fields[3]
        if not path or path == "" then
            sendResponse(id, "ERR", "missing path")
            return
        end
        emu:screenshot(path)
        sendResponse(id, "OK", path)
    elseif command == "SAVESTATE" then
        local path = fields[3]
        if not path or path == "" then
            sendResponse(id, "ERR", "missing path")
            return
        end
        if emu:saveStateFile(path, C.SAVESTATE.ALL) then
            sendResponse(id, "OK", path)
        else
            sendResponse(id, "ERR", "save state failed")
        end
    elseif command == "LOADSTATE" then
        local path = fields[3]
        if not path or path == "" then
            sendResponse(id, "ERR", "missing path")
            return
        end
        if emu:loadStateFile(path) then
            sendResponse(id, "OK", path)
        else
            sendResponse(id, "ERR", "load state failed")
        end
    elseif command == "RESET" then
        emu:reset()
        sendResponse(id, "OK", "reset")
    else
        sendResponse(id, "ERR", "unknown command")
    end
end

local function processReceive()
    while client:hasdata() do
        local chunk, err = client:receive(4096)
        if not chunk then
            if err and tostring(err) ~= "AGAIN" then
                console:error("Arauna QA: receive failed: " .. tostring(err))
            end
            return
        end
        rxBuffer = rxBuffer .. chunk
    end

    while true do
        local newline = string.find(rxBuffer, "\n", 1, true)
        if not newline then
            break
        end
        local line = string.sub(rxBuffer, 1, newline - 1)
        rxBuffer = string.sub(rxBuffer, newline + 1)
        if string.sub(line, -1) == "\r" then
            line = string.sub(line, 1, -2)
        end
        if line ~= "" then
            local ok, err = pcall(handleCommand, line)
            if not ok then
                local fields = splitTabs(line)
                sendResponse(fields[1] or "0", "ERR", err)
            end
        end
    end
end

client:add("received", processReceive)

callbacks:add("keysRead", function()
    if press.active then
        if press.frames > 0 then
            emu:setKeys(press.mask)
        else
            emu:setKeys(0)
        end
    end
end)

callbacks:add("frame", function()
    if not press.active then
        return
    end

    if press.frames > 0 then
        press.frames = press.frames - 1
        if press.frames == 0 then
            press.releaseFrame = true
        end
    elseif press.releaseFrame then
        press.releaseFrame = false
        local id = press.id
        press.active = false
        press.id = nil
        press.mask = 0
        emu:setKeys(0)
        sendResponse(id, "OK", "released")
    end
end)

console:log("Arauna QA bridge connected to " .. HOST .. ":" .. PORT)
sendResponse("0", "HELLO", "ARAUNA_QA_BRIDGE_V1")
