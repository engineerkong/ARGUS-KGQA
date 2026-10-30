# Verification — temporal

Run `SET TIME ZONE 'UTC';` in psql first (`psql -h localhost -U argus -d argus_snapshot`).

## T001 · first_reading

**Question:** When was the first reading recorded at Baltanas?  
**Reference:** 2026-05-13 00:50 UTC.  
**Recomputed:** `2026-05-13 00:50 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'baltanas';
```
| first | last | count |
|---|---|---|
| 2026-05-13 00:50:00 | 2026-08-12 09:15:00 | 709170 |


---

## T002 · first_reading

**Question:** When was the first reading recorded at Delos?  
**Reference:** 2026-05-13 01:00 UTC.  
**Recomputed:** `2026-05-13 01:00 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'delos';
```
| first | last | count |
|---|---|---|
| 2026-05-13 01:00:00 | 2026-08-12 09:14:17 | 225945 |


---

## T003 · first_reading

**Question:** When was the first reading recorded at Lucretili?  
**Reference:** 2026-05-13 00:50 UTC.  
**Recomputed:** `2026-05-13 00:50 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'lucretili';
```
| first | last | count |
|---|---|---|
| 2026-05-13 00:50:00 | 2026-08-12 09:15:00 | 574578 |


---

## T004 · first_reading

**Question:** When was the first reading recorded at Ranverso?  
**Reference:** 2026-05-13 01:00 UTC.  
**Recomputed:** `2026-05-13 01:00 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'ranverso';
```
| first | last | count |
|---|---|---|
| 2026-05-13 01:00:00 | 2026-08-12 09:13:25 | 108150 |


---

## T005 · first_reading

**Question:** When was the first reading recorded at Schenkenberg?  
**Reference:** 2026-05-14 00:00 UTC.  
**Recomputed:** `2026-05-14 00:00 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'schenkenberg';
```
| first | last | count |
|---|---|---|
| 2026-05-14 00:00:00 | 2026-08-12 09:13:57 | 59713 |


---

## T006 · last_reading

**Question:** When was the most recent reading recorded at Baltanas?  
**Reference:** 2026-08-12 09:15 UTC.  
**Recomputed:** `2026-08-12 09:15 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'baltanas';
```
| first | last | count |
|---|---|---|
| 2026-05-13 00:50:00 | 2026-08-12 09:15:00 | 709170 |


---

## T007 · last_reading

**Question:** When was the most recent reading recorded at Delos?  
**Reference:** 2026-08-12 09:14 UTC.  
**Recomputed:** `2026-08-12 09:14 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'delos';
```
| first | last | count |
|---|---|---|
| 2026-05-13 01:00:00 | 2026-08-12 09:14:17 | 225945 |


---

## T008 · last_reading

**Question:** When was the most recent reading recorded at Lucretili?  
**Reference:** 2026-08-12 09:15 UTC.  
**Recomputed:** `2026-08-12 09:15 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'lucretili';
```
| first | last | count |
|---|---|---|
| 2026-05-13 00:50:00 | 2026-08-12 09:15:00 | 574578 |


---

## T009 · last_reading

**Question:** When was the most recent reading recorded at Ranverso?  
**Reference:** 2026-08-12 09:13 UTC.  
**Recomputed:** `2026-08-12 09:13 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'ranverso';
```
| first | last | count |
|---|---|---|
| 2026-05-13 01:00:00 | 2026-08-12 09:13:25 | 108150 |


---

## T010 · last_reading

**Question:** When was the most recent reading recorded at Schenkenberg?  
**Reference:** 2026-08-12 09:13 UTC.  
**Recomputed:** `2026-08-12 09:13 UTC` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'schenkenberg';
```
| first | last | count |
|---|---|---|
| 2026-05-14 00:00:00 | 2026-08-12 09:13:57 | 59713 |


---

## T011 · span

**Question:** What time period do the readings at Baltanas cover?  
**Reference:** From 2026-05-13 00:50 UTC to 2026-08-12 09:15 UTC.  
**Recomputed:** `['2026-05-13 00:50 UTC', '2026-08-12 09:15 UTC']` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'baltanas';
```
| first | last | count |
|---|---|---|
| 2026-05-13 00:50:00 | 2026-08-12 09:15:00 | 709170 |


---

## T012 · span

**Question:** What time period do the readings at Delos cover?  
**Reference:** From 2026-05-13 01:00 UTC to 2026-08-12 09:14 UTC.  
**Recomputed:** `['2026-05-13 01:00 UTC', '2026-08-12 09:14 UTC']` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'delos';
```
| first | last | count |
|---|---|---|
| 2026-05-13 01:00:00 | 2026-08-12 09:14:17 | 225945 |


---

## T013 · span

**Question:** What time period do the readings at Lucretili cover?  
**Reference:** From 2026-05-13 00:50 UTC to 2026-08-12 09:15 UTC.  
**Recomputed:** `['2026-05-13 00:50 UTC', '2026-08-12 09:15 UTC']` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'lucretili';
```
| first | last | count |
|---|---|---|
| 2026-05-13 00:50:00 | 2026-08-12 09:15:00 | 574578 |


---

## T014 · span

