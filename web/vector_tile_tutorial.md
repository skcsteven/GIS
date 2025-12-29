# Loading a Large Shapefile in a Web Browser with Leaflet + Vector Tiles

## Goal
Render a very large polygon-heavy shapefile in a web browser without performance issues by converting it into vector tiles and loading them with Leaflet.

<img width="67" height="24" alt="image" src="https://github.com/user-attachments/assets/4a4be648-d3d0-45af-9706-7cc4987f4e29" />

## Problem
- Original shapefile was extremely large (hundreds of thousands of polygons)
- Direct loading (GeoJSON / TopoJSON) was too slow
- QGIS and browser rendering struggled due to geometry size
- Tiles returned “out of bounds” errors due to incorrect zoom ranges

<img width="705" height="298" alt="image" src="https://github.com/user-attachments/assets/12ba6805-f3d4-4b1b-9122-b5a290f45e36" />

## Solution Overview
1. Convert the shapefile to GeoJSON
2. Generate vector tiles using Tippecanoe
3. Serve the tiles locally
4. Load vector tiles in Leaflet using `Leaflet.VectorGrid`

## Tools Used
- **QGIS** (initial inspection / export)
- **ogr2ogr** (shapefile → GeoJSON)
- **Tippecanoe** (vector tile generation)
- **WSL (Ubuntu)** on Windows
- **Leaflet**
- **Leaflet.VectorGrid**
- **tileserver-gl** (local tile server)

All tools used are free and open source.

---

## Step 1: Convert Shapefile to GeoJSON

Using `ogr2ogr`:

```bash
ogr2ogr -f GeoJSON NASIK.geojson NASIK.shp```

This creates a browser-compatible intermediate format that we will split up into vector tiles.

## Step 2: Generate Vector Tiles with Tippecanoe

Optimized for a country-scale polygon dataset (run in WSL):

```bash
tippecanoe \
  --force \
  -o nasik.mbtiles \
  -Z0 \
  -z10 \
  --drop-densest-as-needed \
  --simplify-only-low-zooms \
  --detect-shared-borders \
  NASIK.geojson
```

Why these flags
-Z0 → global visibility
-z10 → appropriate for country / district scale
--drop-densest-as-needed → prevents oversized tiles
--simplify-only-low-zooms → preserves detail where it matters
--detect-shared-borders → reduces polygon duplication
Incorrect zoom ranges (-z1) caused tiles to be out of bounds.

## Step 3: Serve the Vector Tiles

Using tileserver.gl (run in command prompt for windows):

```bash
tileserver-gl nasik.mbtiles --port 8080
```

These tiles are served at:

```http://localhost:8080/data/nasik/{z}/{x}/{y}.pbf```

## Step 4: Load the Vector Tiles in Leaflet

__index.html__

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    html, body, #map { height: 100%; margin: 0; }
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="https://unpkg.com/leaflet.vectorgrid@1.3.0/dist/Leaflet.VectorGrid.bundled.js"></script>
  <script src="script.js"></script>
</body>
</html>
```

__script.js__

```javascript
var map = L.map('map', {
  center: [20.0, 73.8],
  zoom: 5,
  minZoom: 0,
  maxZoom: 6
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
  .addTo(map);

L.vectorGrid.protobuf(
  "http://localhost:8080/data/nasik/{z}/{x}/{y}.pbf",
  {
    vectorTileLayerStyles: {
      NASIK: {
        color: "#ff0000",
        weight: 1,
        fillColor: "#0000ff",
        fillOpacity: 0.4
      }
    },
    interactive: true
  }
).addTo(map);

```

## Results of using vector tiles

+ Large shapefile renders smoothly in the browser
+ No full-geometry loading into memory
+ No browser freezes or crashes
+ Scales cleanly across districts and zoom levels

## Key Takeaways

+ Do not load massive GeoJSON directly in the browser
+ Vector tiles are the correct approach for large polygon datasets
+ Tippecanoe zoom ranges must match dataset scale
+ Leaflet + VectorGrid is a lightweight, production-ready stack
+ This approach works well for administrative boundaries, districts, and country-level data
