# Verification — spatial

Run `SET TIME ZONE 'UTC';` in psql first (`psql -h localhost -U argus -d argus_snapshot`).

## S001 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Baltanas?  
**Reference:** 382.3 m, between A8610A3230467704 and GNSS_Base. With the altitude difference: 382.7 m, between A8610A3230467704 and GNSS_Base.  
**Recomputed:** `382.3` (with the altitude difference: `382.7`) → **MATCH**

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
| A8610A3230467704 | GNSS_Base | 382.302 |
| Gases | GNSS_Base | 380.928 |
| Acc-3A | GNSS_Base | 360.959 |
| AF2 | GNSS_Base | 340.136 |
| WP1 | GNSS_Base | 338.548 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| A8610A3230467704 | GNSS_Base | 382.688 |
| Gases | GNSS_Base | 381.315 |
| Acc-3A | GNSS_Base | 361.357 |
| AF2 | GNSS_Base | 340.592 |
| WP1 | GNSS_Base | 339.019 |


---

## S002 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Delos?  
**Reference:** 1669.9 m, between 0004A30B0050C42F and H. Fournoi_wall attached 1. With the altitude difference: 1670.1 m, between 0004A30B0050C42F and H. Fournoi_wall attached 1.  
**Recomputed:** `1669.9` (with the altitude difference: `1670.1`) → **MATCH**

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
| 0004A30B0050C42F | H. Fournoi_wall attached 1 | 1669.92 |
| 0004A30B0050C42F | H. Fournoi_pole mounted_outdoors | 1612.35 |
| 0004A30B0050C42F | 2CF7F1C0723001F4 | 1612.35 |
| LS-153157 | H. Fournoi_wall attached 1 | 1355.57 |
| H. Fournoi_pole mounted_outdoors | LS-153157 | 1281.68 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| 0004A30B0050C42F | H. Fournoi_wall attached 1 | 1670.12 |
| 0004A30B0050C42F | H. Fournoi_pole mounted_outdoors | 1612.49 |
| 0004A30B0050C42F | 2CF7F1C0723001F4 | 1612.49 |
| LS-153157 | H. Fournoi_wall attached 1 | 1355.77 |
| H. Fournoi_pole mounted_outdoors | LS-153157 | 1281.82 |


---

## S003 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Lucretili?  
**Reference:** 8653.3 m, between LS-153061 - Tiltmeter Conventillo and LS-177310 Crackmeter Montefalco. With the altitude difference: 8655.2 m, between LS-153061 - Tiltmeter Conventillo and LS-177310 Crackmeter Montefalco.  
**Recomputed:** `8653.3` (with the altitude difference: `8655.2`) → **MATCH**

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

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| LS-153061 - Tiltmeter Conventillo | LS-177310 Crackmeter Montefalco | 8655.18 |
| LS-177281 Humidity-Temperature Montefalco | LS-153061 - Tiltmeter Conventillo | 8654.4 |
| LS-177253 Crackmeter Conventillo | LS-177310 Crackmeter Montefalco | 8654.39 |
| LS-177281 Humidity-Temperature Montefalco | LS-177253 Crackmeter Conventillo | 8653.61 |
| LS-177310 Crackmeter Montefalco | LS-177266 - Crackmeter Conventillo | 8652.06 |


---

## S004 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Ranverso?  
**Reference:** 45.2 m, between LS-170894 and LS-177315.  
**Recomputed:** `45.2` (with the altitude difference: `45.2`) → **MATCH**

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
| LS-177315 | A8610A333526680F | 39.1749 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| LS-177315 | LS-170894 | 45.2226 |
| LS-149361 | LS-170894 | 45.0226 |
| LS-177315 | LS-143276 | 44.3625 |
| LS-149361 | LS-143276 | 44.2299 |
| LS-177315 | A8610A333526680F | 39.1756 |


---

## S005 · farthest_pair

**Question:** How far apart are the two most distant sensor nodes at Schenkenberg?  
**Reference:** 5.3 m, between LS-152555 and LS-175480. With the altitude difference: 8.4 m, between 2CF7F1C072300226 and 2CF7F1C072600345.  
**Recomputed:** `5.3` (with the altitude difference: `8.4`) → **MATCH**

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
| LS-175480 | LS-152555 | 5.29804 |
| LS-159070 | LS-152555 | 4.60259 |
| LS-159070 | LS-152899 | 4.49877 |
| LS-152914 | LS-152555 | 4.24127 |
| LS-152914 | LS-152899 | 4.17605 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id < b.node_id ORDER BY meters DESC LIMIT 5;
```
| node_a | node_b | meters |
|---|---|---|
| 2CF7F1C072300226 | 2CF7F1C072600345 | 8.35366 |
| 2CF7F1C072300226 | LS-149796 | 7.86344 |
| 2CF7F1C072600345 | LS-152555 | 6.66012 |
| 2CF7F1C072300226 | LS-159070 | 6.5424 |
| LS-149796 | LS-152555 | 6.25198 |


---

## S006 · centroid

**Question:** What is the centroid of the sensor nodes at Baltanas?  
**Reference:** Latitude 41.938386, longitude -4.244170 (mean of 15 nodes).  
**Recomputed:** `[41.938386, -4.24417]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 41.9384 | -4.24417 | 15 |


---

## S007 · centroid

**Question:** What is the centroid of the sensor nodes at Delos?  
**Reference:** Latitude 37.396699, longitude 25.269551 (mean of 19 nodes).  
**Recomputed:** `[37.396699, 25.269551]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 37.3967 | 25.2696 | 19 |


---

## S008 · centroid

**Question:** What is the centroid of the sensor nodes at Lucretili?  
**Reference:** Latitude 42.048244, longitude 12.851007 (mean of 15 nodes).  
**Recomputed:** `[42.048244, 12.851007]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 42.0482 | 12.851 | 15 |


---

## S009 · centroid

**Question:** What is the centroid of the sensor nodes at Ranverso?  
**Reference:** Latitude 45.081158, longitude 7.449714 (mean of 10 nodes).  
**Recomputed:** `[45.081158, 7.449714]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 45.0812 | 7.44971 | 10 |


---

## S010 · centroid

**Question:** What is the centroid of the sensor nodes at Schenkenberg?  
**Reference:** Latitude 47.442132, longitude 8.101022 (mean of 9 nodes).  
**Recomputed:** `[47.442132, 8.101022]` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT avg(lat) AS lat, avg(lon) AS lon, count(*) AS nodes FROM n;
```
| lat | lon | nodes |
|---|---|---|
| 47.4421 | 8.10102 | 9 |


---

## S011 · highest_node

