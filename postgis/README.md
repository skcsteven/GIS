## PostGIS

<img width="263" height="155" alt="image" src="https://github.com/user-attachments/assets/72d9fe3f-acfc-4175-b724-0e285671ab54" />

PostGIS is an extension to PostgreSQL that turns a normal relational database into a spatial database.

In simple terms:

__PostgreSQL__ = stores tables, rows, and columns
__PostGIS__ = adds the ability to store, index, and analyze geographic data (points, lines, polygons)

Without PostGIS:
- A database understands numbers and text
- Coordinates are just meaningless numbers

With PostGIS:
- The database understands maps, distance, area, intersection, containment, and proximity

## What PostGIS Adds

### 1. Spatial Data Types
PostGIS allows databases to store geographic shapes:
- POINT → locations (GPS points, addresses)
- LINESTRING → roads, paths, rivers
- POLYGON → parcels, boundaries, zones

These shapes are stored directly in database tables.

### 2. Spatial Functions
PostGIS provides functions to analyze spatial data:
- Measure distance
- Check if a point is inside a polygon
- Find intersections
- Create buffers
- Calculate area and length

Example concept:
> Find all parks within 500 meters of a school

### 3. Spatial Indexing
PostGIS uses spatial indexes to:
- Make spatial queries fast
- Handle large datasets efficiently

This is critical for real-world GIS systems.

## How is it used

### Desktop GIS
- QGIS connects directly to PostGIS
- Data is centralized and shared
- Multiple users can edit the same data

### Web Mapping & Applications
PostGIS is commonly used behind:
- Web maps
- GIS APIs
- Dashboards
- Asset tracking systems

> Typical flow:
> PostGIS → API → Web Map

### Spatial Analysis at Scale
Instead of clicking tools in desktop GIS:
- Analysis is done with queries
- Workflows are repeatable
- Large datasets are manageable
