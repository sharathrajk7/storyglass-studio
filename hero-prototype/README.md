# Storyglass Studio hero (live 3D prototype)

A glass crystal carrying four films rises out of a night sea. The water glows where the
cursor or finger moves. Scroll, drag or hover turns the crystal; a tap flies the facing
film forward into a real player.

## Run it on your Mac

```
python3 tools/serve.py . 8790
```

Then open http://localhost:8790

## Change the films (every few weeks)

Everything lives in `films.json`. The first four films sit on the crystal, in order; the
index under the hero lists every film.

1. Make the 6-second silent loop and poster for the new film:

   ```
   tools/make_loop.sh "/path/to/New Film.mp4" acme-demo 12
   ```

   (`12` = the second the loop starts at; pick a moment with motion. For a letterboxed
   film add a crop as the 4th argument, e.g. `2844:1600:498:280`.)

2. Add an entry to `films.json`:

   ```json
   {
     "id": "acme-demo",
     "title": "Acme product demo",
     "type": "Product demo",
     "length": "1:30",
     "loop": "media/acme-demo.mp4",
     "poster": "media/acme-demo.jpg",
     "full": "https://video.gumlet.io/<collection>/<asset>/main.m3u8"
   }
   ```

3. To remove a film, delete its entry. To change which four are on the crystal, reorder.

`full` is the complete film with sound. Paste the Gumlet link here: MP4 links play
everywhere; `.m3u8` (HLS) links use hls.js automatically on browsers that need it. If the
link fails to load, the player falls back to the loop.

## Devices

- Phones: lighter sea (4,500 particles), no glass colour split, one film decoding at a time.
- Tablets / iPads: 8,000 particles, all four films playing.
- Laptops and desktops: full quality, 12,000 particles, glass dispersion.
- Every device: resolution capped to a pixel budget, so 4K and ultrawide screens stay smooth;
  if the frame rate drops below ~40 fps the page lowers its own resolution.
- Rendering pauses when the hero is scrolled away or the tab is hidden.

Test a tier on a desktop with `?tier=phone` or `?tier=tablet` in the URL.

## Brand assets (media/brand/)

Made from the 3D logo in `~/Downloads/Storyglassstudio/4-Kinetic-Aperture/3D/`:
`mark.png` (menu bar, shown with `mix-blend-mode: screen` so the ink drops out), `icon-32/180/512.png`
(favicon, home-screen icon), `og.jpg` (1200x630 link preview), `emblem-loop.mp4` + `emblem.jpg`
(footer emblem; loads only when the footer is on screen).

## Opening intro and device QA

- The 3D logo reveal (`media/brand/reveal.mp4`, 4.2 s, 329 KB) opens the site once per visit. Tap, scroll or a key
  skips it; it never plays with reduced motion, on a deep link (`#brief`), or when the video is slow to start.
  Add `?nointro` to the URL to skip it while working.
- The line "Videos that make your company" is placed by `placeKicker()` just above the 3D "make"; if the menu bar
  leaves too little room, the headline moves down instead of colliding.
- Checked on 16 sizes from a 320 px phone to a 2560 px monitor (no sideways scrolling, nothing overlapping
  the top, 44 px touch targets): `tools/audit.py`.
