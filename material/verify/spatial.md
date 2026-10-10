# Verification — spatial

Run `SET TIME ZONE 'UTC';` in psql first (`psql -h localhost -U argus -d argus_snapshot`).

## S001 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Baltanas?  
**Reference:** 380.8 m, between Gases and GNSS_Base.  
**Recomputed:** `380.8` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| Gases | GNSS_Base | 380.792 |
| Acc-3A | GNSS_Base | 360.872 |
| AF2 | GNSS_Base | 340.136 |
| WP1 | GNSS_Base | 338.443 |
| WP2 | GNSS_Base | 336.7 |


---

## S002 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Delos?  
**Reference:** 1355.6 m, between H. Fournoi_wall attached 1 and LS-153157.  
**Recomputed:** `1355.6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| LS-153157 | H. Fournoi_wall attached 1 | 1355.57 |
| H. Fournoi_pole mounted_outdoors | LS-153157 | 1281.68 |
| LS-153157 | Outdoors area H. Masks_Mask_pole mounted | 848.26 |
| H. Masks_Dyonisios &panter mosaic_pole mounted 2 | LS-153157 | 834.772 |
| LS-153157 | H. Masks_Dolphins mosaic_pole mounted | 830.345 |


---

## S003 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Lucretili?  
**Reference:** 8653.3 m, between LS-153061 - Tiltmeter Conventillo and LS-177310 Crackmeter Montefalco.  
**Recomputed:** `8653.3` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| LS-153061 - Tiltmeter Conventillo | LS-177310 Crackmeter Montefalco | 8653.33 |
| LS-177253 Crackmeter Conventillo | LS-177310 Crackmeter Montefalco | 8652.58 |
| LS-177281 Humidity-Temperature Montefalco | LS-153061 - Tiltmeter Conventillo | 8652.57 |
| LS-177281 Humidity-Temperature Montefalco | LS-177253 Crackmeter Conventillo | 8651.81 |
| LS-177310 Crackmeter Montefalco | LS-177266 - Crackmeter Conventillo | 8650.34 |


---

## S004 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Ranverso?  
**Reference:** 45.2 m, between LS-170894 and LS-177315.  
**Recomputed:** `45.2` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| LS-177315 | LS-170894 | 45.2195 |
| LS-149361 | LS-170894 | 45.0197 |
| LS-177315 | LS-143276 | 44.3612 |
| LS-149361 | LS-143276 | 44.2287 |
| LS-177315 | LS-174188 | 37.4466 |


---

## S005 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Schenkenberg?  
**Reference:** 5.5 m, between LS-152555 and LS-175480.  
**Recomputed:** `5.5` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| LS-175480 | LS-152555 | 5.53735 |
| LS-159070 | LS-152555 | 4.55761 |
| LS-159070 | LS-152899 | 4.33754 |
| LS-152914 | LS-152555 | 4.157 |
| LS-152555 | LS-152479 | 3.98453 |


---

## S006 · centroid

**Question:** What is the centroid of the sensor nodes at Baltanas?  
**Reference:** Latitude 41.938315, longitude -4.244076 (mean of 12 nodes).  
**Recomputed:** `[41.938315, -4.244076]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 41.9383 | -4.24408 | 12 |


---

## S007 · centroid

**Question:** What is the centroid of the sensor nodes at Delos?  
**Reference:** Latitude 37.396446, longitude 25.269236 (mean of 15 nodes).  
**Recomputed:** `[37.396446, 25.269236]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 37.3964 | 25.2692 | 15 |


---

## S008 · centroid

**Question:** What is the centroid of the sensor nodes at Lucretili?  
**Reference:** Latitude 42.045464, longitude 12.843224 (mean of 13 nodes).  
**Recomputed:** `[42.045464, 12.843224]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 42.0455 | 12.8432 | 13 |


---

## S009 · centroid

**Question:** What is the centroid of the sensor nodes at Ranverso?  
**Reference:** Latitude 45.081183, longitude 7.449715 (mean of 7 nodes).  
**Recomputed:** `[45.081183, 7.449715]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 45.0812 | 7.44972 | 7 |


---

## S010 · centroid

**Question:** What is the centroid of the sensor nodes at Schenkenberg?  
**Reference:** Latitude 47.442133, longitude 8.101044 (mean of 7 nodes).  
**Recomputed:** `[47.442133, 8.101044]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 47.4421 | 8.10104 | 7 |


---

## S011 · highest_node

**Question:** Which sensor node at Baltanas is at the highest altitude?  
**Reference:** AF4, at 798.42 m.  
**Recomputed:** `AF4` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| AF4 | 41.9385 | -4.24394 | 798.424 |
| AF3 | 41.9385 | -4.2439 | 797.918 |
| WP1 | 41.9385 | -4.24384 | 797.842 |


---

## S012 · highest_node

**Question:** Which sensor node at Delos is at the highest altitude?  
**Reference:** LS-153242, at 43.48 m.  
**Recomputed:** `LS-153242` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-153242 | 37.3977 | 25.2709 | 43.48 |
| Outdoors area H. Masks_Mask_pole mounted | 37.3963 | 25.2698 | 36.99 |
| H. Fournoi_wall attached 1 | 37.3914 | 25.2696 | 35.79 |


---

## S013 · highest_node

**Question:** Which sensor node at Lucretili is at the highest altitude?  
**Reference:** LS-177310 Crackmeter Montefalco, at 896.06 m.  
**Recomputed:** `LS-177310 Crackmeter Montefalco` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-177310 Crackmeter Montefalco | 42.1012 | 12.8196 | 896.06 |
| LS-177281 Humidity-Temperature Montefalco | 42.1012 | 12.8196 | 895.55 |
| LS-177320 CrackMeter Conventillo | 42.0237 | 12.8273 | 731.62 |


---

## S014 · highest_node

**Question:** Which sensor node at Ranverso is at the highest altitude?  
**Reference:** LS-170894, at 339.42 m.  
**Recomputed:** `LS-170894` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-170894 | 45.0811 | 7.44991 | 339.42 |
| LS-143276 | 45.0812 | 7.44991 | 339.23 |
| LS-174188 | 45.0812 | 7.44983 | 339.12 |


