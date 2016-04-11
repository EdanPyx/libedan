EdanCombo = {}

function EdanCombo.Wait(ms)
    local finish = os.clock() + ms / 1000
    while os.clock() < finish do
        coroutine.yield()
    end
end

function EdanCombo.WaitUntil(func)
	while func() ~= true do
		coroutine.yield()
	end
end

function EdanCombo.WaitUntilNotDoing(pattern)
	EdanCombo.Wait(300)
	while true do
		local player = GetSelfPlayer()
		if string.match(player.CurrentActionName, pattern) == nil then
			break
		end
		coroutine.yield()
	end
end

function EdanCombo.UseSkillAtPosition(id, position, delay)
	EdanSkills.UseSkillAtPosition(id, position, delay)
	EdanCombo.Wait(delay)
end

function EdanCombo.UseSkill(id, delay)
	EdanSkills.UseSkill(id, delay)
	EdanCombo.Wait(delay)
end

function EdanCombo.DoActionAtPosition(action, position, delay)
	GetSelfPlayer():DoActionAtPosition(action, position, delay)
	EdanCombo.Wait(delay)
end

function EdanCombo.DoAction(action, delay)
	GetSelfPlayer():DoAction(action, delay)
	EdanCombo.Wait(delay)
end

function EdanCombo.HoldUntilDone(keys, position)
	if position then
		GetSelfPlayer():SetActionStateAtPosition(keys, position, 200)
	else
		GetSelfPlayer():SetActionState(keys, 200)
	end
	
	EdanCombo.Wait(100)

	while true do
		local player = GetSelfPlayer()
		local action = player.CurrentActionName
		
		if EdanCombo.NotUsingSkill(action) then
			break
		end

		if position then
			player:SetActionStateAtPosition(keys, position, 200)
		else
			player:SetActionState(keys, 200)
		end

		coroutine.yield()
	end
end

function EdanCombo.PressAndWait(keys, position, duration)
	local player = GetSelfPlayer()
	player:SetActionStateAtPosition(keys, position, duration or 200)
	EdanCombo.Wait(duration or 200)

	while true do
		player = GetSelfPlayer()
		local action = player.CurrentActionName
		if EdanCombo.NotUsingSkill(action) then
			break
		end
		coroutine.yield()
	end
end

EdanCombo.WaitActions = {
	-- BT_WAIT_HOLD_ON = 1,
	BT_WAIT = 1,
}

function EdanCombo.NotUsingSkill(action)
	
	local result = 
	string.match(action, "_End$") or
	string.match(action, "^BT_RUN_") or
	string.match(action, "^BT_") == nil or
	EdanCombo.WaitActions[action] ~= nil

	-- print(string.format("wait: %s %s %s", action, tostring(EdanCombo.WaitActions[action]), tostring(result)))
	return result
end