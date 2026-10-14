# The University of Sydney Llara Farm 360° Panoramas

Interactive, high resolution spherical panoramas of field sites at Llara Farm, Narrabri NSW, Australia. They support teaching and outreach at The University of Sydney.

**Gallery:** [williamtsalter.github.io/360panos](https://williamtsalter.github.io/360panos/)
**Repository:** [github.com/williamtsalter/360panos](https://github.com/williamtsalter/360panos)

## Sites

| Site | Location | Viewer |
|------|----------|--------|
| 1 | Mulgate Creek Weir West | Coming soon |
| 2 | Mulgate Creek Driveway East | [Open viewer](https://williamtsalter.github.io/360panos/02-mulgate-creek-driveway-east/viewer.html) |
| 3 | Mulgate Creek Dam | [Open viewer](https://williamtsalter.github.io/360panos/03-mulgate-creek-dam/viewer.html) |
| 4 | Llara Hillside | [Open viewer](https://williamtsalter.github.io/360panos/04-llara-hillside/viewer.html) |
| 5 | Llara 1 | Coming soon |
| 6 | Llara Forest | [Open viewer](https://williamtsalter.github.io/360panos/06-llara-forest/viewer.html) |
| 7 | Horsearm Creek Dam | [Open viewer](https://williamtsalter.github.io/360panos/07-horsearm-creek-dam/viewer.html) |
| 8 | Mulgate Creek West | [Open viewer](https://williamtsalter.github.io/360panos/08-mulgate-creek-west/viewer.html) |

Click and drag to look around. Scroll or pinch to zoom.

## Image acquisition

Each panorama was captured with a DJI Mavic 4 Pro [1] in sphere panorama mode, using the 2X (medium tele) camera. At each site the aircraft hovered at a fixed position and took 155 overlapping frames in raw DNG format across the full sphere.

The 2X camera has a narrower field of view than the main camera. More frames are needed to cover the sphere, but each frame resolves finer detail. This gives a much higher angular resolution in the final panorama. Raw capture keeps the full sensor dynamic range for tone and white balance correction.

## Image processing

**1. Stitching.** For each site, the 155 DNG frames were stitched into one equirectangular panorama in Panovolo 1.12.1 [2]. An equirectangular projection maps 360° of longitude and 180° of latitude onto a 2:1 image grid. For Site 2 the output was 32,716 × 16,358 pixels (about 535 megapixels, 274 MB as JPEG).

**2. Tiling.** An image this size can't be streamed efficiently in a browser. Each panorama was reprojected onto the six faces of a cube with `nona` from Hugin [3]. Each face was then split into a multiresolution pyramid of 512 × 512 pixel tiles with the Pannellum `generate.py` utility [4, 5]. Image handling used Pillow [6] and NumPy [7]. For Site 2 this produced six zoom levels, a cube face resolution of 10,408 pixels and a 98 MB tile set.

**3. Display.** Panoramas are rendered in the browser with Pannellum 2.5.7 [4, 5], a WebGL panorama viewer. It only requests the tiles needed for the current view and zoom level, so very large panoramas still load quickly on ordinary laptops and phones.

**4. Hosting.** Tiles and viewer pages are served as static files through [GitHub Pages](https://pages.github.com/). The original sphere JPEGs are kept locally and excluded with `.gitignore`, because they exceed GitHub's 100 MB file limit.

## Reproducing the workflow

Set up the environment (conda forge channel):

```bash
conda create -n pannellum -c conda-forge python=3.12 pillow numpy hugin-base
conda activate pannellum
git clone https://github.com/mpetroff/pannellum.git ~/pano/pannellum
```

Use the macOS system git for pushing, not a conda installed git. This avoids SSL certificate errors.

To add a site, put the equirectangular JPEG and `generate_photosphere.py` in a new site folder and run:

```bash
conda activate pannellum
cd ~/pano/360panos/<site-folder>
python generate_photosphere.py
```

The script finds the JPEG, generates the tile set and writes a `viewer.html` for that site. Commit and push the site folder, then update its card in `index.html`.

## Acknowledgements

The repository structure, viewer pages, `generate_photosphere.py` script and this README were developed with the assistance of Claude Opus 5.5 (Anthropic), accessed through Microsoft 365 Copilot [8]. All outputs were reviewed, tested and edited by the author.

## References

[1] DJI (2025). Mavic 4 Pro. [dji.com/mavic-4-pro](https://www.dji.com/mavic-4-pro)

[2] Panovolo (2026). Panovolo. Version 1.12.1. [panovolo.com](https://www.panovolo.com/)

[3] Hugin Development Team (2025). Hugin: panorama photo stitcher. Version 2025.0.1. [hugin.sourceforge.io](https://hugin.sourceforge.io/)

[4] Petroff, M. A. (2019). Pannellum: a lightweight web based panorama viewer. Journal of Open Source Software 4(40), 1628. [doi:10.21105/joss.01628](https://doi.org/10.21105/joss.01628)

[5] Petroff, M. A. (2026). Pannellum. Version 2.5.7. MIT licence. [github.com/mpetroff/pannellum](https://github.com/mpetroff/pannellum)

[6] Clark, A. and contributors (2026). Pillow. [python-pillow.org](https://python-pillow.org/)

[7] Harris, C. R. et al. (2020). Array programming with NumPy. Nature 585, 357 to 362. [doi:10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)

[8] Anthropic (2026). Claude Opus 5.5. [anthropic.com/claude](https://www.anthropic.com/claude)

## Citation

Salter, W. T. (2026). Llara Farm 360° Panoramas. The University of Sydney. [github.com/williamtsalter/360panos](https://github.com/williamtsalter/360panos)

## Contact

William Salter, School of Life and Environmental Sciences, The University of Sydney