---

## S015 · lowest_node

**Question:** Which sensor node at Baltanas is at the lowest altitude?  
**Reference:** GNSS_Base, at 779.9 m.  
**Recomputed:** `GNSS_Base` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| GNSS_Base | 41.9372 | -4.24758 | 779.901 |
| Acc-3A | 41.9379 | -4.24331 | 796.895 |
| Gases | 41.9385 | -4.24331 | 797.162 |


---

## S016 · lowest_node

**Question:** Which sensor node at Delos is at the lowest altitude?  
**Reference:** LS-153157, at 12.32 m.  
**Recomputed:** `LS-153157` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-153157 | 37.4033 | 25.2662 | 12.32 |
| LS-150900 | 37.397 | 25.2675 | 17.92 |
| LS-153295 | 37.3984 | 25.2699 | 26.45 |


---

## S017 · lowest_node

**Question:** Which sensor node at Ranverso is at the lowest altitude?  
**Reference:** LS-177315, at 338.89 m.  
**Recomputed:** `LS-177315` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-177315 | 45.0812 | 7.44935 | 338.89 |
| LS-149361 | 45.0812 | 7.44935 | 338.91 |
| LS-149248 | 45.0812 | 7.44983 | 339.11 |


---

## S018 · lowest_node

**Question:** Which sensor node at Schenkenberg is at the lowest altitude?  
**Reference:** LS-149796, at 637.9 m.  
**Recomputed:** `LS-149796` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-149796 | 47.4421 | 8.10104 | 637.9 |
| LS-159070 | 47.4421 | 8.10102 | 640.99 |
| LS-152899 | 47.4421 | 8.10107 | 642.68 |


---

## S019 · altitude_range

**Question:** What is the altitude range of the sensor nodes at Baltanas?  
**Reference:** 18.52 m (from 779.9 m to 798.42 m).  
**Recomputed:** `18.52` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT max(alt) - min(alt) AS range_m, min(alt), max(alt), count(alt) AS nodes FROM n;
```
| range_m | min | max | nodes |
|---|---|---|---|
| 18.5236 | 779.901 | 798.424 | 12 |


---

## S020 · altitude_range

**Question:** What is the altitude range of the sensor nodes at Delos?  
**Reference:** 31.16 m (from 12.32 m to 43.48 m).  
**Recomputed:** `31.16` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT max(alt) - min(alt) AS range_m, min(alt), max(alt), count(alt) AS nodes FROM n;
```
| range_m | min | max | nodes |
|---|---|---|---|
| 31.16 | 12.32 | 43.48 | 15 |


---

## S021 · altitude_range

**Question:** What is the altitude range of the sensor nodes at Lucretili?  
**Reference:** 471.43 m (from 424.63 m to 896.06 m).  
**Recomputed:** `471.43` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT max(alt) - min(alt) AS range_m, min(alt), max(alt), count(alt) AS nodes FROM n;
```
| range_m | min | max | nodes |
|---|---|---|---|
| 471.43 | 424.63 | 896.06 | 13 |


---

## S022 · altitude_range

**Question:** What is the altitude range of the sensor nodes at Ranverso?  
**Reference:** 0.53 m (from 338.89 m to 339.42 m).  
**Recomputed:** `0.53` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT max(alt) - min(alt) AS range_m, min(alt), max(alt), count(alt) AS nodes FROM n;
```
| range_m | min | max | nodes |
|---|---|---|---|
| 0.53 | 338.89 | 339.42 | 7 |


---

## S023 · altitude_range

**Question:** What is the altitude range of the sensor nodes at Schenkenberg?  
**Reference:** 5.63 m (from 637.9 m to 643.53 m).  
**Recomputed:** `5.63` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT max(alt) - min(alt) AS range_m, min(alt), max(alt), count(alt) AS nodes FROM n;
```
| range_m | min | max | nodes |
|---|---|---|---|
| 5.63 | 637.9 | 643.53 | 7 |


---

## S024 · northernmost

**Question:** Which sensor node at Baltanas is the northernmost?  
**Reference:** AF4 (latitude 41.938544).  
**Recomputed:** `AF4` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| AF4 | 41.9385 | -4.24394 | 798.424 |
| Gases | 41.9385 | -4.24331 | 797.162 |
| WP1 | 41.9385 | -4.24384 | 797.842 |


---

## S025 · northernmost

**Question:** Which sensor node at Delos is the northernmost?  
**Reference:** LS-153157 (latitude 37.403328).  
**Recomputed:** `LS-153157` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-153157 | 37.4033 | 25.2662 | 12.32 |
| LS-153295 | 37.3984 | 25.2699 | 26.45 |
| LS-153242 | 37.3977 | 25.2709 | 43.48 |


---

## S026 · northernmost

**Question:** Which sensor node at Lucretili is the northernmost?  
**Reference:** LS-177310 Crackmeter Montefalco (latitude 42.101244).  
**Recomputed:** `LS-177310 Crackmeter Montefalco` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-177310 Crackmeter Montefalco | 42.1012 | 12.8196 | 896.06 |
| LS-177281 Humidity-Temperature Montefalco | 42.1012 | 12.8196 | 895.55 |
| LS-174156 Crackmeter Villa Orazio | 42.0665 | 12.9013 | 425.63 |


---

## S027 · northernmost

**Question:** Which sensor node at Ranverso is the northernmost?  
**Reference:** LS-177315 (latitude 45.081225).  
**Recomputed:** `LS-177315` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-177315 | 45.0812 | 7.44935 | 338.89 |
| LS-149361 | 45.0812 | 7.44935 | 338.91 |
| LS-149248 | 45.0812 | 7.44983 | 339.11 |


---

## S028 · southernmost

**Question:** Which sensor node at Baltanas is the southernmost?  
**Reference:** GNSS_Base (latitude 41.937244).  
**Recomputed:** `GNSS_Base` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| GNSS_Base | 41.9372 | -4.24758 | 779.901 |
| Acc-3A | 41.9379 | -4.24331 | 796.895 |
| GNSS-Rover | 41.9384 | -4.24384 | 797.293 |


---

## S029 · southernmost

**Question:** Which sensor node at Delos is the southernmost?  
**Reference:** H. Fournoi_wall attached 1 (latitude 37.391439).  
**Recomputed:** `H. Fournoi_wall attached 1` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| H. Fournoi_wall attached 1 | 37.3914 | 25.2696 | 35.79 |
| H. Fournoi_pole mounted_outdoors | 37.3921 | 25.2693 | 30.84 |
| Outdoors area H. Masks_Mask_pole mounted | 37.3963 | 25.2698 | 36.99 |


---

## S030 · southernmost

**Question:** Which sensor node at Ranverso is the southernmost?  
**Reference:** LS-170894 (latitude 45.081133).  
**Recomputed:** `LS-170894` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-170894 | 45.0811 | 7.44991 | 339.42 |
| LS-143276 | 45.0812 | 7.44991 | 339.23 |
| LS-174188 | 45.0812 | 7.44983 | 339.12 |


---

## S031 · southernmost

**Question:** Which sensor node at Schenkenberg is the southernmost?  
**Reference:** LS-152479 (latitude 47.442119).  
**Recomputed:** `LS-152479` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-152479 | 47.4421 | 8.10106 | 643.18 |
| LS-152899 | 47.4421 | 8.10107 | 642.68 |
| LS-175480 | 47.4421 | 8.10102 | 642.77 |


---

## S032 · pair_distance

**Question:** What is the distance between sensor nodes AF3 and GNSS-Rover at Baltanas?  
**Reference:** 10.8 m.  
**Recomputed:** `10.8` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'AF3' AND b.label = 'GNSS-Rover';
```
| node_a | node_b | meters |
|---|---|---|
| AF3 | GNSS-Rover | 10.7634 |


