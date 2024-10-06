# replace water at destroyed custom block with air (water origins from custom block being based on a waterlogged block)
execute as @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_model_data": 90100}}}] run execute at @s if block ~ ~ ~ water run setblock ~ ~ ~ air
# remove the marker item dropped as an extra loot when the custom block was destroyed
execute as @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_model_data": 90100}}}] run kill @s
# store the custom model data of held item to enable custom block creation
execute as @a store result score @s heldItem run data get entity @s SelectedItem.components."minecraft:custom_model_data"
# remove temporary custom block place trigger achievement
advancement revoke @a only blocks:place_block/trigger

