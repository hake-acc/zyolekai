import os
from PIL import Image

def optimize_image(src_path, dst_path, max_width=None, quality=82):
    with Image.open(src_path) as im:
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            im = im.convert('RGBA')
        else:
            im = im.convert('RGB')
            
        if max_width and im.width > max_width:
            ratio = max_width / im.width
            new_height = int(im.height * ratio)
            im = im.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
        im.save(dst_path, 'WEBP', quality=quality, method=6)
        print(f"Optimized {src_path} -> {dst_path}: {os.path.getsize(dst_path)/1024:.1f} KB")

# 1. Optimize Avatars to 320x320 retina WebP @ quality 82
avatars_dir = 'public/avatars'
for f in os.listdir(avatars_dir):
    if f.endswith('.png'):
        base = os.path.splitext(f)[0]
        src = os.path.join(avatars_dir, f)
        dst = os.path.join(avatars_dir, f"{base}.webp")
        optimize_image(src, dst, max_width=320, quality=82)

# 2. Optimize Navbar and Hero Logos
optimize_image('public/brand/exact_zyolekai_logo.png', 'public/brand/exact_zyolekai_logo.webp', max_width=600, quality=85)
optimize_image('public/brand/wordmark.png', 'public/brand/wordmark.webp', max_width=600, quality=85)
optimize_image('public/brand/exact_slogan.png', 'public/brand/exact_slogan.webp', max_width=700, quality=85)
optimize_image('public/brand/logo.png', 'public/brand/logo.webp', max_width=128, quality=85)

# 3. Optimize Favicon PNG
with Image.open('public/brand/logo.png') as im:
    im = im.convert('RGBA').resize((64, 64), Image.Resampling.LANCZOS)
    im.save('public/brand/logo.png', 'PNG', optimize=True)
    print(f"Favicon logo.png optimized to {os.path.getsize('public/brand/logo.png')/1024:.1f} KB")

# 4. Optimize Media Kits
mk_dir = 'public/media-kits'
if os.path.exists(mk_dir):
    for f in os.listdir(mk_dir):
        if f.endswith('.png'):
            base = os.path.splitext(f)[0]
            src = os.path.join(mk_dir, f)
            dst = os.path.join(mk_dir, f"{base}.webp")
            optimize_image(src, dst, max_width=800, quality=80)

print("\nAsset optimization completed!")