---

## S033 · pair_distance

**Question:** What is the distance between sensor nodes AF4 and GNSS_Base at Baltanas?  
**Reference:** 333.7 m.  
**Recomputed:** `333.7` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'AF4' AND b.label = 'GNSS_Base';
```
| node_a | node_b | meters |
|---|---|---|
| AF4 | GNSS_Base | 333.725 |


---

## S034 · pair_distance

**Question:** What is the distance between sensor nodes Acc-2A and AF4 at Baltanas?  
**Reference:** 13.7 m.  
**Recomputed:** `13.7` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'Acc-2A' AND b.label = 'AF4';
```
| node_a | node_b | meters |
|---|---|---|
| Acc-2A | AF4 | 13.6932 |


---

## S035 · pair_distance

**Question:** What is the distance between sensor nodes Gases and P_WL at Baltanas?  
**Reference:** 46.4 m.  
**Recomputed:** `46.4` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'Gases' AND b.label = 'P_WL';
```
| node_a | node_b | meters |
|---|---|---|
| Gases | P_WL | 46.429 |


---

## S036 · pair_distance

**Question:** What is the distance between sensor nodes Gases and WP2 at Baltanas?  
**Reference:** 44.9 m.  
**Recomputed:** `44.9` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'Gases' AND b.label = 'WP2';
```
| node_a | node_b | meters |
|---|---|---|
| Gases | WP2 | 44.8987 |


---

## S037 · pair_distance

**Question:** What is the distance between sensor nodes H. Fournoi_wall attached 1 and H. Masks_Dyonisios &panter mosaic_pole mounted 2 at Delos?  
**Reference:** 540.3 m.  
**Recomputed:** `540.3` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'H. Fournoi_wall attached 1' AND b.label = 'H. Masks_Dyonisios &panter mosaic_pole mounted 2';
```
| node_a | node_b | meters |
|---|---|---|
| H. Fournoi_wall attached 1 | H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 540.269 |


---

## S038 · pair_distance

**Question:** What is the distance between sensor nodes H. Fournoi_wall attached 1 and LS-150900 at Delos?  
**Reference:** 645.7 m.  
**Recomputed:** `645.7` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'H. Fournoi_wall attached 1' AND b.label = 'LS-150900';
```
| node_a | node_b | meters |
|---|---|---|
| H. Fournoi_wall attached 1 | LS-150900 | 645.667 |


---

## S039 · pair_distance

**Question:** What is the distance between sensor nodes H. Masks_Dolphins mosaic_pole mounted and H. Masks_Dyonisios &panter mosaic_pole mounted 2 at Delos?  
**Reference:** 20 m.  
**Recomputed:** `20.0` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'H. Masks_Dolphins mosaic_pole mounted' AND b.label = 'H. Masks_Dyonisios &panter mosaic_pole mounted 2';
```
| node_a | node_b | meters |
|---|---|---|
| H. Masks_Dolphins mosaic_pole mounted | H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 20.0293 |


---

## S040 · pair_distance

**Question:** What is the distance between sensor nodes H. Masks_Mask mosaic_pole mounted 2 and LS-153242 at Delos?  
**Reference:** 199.9 m.  
**Recomputed:** `199.9` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'H. Masks_Mask mosaic_pole mounted 2' AND b.label = 'LS-153242';
```
| node_a | node_b | meters |
|---|---|---|
| H. Masks_Mask mosaic_pole mounted 2 | LS-153242 | 199.897 |


---

## S041 · pair_distance

**Question:** What is the distance between sensor nodes H. Masks_Mask mosaic_pole mounted 2 and Outdoors area H. Masks_Mask_pole mounted at Delos?  
**Reference:** 40.2 m.  
**Recomputed:** `40.2` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'H. Masks_Mask mosaic_pole mounted 2' AND b.label = 'Outdoors area H. Masks_Mask_pole mounted';
```
| node_a | node_b | meters |
|---|---|---|
| H. Masks_Mask mosaic_pole mounted 2 | Outdoors area H. Masks_Mask_pole mounted | 40.249 |


---

## S042 · pair_distance

**Question:** What is the distance between sensor nodes H. Masks_Mask mosaic_window and LS-153295 at Delos?  
**Reference:** 230.8 m.  
**Recomputed:** `230.8` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'H. Masks_Mask mosaic_window' AND b.label = 'LS-153295';
```
| node_a | node_b | meters |
|---|---|---|
| H. Masks_Mask mosaic_window | LS-153295 | 230.804 |


---