**Question:** Which sensor node at Baltanas is at the highest altitude?  
**Reference:** AF4, at 798.38 m.  
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
| AF4 | 41.9385 | -4.24394 | 798.38 |
| AF3 | 41.9385 | -4.2439 | 797.81 |
| WP1 | 41.9385 | -4.24384 | 797.75 |


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
| 2CF7F1C061300548 | 37.3963 | 25.2698 | 36.99 |
| Outdoors area H. Masks_Mask_pole mounted | 37.3963 | 25.2698 | 36.99 |


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
**Reference:** ae_ranverso, at 340.16 m.  
**Recomputed:** `ae_ranverso` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| ae_ranverso | 45.0811 | 7.44965 | 340.16 |
| A8610A3338359111 | 45.0811 | 7.44964 | 340.09 |
| LS-170894 | 45.0811 | 7.44991 | 339.42 |


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
| 2CF7F1C073400212 | 41.9391 | -4.24658 | 789.85 |
| Acc-3A | 41.9379 | -4.24331 | 796.85 |


---

## S016 · lowest_node

**Question:** Which sensor node at Delos is at the lowest altitude?  
**Reference:** 0004A30B0050C42F, at 9.64 m.  
**Recomputed:** `0004A30B0050C42F` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| 0004A30B0050C42F | 37.406 | 25.2744 | 9.64 |
| LS-153157 | 37.4033 | 25.2662 | 12.32 |
| LS-150900 | 37.397 | 25.2675 | 17.92 |


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
| LS-168442 | 45.0812 | 7.44983 | 339.11 |


---

## S018 · lowest_node

**Question:** Which sensor node at Schenkenberg is at the lowest altitude?  
**Reference:** 2CF7F1C072600345, at 643 m.  
**Recomputed:** `2CF7F1C072600345` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| 2CF7F1C072600345 | 47.4421 | 8.10102 | 643 |
| LS-149796 | 47.4421 | 8.10102 | 643.5 |
| LS-159070 | 47.4421 | 8.10099 | 645.99 |


---

## S019 · altitude_range

**Question:** What is the altitude range of the sensor nodes at Baltanas?  
**Reference:** 18.48 m (from 779.9 m to 798.38 m).  
**Recomputed:** `18.48` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT max(alt) - min(alt) AS range_m, min(alt), max(alt), count(alt) AS nodes FROM n;
```
| range_m | min | max | nodes |
|---|---|---|---|
| 18.4793 | 779.901 | 798.38 | 15 |


---

## S020 · altitude_range

**Question:** What is the altitude range of the sensor nodes at Delos?  
**Reference:** 33.84 m (from 9.64 m to 43.48 m).  
**Recomputed:** `33.84` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT max(alt) - min(alt) AS range_m, min(alt), max(alt), count(alt) AS nodes FROM n;
```
| range_m | min | max | nodes |
|---|---|---|---|
| 33.84 | 9.64 | 43.48 | 19 |


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
| 471.43 | 424.63 | 896.06 | 15 |


---

## S022 · altitude_range

**Question:** What is the altitude range of the sensor nodes at Ranverso?  
**Reference:** 1.27 m (from 338.89 m to 340.16 m).  
**Recomputed:** `1.27` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT max(alt) - min(alt) AS range_m, min(alt), max(alt), count(alt) AS nodes FROM n;
```
| range_m | min | max | nodes |
|---|---|---|---|
| 1.27 | 338.89 | 340.16 | 10 |


---

## S023 · altitude_range

**Question:** What is the altitude range of the sensor nodes at Schenkenberg?  
**Reference:** 8.2 m (from 643 m to 651.2 m).  
**Recomputed:** `8.2` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT max(alt) - min(alt) AS range_m, min(alt), max(alt), count(alt) AS nodes FROM n;
```
| range_m | min | max | nodes |
|---|---|---|---|
| 8.2 | 643 | 651.2 | 9 |


---

## S024 · northernmost

**Question:** Which sensor node at Baltanas is the northernmost?  
**Reference:** 2CF7F1C073400212 (latitude 41.939097).  
**Recomputed:** `2CF7F1C073400212` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| 2CF7F1C073400212 | 41.9391 | -4.24658 | 789.85 |
| AF4 | 41.9385 | -4.24394 | 798.38 |
| Gases | 41.9385 | -4.24331 | 797.07 |


---

## S025 · northernmost

**Question:** Which sensor node at Delos is the northernmost?  
**Reference:** 0004A30B0050C42F (latitude 37.405975).  
**Recomputed:** `0004A30B0050C42F` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| 0004A30B0050C42F | 37.406 | 25.2744 | 9.64 |
| LS-153157 | 37.4033 | 25.2662 | 12.32 |
| LS-153295 | 37.3984 | 25.2699 | 26.45 |


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
| LS-168442 | 45.0812 | 7.44983 | 339.11 |


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
| Acc-3A | 41.9379 | -4.24331 | 796.85 |
| GNSS-Rover | 41.9384 | -4.24384 | 797.22 |


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
| 2CF7F1C0723001F4 | 37.3921 | 25.2693 | 30.84 |


---

## S030 · southernmost

**Question:** Which sensor node at Ranverso is the southernmost?  
**Reference:** ae_ranverso (latitude 45.081058).  
**Recomputed:** `ae_ranverso` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE lat IS NOT NULL ORDER BY lat ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| ae_ranverso | 45.0811 | 7.44965 | 340.16 |
| A8610A3338359111 | 45.0811 | 7.44964 | 340.09 |
| LS-170894 | 45.0811 | 7.44991 | 339.42 |


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
| LS-152479 | 47.4421 | 8.10103 | 648.18 |
| LS-152899 | 47.4421 | 8.10104 | 647.3 |
| LS-175480 | 47.4421 | 8.10099 | 648.18 |


---

## S032 · pair_distance

