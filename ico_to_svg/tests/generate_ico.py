from pathlib import Path

from PIL import Image

# Ensure data directory exists
out_dir = Path(__file__).resolve().parents[1] / "data"
out_dir.mkdir(parents=True, exist_ok=True)

# Create a base 256x256 and let Pillow generate multiple sizes for ICO
base_size = 256
base = Image.new("RGBA", (base_size, base_size), (255, 0, 0, 255))

# Draw simple pattern
for i in range(base_size):
    base.putpixel((i, i), (0, 128, 255, 255))
    base.putpixel((i, base_size - 1 - i), (0, 128, 255, 255))
for x in range(base_size):
    base.putpixel((x, 0), (0, 200, 0, 255))
    base.putpixel((x, base_size - 1), (0, 200, 0, 255))
for y in range(base_size):
    base.putpixel((0, y), (0, 200, 0, 255))
    base.putpixel((base_size - 1, y), (0, 200, 0, 255))

multi_path = out_dir / "test-multi.ico"
sizes = [(16, 16), (32, 32), (64, 64), (128, 128)]
base.save(multi_path, format="ICO", sizes=sizes)
print(f"Created test ICO: {multi_path}")