## S043 · pair_distance

**Question:** What is the distance between sensor nodes LS-143276 and LS-149248 at Ranverso?  
**Reference:** 7 m.  
**Recomputed:** `7.0` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-143276' AND b.label = 'LS-149248';
```
| node_a | node_b | meters |
|---|---|---|
| LS-143276 | LS-149248 | 7.01043 |


---

## S044 · pair_distance

**Question:** What is the distance between sensor nodes LS-143276 and LS-149361 at Ranverso?  
**Reference:** 44.2 m.  
**Recomputed:** `44.2` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-143276' AND b.label = 'LS-149361';
```
| node_a | node_b | meters |
|---|---|---|
| LS-143276 | LS-149361 | 44.2287 |


---

## S045 · pair_distance

**Question:** What is the distance between sensor nodes LS-143276 and LS-168442 at Ranverso?  
**Reference:** 7 m.  
**Recomputed:** `7.0` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-143276' AND b.label = 'LS-168442';
```
| node_a | node_b | meters |
|---|---|---|
| LS-143276 | LS-168442 | 7.01043 |


---

## S046 · pair_distance

**Question:** What is the distance between sensor nodes LS-149248 and LS-168442 at Ranverso?  
**Reference:** 0 m.  
**Recomputed:** `0.0` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-149248' AND b.label = 'LS-168442';
```
| node_a | node_b | meters |
|---|---|---|
| LS-149248 | LS-168442 | 0 |


---

## S047 · pair_distance

**Question:** What is the distance between sensor nodes LS-149361 and LS-174188 at Ranverso?  
**Reference:** 37.3 m.  
**Recomputed:** `37.3` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-149361' AND b.label = 'LS-174188';
```
| node_a | node_b | meters |
|---|---|---|
| LS-149361 | LS-174188 | 37.3279 |


---

## S048 · pair_distance

**Question:** What is the distance between sensor nodes LS-149361 and LS-177315 at Ranverso?  
**Reference:** 0.9 m.  
**Recomputed:** `0.9` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-149361' AND b.label = 'LS-177315';
```
| node_a | node_b | meters |
|---|---|---|
| LS-149361 | LS-177315 | 0.926624 |


---

## S049 · pair_distance

**Question:** What is the distance between sensor nodes LS-149796 and LS-152479 at Schenkenberg?  
**Reference:** 1.6 m.  
**Recomputed:** `1.6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-149796' AND b.label = 'LS-152479';
```
| node_a | node_b | meters |
|---|---|---|
| LS-149796 | LS-152479 | 1.61786 |


---

## S050 · pair_distance

**Question:** What is the distance between sensor nodes LS-149796 and LS-175480 at Schenkenberg?  
**Reference:** 2.2 m.  
**Recomputed:** `2.2` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-149796' AND b.label = 'LS-175480';
```
| node_a | node_b | meters |
|---|---|---|
| LS-149796 | LS-175480 | 2.17845 |


---

## S051 · pair_distance

**Question:** What is the distance between sensor nodes LS-152479 and LS-152899 at Schenkenberg?  
**Reference:** 0.9 m.  
**Recomputed:** `0.9` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-152479' AND b.label = 'LS-152899';
```
| node_a | node_b | meters |
|---|---|---|
| LS-152479 | LS-152899 | 0.89087 |


---

## S052 · pair_distance

**Question:** What is the distance between sensor nodes LS-152479 and LS-152914 at Schenkenberg?  
**Reference:** 3.5 m.  
**Recomputed:** `3.5` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-152479' AND b.label = 'LS-152914';
```
| node_a | node_b | meters |
|---|---|---|
| LS-152479 | LS-152914 | 3.51995 |


---

## S053 · pair_distance

**Question:** What is the distance between sensor nodes LS-152555 and LS-152914 at Schenkenberg?  
**Reference:** 4.2 m.  
**Recomputed:** `4.2` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-152555' AND b.label = 'LS-152914';
```
| node_a | node_b | meters |
|---|---|---|
| LS-152555 | LS-152914 | 4.157 |


---

## S054 · pair_distance

**Question:** What is the distance between sensor nodes LS-152555 and LS-159070 at Schenkenberg?  
**Reference:** 4.6 m.  
**Recomputed:** `4.6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-152555' AND b.label = 'LS-159070';
```
| node_a | node_b | meters |
|---|---|---|
| LS-152555 | LS-159070 | 4.55761 |


---

## S055 · pair_distance

**Question:** What is the distance between sensor nodes LS-152608 - Tiltmeter Conventillo and LS-177239 - Humidity sensor Conventillo at Lucretili?  
**Reference:** 3.1 m.  
**Recomputed:** `3.1` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-152608 - Tiltmeter Conventillo' AND b.label = 'LS-177239 - Humidity sensor Conventillo';
```
| node_a | node_b | meters |
|---|---|---|
| LS-152608 - Tiltmeter Conventillo | LS-177239 - Humidity sensor Conventillo | 3.1235 |


---

## S056 · pair_distance

**Question:** What is the distance between sensor nodes LS-152608 - Tiltmeter Conventillo and LS-177320 CrackMeter Conventillo at Lucretili?  
**Reference:** 6.7 m.  
**Recomputed:** `6.7` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-152608 - Tiltmeter Conventillo' AND b.label = 'LS-177320 CrackMeter Conventillo';
```
| node_a | node_b | meters |
|---|---|---|
| LS-152608 - Tiltmeter Conventillo | LS-177320 CrackMeter Conventillo | 6.68664 |


---

## S057 · pair_distance

**Question:** What is the distance between sensor nodes LS-152816 Tiltmeter Conventillo and LS-174156 Crackmeter Villa Orazio at Lucretili?  
**Reference:** 7736.3 m.  
**Recomputed:** `7736.3` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-152816 Tiltmeter Conventillo' AND b.label = 'LS-174156 Crackmeter Villa Orazio';
```
| node_a | node_b | meters |
|---|---|---|
| LS-152816 Tiltmeter Conventillo | LS-174156 Crackmeter Villa Orazio | 7736.26 |


---

## S058 · pair_distance

**Question:** What is the distance between sensor nodes LS-159070 and LS-175480 at Schenkenberg?  
**Reference:** 1.9 m.  
**Recomputed:** `1.9` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-159070' AND b.label = 'LS-175480';
```
| node_a | node_b | meters |
|---|---|---|
| LS-159070 | LS-175480 | 1.86499 |