**Question:** What time period do the readings at Ranverso cover?  
**Reference:** From 2026-05-13 01:00 UTC to 2026-08-12 09:13 UTC.  
**Recomputed:** `['2026-05-13 01:00 UTC', '2026-08-12 09:13 UTC']` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'ranverso';
```
| first | last | count |
|---|---|---|
| 2026-05-13 01:00:00 | 2026-08-12 09:13:25 | 108150 |


---

## T015 · span

**Question:** What time period do the readings at Schenkenberg cover?  
**Reference:** From 2026-05-14 00:00 UTC to 2026-08-12 09:13 UTC.  
**Recomputed:** `['2026-05-14 00:00 UTC', '2026-08-12 09:13 UTC']` → **MATCH**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'schenkenberg';
```
| first | last | count |
|---|---|---|
| 2026-05-14 00:00:00 | 2026-08-12 09:13:57 | 59713 |


---

## T016 · latest_quantity

**Question:** When was the most recent composed peak ground acceleration (pgaComposed) reading at Schenkenberg?  
**Reference:** 2026-05-28 11:30 UTC.  
**Recomputed:** `2026-05-28 11:30 UTC` → **MATCH**

```sql
SELECT max(o.result_time) AS latest FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'pgaComposed' AND o.value IS NOT NULL;
```
| latest |
|---|
| 2026-05-28 11:30:00 |


---

## T017 · latest_quantity

**Question:** When was the most recent potentiometer displacement reading at Delos?  
**Reference:** 2026-08-12 09:00 UTC.  
**Recomputed:** `2026-08-12 09:00 UTC` → **MATCH**

```sql
SELECT max(o.result_time) AS latest FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'potentiometer_displacement' AND o.value IS NOT NULL;
```
| latest |
|---|
| 2026-08-12 09:00:00 |


---

## T018 · latest_quantity

**Question:** When was the most recent rainfall reading at Ranverso?  
**Reference:** 2026-08-12 09:00 UTC.  
**Recomputed:** `2026-08-12 09:00 UTC` → **MATCH**

```sql
SELECT max(o.result_time) AS latest FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall' AND o.value IS NOT NULL;
```
| latest |
|---|
| 2026-08-12 09:00:00 |


---

## T019 · latest_quantity

**Question:** When was the most recent soil temperature reading at Baltanas?  
**Reference:** 2026-08-12 09:15 UTC.  
**Recomputed:** `2026-08-12 09:15 UTC` → **MATCH**

```sql
SELECT max(o.result_time) AS latest FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL;
```
| latest |
|---|
| 2026-08-12 09:15:00 |


---

## T020 · latest_quantity

**Question:** When was the most recent temperature reading at Baltanas?  
**Reference:** 2026-08-12 09:15 UTC.  
**Recomputed:** `2026-08-12 09:15 UTC` → **MATCH**

```sql
SELECT max(o.result_time) AS latest FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| latest |
|---|
| 2026-08-12 09:15:00 |


---

## T021 · latest_quantity

**Question:** When was the most recent temperature reading at Ranverso?  
**Reference:** 2026-08-12 09:00 UTC.  
**Recomputed:** `2026-08-12 09:00 UTC` → **MATCH**

```sql
SELECT max(o.result_time) AS latest FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| latest |
|---|
| 2026-08-12 09:00:00 |


---

## T022 · latest_quantity

**Question:** When was the most recent temperature reading at Schenkenberg?  
**Reference:** 2026-08-12 09:00 UTC.  
**Recomputed:** `2026-08-12 09:00 UTC` → **MATCH**

```sql
SELECT max(o.result_time) AS latest FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| latest |
|---|
| 2026-08-12 09:00:00 |


---

## T023 · latest_quantity

**Question:** When was the most recent voltage reading at Ranverso?  
**Reference:** 2026-08-12 09:00 UTC.  
**Recomputed:** `2026-08-12 09:00 UTC` → **MATCH**

```sql
SELECT max(o.result_time) AS latest FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| latest |
|---|
| 2026-08-12 09:00:00 |


---

## T024 · time_of_max

**Question:** When was the highest composed RMS acceleration (rmsComposed) at Schenkenberg recorded?  
**Reference:** 2026-05-22 09:33 UTC (value 777).  
**Recomputed:** `2026-05-22 09:33 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'rmsComposed' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 777 | 2026-05-22 09:33:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |
| 505.4 | 2026-05-22 09:38:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |
| 342.1 | 2026-05-22 09:36:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |
| 301.6 | 2026-05-22 09:39:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |
| 41.7 | 2026-05-22 09:40:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |


---

## T025 · time_of_max

**Question:** When was the highest composed peak ground acceleration (pgaComposed) at Schenkenberg recorded?  
**Reference:** 2026-05-22 09:41 UTC (value 1238.6).  
**Recomputed:** `2026-05-22 09:41 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'pgaComposed' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 1238.6 | 2026-05-22 09:41:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |
| 905.7 | 2026-05-22 09:40:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |
| 184.2 | 2026-05-22 09:42:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |
| 143.7 | 2026-05-22 09:37:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |
| 77.6 | 2026-05-22 09:34:00 | 3dff8100-55c1-11f1-9208-83a949003bcf |


---

## T026 · time_of_max