**Question:** What is the distance between sensor nodes AF3 and GNSS-Rover at Baltanas?  
**Reference:** 11 m.  
**Recomputed:** `11.0` (with the altitude difference: `11.0`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'AF3' AND b.label = 'GNSS-Rover';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| AF3 | GNSS-Rover | 10.9988 | 11.0146 |


---

## S033 · pair_distance

**Question:** What is the distance between sensor nodes AF4 and GNSS_Base at Baltanas?  
**Reference:** 333.7 m. With the altitude difference: 334.2 m.  
**Recomputed:** `333.7` (with the altitude difference: `334.2`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'AF4' AND b.label = 'GNSS_Base';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| AF4 | GNSS_Base | 333.68 | 334.191 |


---

## S034 · pair_distance

**Question:** What is the distance between sensor nodes Acc-2A and AF4 at Baltanas?  
**Reference:** 13.7 m. With the altitude difference: 13.8 m.  
**Recomputed:** `13.7` (with the altitude difference: `13.8`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'Acc-2A' AND b.label = 'AF4';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| Acc-2A | AF4 | 13.7234 | 13.751 |


---

## S035 · pair_distance

**Question:** What is the distance between sensor nodes Gases and P_WL at Baltanas?  
**Reference:** 46.5 m.  
**Recomputed:** `46.5` (with the altitude difference: `46.5`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'Gases' AND b.label = 'P_WL';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| Gases | P_WL | 46.4606 | 46.4627 |


---

## S036 · pair_distance

**Question:** What is the distance between sensor nodes Gases and WP2 at Baltanas?  
**Reference:** 45.1 m.  
**Recomputed:** `45.1` (with the altitude difference: `45.1`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'Gases' AND b.label = 'WP2';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| Gases | WP2 | 45.0767 | 45.0798 |


---

## S037 · pair_distance

**Question:** What is the distance between sensor nodes H. Fournoi_wall attached 1 and H. Masks_Dyonisios &panter mosaic_pole mounted 2 at Delos?  
**Reference:** 540.3 m.  
**Recomputed:** `540.3` (with the altitude difference: `540.3`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'H. Fournoi_wall attached 1' AND b.label = 'H. Masks_Dyonisios &panter mosaic_pole mounted 2';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| H. Fournoi_wall attached 1 | H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 540.269 | 540.269 |


---

## S038 · pair_distance

**Question:** What is the distance between sensor nodes H. Fournoi_wall attached 1 and LS-150900 at Delos?  
**Reference:** 645.7 m. With the altitude difference: 645.9 m.  
**Recomputed:** `645.7` (with the altitude difference: `645.9`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'H. Fournoi_wall attached 1' AND b.label = 'LS-150900';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| H. Fournoi_wall attached 1 | LS-150900 | 645.667 | 645.914 |


---

## S039 · pair_distance

**Question:** What is the distance between sensor nodes H. Masks_Dolphins mosaic_pole mounted and H. Masks_Dyonisios &panter mosaic_pole mounted 2 at Delos?  
**Reference:** 20 m. With the altitude difference: 20.1 m.  
**Recomputed:** `20.0` (with the altitude difference: `20.1`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'H. Masks_Dolphins mosaic_pole mounted' AND b.label = 'H. Masks_Dyonisios &panter mosaic_pole mounted 2';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| H. Masks_Dolphins mosaic_pole mounted | H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 20.0293 | 20.0584 |


---

## S040 · pair_distance

**Question:** What is the distance between sensor nodes H. Masks_Mask mosaic_pole mounted 2 and LS-153242 at Delos?  
**Reference:** 199.9 m. With the altitude difference: 200.1 m.  
**Recomputed:** `199.9` (with the altitude difference: `200.1`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'H. Masks_Mask mosaic_pole mounted 2' AND b.label = 'LS-153242';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| H. Masks_Mask mosaic_pole mounted 2 | LS-153242 | 199.897 | 200.066 |


---

## S041 · pair_distance

**Question:** What is the distance between sensor nodes H. Masks_Mask mosaic_pole mounted 2 and Outdoors area H. Masks_Mask_pole mounted at Delos?  
**Reference:** 40.2 m. With the altitude difference: 40.3 m.  
**Recomputed:** `40.2` (with the altitude difference: `40.3`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'H. Masks_Mask mosaic_pole mounted 2' AND b.label = 'Outdoors area H. Masks_Mask_pole mounted';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| H. Masks_Mask mosaic_pole mounted 2 | Outdoors area H. Masks_Mask_pole mounted | 40.249 | 40.2866 |


---

## S042 · pair_distance

**Question:** What is the distance between sensor nodes H. Masks_Mask mosaic_window and LS-153295 at Delos?  
**Reference:** 230.8 m. With the altitude difference: 231 m.  
**Recomputed:** `230.8` (with the altitude difference: `231.0`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'H. Masks_Mask mosaic_window' AND b.label = 'LS-153295';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| H. Masks_Mask mosaic_window | LS-153295 | 230.804 | 230.967 |


---

## S043 · pair_distance

**Question:** What is the distance between sensor nodes LS-143276 and LS-149248 at Ranverso?  
**Reference:** 7 m.  
**Recomputed:** `7.0` (with the altitude difference: `7.0`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-143276' AND b.label = 'LS-149248';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-143276 | LS-149248 | 7.01043 | 7.01145 |


---

## S044 · pair_distance

**Question:** What is the distance between sensor nodes LS-143276 and LS-149361 at Ranverso?  
**Reference:** 44.2 m.  
**Recomputed:** `44.2` (with the altitude difference: `44.2`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-143276' AND b.label = 'LS-149361';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-143276 | LS-149361 | 44.2287 | 44.2299 |


---

## S045 · pair_distance

**Question:** What is the distance between sensor nodes LS-143276 and LS-168442 at Ranverso?  
**Reference:** 7 m.  
**Recomputed:** `7.0` (with the altitude difference: `7.0`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-143276' AND b.label = 'LS-168442';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-143276 | LS-168442 | 7.01043 | 7.01145 |


---

## S046 · pair_distance

**Question:** What is the distance between sensor nodes LS-149248 and LS-168442 at Ranverso?  
**Reference:** 0 m.  
**Recomputed:** `0.0` (with the altitude difference: `0.0`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-149248' AND b.label = 'LS-168442';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-149248 | LS-168442 | 0 | 0 |


---

## S047 · pair_distance

**Question:** What is the distance between sensor nodes LS-149361 and LS-174188 at Ranverso?  
**Reference:** 37.3 m.  
**Recomputed:** `37.3` (with the altitude difference: `37.3`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-149361' AND b.label = 'LS-174188';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-149361 | LS-174188 | 37.3279 | 37.3285 |


---

## S048 · pair_distance

**Question:** What is the distance between sensor nodes LS-149361 and LS-177315 at Ranverso?  
**Reference:** 0.9 m.  
**Recomputed:** `0.9` (with the altitude difference: `0.9`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-149361' AND b.label = 'LS-177315';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-149361 | LS-177315 | 0.926624 | 0.92684 |


---

## S049 · pair_distance

**Question:** What is the distance between sensor nodes LS-149796 and LS-152479 at Schenkenberg?  
**Reference:** 1.5 m. With the altitude difference: 4.9 m.  
**Recomputed:** `1.5` (with the altitude difference: `4.9`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-149796' AND b.label = 'LS-152479';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-149796 | LS-152479 | 1.508 | 4.91696 |


---

## S050 · pair_distance

**Question:** What is the distance between sensor nodes LS-149796 and LS-175480 at Schenkenberg?  
**Reference:** 1.8 m. With the altitude difference: 5 m.  
**Recomputed:** `1.8` (with the altitude difference: `5.0`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-149796' AND b.label = 'LS-175480';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-149796 | LS-175480 | 1.83549 | 5.02707 |


---

## S051 · pair_distance

**Question:** What is the distance between sensor nodes LS-152479 and LS-152899 at Schenkenberg?  
**Reference:** 0.9 m. With the altitude difference: 1.3 m.  
**Recomputed:** `0.9` (with the altitude difference: `1.3`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-152479' AND b.label = 'LS-152899';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-152479 | LS-152899 | 0.891981 | 1.25301 |


---

## S052 · pair_distance

**Question:** What is the distance between sensor nodes LS-152479 and LS-152914 at Schenkenberg?  
**Reference:** 3.7 m.  
**Recomputed:** `3.7` (with the altitude difference: `3.7`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-152479' AND b.label = 'LS-152914';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-152479 | LS-152914 | 3.72433 | 3.73982 |


---

## S053 · pair_distance

**Question:** What is the distance between sensor nodes LS-152555 and LS-152914 at Schenkenberg?  
**Reference:** 4.2 m.  
**Recomputed:** `4.2` (with the altitude difference: `4.2`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-152555' AND b.label = 'LS-152914';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-152555 | LS-152914 | 4.24127 | 4.24127 |


---

## S054 · pair_distance

**Question:** What is the distance between sensor nodes LS-152555 and LS-159070 at Schenkenberg?  
**Reference:** 4.6 m. With the altitude difference: 5.3 m.  
**Recomputed:** `4.6` (with the altitude difference: `5.3`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-152555' AND b.label = 'LS-159070';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-152555 | LS-159070 | 4.60259 | 5.25212 |


---

## S055 · pair_distance

**Question:** What is the distance between sensor nodes LS-152608 - Tiltmeter Conventillo and LS-177239 - Humidity sensor Conventillo at Lucretili?  
**Reference:** 3.1 m. With the altitude difference: 3.8 m.  
**Recomputed:** `3.1` (with the altitude difference: `3.8`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-152608 - Tiltmeter Conventillo' AND b.label = 'LS-177239 - Humidity sensor Conventillo';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-152608 - Tiltmeter Conventillo | LS-177239 - Humidity sensor Conventillo | 3.1235 | 3.82051 |


---

## S056 · pair_distance

**Question:** What is the distance between sensor nodes LS-152608 - Tiltmeter Conventillo and LS-177320 CrackMeter Conventillo at Lucretili?  
**Reference:** 6.7 m. With the altitude difference: 7.6 m.  
**Recomputed:** `6.7` (with the altitude difference: `7.6`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-152608 - Tiltmeter Conventillo' AND b.label = 'LS-177320 CrackMeter Conventillo';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-152608 - Tiltmeter Conventillo | LS-177320 CrackMeter Conventillo | 6.68664 | 7.6324 |


---

## S057 · pair_distance

**Question:** What is the distance between sensor nodes LS-152816 Tiltmeter Conventillo and LS-174156 Crackmeter Villa Orazio at Lucretili?  
**Reference:** 7736.3 m. With the altitude difference: 7742.2 m.  
**Recomputed:** `7736.3` (with the altitude difference: `7742.2`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-152816 Tiltmeter Conventillo' AND b.label = 'LS-174156 Crackmeter Villa Orazio';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-152816 Tiltmeter Conventillo | LS-174156 Crackmeter Villa Orazio | 7736.26 | 7742.21 |


---

## S058 · pair_distance

**Question:** What is the distance between sensor nodes LS-159070 and LS-175480 at Schenkenberg?  
**Reference:** 1.9 m. With the altitude difference: 2.9 m.  
**Recomputed:** `1.9` (with the altitude difference: `2.9`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-159070' AND b.label = 'LS-175480';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-159070 | LS-175480 | 1.89629 | 2.8969 |


---

## S059 · pair_distance

**Question:** What is the distance between sensor nodes LS-170894 and LS-174188 at Ranverso?  
**Reference:** 8.6 m.  
**Recomputed:** `8.6` (with the altitude difference: `8.6`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT a.label AS node_a, b.label AS node_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters,
       sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a, n b WHERE a.label = 'LS-170894' AND b.label = 'LS-174188';
```
| node_a | node_b | meters | meters_with_alt |
|---|---|---|---|
| LS-170894 | LS-174188 | 8.5517 | 8.55696 |


---

## S060 · nearest_node

**Question:** Which sensor node is closest to Acc-3A at Baltanas?  
**Reference:** sensor, 65.2 m away.  
**Recomputed:** `sensor` (with the altitude difference: `sensor`) → **MATCH**

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
| sensor | 65.2259 |
| GNSS-Rover | 66.6372 |
| A8610A3230467704 | 67.0451 |
| Gases | 67.3347 |
| AF1 | 67.51 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'Acc-3A' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| sensor | 65.2272 |
| GNSS-Rover | 66.6382 |
| A8610A3230467704 | 67.0456 |
| Gases | 67.3351 |
| AF1 | 67.5117 |


---

## S061 · nearest_node

**Question:** Which sensor node is closest to Gases at Baltanas?  
**Reference:** A8610A3230467704, 1.6 m away.  
**Recomputed:** `A8610A3230467704` (with the altitude difference: `A8610A3230467704`) → **MATCH**

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
| A8610A3230467704 | 1.63771 |
| AF2 | 41.3325 |
| sensor | 42.4293 |
| WP1 | 43.8619 |
| AF1 | 44.4818 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'Gases' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| A8610A3230467704 | 1.63783 |
| AF2 | 41.3349 |
| sensor | 42.4297 |
| WP1 | 43.8672 |
| AF1 | 44.4825 |


---

## S062 · nearest_node

**Question:** Which sensor node is closest to H. Masks_Mask mosaic_pole mounted 2 at Delos?  
**Reference:** H. Masks_Masks mosaic_flow meter, 0 m away.  
**Recomputed:** `H. Masks_Masks mosaic_flow meter` (with the altitude difference: `H. Masks_Masks mosaic_flow meter`) → **MATCH**

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

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Mask mosaic_pole mounted 2' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| H. Masks_Masks mosaic_flow meter | 0 |
| H. Masks_Mask mosaic_pole mounted | 1.15993 |
| H. Masks_Dyonisios mosaic_pole mounted | 2.70238 |
| H. Masks_Mask mosaic_window | 2.95094 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.8563 |


---

## S063 · nearest_node

**Question:** Which sensor node is closest to H. Masks_Mask mosaic_window at Delos?  
**Reference:** H. Masks_Mask mosaic_pole mounted, 2.2 m away.  
**Recomputed:** `H. Masks_Mask mosaic_pole mounted` (with the altitude difference: `H. Masks_Mask mosaic_pole mounted`) → **MATCH**

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

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Mask mosaic_window' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| H. Masks_Mask mosaic_pole mounted | 2.16732 |
| H. Masks_Mask mosaic_pole mounted 2 | 2.95094 |
| H. Masks_Masks mosaic_flow meter | 2.95094 |
| H. Masks_Dyonisios mosaic_pole mounted | 4.61259 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.14844 |


---

## S064 · nearest_node

**Question:** Which sensor node is closest to LS-143276 at Ranverso?  
**Reference:** LS-170894, 3.4 m away.  
**Recomputed:** `LS-170894` (with the altitude difference: `LS-170894`) → **MATCH**

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
| A8610A333526680F | 5.24861 |
| LS-174188 | 6.93518 |
| LS-168442 | 7.01043 |
| LS-149248 | 7.01043 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-143276' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-170894 | 3.40991 |
| A8610A333526680F | 5.24976 |
| LS-174188 | 6.93605 |
| LS-168442 | 7.01145 |
| LS-149248 | 7.01145 |


---

## S065 · nearest_node

**Question:** Which sensor node is closest to LS-149248 at Ranverso?  
**Reference:** LS-168442, 0 m away.  
**Recomputed:** `LS-168442` (with the altitude difference: `LS-168442`) → **MATCH**

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
| A8610A333526680F | 1.77191 |
| LS-143276 | 7.01043 |
| LS-170894 | 8.73384 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-149248' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-168442 | 0 |
| LS-174188 | 0.309037 |
| A8610A333526680F | 1.77194 |
| LS-143276 | 7.01145 |
| LS-170894 | 8.73934 |


---

## S066 · nearest_node

**Question:** Which sensor node is closest to LS-152608 - Tiltmeter Conventillo at Lucretili?  
**Reference:** LS-177239 - Humidity sensor Conventillo, 3.1 m away. With the altitude difference: LS-177239 - Humidity sensor Conventillo, 3.8 m away.  
**Recomputed:** `LS-177239 - Humidity sensor Conventillo` (with the altitude difference: `LS-177239 - Humidity sensor Conventillo`) → **MATCH**

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

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152608 - Tiltmeter Conventillo' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-177239 - Humidity sensor Conventillo | 3.82051 |
| LS-152816 Tiltmeter Conventillo | 5.05862 |
| LS-177266 - Crackmeter Conventillo | 5.92225 |
| LS-152931 Tiltemeter Conventillo | 6.45923 |
| LS-177320 CrackMeter Conventillo | 7.6324 |


---

## S067 · nearest_node

**Question:** Which sensor node is closest to LS-152899 at Schenkenberg?  
**Reference:** 2CF7F1C072300226, 0.6 m away. With the altitude difference: LS-152479, 1.3 m away.  
**Recomputed:** `2CF7F1C072300226` (with the altitude difference: `LS-152479`) → **MATCH**

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
| 2CF7F1C072300226 | 0.582429 |
| LS-152479 | 0.891981 |
| 2CF7F1C072600345 | 2.06602 |
| LS-149796 | 2.06602 |
| LS-152555 | 3.48701 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152899' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-152479 | 1.25301 |
| LS-152555 | 3.69427 |
| LS-175480 | 3.87623 |
| 2CF7F1C072300226 | 3.94325 |
| LS-149796 | 4.32532 |


---

## S068 · nearest_node

**Question:** Which sensor node is closest to LS-152914 at Schenkenberg?  
**Reference:** LS-159070, 0.4 m away. With the altitude difference: LS-175480, 1.9 m away.  
**Recomputed:** `LS-159070` (with the altitude difference: `LS-175480`) → **MATCH**

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
| LS-159070 | 0.376025 |
| LS-175480 | 1.90373 |
| 2CF7F1C072600345 | 2.21757 |
| LS-149796 | 2.21757 |
| 2CF7F1C072300226 | 3.6252 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152914' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-175480 | 1.93385 |
| LS-159070 | 2.55779 |
| LS-152479 | 3.73982 |
| LS-152555 | 4.24127 |
| LS-152899 | 4.3506 |


---

## S069 · nearest_node

**Question:** Which sensor node is closest to LS-170894 at Ranverso?  
**Reference:** LS-143276, 3.4 m away.  
**Recomputed:** `LS-143276` (with the altitude difference: `LS-143276`) → **MATCH**

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
| A8610A333526680F | 7.19873 |
| LS-174188 | 8.5517 |
| LS-168442 | 8.73384 |
| LS-149248 | 8.73384 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-170894' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-143276 | 3.40991 |
| A8610A333526680F | 7.20498 |
| LS-174188 | 8.55696 |
| LS-168442 | 8.73934 |
| LS-149248 | 8.73934 |


---

## S070 · nearest_node

**Question:** Which sensor node is closest to LS-177266 - Crackmeter Conventillo at Lucretili?  
**Reference:** LS-152931 Tiltemeter Conventillo, 0.2 m away. With the altitude difference: LS-152931 Tiltemeter Conventillo, 0.6 m away.  
**Recomputed:** `LS-152931 Tiltemeter Conventillo` (with the altitude difference: `LS-152931 Tiltemeter Conventillo`) → **MATCH**

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

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177266 - Crackmeter Conventillo' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| LS-152931 Tiltemeter Conventillo | 0.586727 |
| LS-152608 - Tiltmeter Conventillo | 5.92225 |
| LS-152816 Tiltmeter Conventillo | 6.018 |
| LS-177239 - Humidity sensor Conventillo | 6.90309 |
| LS-177253 Crackmeter Conventillo | 7.1914 |


---

## S071 · nearest_node

**Question:** Which sensor node is closest to P_WL at Baltanas?  
**Reference:** Acc-2A, 1 m away.  
**Recomputed:** `Acc-2A` (with the altitude difference: `Acc-2A`) → **MATCH**

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
| Acc-2A | 0.969558 |
| WP2 | 2.34934 |
| AF1 | 4.29673 |
| AF2 | 5.16865 |
| WP1 | 5.49166 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'P_WL' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| Acc-2A | 0.96961 |
| WP2 | 2.35071 |
| AF1 | 4.30093 |
| AF2 | 5.16865 |
| WP1 | 5.49648 |


---

## S072 · nearest_node

**Question:** Which sensor node is closest to WP2 at Baltanas?  
**Reference:** P_WL, 2.3 m away. With the altitude difference: P_WL, 2.4 m away.  
**Recomputed:** `P_WL` (with the altitude difference: `P_WL`) → **MATCH**

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
| P_WL | 2.34934 |
| Acc-2A | 3.07967 |
| WP1 | 3.16472 |
| AF2 | 3.91812 |
| AF3 | 4.87154 |

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'WP2' ORDER BY meters LIMIT 5;
```
| node | meters |
|---|---|
| P_WL | 2.35071 |
| Acc-2A | 3.08099 |
| WP1 | 3.16828 |
| AF2 | 3.91894 |
| AF3 | 4.87607 |


---

## S073 · within_radius

**Question:** How many other sensor nodes at Baltanas are within 10 m of P_WL?  
**Reference:** 8.  
**Recomputed:** `8` (with the altitude difference: `8`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'P_WL' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| Acc-2A | 0.969558 | 0.96961 |
| WP2 | 2.34934 | 2.35071 |
| AF1 | 4.29673 | 4.30093 |
| AF2 | 5.16865 | 5.16865 |
| WP1 | 5.49166 | 5.49648 |
| AF3 | 5.52963 | 5.53723 |
| GNSS-Rover | 5.72811 | 5.73596 |
| sensor | 6.82131 | 6.82626 |
| AF4 | 13.8788 | 13.9054 |
| Gases | 46.4606 | 46.4627 |
| A8610A3230467704 | 47.9485 | 47.9505 |
| Acc-3A | 71.788 | 71.7911 |
| 2CF7F1C073400212 | 237.175 | 237.299 |
| GNSS_Base | 334.972 | 335.435 |

- Rows with meters <= 10: 8; with meters_with_alt <= 10: 8.

---

## S074 · within_radius

**Question:** How many other sensor nodes at Baltanas are within 50 m of Acc-3A?  
**Reference:** 0.  
**Recomputed:** `0` (with the altitude difference: `0`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'baltanas' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'Acc-3A' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| sensor | 65.2259 | 65.2272 |
| GNSS-Rover | 66.6372 | 66.6382 |
| A8610A3230467704 | 67.0451 | 67.0456 |
| Gases | 67.3347 | 67.3351 |
| AF1 | 67.51 | 67.5117 |
| AF2 | 70.3767 | 70.3799 |
| P_WL | 71.788 | 71.7911 |
| Acc-2A | 72.1297 | 72.1327 |
| WP2 | 72.9247 | 72.9285 |
| WP1 | 75.0062 | 75.0116 |
| AF3 | 77.3175 | 77.3235 |
| AF4 | 85.5211 | 85.5348 |
| 2CF7F1C073400212 | 299.934 | 300.016 |
| GNSS_Base | 360.959 | 361.357 |

- Rows with meters <= 50: 0; with meters_with_alt <= 50: 0.

---

## S075 · within_radius

**Question:** How many other sensor nodes at Delos are within 10 m of H. Masks_Mask mosaic_window?  
**Reference:** 7.  
**Recomputed:** `7` (with the altitude difference: `7`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Mask mosaic_window' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| H. Masks_Mask mosaic_pole mounted | 2.16212 | 2.16732 |
| H. Masks_Mask mosaic_pole mounted 2 | 2.94807 | 2.95094 |
| H. Masks_Masks mosaic_flow meter | 2.94807 | 2.95094 |
| H. Masks_Dyonisios mosaic_pole mounted | 4.61259 | 4.61259 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.1446 | 8.14844 |
| 2CF7F1C062800035 | 8.19147 | 8.1925 |
| H. Masks_Dolphins mosaic_pole mounted | 8.66394 | 8.71919 |
| H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 12.9972 | 12.9975 |
| 2CF7F1C061300548 | 38.6927 | 38.7379 |
| Outdoors area H. Masks_Mask_pole mounted | 38.6927 | 38.7379 |
| LS-150900 | 182.327 | 183.136 |
| LS-153242 | 201.276 | 201.449 |
| LS-153295 | 230.804 | 230.967 |
| 2CF7F1C0723001F4 | 474.282 | 474.301 |
| H. Fournoi_pole mounted_outdoors | 474.282 | 474.301 |
| H. Fournoi_wall attached 1 | 543.057 | 543.057 |
| LS-153157 | 828.058 | 828.372 |
| 0004A30B0050C42F | 1160.11 | 1160.39 |

- Rows with meters <= 10: 7; with meters_with_alt <= 10: 7.

---

## S076 · within_radius

**Question:** How many other sensor nodes at Delos are within 10 m of H. Masks_Masks mosaic_flow meter?  
**Reference:** 7.  
**Recomputed:** `7` (with the altitude difference: `7`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Masks mosaic_flow meter' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| H. Masks_Mask mosaic_pole mounted 2 | 0 | 0 |
| H. Masks_Mask mosaic_pole mounted | 1.15976 | 1.15993 |
| H. Masks_Dyonisios mosaic_pole mounted | 2.69925 | 2.70238 |
| H. Masks_Mask mosaic_window | 2.94807 | 2.95094 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.85549 | 8.8563 |
| H. Masks_Dolphins mosaic_pole mounted | 9.86212 | 9.92439 |
| 2CF7F1C062800035 | 9.92759 | 9.92759 |
| H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 14.7107 | 14.7107 |
| 2CF7F1C061300548 | 40.249 | 40.2866 |
| Outdoors area H. Masks_Mask_pole mounted | 40.249 | 40.2866 |
| LS-150900 | 180.292 | 181.123 |
| LS-153242 | 199.897 | 200.066 |
| LS-153295 | 228.283 | 228.453 |
| H. Fournoi_pole mounted_outdoors | 477.036 | 477.057 |
| 2CF7F1C0723001F4 | 477.036 | 477.057 |
| H. Fournoi_wall attached 1 | 545.872 | 545.872 |
| LS-153157 | 825.11 | 825.428 |
| 0004A30B0050C42F | 1157.91 | 1158.19 |

- Rows with meters <= 10: 7; with meters_with_alt <= 10: 7.

---

## S077 · within_radius

**Question:** How many other sensor nodes at Delos are within 100 m of H. Masks_Dyonisios mosaic_pole mounted?  
**Reference:** 10.  
**Recomputed:** `10` (with the altitude difference: `10`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Dyonisios mosaic_pole mounted' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| H. Masks_Mask mosaic_pole mounted 2 | 2.69925 | 2.70238 |
| H. Masks_Masks mosaic_flow meter | 2.69925 | 2.70238 |
| H. Masks_Mask mosaic_pole mounted | 3.73228 | 3.73529 |
| H. Masks_Mask mosaic_window | 4.61259 | 4.61259 |
| H. Masks_Dolphins mosaic_pole mounted | 8.45159 | 8.50822 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 11.5497 | 11.5524 |
| 2CF7F1C062800035 | 12.4442 | 12.4449 |
| H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 17.2591 | 17.2593 |
| 2CF7F1C061300548 | 42.8707 | 42.9115 |
| Outdoors area H. Masks_Mask_pole mounted | 42.8707 | 42.9115 |
| LS-150900 | 177.827 | 178.657 |
| LS-153242 | 201.749 | 201.922 |
| LS-153295 | 228.858 | 229.022 |
| 2CF7F1C0723001F4 | 476.98 | 476.999 |
| H. Fournoi_pole mounted_outdoors | 476.98 | 476.999 |
| H. Fournoi_wall attached 1 | 545.981 | 545.982 |
| LS-153157 | 824.201 | 824.516 |
| 0004A30B0050C42F | 1158.94 | 1159.22 |

- Rows with meters <= 100: 10; with meters_with_alt <= 100: 10.

---

## S078 · within_radius

**Question:** How many other sensor nodes at Delos are within 100 m of H. Masks_Mask mosaic_pole mounted 2?  
**Reference:** 10.  
**Recomputed:** `10` (with the altitude difference: `10`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'delos' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'H. Masks_Mask mosaic_pole mounted 2' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| H. Masks_Masks mosaic_flow meter | 0 | 0 |
| H. Masks_Mask mosaic_pole mounted | 1.15976 | 1.15993 |
| H. Masks_Dyonisios mosaic_pole mounted | 2.69925 | 2.70238 |
| H. Masks_Mask mosaic_window | 2.94807 | 2.95094 |
| H. Masks_Dyonisios &panter mosaic_flow meter | 8.85549 | 8.8563 |
| H. Masks_Dolphins mosaic_pole mounted | 9.86212 | 9.92439 |
| 2CF7F1C062800035 | 9.92759 | 9.92759 |
| H. Masks_Dyonisios &panter mosaic_pole mounted 2 | 14.7107 | 14.7107 |
| 2CF7F1C061300548 | 40.249 | 40.2866 |
| Outdoors area H. Masks_Mask_pole mounted | 40.249 | 40.2866 |
| LS-150900 | 180.292 | 181.123 |
| LS-153242 | 199.897 | 200.066 |
| LS-153295 | 228.283 | 228.453 |
| H. Fournoi_pole mounted_outdoors | 477.036 | 477.057 |
| 2CF7F1C0723001F4 | 477.036 | 477.057 |
| H. Fournoi_wall attached 1 | 545.872 | 545.872 |
| LS-153157 | 825.11 | 825.428 |
| 0004A30B0050C42F | 1157.91 | 1158.19 |

- Rows with meters <= 100: 10; with meters_with_alt <= 100: 10.

---

## S079 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 100 m of LS-152608 - Tiltmeter Conventillo?  
**Reference:** 7.  
**Recomputed:** `7` (with the altitude difference: `7`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152608 - Tiltmeter Conventillo' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| LS-177239 - Humidity sensor Conventillo | 3.1235 | 3.82051 |
| LS-177253 Crackmeter Conventillo | 3.66595 | 9.44083 |
| LS-177266 - Crackmeter Conventillo | 4.19531 | 5.92225 |
| LS-152931 Tiltemeter Conventillo | 4.40946 | 6.45923 |
| LS-153061 - Tiltmeter Conventillo | 4.42058 | 11.4941 |
| LS-152816 Tiltmeter Conventillo | 4.90681 | 5.05862 |
| LS-177320 CrackMeter Conventillo | 6.68664 | 7.6324 |
| LS-177237 Pyranometer Villa Orazio | 7715.17 | 7721.13 |
| LS-177287 Crackmeter Villa Orazio | 7729.81 | 7735.7 |
| LS-174156 Crackmeter Villa Orazio | 7733.03 | 7738.94 |
| 24E124600E450308 | 7741.49 | 7747.24 |
| 2CF7F1C072300286 | 7750.54 | 7756.29 |
| LS-177281 Humidity-Temperature Montefalco | 8648.32 | 8649.95 |
| LS-177310 Crackmeter Montefalco | 8649.09 | 8650.73 |

- Rows with meters <= 100: 7; with meters_with_alt <= 100: 7.

---

## S080 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 100 m of LS-177281 Humidity-Temperature Montefalco?  
**Reference:** 1.  
**Recomputed:** `1` (with the altitude difference: `1`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177281 Humidity-Temperature Montefalco' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| LS-177310 Crackmeter Montefalco | 6.19538 | 6.21634 |
| LS-177237 Pyranometer Villa Orazio | 7760.75 | 7775.03 |
| LS-174156 Crackmeter Villa Orazio | 7767.67 | 7781.88 |
| LS-177287 Crackmeter Villa Orazio | 7777.55 | 7791.7 |
| 2CF7F1C072300286 | 7797.04 | 7810.96 |
| 24E124600E450308 | 7803.36 | 7817.26 |
| LS-177320 CrackMeter Conventillo | 8646 | 8647.55 |
| LS-152816 Tiltmeter Conventillo | 8647.04 | 8648.64 |
| LS-177239 - Humidity sensor Conventillo | 8647.18 | 8648.76 |
| LS-152608 - Tiltmeter Conventillo | 8648.32 | 8649.95 |
| LS-152931 Tiltemeter Conventillo | 8649.56 | 8651.27 |
| LS-177266 - Crackmeter Conventillo | 8649.57 | 8651.28 |
| LS-177253 Crackmeter Conventillo | 8651.81 | 8653.61 |
| LS-153061 - Tiltmeter Conventillo | 8652.57 | 8654.4 |

- Rows with meters <= 100: 1; with meters_with_alt <= 100: 1.

---

## S081 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 100 m of LS-177310 Crackmeter Montefalco?  
**Reference:** 1.  
**Recomputed:** `1` (with the altitude difference: `1`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177310 Crackmeter Montefalco' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| LS-177281 Humidity-Temperature Montefalco | 6.19538 | 6.21634 |
| LS-177237 Pyranometer Villa Orazio | 7766.27 | 7780.57 |
| LS-174156 Crackmeter Villa Orazio | 7773.2 | 7787.42 |
| LS-177287 Crackmeter Villa Orazio | 7783.07 | 7797.24 |
| 2CF7F1C072300286 | 7802.56 | 7816.5 |
| 24E124600E450308 | 7808.88 | 7822.8 |
| LS-177320 CrackMeter Conventillo | 8646.76 | 8648.33 |
| LS-152816 Tiltmeter Conventillo | 8647.81 | 8649.42 |
| LS-177239 - Humidity sensor Conventillo | 8647.94 | 8649.54 |
| LS-152608 - Tiltmeter Conventillo | 8649.09 | 8650.73 |
| LS-152931 Tiltemeter Conventillo | 8650.32 | 8652.05 |
| LS-177266 - Crackmeter Conventillo | 8650.34 | 8652.06 |
| LS-177253 Crackmeter Conventillo | 8652.58 | 8654.39 |
| LS-153061 - Tiltmeter Conventillo | 8653.33 | 8655.18 |

- Rows with meters <= 100: 1; with meters_with_alt <= 100: 1.

---

## S082 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 500 m of LS-152816 Tiltmeter Conventillo?  
**Reference:** 7.  
**Recomputed:** `7` (with the altitude difference: `7`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152816 Tiltmeter Conventillo' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| LS-177239 - Humidity sensor Conventillo | 1.83563 | 2.07616 |
| LS-177320 CrackMeter Conventillo | 1.8543 | 3.07261 |
| LS-152931 Tiltemeter Conventillo | 2.56509 | 6.47937 |
| LS-177266 - Crackmeter Conventillo | 2.63595 | 6.018 |
| LS-152608 - Tiltmeter Conventillo | 4.90681 | 5.05862 |
| LS-153061 - Tiltmeter Conventillo | 6.54119 | 13.5267 |
| LS-177253 Crackmeter Conventillo | 7.55514 | 12.4774 |
| LS-177237 Pyranometer Villa Orazio | 7718.4 | 7724.4 |
| LS-177287 Crackmeter Villa Orazio | 7733.05 | 7738.98 |
| LS-174156 Crackmeter Villa Orazio | 7736.26 | 7742.21 |
| 24E124600E450308 | 7744.74 | 7750.53 |
| 2CF7F1C072300286 | 7753.78 | 7759.57 |
| LS-177281 Humidity-Temperature Montefalco | 8647.04 | 8648.64 |
| LS-177310 Crackmeter Montefalco | 8647.81 | 8649.42 |

- Rows with meters <= 500: 7; with meters_with_alt <= 500: 7.

---

## S083 · within_radius

**Question:** How many other sensor nodes at Lucretili are within 500 m of LS-177266 - Crackmeter Conventillo?  
**Reference:** 7.  
**Recomputed:** `7` (with the altitude difference: `7`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177266 - Crackmeter Conventillo' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| LS-152931 Tiltemeter Conventillo | 0.229453 | 0.586727 |
| LS-177239 - Humidity sensor Conventillo | 2.63595 | 6.90309 |
| LS-152816 Tiltmeter Conventillo | 2.63595 | 6.018 |
| LS-153061 - Tiltmeter Conventillo | 4.07742 | 7.61382 |
| LS-152608 - Tiltmeter Conventillo | 4.19531 | 5.92225 |
| LS-177320 CrackMeter Conventillo | 4.23253 | 8.92715 |
| LS-177253 Crackmeter Conventillo | 5.59337 | 7.1914 |
| LS-177237 Pyranometer Villa Orazio | 7719.2 | 7724.99 |
| LS-177287 Crackmeter Villa Orazio | 7733.84 | 7739.56 |
| LS-174156 Crackmeter Villa Orazio | 7737.05 | 7742.8 |
| 24E124600E450308 | 7745.52 | 7751.1 |
| 2CF7F1C072300286 | 7754.57 | 7760.15 |
| LS-177281 Humidity-Temperature Montefalco | 8649.57 | 8651.28 |
| LS-177310 Crackmeter Montefalco | 8650.34 | 8652.06 |

- Rows with meters <= 500: 7; with meters_with_alt <= 500: 7.

---

## S084 · within_radius

**Question:** How many other sensor nodes at Ranverso are within 100 m of LS-149248?  
**Reference:** 9.  
**Recomputed:** `9` (with the altitude difference: `9`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-149248' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| LS-168442 | 0 | 0 |
| LS-174188 | 0.308875 | 0.309037 |
| A8610A333526680F | 1.77191 | 1.77194 |
| LS-143276 | 7.01043 | 7.01145 |
| LS-170894 | 8.73384 | 8.73934 |
| A8610A3338359111 | 19.3365 | 19.3613 |
| ae_ranverso | 19.4817 | 19.5099 |
| LS-149361 | 37.2934 | 37.2939 |
| LS-177315 | 37.4045 | 37.4052 |

- Rows with meters <= 100: 9; with meters_with_alt <= 100: 9.

---

## S085 · within_radius

**Question:** How many other sensor nodes at Ranverso are within 500 m of LS-174188?  
**Reference:** 9.  
**Recomputed:** `9` (with the altitude difference: `9`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-174188' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| LS-149248 | 0.308875 | 0.309037 |
| LS-168442 | 0.308875 | 0.309037 |
| A8610A333526680F | 1.74478 | 1.74478 |
| LS-143276 | 6.93518 | 6.93605 |
| LS-170894 | 8.5517 | 8.55696 |
| A8610A3338359111 | 19.1356 | 19.1602 |
| ae_ranverso | 19.2675 | 19.2955 |
| LS-149361 | 37.3279 | 37.3285 |
| LS-177315 | 37.4466 | 37.4473 |

- Rows with meters <= 500: 9; with meters_with_alt <= 500: 9.

---

## S086 · within_radius

**Question:** How many other sensor nodes at Ranverso are within 500 m of LS-177315?  
**Reference:** 9.  
**Recomputed:** `9` (with the altitude difference: `9`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'ranverso' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-177315' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| LS-149361 | 0.926624 | 0.92684 |
| A8610A3338359111 | 28.5412 | 28.5664 |
| ae_ranverso | 29.6296 | 29.6568 |
| LS-168442 | 37.4045 | 37.4052 |
| LS-149248 | 37.4045 | 37.4052 |
| LS-174188 | 37.4466 | 37.4473 |
| A8610A333526680F | 39.1749 | 39.1756 |
| LS-143276 | 44.3612 | 44.3625 |
| LS-170894 | 45.2195 | 45.2226 |

- Rows with meters <= 500: 9; with meters_with_alt <= 500: 9.

---

## S087 · within_radius

**Question:** How many other sensor nodes at Schenkenberg are within 50 m of LS-152555?  
**Reference:** 8.  
**Recomputed:** `8` (with the altitude difference: `8`) → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT b.label AS node, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) AS meters, sqrt(power(2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))),2)+power(b.alt-a.alt,2)) AS meters_with_alt
FROM n a JOIN n b ON a.node_id <> b.node_id WHERE a.label = 'LS-152555' ORDER BY meters;
```
| node | meters | meters_with_alt |
|---|---|---|
| 2CF7F1C072300226 | 3.13497 | 4.12437 |
| LS-152899 | 3.48701 | 3.69427 |
| LS-149796 | 3.72651 | 6.25198 |
| 2CF7F1C072600345 | 3.72651 | 6.66012 |
| LS-152479 | 4.01567 | 4.03004 |
| LS-152914 | 4.24127 | 4.24127 |
| LS-159070 | 4.60259 | 5.25212 |
| LS-175480 | 5.29804 | 5.30894 |

- Rows with meters <= 50: 8; with meters_with_alt <= 50: 8.

---

## S088 · site_distance

**Question:** How far apart are Baltanas and Delos, measured between the centroids of their sensor nodes?  
**Reference:** 2562.9 km.  
**Recomputed:** `2562.9` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'baltanas' AND b.site_id = 'delos';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 41.9384 | -4.24417 | 37.3967 | 25.2696 | 2562.85 |


---

## S089 · site_distance

**Question:** How far apart are Baltanas and Lucretili, measured between the centroids of their sensor nodes?  
**Reference:** 1410.5 km.  
**Recomputed:** `1410.5` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'baltanas' AND b.site_id = 'lucretili';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 41.9384 | -4.24417 | 42.0482 | 12.851 | 1410.49 |


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
| 41.9384 | -4.24417 | 45.0812 | 7.44971 | 1004.58 |


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
| 41.9384 | -4.24417 | 47.4421 | 8.10102 | 1149.87 |


---

## S092 · site_distance

**Question:** How far apart are Delos and Lucretili, measured between the centroids of their sensor nodes?  
**Reference:** 1179.8 km.  
**Recomputed:** `1179.8` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'delos' AND b.site_id = 'lucretili';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 37.3967 | 25.2696 | 42.0482 | 12.851 | 1179.78 |


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
| 37.3967 | 25.2696 | 45.0812 | 7.44971 | 1712.14 |


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
| 37.3967 | 25.2696 | 47.4421 | 8.10102 | 1791.43 |


---

## S095 · site_distance

**Question:** How far apart are Lucretili and Ranverso, measured between the centroids of their sensor nodes?  
**Reference:** 550.4 km.  
**Recomputed:** `550.4` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'lucretili' AND b.site_id = 'ranverso';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 42.0482 | 12.851 | 45.0812 | 7.44971 | 550.358 |


---

## S096 · site_distance

**Question:** How far apart are Lucretili and Schenkenberg, measured between the centroids of their sensor nodes?  
**Reference:** 707.1 km.  
**Recomputed:** `707.1` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT r.site_id, n.node_id, n.latitude::float8 AS lat, n.longitude::float8 AS lon
           FROM nodes n JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL),
c AS (SELECT site_id, avg(lat) AS lat, avg(lon) AS lon FROM n GROUP BY 1)
SELECT a.lat AS lat_a, a.lon AS lon_a, b.lat AS lat_b, b.lon AS lon_b, 2*6371000*asin(sqrt(power(sin(radians(b.lat-a.lat)/2),2)+cos(radians(a.lat))*cos(radians(b.lat))*power(sin(radians(b.lon-a.lon)/2),2))) / 1000 AS km
FROM c a, c b WHERE a.site_id = 'lucretili' AND b.site_id = 'schenkenberg';
```
| lat_a | lon_a | lat_b | lon_b | km |
|---|---|---|---|---|
| 42.0482 | 12.851 | 47.4421 | 8.10102 | 707.108 |


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
| 45.0812 | 7.44971 | 47.4421 | 8.10102 | 267.258 |


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