---

## S059 · pair_distance

**Question:** What is the distance between sensor nodes LS-170894 and LS-174188 at Ranverso?  
**Reference:** 8.6 m.  
**Recomputed:** `8.6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a, n b WHERE a.label = 'LS-170894' AND b.label = 'LS-174188';
```
| node_a | node_b | meters |
|---|---|---|
| LS-170894 | LS-174188 | 8.5517 |


---

## S060 · nearest_node

**Question:** Which sensor node is closest to Acc-3A at Baltanas?  
**Reference:** GNSS-Rover, 66.6 m away.  
**Recomputed:** `GNSS-Rover` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'Acc-3A' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| GNSS-Rover | 66.6477 |
| Gases | 67.2218 |
| AF1 | 67.5573 |
| AF2 | 70.3827 |
| P_WL | 71.7545 |


---

## S061 · nearest_node

**Question:** Which sensor node is closest to Gases at Baltanas?  
**Reference:** AF2, 41.2 m away.  
**Recomputed:** `AF2` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'Gases' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| AF2 | 41.2181 |
| WP1 | 43.8516 |
| AF1 | 44.437 |
| WP2 | 44.8987 |
| P_WL | 46.429 |


---

## S062 · nearest_node

**Question:** Which sensor node is closest to H. Masks_Mask mosaic_pole mounted 2 at Delos?  
**Reference:** H. Masks_Masks mosaic_flow meter, 0 m away.  
**Recomputed:** `H. Masks_Masks mosaic_flow meter` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Mask mosaic_pole mounted 2' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| H. Masks_Masks mosaic_flow meter | 0 |
| H. Masks_Mask mosaic_pole mounted | 1.15976 |
| H. Masks_Dyonisios mosaic_pole mounted | 2.69925 |
| H. Masks_Mask mosaic_window | 2.94807 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.85549 |


---

## S063 · nearest_node

**Question:** Which sensor node is closest to H. Masks_Mask mosaic_window at Delos?  
**Reference:** H. Masks_Mask mosaic_pole mounted, 2.2 m away.  
**Recomputed:** `H. Masks_Mask mosaic_pole mounted` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Mask mosaic_window' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| H. Masks_Mask mosaic_pole mounted | 2.16212 |
| H. Masks_Mask mosaic_pole mounted 2 | 2.94807 |
| H. Masks_Masks mosaic_flow meter | 2.94807 |
| H. Masks_Dyonisios mosaic_pole mounted | 4.61259 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.1446 |


---

## S064 · nearest_node

**Question:** Which sensor node is closest to LS-143276 at Ranverso?  
**Reference:** LS-170894, 3.4 m away.  
**Recomputed:** `LS-170894` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-143276' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-170894 | 3.40462 |
| LS-174188 | 6.93518 |
| LS-149248 | 7.01043 |
| LS-168442 | 7.01043 |
| LS-149361 | 44.2287 |


---

## S065 · nearest_node

**Question:** Which sensor node is closest to LS-149248 at Ranverso?  
**Reference:** LS-168442, 0 m away.  
**Recomputed:** `LS-168442` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-149248' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-168442 | 0 |
| LS-174188 | 0.308875 |
| LS-143276 | 7.01043 |
| LS-170894 | 8.73384 |
| LS-149361 | 37.2934 |


---

## S066 · nearest_node

**Question:** Which sensor node is closest to LS-152608 - Tiltmeter Conventillo at Lucretili?  
**Reference:** LS-177239 - Humidity sensor Conventillo, 3.1 m away.  
**Recomputed:** `LS-177239 - Humidity sensor Conventillo` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152608 - Tiltmeter Conventillo' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-177239 - Humidity sensor Conventillo | 3.1235 |
| LS-177253 Crackmeter Conventillo | 3.66595 |
| LS-177266 - Crackmeter Conventillo | 4.19531 |
| LS-152931 Tiltemeter Conventillo | 4.40946 |
| LS-153061 - Tiltmeter Conventillo | 4.42058 |


---

## S067 · nearest_node

**Question:** Which sensor node is closest to LS-152899 at Schenkenberg?  
**Reference:** LS-152479, 0.9 m away.  
**Recomputed:** `LS-152479` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152899' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-152479 | 0.89087 |
| LS-149796 | 2.09607 |
| LS-152555 | 3.45494 |
| LS-152914 | 3.98079 |
| LS-175480 | 3.98115 |


---

## S068 · nearest_node

**Question:** Which sensor node is closest to LS-152914 at Schenkenberg?  
**Reference:** LS-159070, 0.4 m away.  
**Recomputed:** `LS-159070` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152914' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-159070 | 0.417805 |
| LS-149796 | 1.91438 |
| LS-175480 | 1.95635 |
| LS-152479 | 3.51995 |
| LS-152899 | 3.98079 |


---

## S069 · nearest_node

**Question:** Which sensor node is closest to LS-170894 at Ranverso?  
**Reference:** LS-143276, 3.4 m away.  
**Recomputed:** `LS-143276` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-170894' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-143276 | 3.40462 |
| LS-174188 | 8.5517 |
| LS-149248 | 8.73384 |
| LS-168442 | 8.73384 |
| LS-149361 | 45.0197 |


---

## S070 · nearest_node

**Question:** Which sensor node is closest to LS-177266 - Crackmeter Conventillo at Lucretili?  
**Reference:** LS-152931 Tiltemeter Conventillo, 0.2 m away.  
**Recomputed:** `LS-152931 Tiltemeter Conventillo` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177266 - Crackmeter Conventillo' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-152931 Tiltemeter Conventillo | 0.229453 |
| LS-177239 - Humidity sensor Conventillo | 2.63595 |
| LS-152816 Tiltmeter Conventillo | 2.63595 |
| LS-153061 - Tiltmeter Conventillo | 4.07742 |
| LS-152608 - Tiltmeter Conventillo | 4.19531 |


---