**Question:** When was the highest potentiometer displacement at Delos recorded?  
**Reference:** 2026-06-04 02:00 UTC (value 49.5).  
**Recomputed:** `2026-06-04 02:00 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'potentiometer_displacement' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 49.5 | 2026-06-04 02:00:00 | 002218a0-6640-11f0-8a4b-6bd692b5baa4 |
| 49.4932 | 2026-06-04 04:00:00 | 002218a0-6640-11f0-8a4b-6bd692b5baa4 |
| 49.4879 | 2026-06-04 05:00:00 | 002218a0-6640-11f0-8a4b-6bd692b5baa4 |
| 49.4736 | 2026-06-04 00:00:00 | 002218a0-6640-11f0-8a4b-6bd692b5baa4 |
| 49.4577 | 2026-06-04 06:00:00 | 002218a0-6640-11f0-8a4b-6bd692b5baa4 |


---

## T027 · time_of_max

**Question:** When was the highest soil temperature at Baltanas recorded?  
**Reference:** 2026-06-07 09:35 UTC (value 38.51).  
**Recomputed:** `2026-06-07 09:35 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 38.51 | 2026-06-07 09:35:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |
| 38.17 | 2026-06-07 09:30:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |
| 37.84 | 2026-06-07 09:40:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |
| 37.73 | 2026-06-07 09:25:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |
| 37.17 | 2026-06-07 09:20:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |


---

## T028 · time_of_max

**Question:** When was the highest soil water potential at Baltanas recorded?  
**Reference:** 2026-05-26 09:40 UTC (value 94.767).  
**Recomputed:** `2026-05-26 09:40 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_water_potential' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 94.767 | 2026-05-26 09:40:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |
| 94.728 | 2026-05-25 09:40:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |
| 94.688 | 2026-05-26 09:35:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |
| 94.68 | 2026-05-25 09:35:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |
| 94.615 | 2026-05-26 08:20:00 | f61c2ae0-c9da-11f0-a18a-496739762f81 |


---

## T029 · time_of_max

**Question:** When was the highest temperature at Lucretili recorded?  
**Reference:** 2026-07-31 11:30 UTC (value 50).  
**Recomputed:** `2026-07-31 11:30 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 50 | 2026-07-31 11:30:00 | 8250dd80-8269-11f0-9283-e956b63ef652 |
| 50 | 2026-07-31 11:30:00 | 82508f60-8269-11f0-b6dc-556f88243956 |
| 50 | 2026-07-31 11:30:00 | 0cf22310-81be-11f0-9283-e956b63ef652 |
| 50 | 2026-08-01 11:30:00 | 8250dd80-8269-11f0-9283-e956b63ef652 |
| 50 | 2026-08-01 11:30:00 | 82508f60-8269-11f0-b6dc-556f88243956 |

- The maximum occurs more than once; the reference uses the earliest.

---

## T030 · time_of_max

**Question:** When was the highest voltage at Lucretili recorded?  
**Reference:** 2026-06-22 14:55 UTC (value 4.619).  
**Recomputed:** `2026-06-22 14:55 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'voltage' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 4.61947 | 2026-06-22 14:55:00 | 6d46d0f0-d103-11f0-8484-ad77d9ec8692 |
| 4.61072 | 2026-06-22 14:45:00 | 6d46d0f0-d103-11f0-8484-ad77d9ec8692 |
| 4.59606 | 2026-06-22 15:00:00 | 6d46d0f0-d103-11f0-8484-ad77d9ec8692 |
| 4.59555 | 2026-05-17 00:00:00 | 6d46d0f0-d103-11f0-8484-ad77d9ec8692 |
| 4.5857 | 2026-06-22 14:50:00 | 6d46d0f0-d103-11f0-8484-ad77d9ec8692 |


---

## T031 · time_of_max

**Question:** When was the highest voltage at Ranverso recorded?  
**Reference:** 2026-06-03 01:00 UTC (value 4.428).  
**Recomputed:** `2026-06-03 01:00 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 4.42806 | 2026-06-03 01:00:00 | 918d6d40-8e53-11f0-9283-e956b63ef652 |
| 4.40535 | 2026-05-16 03:00:00 | 918d6d40-8e53-11f0-9283-e956b63ef652 |
| 4.39011 | 2026-06-03 04:00:00 | 918d6d40-8e53-11f0-9283-e956b63ef652 |
| 4.3873 | 2026-06-10 04:00:00 | 918d6d40-8e53-11f0-9283-e956b63ef652 |
| 4.38717 | 2026-06-10 03:00:00 | 918d6d40-8e53-11f0-9283-e956b63ef652 |


---

## T032 · monthly_count

**Question:** How many readings were recorded at Baltanas in August 2026?  
**Reference:** 82932 readings.  
**Recomputed:** `82932` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'baltanas'
  AND result_time >= '2026-08-01' AND result_time < '2026-08-01'::date + interval '1 month';
```
| readings |
|---|
| 82932 |


---

## T033 · monthly_count

**Question:** How many readings were recorded at Baltanas in July 2026?  
**Reference:** 239902 readings.  
**Recomputed:** `239902` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'baltanas'
  AND result_time >= '2026-07-01' AND result_time < '2026-07-01'::date + interval '1 month';
```
| readings |
|---|
| 239902 |


---

## T034 · monthly_count

**Question:** How many readings were recorded at Delos in June 2026?  
**Reference:** 65551 readings.  
**Recomputed:** `65551` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'delos'
  AND result_time >= '2026-06-01' AND result_time < '2026-06-01'::date + interval '1 month';
