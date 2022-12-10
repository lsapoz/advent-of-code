from pathlib import Path

here = Path(__file__).parent
lines = Path(here/"10.txt").read_text().splitlines()

timeline = [1]  # val of X at the end of the ith cycle

for line in lines:
    parts = line.split()
    if parts[0] == 'noop':
        timeline.append(timeline[-1])
    else:
        val = int(parts[1])
        timeline.append(timeline[-1])
        timeline.append(timeline[-1] + val)

sum_signal_strength = 0
for i in range(20, len(timeline), 40):
    sum_signal_strength += i * timeline[i-1]  # val during the cycle is the val at the end of the previous cycle
print(f"Sum of signal strength: {sum_signal_strength}")

pixels = []
width = 40
for i in range(240):
    x = timeline[i]
    sprite_pos = [x - 1, x, x + 1]
    pixel_val = '#' if i % width in sprite_pos else '.'
    pixels.append(pixel_val)

for i in range(0, len(pixels), width):
    print(''.join(pixels[i:i + width]))