## S071 · nearest_node

**Question:** Which sensor node is closest to P_WL at Baltanas?  
**Reference:** Acc-2A, 0.9 m away.  
**Recomputed:** `Acc-2A` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'P_WL' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| Acc-2A | 0.930504 |
| WP2 | 2.34649 |
| AF1 | 4.22 |
| AF2 | 5.26244 |
| AF3 | 5.38551 |


---

## S072 · nearest_node

**Question:** Which sensor node is closest to WP2 at Baltanas?  
**Reference:** P_WL, 2.3 m away.  
**Recomputed:** `P_WL` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'WP2' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| P_WL | 2.34649 |
| Acc-2A | 3.09655 |
| WP1 | 3.22272 |
| AF2 | 3.80202 |
| AF3 | 4.98674 |


---

## S073 · within_radius

**Question:** How many other sensor nodes at Baltanas are within 10 m of P_WL?  
**Reference:** 7.  
**Recomputed:** `7` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'P_WL' ORDER BY meters;
```
| node | meters |
|---|---|
| Acc-2A | 0.930504 |
| WP2 | 2.34649 |
| AF1 | 4.22 |
| AF2 | 5.26244 |
| AF3 | 5.38551 |
| WP1 | 5.49737 |
| GNSS-Rover | 5.64566 |
| AF4 | 13.8147 |
| Gases | 46.429 |
| Acc-3A | 71.7545 |
| GNSS_Base | 334.876 |

- Rows with meters <= 10: 7.

---

## S074 · within_radius

**Question:** How many other sensor nodes at Baltanas are within 50 m of Acc-3A?  
**Reference:** 0.  
**Recomputed:** `0` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'Acc-3A' ORDER BY meters;
```
| node | meters |
|---|---|
| GNSS-Rover | 66.6477 |
| Gases | 67.2218 |
| AF1 | 67.5573 |
| AF2 | 70.3827 |
| P_WL | 71.7545 |
| Acc-2A | 72.064 |
| WP2 | 72.7212 |
| WP1 | 74.9892 |
| AF3 | 77.1392 |
| AF4 | 85.4049 |
| GNSS_Base | 360.872 |

- Rows with meters <= 50: 0.

---

## S075 · within_radius

**Question:** How many other sensor nodes at Delos are within 10 m of H. Masks_Mask mosaic_window?  
**Reference:** 6.  
**Recomputed:** `6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Mask mosaic_window' ORDER BY meters;
```
| node | meters |
|---|---|
| H. Masks_Mask mosaic_pole mounted | 2.16212 |
| H. Masks_Mask mosaic_pole mounted 2 | 2.94807 |
| H. Masks_Masks mosaic_flow meter | 2.94807 |
| H. Masks_Dyonisios mosaic_pole mounted | 4.61259 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.1446 |
| H. Masks_Dolphins mosaic_pole mounted | 8.66394 |
| H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 12.9972 |
| Outdoors area H. Masks_Mask_pole mounted | 38.6927 |
| LS-150900 | 182.327 |
| LS-153242 | 201.276 |
| LS-153295 | 230.804 |
| H. Fournoi_pole mounted_outdoors | 474.282 |
| H. Fournoi_wall attached 1 | 543.057 |
| LS-153157 | 828.058 |

- Rows with meters <= 10: 6.

---

## S076 · within_radius

**Question:** How many other sensor nodes at Delos are within 10 m of H. Masks_Masks mosaic_flow meter?  
**Reference:** 6.  
**Recomputed:** `6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Masks mosaic_flow meter' ORDER BY meters;
```
| node | meters |
|---|---|
| H. Masks_Mask mosaic_pole mounted 2 | 0 |
| H. Masks_Mask mosaic_pole mounted | 1.15976 |
| H. Masks_Dyonisios mosaic_pole mounted | 2.69925 |
| H. Masks_Mask mosaic_window | 2.94807 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.85549 |
| H. Masks_Dolphins mosaic_pole mounted | 9.86212 |
| H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 14.7107 |
| Outdoors area H. Masks_Mask_pole mounted | 40.249 |
| LS-150900 | 180.292 |
| LS-153242 | 199.897 |
| LS-153295 | 228.283 |
| H. Fournoi_pole mounted_outdoors | 477.036 |
| H. Fournoi_wall attached 1 | 545.872 |
| LS-153157 | 825.11 |

- Rows with meters <= 10: 6.

---

## S077 · within_radius

**Question:** How many other sensor nodes at Delos are within 100 m of H. Masks_Dyonisios mosaic_pole mounted?  
**Reference:** 8.  
**Recomputed:** `8` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Dyonisios mosaic_pole mounted' ORDER BY meters;
```
| node | meters |
|---|---|
| H. Masks_Mask mosaic_pole mounted 2 | 2.69925 |
| H. Masks_Masks mosaic_flow meter | 2.69925 |
| H. Masks_Mask mosaic_pole mounted | 3.73228 |
| H. Masks_Mask mosaic_window | 4.61259 |
| H. Masks_Dolphins mosaic_pole mounted | 8.45159 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 11.5497 |
| H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 17.2591 |
| Outdoors area H. Masks_Mask_pole mounted | 42.8707 |
| LS-150900 | 177.827 |
| LS-153242 | 201.749 |
| LS-153295 | 228.858 |
| H. Fournoi_pole mounted_outdoors | 476.98 |
| H. Fournoi_wall attached 1 | 545.981 |
| LS-153157 | 824.201 |

- Rows with meters <= 100: 8.

---

## S078 · within_radius

**Question:** How many other sensor nodes at Delos are within 100 m of H. Masks_Mask mosaic_pole mounted 2?  
**Reference:** 8.  
**Recomputed:** `8` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Mask mosaic_pole mounted 2' ORDER BY meters;
```
| node | meters |
|---|---|
| H. Masks_Masks mosaic_flow meter | 0 |
| H. Masks_Mask mosaic_pole mounted | 1.15976 |
| H. Masks_Dyonisios mosaic_pole mounted | 2.69925 |
| H. Masks_Mask mosaic_window | 2.94807 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.85549 |
| H. Masks_Dolphins mosaic_pole mounted | 9.86212 |
| H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 14.7107 |
| Outdoors area H. Masks_Mask_pole mounted | 40.249 |
| LS-150900 | 180.292 |
| LS-153242 | 199.897 |
| LS-153295 | 228.283 |
| H. Fournoi_pole mounted_outdoors | 477.036 |
| H. Fournoi_wall attached 1 | 545.872 |
| LS-153157 | 825.11 |

