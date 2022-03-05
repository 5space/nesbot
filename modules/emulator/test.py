from pytari2600.pytari2600 import new_atari

emulator = new_atari("../../roms/dragster.a26", headless=False)
while True:
    emulator.core.step()
    # print("---AFTER EXECUTION---" + str(emulator.stella.clocks.system_clock))
    # print(emulator.stella.display_cache)