```
| readings |
|---|
| 65551 |


---

## T035 · monthly_count

**Question:** How many readings were recorded at Lucretili in July 2026?  
**Reference:** 220581 readings.  
**Recomputed:** `220581` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili'
  AND result_time >= '2026-07-01' AND result_time < '2026-07-01'::date + interval '1 month';
```
| readings |
|---|
| 220581 |


---

## T036 · monthly_count

**Question:** How many readings were recorded at Lucretili in May 2026?  
**Reference:** 60353 readings.  
**Recomputed:** `60353` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili'
  AND result_time >= '2026-05-01' AND result_time < '2026-05-01'::date + interval '1 month';
```
| readings |
|---|
| 60353 |


---

## T037 · monthly_count

**Question:** How many readings were recorded at Ranverso in August 2026?  
**Reference:** 16263 readings.  
**Recomputed:** `16263` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'ranverso'
  AND result_time >= '2026-08-01' AND result_time < '2026-08-01'::date + interval '1 month';
```
| readings |
|---|
| 16263 |


---

## T038 · monthly_count

**Question:** How many readings were recorded at Ranverso in July 2026?  
**Reference:** 51009 readings.  
**Recomputed:** `51009` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'ranverso'
  AND result_time >= '2026-07-01' AND result_time < '2026-07-01'::date + interval '1 month';
```
| readings |
|---|
| 51009 |


---

## T039 · monthly_count

**Question:** How many readings were recorded at Ranverso in June 2026?  
**Reference:** 31666 readings.  
**Recomputed:** `31666` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'ranverso'
  AND result_time >= '2026-06-01' AND result_time < '2026-06-01'::date + interval '1 month';
```
| readings |
|---|
| 31666 |


---

## T040 · monthly_count

**Question:** How many readings were recorded at Schenkenberg in August 2026?  
**Reference:** 8782 readings.  
**Recomputed:** `8782` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'schenkenberg'
  AND result_time >= '2026-08-01' AND result_time < '2026-08-01'::date + interval '1 month';
```
| readings |
|---|
| 8782 |


---

## T041 · monthly_count

**Question:** How many readings were recorded at Schenkenberg in June 2026?  
**Reference:** 15272 readings.  
**Recomputed:** `15272` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'schenkenberg'
  AND result_time >= '2026-06-01' AND result_time < '2026-06-01'::date + interval '1 month';
```
| readings |
|---|
| 15272 |


---

## T042 · relative_window

**Question:** What was the average temperature at Baltanas over the last 24 hours?  
**Reference:** 25.871 (4713 observations, window ending 2026-08-12 09:15 UTC).  
**Recomputed:** `25.870952684065372` → **MATCH**

```sql
WITH e AS (SELECT max(result_time) AS t FROM observations)
SELECT e.t AS window_end, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id), e
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time > e.t - interval '24 hours' AND o.result_time <= e.t GROUP BY e.t;
```
| window_end | avg | n |
|---|---|---|
| 2026-08-12 09:15:00 | 25.871 | 4713 |


---

## T043 · relative_window

**Question:** What was the average temperature at Baltanas over the last 7 days?  
**Reference:** 24.263 (32913 observations, window ending 2026-08-12 09:15 UTC).  
**Recomputed:** `24.262750281043875` → **MATCH**

```sql
WITH e AS (SELECT max(result_time) AS t FROM observations)
SELECT e.t AS window_end, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id), e
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time > e.t - interval '168 hours' AND o.result_time <= e.t GROUP BY e.t;
```
| window_end | avg | n |
|---|---|---|
| 2026-08-12 09:15:00 | 24.2628 | 32913 |


---

## T044 · relative_window

**Question:** What was the average temperature at Delos over the last 24 hours?  
**Reference:** 27.706 (232 observations, window ending 2026-08-12 09:15 UTC).  
**Recomputed:** `27.706034482758625` → **MATCH**

```sql
WITH e AS (SELECT max(result_time) AS t FROM observations)
SELECT e.t AS window_end, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id), e
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time > e.t - interval '24 hours' AND o.result_time <= e.t GROUP BY e.t;
```
| window_end | avg | n |
|---|---|---|
| 2026-08-12 09:15:00 | 27.706 | 232 |


---

## T045 · relative_window

**Question:** What was the average temperature at Delos over the last 7 days?  
**Reference:** 28.315 (1735 observations, window ending 2026-08-12 09:15 UTC).  
**Recomputed:** `28.314639769452445` → **MATCH**

```sql
WITH e AS (SELECT max(result_time) AS t FROM observations)
SELECT e.t AS window_end, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id), e
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time > e.t - interval '168 hours' AND o.result_time <= e.t GROUP BY e.t;
```
| window_end | avg | n |
|---|---|---|
| 2026-08-12 09:15:00 | 28.3146 | 1735 |


---

## T046 · relative_window

**Question:** What was the average temperature at Lucretili over the last 24 hours?  
**Reference:** 28.431 (3635 observations, window ending 2026-08-12 09:15 UTC).  
**Recomputed:** `28.43050894085283` → **MATCH**

```sql
WITH e AS (SELECT max(result_time) AS t FROM observations)
SELECT e.t AS window_end, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id), e
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time > e.t - interval '24 hours' AND o.result_time <= e.t GROUP BY e.t;
```
| window_end | avg | n |
|---|---|---|
| 2026-08-12 09:15:00 | 28.4305 | 3635 |


---

## T047 · relative_window