- Rows with meters <= 100: 8.

---

## S079 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 100 m of LS-152608 - Tiltmeter Conventillo?  
**Reference:** 7.  
**Recomputed:** `7` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152608 - Tiltmeter Conventillo' ORDER BY meters;
```
| node | meters |
|---|---|
| LS-177239 - Humidity sensor Conventillo | 3.1235 |
| LS-177253 Crackmeter Conventillo | 3.66595 |
| LS-177266 - Crackmeter Conventillo | 4.19531 |
| LS-152931 Tiltemeter Conventillo | 4.40946 |
| LS-153061 - Tiltmeter Conventillo | 4.42058 |
| LS-152816 Tiltmeter Conventillo | 4.90681 |
| LS-177320 CrackMeter Conventillo | 6.68664 |
| LS-177237 Pyranometer Villa Orazio | 7715.17 |
| LS-177287 Crackmeter Villa Orazio | 7729.81 |
| LS-174156 Crackmeter Villa Orazio | 7733.03 |
| LS-177281 Humidity-Temperature Montefalco | 8648.32 |
| LS-177310 Crackmeter Montefalco | 8649.09 |

- Rows with meters <= 100: 7.

---

## S080 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 100 m of LS-177281 Humidity-Temperature Montefalco?  
**Reference:** 1.  
**Recomputed:** `1` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177281 Humidity-Temperature Montefalco' ORDER BY meters;
```
| node | meters |
|---|---|
| LS-177310 Crackmeter Montefalco | 6.19538 |
| LS-177237 Pyranometer Villa Orazio | 7760.75 |
| LS-174156 Crackmeter Villa Orazio | 7767.67 |
| LS-177287 Crackmeter Villa Orazio | 7777.55 |
| LS-177320 CrackMeter Conventillo | 8646 |
| LS-152816 Tiltmeter Conventillo | 8647.04 |
| LS-177239 - Humidity sensor Conventillo | 8647.18 |
| LS-152608 - Tiltmeter Conventillo | 8648.32 |
| LS-152931 Tiltemeter Conventillo | 8649.56 |
| LS-177266 - Crackmeter Conventillo | 8649.57 |
| LS-177253 Crackmeter Conventillo | 8651.81 |
| LS-153061 - Tiltmeter Conventillo | 8652.57 |

- Rows with meters <= 100: 1.

---

## S081 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 100 m of LS-177310 Crackmeter Montefalco?  
**Reference:** 1.  
**Recomputed:** `1` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177310 Crackmeter Montefalco' ORDER BY meters;
```
| node | meters |
|---|---|
| LS-177281 Humidity-Temperature Montefalco | 6.19538 |
| LS-177237 Pyranometer Villa Orazio | 7766.27 |
| LS-174156 Crackmeter Villa Orazio | 7773.2 |
| LS-177287 Crackmeter Villa Orazio | 7783.07 |
| LS-177320 CrackMeter Conventillo | 8646.76 |
| LS-152816 Tiltmeter Conventillo | 8647.81 |
| LS-177239 - Humidity sensor Conventillo | 8647.94 |
| LS-152608 - Tiltmeter Conventillo | 8649.09 |
| LS-152931 Tiltemeter Conventillo | 8650.32 |
| LS-177266 - Crackmeter Conventillo | 8650.34 |
| LS-177253 Crackmeter Conventillo | 8652.58 |
| LS-153061 - Tiltmeter Conventillo | 8653.33 |

- Rows with meters <= 100: 1.

---

## S082 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 500 m of LS-152816 Tiltmeter Conventillo?  
**Reference:** 7.  
**Recomputed:** `7` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152816 Tiltmeter Conventillo' ORDER BY meters;
```
| node | meters |
|---|---|
| LS-177239 - Humidity sensor Conventillo | 1.83563 |
| LS-177320 CrackMeter Conventillo | 1.8543 |
| LS-152931 Tiltemeter Conventillo | 2.56509 |
| LS-177266 - Crackmeter Conventillo | 2.63595 |
| LS-152608 - Tiltmeter Conventillo | 4.90681 |
| LS-153061 - Tiltmeter Conventillo | 6.54119 |
| LS-177253 Crackmeter Conventillo | 7.55514 |
| LS-177237 Pyranometer Villa Orazio | 7718.4 |
| LS-177287 Crackmeter Villa Orazio | 7733.05 |
| LS-174156 Crackmeter Villa Orazio | 7736.26 |
| LS-177281 Humidity-Temperature Montefalco | 8647.04 |
| LS-177310 Crackmeter Montefalco | 8647.81 |

- Rows with meters <= 500: 7.

---

