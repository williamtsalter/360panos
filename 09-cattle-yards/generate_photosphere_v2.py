#!/usr/bin/env python3
"""
generate_photosphere.py
Drop into any site folder alongside the sphere JPEG and run:
    conda activate pannellum
    python generate_photosphere.py
Works with any folder name. Known sites get a numbered display name.
"""
import json, shutil, subprocess, sys
from pathlib import Path

SITE_DIR      = Path(__file__).parent.resolve()
PANNELLUM_DIR = SITE_DIR.parent.parent / "pannellum"
GENERATOR     = PANNELLUM_DIR / "utils" / "multires" / "generate.py"
TILES_DIR     = SITE_DIR / "tiles"

SITE_NAMES = {
    "01-mulgate-creek-weir-west":     ("1", "Mulgate Creek Weir West"),
    "02-mulgate-creek-driveway-east": ("2", "Mulgate Creek Driveway East"),
    "03-mulgate-creek-dam":           ("3", "Mulgate Creek Dam"),
    "04-llara-hillside":              ("4", "Llara Hillside"),
    "05-llara-1":                     ("5", "Llara 1"),
    "06-llara-forest":                ("6", "Llara Forest"),
    "07-horsearm-creek-dam":          ("7", "Horsearm Creek Dam"),
    "08-mulgate-creek-west":          ("8", "Mulgate Creek West"),
    "09-cattle-yards":                ("9", "Cattle Yards"),
    "10-eddy-covariance-tower":       ("10", "Eddy Covariance Tower"),
}

VIEWER_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{display_name} | Llara Farm 360</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pannellum@2.5.7/build/pannellum.css">
  <script src="https://cdn.jsdelivr.net/npm/pannellum@2.5.7/build/pannellum.js"></script>
  <style>
    html, body {{ width:100%; height:100%; margin:0; font-family:sans-serif; }}
    #panorama {{ width:100%; height:92%; }}
    #label {{
      background:#2c6e49; color:white;
      padding:8px 16px; font-size:14px;
      display:flex; justify-content:space-between; align-items:center;
    }}
    #label a {{ color:#ccc; font-size:12px; text-decoration:none; }}
  </style>
</head>
<body>
  <div id="label">
    <span>📍 {display_name}</span>
    <a href="../index.html">← All sites</a>
  </div>
  <div id="panorama"></div>
  <script>
    pannellum.viewer('panorama', {{
      type: 'multires',
      autoLoad: true,
      multiRes: {{
        basePath: 'tiles',
        path: '/%l/%s%y_%x',
        fallbackPath: '/fallback/%s',
        extension: 'jpg',
        tileResolution: {tile_res},
        maxLevel: {max_level},
        cubeResolution: {cube_res}
      }}
    }});
  </script>
</body>
</html>
"""

def get_display_name(slug):
    if slug in SITE_NAMES:
        num, name = SITE_NAMES[slug]
        return f"Site {num} - {name}"
    return slug.replace("-", " ").replace("_", " ").title()

def find_jpeg():
    matches = [
        p for ext in ("*.jpg", "*.jpeg", "*.JPG", "*.JPEG")
        for p in SITE_DIR.glob(ext)
        if p.parent == SITE_DIR
    ]
    matches = list({str(p): p for p in matches}.values())
    if len(matches) == 0:
        sys.exit("ERROR: No JPEG found directly in this folder.")
    if len(matches) > 1:
        names = "\n  ".join(p.name for p in matches)
        sys.exit(f"ERROR: More than one JPEG found:\n  {names}\n  Keep only the sphere JPEG.")
    return matches[0]

def main():
    if not GENERATOR.exists():
        sys.exit(f"ERROR: Pannellum generator not found at:\n  {GENERATOR}")

    slug         = SITE_DIR.name
    display_name = get_display_name(slug)

    print(f"\n{'='*60}")
    print(f"  Site   : {display_name}")
    print(f"  Folder : {SITE_DIR}")
    print(f"{'='*60}\n")

    jpeg = find_jpeg()
    print(f"  JPEG       : {jpeg.name}  ({jpeg.stat().st_size / 1e6:.1f} MB)")

    if TILES_DIR.exists():
        print("  Removing existing tiles ...")
        shutil.rmtree(TILES_DIR)

    print("  Generating tiles, this may take several minutes ...\n")
    result = subprocess.run(
        [sys.executable, str(GENERATOR), str(jpeg), "--output", str(TILES_DIR)]
    )
    if result.returncode != 0:
        sys.exit("ERROR: Tile generation failed.")

    config_path = TILES_DIR / "config.json"
    if not config_path.exists():
        sys.exit("ERROR: config.json not found after generation.")

    with open(config_path) as f:
        config = json.load(f)

    mr    = config.get("multiRes", {})
    total = sum(f.stat().st_size for f in TILES_DIR.rglob("*") if f.is_file())
    print(f"\n  Tiles done : maxLevel={mr.get('maxLevel')}  cubeResolution={mr.get('cubeResolution')}  total={total / 1e6:.1f} MB")

    html = VIEWER_TEMPLATE.format(
        display_name=display_name,
        tile_res=mr.get("tileResolution", 512),
        max_level=mr.get("maxLevel", 6),
        cube_res=mr.get("cubeResolution", 8432),
    )
    (SITE_DIR / "viewer.html").write_text(html)
    print("  viewer.html written.")

    repo_dir = SITE_DIR.parent
    print("\n  Done. To publish:\n")
    print(f"    cd {repo_dir}")
    print(f"    git add {slug}/")
    print(f"    git commit -m \"Add {display_name} panorama\"")
    print("    git push origin main\n")
    print(f"  Live at: https://williamtsalter.github.io/360panos/{slug}/viewer.html\n")

if __name__ == "__main__":
    main()