**Question:** What was the average temperature at Lucretili over the last 7 days?  
**Reference:** 27.191 (23894 observations, window ending 2026-08-12 09:15 UTC).  
**Recomputed:** `27.191043776680246` → **MATCH**

```sql
WITH e AS (SELECT max(result_time) AS t FROM observations)
SELECT e.t AS window_end, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id), e
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time > e.t - interval '168 hours' AND o.result_time <= e.t GROUP BY e.t;
```
| window_end | avg | n |
|---|---|---|
| 2026-08-12 09:15:00 | 27.191 | 23894 |


---

## T048 · relative_window

**Question:** What was the average temperature at Ranverso over the last 24 hours?  
**Reference:** 26.247 (209 observations, window ending 2026-08-12 09:15 UTC).  
**Recomputed:** `26.247368421052627` → **MATCH**

```sql
WITH e AS (SELECT max(result_time) AS t FROM observations)
SELECT e.t AS window_end, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id), e
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time > e.t - interval '24 hours' AND o.result_time <= e.t GROUP BY e.t;
```
| window_end | avg | n |
|---|---|---|
| 2026-08-12 09:15:00 | 26.2474 | 209 |


---

## T049 · relative_window

**Question:** What was the average temperature at Schenkenberg over the last 24 hours?  
**Reference:** 29.107 (171 observations, window ending 2026-08-12 09:15 UTC).  
**Recomputed:** `29.107017543859644` → **MATCH**

```sql
WITH e AS (SELECT max(result_time) AS t FROM observations)
SELECT e.t AS window_end, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id), e
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time > e.t - interval '24 hours' AND o.result_time <= e.t GROUP BY e.t;
```
| window_end | avg | n |
|---|---|---|
| 2026-08-12 09:15:00 | 29.107 | 171 |


---

## T050 · daily_avg

**Question:** What was the average rainfall at Ranverso on 2026-05-24?  
**Reference:** 0.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-24' AND o.result_time < '2026-05-24'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 0 | 0 | 0 | 24 |


---

## T051 · daily_avg

**Question:** What was the average soil temperature at Baltanas on 2026-06-17?  
**Reference:** 27.895.  
**Recomputed:** `27.894711033274945` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-17' AND o.result_time < '2026-06-17'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 27.8947 | 28.83 | 25.64 | 571 |


---

## T052 · daily_avg

**Question:** What was the average soil temperature at Baltanas on 2026-06-24?  
**Reference:** 28.933.  
**Recomputed:** `28.933142361111077` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-24' AND o.result_time < '2026-06-24'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 28.9331 | 30.47 | 26.58 | 576 |


---

## T053 · daily_avg

**Question:** What was the average temperature at Baltanas on 2026-06-18?  
**Reference:** 22.54.  
**Recomputed:** `22.539979716024362` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-18' AND o.result_time < '2026-06-18'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 22.54 | 41.2 | 9 | 4930 |


---

## T054 · daily_avg

**Question:** What was the average temperature at Baltanas on 2026-08-10?  
**Reference:** 23.981.  
**Recomputed:** `23.98112050739957` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-10' AND o.result_time < '2026-08-10'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 23.9811 | 41.3 | 10 | 4730 |


---

## T055 · daily_avg

**Question:** What was the average temperature at Lucretili on 2026-07-31?  
**Reference:** 29.166.  
**Recomputed:** `29.166180302240747` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-31' AND o.result_time < '2026-07-31'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 29.1662 | 50 | 15 | 3838 |


---

## T056 · daily_avg

**Question:** What was the average temperature at Lucretili on 2026-08-11?  
**Reference:** 28.258.  
**Recomputed:** `28.257662624035287` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-11' AND o.result_time < '2026-08-11'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 28.2577 | 49 | 14 | 3628 |


---

## T057 · daily_avg

**Question:** What was the average temperature at Ranverso on 2026-05-21?  
**Reference:** 17.879.  
**Recomputed:** `17.878703703703707` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-21' AND o.result_time < '2026-05-21'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 17.8787 | 28 | 11 | 216 |


---

## T058 · daily_avg

**Question:** What was the average temperature at Ranverso on 2026-06-09?  
**Reference:** 22.154.  
**Recomputed:** `22.154166666666665` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-09' AND o.result_time < '2026-06-09'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 22.1542 | 30 | 16 | 216 |


---

## T059 · daily_avg

**Question:** What was the average temperature at Ranverso on 2026-06-20?  
**Reference:** 25.803.  
**Recomputed:** `25.80252525252525` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-20' AND o.result_time < '2026-06-20'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 25.8025 | 35 | 21 | 198 |


---

## T060 · daily_max

**Question:** What was the maximum rainfall at Lucretili on 2026-07-18?  
**Reference:** 0.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'rainfall' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-18' AND o.result_time < '2026-07-18'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 0 | 0 | 0 | 31 |


---

## T061 · daily_max

**Question:** What was the maximum rainfall at Lucretili on 2026-08-02?  
**Reference:** 0.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'rainfall' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-02' AND o.result_time < '2026-08-02'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 0 | 0 | 0 | 44 |


---

## T062 · daily_max

**Question:** What was the maximum rainfall at Ranverso on 2026-06-07?  
**Reference:** 0.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-07' AND o.result_time < '2026-06-07'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 0 | 0 | 0 | 24 |


---

## T063 · daily_max