## S083 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 500 m of LS-177266 - Crackmeter Conventillo?  
**Reference:** 7.  
**Recomputed:** `7` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177266 - Crackmeter Conventillo' ORDER BY meters;
```
| node | meters |
|---|---|
| LS-152931 Tiltemeter Conventillo | 0.229453 |
| LS-177239 - Humidity sensor Conventillo | 2.63595 |
| LS-152816 Tiltmeter Conventillo | 2.63595 |
| LS-153061 - Tiltmeter Conventillo | 4.07742 |
| LS-152608 - Tiltmeter Conventillo | 4.19531 |
| LS-177320 CrackMeter Conventillo | 4.23253 |
| LS-177253 Crackmeter Conventillo | 5.59337 |
| LS-177237 Pyranometer Villa Orazio | 7719.2 |
| LS-177287 Crackmeter Villa Orazio | 7733.84 |
| LS-174156 Crackmeter Villa Orazio | 7737.05 |
| LS-177281 Humidity-Temperature Montefalco | 8649.57 |
| LS-177310 Crackmeter Montefalco | 8650.34 |

- Rows with meters <= 500: 7.

---

## S084 · within_radius

**Question:** How many other sensor nodes at Ranverso are within 100 m of LS-149248?  
**Reference:** 6.  
**Recomputed:** `6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-149248' ORDER BY meters;
```
| node | meters |
|---|---|
| LS-168442 | 0 |
| LS-174188 | 0.308875 |
| LS-143276 | 7.01043 |
| LS-170894 | 8.73384 |
| LS-149361 | 37.2934 |
| LS-177315 | 37.4045 |

- Rows with meters <= 100: 6.

---

## S085 · within_radius

**Question:** How many other sensor nodes at Ranverso are within 500 m of LS-174188?  
**Reference:** 6.  
**Recomputed:** `6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-174188' ORDER BY meters;
```
| node | meters |
|---|---|
| LS-149248 | 0.308875 |
| LS-168442 | 0.308875 |
| LS-143276 | 6.93518 |
| LS-170894 | 8.5517 |
| LS-149361 | 37.3279 |
| LS-177315 | 37.4466 |

- Rows with meters <= 500: 6.

---

## S086 · within_radius

**Question:** How many other sensor nodes at Ranverso are within 500 m of LS-177315?  
**Reference:** 6.  
**Recomputed:** `6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177315' ORDER BY meters;
```
| node | meters |
|---|---|
| LS-149361 | 0.926624 |
| LS-149248 | 37.4045 |
| LS-168442 | 37.4045 |
| LS-174188 | 37.4466 |
| LS-143276 | 44.3612 |
| LS-170894 | 45.2195 |

- Rows with meters <= 500: 6.

---

## S087 · within_radius

**Question:** How many other sensor nodes at Schenkenberg are within 50 m of LS-152555?  
**Reference:** 6.  
**Recomputed:** `6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152555' ORDER BY meters;
```
| node | meters |
|---|---|
| LS-152899 | 3.45494 |
| LS-149796 | 3.51995 |
| LS-152479 | 3.98453 |
| LS-152914 | 4.157 |
| LS-159070 | 4.55761 |
| LS-175480 | 5.53735 |

- Rows with meters <= 50: 6.

---

## S088 · site_distance

**Question:** How far apart are Baltanas and Delos, measured between the centroids of their sensor nodes?  
**Reference:** 2562.8 km.  
**Recomputed:** `2562.8` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'baltanas' AND b.site_id = 'delos';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 41.9383 | -4.24408 | 37.3964 | 25.2692 | 2562.83 |


---

## S089 · site_distance

**Question:** How far apart are Baltanas and Lucretili, measured between the centroids of their sensor nodes?  
**Reference:** 1409.9 km.  
**Recomputed:** `1409.9` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'baltanas' AND b.site_id = 'lucretili';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 41.9383 | -4.24408 | 42.0455 | 12.8432 | 1409.87 |


---

## S090 · site_distance

**Question:** How far apart are Baltanas and Ranverso, measured between the centroids of their sensor nodes?  
**Reference:** 1004.6 km.  
**Recomputed:** `1004.6` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'baltanas' AND b.site_id = 'ranverso';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 41.9383 | -4.24408 | 45.0812 | 7.44972 | 1004.58 |


---

## S091 · site_distance

**Question:** How far apart are Baltanas and Schenkenberg, measured between the centroids of their sensor nodes?  
**Reference:** 1149.9 km.  
**Recomputed:** `1149.9` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'baltanas' AND b.site_id = 'schenkenberg';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 41.9383 | -4.24408 | 47.4421 | 8.10104 | 1149.87 |


---

## S092 · site_distance

**Question:** How far apart are Delos and Lucretili, measured between the centroids of their sensor nodes?  
**Reference:** 1180.2 km.  
**Recomputed:** `1180.2` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'delos' AND b.site_id = 'lucretili';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 37.3964 | 25.2692 | 42.0455 | 12.8432 | 1180.25 |


---

## S093 · site_distance

**Question:** How far apart are Delos and Ranverso, measured between the centroids of their sensor nodes?  
**Reference:** 1712.1 km.  
**Recomputed:** `1712.1` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'delos' AND b.site_id = 'ranverso';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 37.3964 | 25.2692 | 45.0812 | 7.44972 | 1712.13 |


---

## S094 · site_distance

**Question:** How far apart are Delos and Schenkenberg, measured between the centroids of their sensor nodes?  
**Reference:** 1791.4 km.  
**Recomputed:** `1791.4` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'delos' AND b.site_id = 'schenkenberg';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 37.3964 | 25.2692 | 47.4421 | 8.10104 | 1791.43 |


---

## S095 · site_distance

**Question:** How far apart are Lucretili and Ranverso, measured between the centroids of their sensor nodes?  
**Reference:** 550.1 km.  
**Recomputed:** `550.1` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'lucretili' AND b.site_id = 'ranverso';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 42.0455 | 12.8432 | 45.0812 | 7.44972 | 550.061 |


---

## S096 · site_distance

**Question:** How far apart are Lucretili and Schenkenberg, measured between the centroids of their sensor nodes?  
**Reference:** 707 km.  
**Recomputed:** `707.0` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'lucretili' AND b.site_id = 'schenkenberg';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 42.0455 | 12.8432 | 47.4421 | 8.10104 | 707.049 |


---

## S097 · site_distance

**Question:** How far apart are Ranverso and Schenkenberg, measured between the centroids of their sensor nodes?  
**Reference:** 267.3 km.  
**Recomputed:** `267.3` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'ranverso' AND b.site_id = 'schenkenberg';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 45.0812 | 7.44972 | 47.4421 | 8.10104 | 267.255 |


---

## S098 · unanswerable

**Question:** How far are the Baltanas sensor nodes from the nearest river?  
**Reference:** Cannot be answered from the knowledge graph.  
→ **MANUAL** (no KG data can answer it)

---

## S099 · unanswerable

**Question:** What is the height of the Schenkenberg castle tower?  
**Reference:** Cannot be answered from the knowledge graph.  
→ **MANUAL** (no KG data can answer it)

---

## S100 · unanswerable

**Question:** Which sensor node at Delos is closest to the harbour?  
**Reference:** Cannot be answered from the knowledge graph.  
→ **MANUAL** (no KG data can answer it)

---
