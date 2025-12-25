## PostGIS Setup Lab

### Lab Goal

By the end of this lab, I will:
- Install PostgreSQL + PostGIS
- Create a spatial database
- Load real-world GIS data
- Run basic spatial queries
- Connect PostGIS to QGIS

### 1. Install PostgreSQL and PostGIS

1. Install PostgreSQL
   - https://www.postgresql.org/download/
   - port 5432
2. Install PostGIS
   - select under spatial extensions when downloading postgresql
  
### 2. Open pgAdmin
- Launch pgAdmin
- Connect to your PostgreSQL server
- Log in with user `postgres`

<img width="1005" height="750" alt="image" src="https://github.com/user-attachments/assets/bfc283b5-19bb-469c-b1c8-9170b0e08ee5" />

### 3. Create Database
- Right-click **Databases**
- Create → Database
- Name: `gis_lab`

<img width="696" height="537" alt="image" src="https://github.com/user-attachments/assets/772a7e52-d5e3-4d4c-b3b4-4e11eebecb99" />

or use the SQL command:

```sql
CREATE DATABASE "setupLab"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
```

Immediately after creation, the database should show up in the databases section on the side:

<img width="241" height="497" alt="image" src="https://github.com/user-attachments/assets/6a010b5d-3b1c-4340-9f2d-81242d4af319" />


### 4. Enable PostGIS

Right now, the database is a normal postgres database, but for GIS projects and spatial data we need to enable PostGIS.

Open Query Tool for `gis_lab` and run:

<img width="749" height="249" alt="image" src="https://github.com/user-attachments/assets/f20ec72d-e294-4601-9ff6-3035f0fd5ee0" />

Verify:

<img width="387" height="513" alt="image" src="https://github.com/user-attachments/assets/358dd213-6530-4c7a-af98-dc3756d3b5d5" />

**You can also enable it using the gui by right clicking on extensions**

### 5. Create Spatial Table

```sql
CREATE TABLE test_points (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geom GEOMETRY(Point, 4326)
);
```

The line beginning with 'id' creates a new column named id that increments automatically through SERIAL and this is assigned as the primary key to uniquely identify each row. These cannot be NULL or duplicated and are used for indexing and relationships.

The next line creates a column of type TEXT.

Finally the last line creates a column named geom with point geometries using the EPSG:4326 spatial reference system.

Verify:

<img width="687" height="429" alt="image" src="https://github.com/user-attachments/assets/f1748356-008a-4ccf-9ab1-a719fade667f" />

### 6. Insert Test Data

We just made the columns, now add data into the table:

```sql
INSERT INTO test_points (name, geom)
VALUES
('Test A', ST_SetSRID(ST_MakePoint(-83.0, 40.0), 4326)),
('Test B', ST_SetSRID(ST_MakePoint(-83.01, 40.01), 4326));
```

Verify:

<img width="449" height="474" alt="image" src="https://github.com/user-attachments/assets/a9e7d9ca-7dba-44cb-8c86-e7b39cbbe3c8" />

**Important to note that the ST_AsText(geom) function makes the geometery human readable**

### 7. Connect to QGIS

Connecting to the database through QGIS will confirm successful creation of our spatial database.

Through QGIS:

<img width="430" height="687" alt="image" src="https://github.com/user-attachments/assets/c65eeeb0-d3b5-47df-b769-74fa555bce00" />

Make sure the database name is the same as in pgadmin. I used basic configurations for this. With multiple users there may be a need for tailored configurations.

To see load the data, you can add our table (test_points) through the DB manager as below:

<img width="1582" height="642" alt="image" src="https://github.com/user-attachments/assets/e42072ee-6e31-4b80-9970-f85b82dc900d" />

Or throught Data Source Manager:

<img width="566" height="550" alt="image" src="https://github.com/user-attachments/assets/32e4c37b-8bf9-4217-b2ff-0d03bc08d346" />

Or through the layer tab:

<img width="852" height="717" alt="image" src="https://github.com/user-attachments/assets/090c18c7-fd4f-4402-818a-fafb33404b41" />

Verify the points are loaded:

<img width="985" height="628" alt="image" src="https://github.com/user-attachments/assets/8894379e-4e5e-4f34-bc81-8c8ee5d915ba" />

Let's add a basemap to give the points some context and officially call this a map. In QGIS, basemaps are labelled as XYZ tiles, add them through the browser panel or through the layer tab:

<img width="1101" height="626" alt="image" src="https://github.com/user-attachments/assets/0557d729-3c54-41ed-8208-6e971bca3c41" />

Our first map with PostGIS is a success! 