**Question:** What was the maximum soil temperature at Baltanas on 2026-06-11?  
**Reference:** 27.92.  
**Recomputed:** `27.92` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-11' AND o.result_time < '2026-06-11'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 27.4001 | 27.92 | 26.71 | 576 |


---

## T064 · daily_max

**Question:** What was the maximum soil temperature at Baltanas on 2026-06-26?  
**Reference:** 29.24.  
**Recomputed:** `29.24` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-26' AND o.result_time < '2026-06-26'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 28.1309 | 29.24 | 25.49 | 575 |


---

## T065 · daily_max

**Question:** What was the maximum temperature at Delos on 2026-05-29?  
**Reference:** 42.  
**Recomputed:** `42.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-29' AND o.result_time < '2026-05-29'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 22.7946 | 42 | 14.9 | 239 |


---

## T066 · daily_max

**Question:** What was the maximum temperature at Lucretili on 2026-06-10?  
**Reference:** 36.  
**Recomputed:** `36.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-10' AND o.result_time < '2026-06-10'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 21.2698 | 36 | 8 | 4160 |


---

## T067 · daily_max

**Question:** What was the maximum temperature at Schenkenberg on 2026-06-03?  
**Reference:** 28.1.  
**Recomputed:** `28.1` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-03' AND o.result_time < '2026-06-03'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 15.7458 | 28.1 | 10.7 | 502 |


---

## T068 · daily_max

**Question:** What was the maximum temperature at Schenkenberg on 2026-07-26?  
**Reference:** 30.5.  
**Recomputed:** `30.5` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-26' AND o.result_time < '2026-07-26'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 22.7883 | 30.5 | 18.1 | 180 |


---

## T069 · daily_min

**Question:** What was the minimum rainfall at Lucretili on 2026-07-20?  
**Reference:** 0.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'rainfall' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-20' AND o.result_time < '2026-07-20'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 0 | 0 | 0 | 21 |


---

## T070 · daily_min

**Question:** What was the minimum rainfall at Lucretili on 2026-07-27?  
**Reference:** 0.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'rainfall' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-27' AND o.result_time < '2026-07-27'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 0 | 0 | 0 | 28 |


---

## T071 · daily_min

**Question:** What was the minimum rainfall at Lucretili on 2026-07-29?  
**Reference:** 0.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'rainfall' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-29' AND o.result_time < '2026-07-29'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 0 | 0 | 0 | 26 |


---

## T072 · daily_min

**Question:** What was the minimum rainfall at Ranverso on 2026-07-31?  
**Reference:** 0.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-31' AND o.result_time < '2026-07-31'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 0 | 0 | 0 | 24 |


---

## T073 · daily_min

**Question:** What was the minimum soil temperature at Baltanas on 2026-06-28?  
**Reference:** 30.35.  
**Recomputed:** `30.35` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-28' AND o.result_time < '2026-06-28'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 30.8057 | 31.05 | 30.35 | 555 |


---

## T074 · daily_min

**Question:** What was the minimum soil water potential at Baltanas on 2026-05-14?  
**Reference:** -42.424.  
**Recomputed:** `-42.424` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_water_potential' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-14' AND o.result_time < '2026-05-14'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 91.429 | 93.359 | -42.424 | 271 |


---

## T075 · daily_min

**Question:** What was the minimum temperature at Baltanas on 2026-05-31?  
**Reference:** 8.  
**Recomputed:** `8.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-31' AND o.result_time < '2026-05-31'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 20.4995 | 36.2 | 8 | 4931 |


---

## T076 · daily_min

**Question:** What was the minimum temperature at Delos on 2026-05-23?  
**Reference:** 14.6.  
**Recomputed:** `14.6` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-23' AND o.result_time < '2026-05-23'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 20.2171 | 38.3 | 14.6 | 240 |


---

## T077 · daily_min

**Question:** What was the minimum temperature at Schenkenberg on 2026-08-03?  
**Reference:** 22.1.  
**Recomputed:** `22.1` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-03' AND o.result_time < '2026-08-03'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 30.289 | 45 | 22.1 | 172 |


---

## T078 · hottest_day

**Question:** Which day in July 2026 had the highest average temperature at Delos?  
**Reference:** 2026-07-22 (daily average 30.556).  
**Recomputed:** `2026-07-22` → **MATCH**

```sql
SELECT o.result_time::date AS day, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-01' AND o.result_time < '2026-07-01'::date + interval '1 month'
GROUP BY 1 HAVING count(*) >= 10 ORDER BY 2 DESC LIMIT 5;
```
| day | avg | n |
|---|---|---|
| 2026-07-22 | 30.5561 | 237 |
| 2026-07-20 | 30.0987 | 240 |
| 2026-07-21 | 29.7921 | 239 |
| 2026-07-03 | 29.4208 | 240 |
| 2026-07-02 | 29.1988 | 240 |


---

## T079 · hottest_day

**Question:** Which day in July 2026 had the highest average temperature at Ranverso?  
**Reference:** 2026-07-30 (daily average 27.775).  
**Recomputed:** `2026-07-30` → **MATCH**

```sql
SELECT o.result_time::date AS day, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-01' AND o.result_time < '2026-07-01'::date + interval '1 month'
GROUP BY 1 HAVING count(*) >= 10 ORDER BY 2 DESC LIMIT 5;
```
| day | avg | n |
|---|---|---|
| 2026-07-30 | 27.775 | 216 |
| 2026-07-08 | 27.237 | 216 |
| 2026-07-31 | 27 | 216 |
| 2026-07-09 | 26.9824 | 216 |
| 2026-07-14 | 26.906 | 216 |


---

## T080 · hottest_day

**Question:** Which day in July 2026 had the highest average temperature at Schenkenberg?  
**Reference:** 2026-07-30 (daily average 30.634).  
**Recomputed:** `2026-07-30` → **MATCH**

```sql
SELECT o.result_time::date AS day, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-01' AND o.result_time < '2026-07-01'::date + interval '1 month'
GROUP BY 1 HAVING count(*) >= 10 ORDER BY 2 DESC LIMIT 5;
```
| day | avg | n |
|---|---|---|
| 2026-07-30 | 30.6336 | 149 |
| 2026-07-29 | 29.6212 | 189 |
| 2026-07-31 | 28.7518 | 193 |
| 2026-07-11 | 28.6702 | 289 |
| 2026-07-14 | 28.1327 | 226 |


---

## T081 · hottest_day

**Question:** Which day in June 2026 had the highest average temperature at Baltanas?  
**Reference:** 2026-06-24 (daily average 24.692).  
**Recomputed:** `2026-06-24` → **MATCH**

```sql
SELECT o.result_time::date AS day, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-01' AND o.result_time < '2026-06-01'::date + interval '1 month'
GROUP BY 1 HAVING count(*) >= 10 ORDER BY 2 DESC LIMIT 5;
```
| day | avg | n |
|---|---|---|
| 2026-06-24 | 24.6922 | 4922 |
| 2026-06-23 | 24.6362 | 4932 |
| 2026-06-22 | 24.6119 | 4933 |
| 2026-06-21 | 24.4468 | 4929 |
| 2026-06-27 | 23.9445 | 4931 |


---

## T082 · hottest_day

**Question:** Which day in June 2026 had the highest average temperature at Delos?  
**Reference:** 2026-06-30 (daily average 28.3).  
**Recomputed:** `2026-06-30` → **MATCH**

```sql
SELECT o.result_time::date AS day, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-01' AND o.result_time < '2026-06-01'::date + interval '1 month'
GROUP BY 1 HAVING count(*) >= 10 ORDER BY 2 DESC LIMIT 5;
```
| day | avg | n |
|---|---|---|
| 2026-06-30 | 28.3004 | 240 |
| 2026-06-29 | 27.3879 | 240 |
| 2026-06-26 | 27.0862 | 240 |
| 2026-06-12 | 27.0512 | 240 |
| 2026-06-25 | 27.0379 | 240 |


---

## T083 · hottest_day

**Question:** Which day in June 2026 had the highest average temperature at Lucretili?  
**Reference:** 2026-06-28 (daily average 27.266).  
**Recomputed:** `2026-06-28` → **MATCH**

```sql
SELECT o.result_time::date AS day, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-01' AND o.result_time < '2026-06-01'::date + interval '1 month'
GROUP BY 1 HAVING count(*) >= 10 ORDER BY 2 DESC LIMIT 5;
```
| day | avg | n |
|---|---|---|
| 2026-06-28 | 27.2656 | 3938 |
| 2026-06-21 | 26.6404 | 4110 |
| 2026-06-27 | 26.2868 | 3961 |
| 2026-06-30 | 25.4573 | 3947 |
| 2026-06-20 | 25.4494 | 4126 |


---

## T084 · hottest_day

**Question:** Which day in June 2026 had the highest average temperature at Ranverso?  
**Reference:** 2026-06-28 (daily average 27.918).  
**Recomputed:** `2026-06-28` → **MATCH**

```sql
SELECT o.result_time::date AS day, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-01' AND o.result_time < '2026-06-01'::date + interval '1 month'
GROUP BY 1 HAVING count(*) >= 10 ORDER BY 2 DESC LIMIT 5;
```
| day | avg | n |
|---|---|---|
| 2026-06-28 | 27.9179 | 162 |
| 2026-06-27 | 27.7917 | 216 |
| 2026-06-25 | 27.6392 | 153 |
| 2026-06-26 | 26.9088 | 216 |
| 2026-06-29 | 26.7014 | 216 |


---

## T085 · hottest_day

**Question:** Which day in June 2026 had the highest average temperature at Schenkenberg?  
**Reference:** 2026-06-27 (daily average 34.236).  
**Recomputed:** `2026-06-27` → **MATCH**

```sql
SELECT o.result_time::date AS day, avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-01' AND o.result_time < '2026-06-01'::date + interval '1 month'
GROUP BY 1 HAVING count(*) >= 10 ORDER BY 2 DESC LIMIT 5;
```
| day | avg | n |
|---|---|---|
| 2026-06-27 | 34.2356 | 132 |
| 2026-06-26 | 34.1027 | 146 |
| 2026-06-28 | 33.6752 | 105 |
| 2026-06-25 | 33.0815 | 151 |
| 2026-06-24 | 31.396 | 173 |


---

## T086 · range_avg

**Question:** What was the average temperature at Baltanas between 2026-05-19 and 2026-05-25?  
**Reference:** 19.074 (31989 observations, both days inclusive).  
**Recomputed:** `19.074062959142303` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-19' AND o.result_time < '2026-05-25'::date + 1;
```
| avg | n |
|---|---|
| 19.0741 | 31989 |


---

## T087 · range_avg

**Question:** What was the average temperature at Baltanas between 2026-06-18 and 2026-06-24?  
**Reference:** 23.44 (34506 observations, both days inclusive).  
**Recomputed:** `23.439610502521294` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-18' AND o.result_time < '2026-06-24'::date + 1;
```
| avg | n |
|---|---|
| 23.4396 | 34506 |


---

## T088 · range_avg

**Question:** What was the average temperature at Baltanas between 2026-07-27 and 2026-08-02?  
**Reference:** 24.215 (34409 observations, both days inclusive).  
**Recomputed:** `24.215089075532543` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-27' AND o.result_time < '2026-08-02'::date + 1;
```
| avg | n |
|---|---|
| 24.2151 | 34409 |


---

## T089 · range_avg

**Question:** What was the average temperature at Delos between 2026-05-20 and 2026-05-26?  
**Reference:** 21.651 (1663 observations, both days inclusive).  
**Recomputed:** `21.650691521346964` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-20' AND o.result_time < '2026-05-26'::date + 1;
```
| avg | n |
|---|---|
| 21.6507 | 1663 |


---

## T090 · range_avg

**Question:** What was the average temperature at Delos between 2026-06-29 and 2026-07-05?  
**Reference:** 28.318 (1680 observations, both days inclusive).  
**Recomputed:** `28.317559523809514` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-29' AND o.result_time < '2026-07-05'::date + 1;
```
| avg | n |
|---|---|
| 28.3176 | 1680 |


---

## T091 · range_avg

**Question:** What was the average temperature at Lucretili between 2026-07-04 and 2026-07-10?  
**Reference:** 23.698 (27435 observations, both days inclusive).  
**Recomputed:** `23.698487333697855` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-04' AND o.result_time < '2026-07-10'::date + 1;
```
| avg | n |
|---|---|
| 23.6985 | 27435 |


---

## T092 · range_avg

**Question:** What was the average temperature at Lucretili between 2026-07-06 and 2026-07-12?  
**Reference:** 24.241 (27290 observations, both days inclusive).  
**Recomputed:** `24.24065225357277` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-06' AND o.result_time < '2026-07-12'::date + 1;
```
| avg | n |
|---|---|
| 24.2407 | 27290 |


---

## T093 · range_avg

**Question:** What was the average temperature at Lucretili between 2026-07-08 and 2026-07-14?  
**Reference:** 25.067 (27656 observations, both days inclusive).  
**Recomputed:** `25.066690772346004` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-08' AND o.result_time < '2026-07-14'::date + 1;
```
| avg | n |
|---|---|
| 25.0667 | 27656 |


---

## T094 · range_avg

**Question:** What was the average temperature at Ranverso between 2026-06-20 and 2026-06-26?  
**Reference:** 26.529 (1359 observations, both days inclusive).  
**Recomputed:** `26.528697571743923` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-20' AND o.result_time < '2026-06-26'::date + 1;
```
| avg | n |
|---|---|
| 26.5287 | 1359 |


---

## T095 · range_avg

**Question:** What was the average temperature at Ranverso between 2026-06-29 and 2026-07-05?  
**Reference:** 26.248 (1512 observations, both days inclusive).  
**Recomputed:** `26.247751322751327` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-29' AND o.result_time < '2026-07-05'::date + 1;
```
| avg | n |
|---|---|
| 26.2478 | 1512 |


---

## T096 · range_avg

**Question:** What was the average temperature at Schenkenberg between 2026-06-07 and 2026-06-13?  
**Reference:** 16.821 (2332 observations, both days inclusive).  
**Recomputed:** `16.82092624356776` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-07' AND o.result_time < '2026-06-13'::date + 1;
```
| avg | n |
|---|---|
| 16.8209 | 2332 |


---

## T097 · range_avg

**Question:** What was the average temperature at Schenkenberg between 2026-07-10 and 2026-07-16?  
**Reference:** 27.677 (1610 observations, both days inclusive).  
**Recomputed:** `27.676894409937887` → **MATCH**

```sql
SELECT avg(o.value) AS avg, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-10' AND o.result_time < '2026-07-16'::date + 1;
```
| avg | n |
|---|---|
| 27.6769 | 1610 |


---

## T098 · unanswerable

**Question:** How many readings were recorded at Ranverso in September 2026?  
**Reference:** Cannot be answered: the data ends on 2026-08-12.  
**Recomputed:** `0` → **MANUAL**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'ranverso'
  AND result_time >= '2026-09-01' AND result_time < '2026-09-01'::date + interval '1 month';
```
| readings |
|---|
| 0 |


---

## T099 · daily_avg

**Question:** What was the relative humidity at Baltanas on 2026-07-01?  
**Reference:** 57.118 % on average (296 observations, from 33 % to 78 %).  
**Recomputed:** `57.11824324324324` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'hum1' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-01' AND o.result_time < '2026-07-01'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 57.1182 | 78 | 33 | 296 |


---

## T100 · unanswerable

**Question:** What was the temperature at Delos in April 2026?  
**Reference:** Cannot be answered: the data starts on 2026-05-13.  
**Recomputed:** `None` → **MANUAL**

```sql
SELECT min(result_time) AS first, max(result_time) AS last, count(*) FROM readings WHERE site_id = 'delos';
```
| first | last | count |
|---|---|---|
| 2026-05-13 01:00:00 | 2026-08-12 09:14:17 | 225945 |

- Expected: the asked period lies outside first..last.

---
