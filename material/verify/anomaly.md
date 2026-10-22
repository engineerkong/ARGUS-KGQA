# Verification — anomaly

Run `SET TIME ZONE 'UTC';` in psql first (`psql -h localhost -U argus -d argus_snapshot`).

## A001 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a rainfall anomaly at Lucretili on 2026-06-01?  
**Reference:** No. R6a_rain: metric 0 vs threshold 20 (window ending 2026-06-01 20:30 UTC); R6b_rain_cum7d: metric 0 vs threshold 100 (window ending 2026-06-01 20:30 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6a_rain';
```
| threshold_value | threshold_json |
|---|---|
| None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-01 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n_24h,
       avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour') AS mean_1h,
       avg(o.value) AS mean_24h,
       greatest(avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour'), avg(o.value)) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n_24h | mean_1h | mean_24h | metric |
|---|---|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 38 | 0 | 0 | 0 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6b_rain_cum7d';
```
| threshold_value | threshold_json |
|---|---|
| 100 | {"R6b_rain_cum7d": 100} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-01 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 192 | 0 |

- as_of = 2026-06-01 23:59:59+00 (windows end at the latest matching reading at or before it)
- R6a_rain: metric 0 vs threshold 20 → does not fire
- R6b_rain_cum7d: metric 0 vs threshold 100 → does not fire
- Raw readings: [data/A001_R6a_rain.csv](data/A001_R6a_rain.csv) (38 rows)
- Raw readings: [data/A001_R6b_rain_cum7d.csv](data/A001_R6b_rain_cum7d.csv) (192 rows)

---

## A002 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a rainfall anomaly at Lucretili on 2026-06-18?  
**Reference:** No. R6a_rain: metric 0 vs threshold 20 (window ending 2026-06-18 23:30 UTC); R6b_rain_cum7d: metric 0 vs threshold 100 (window ending 2026-06-18 23:30 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6a_rain';
```
| threshold_value | threshold_json |
|---|---|
| None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-18 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n_24h,
       avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour') AS mean_1h,
       avg(o.value) AS mean_24h,
       greatest(avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour'), avg(o.value)) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n_24h | mean_1h | mean_24h | metric |
|---|---|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 45 | 0 | 0 | 0 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6b_rain_cum7d';
```
| threshold_value | threshold_json |
|---|---|
| 100 | {"R6b_rain_cum7d": 100} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-18 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 317 | 0 |

- as_of = 2026-06-18 23:59:59+00 (windows end at the latest matching reading at or before it)
- R6a_rain: metric 0 vs threshold 20 → does not fire
- R6b_rain_cum7d: metric 0 vs threshold 100 → does not fire
- Raw readings: [data/A002_R6a_rain.csv](data/A002_R6a_rain.csv) (45 rows)
- Raw readings: [data/A002_R6b_rain_cum7d.csv](data/A002_R6b_rain_cum7d.csv) (317 rows)

---

## A003 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a rainfall anomaly at Lucretili on 2026-06-22?  
**Reference:** No. R6a_rain: metric 0 vs threshold 20 (window ending 2026-06-22 23:30 UTC); R6b_rain_cum7d: metric 0 vs threshold 100 (window ending 2026-06-22 23:30 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6a_rain';
```
| threshold_value | threshold_json |
|---|---|
| None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-22 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n_24h,
       avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour') AS mean_1h,
       avg(o.value) AS mean_24h,
       greatest(avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour'), avg(o.value)) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n_24h | mean_1h | mean_24h | metric |
|---|---|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 45 | 0 | 0 | 0 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6b_rain_cum7d';
```
| threshold_value | threshold_json |
|---|---|
| 100 | {"R6b_rain_cum7d": 100} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-22 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 307 | 0 |

- as_of = 2026-06-22 23:59:59+00 (windows end at the latest matching reading at or before it)
- R6a_rain: metric 0 vs threshold 20 → does not fire
- R6b_rain_cum7d: metric 0 vs threshold 100 → does not fire
- Raw readings: [data/A003_R6a_rain.csv](data/A003_R6a_rain.csv) (45 rows)
- Raw readings: [data/A003_R6b_rain_cum7d.csv](data/A003_R6b_rain_cum7d.csv) (307 rows)

---

## A004 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a rainfall anomaly at Ranverso on 2026-07-20?  
**Reference:** No. R2_rain_7d: metric 5.2 vs threshold 20 (window ending 2026-07-20 23:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-20 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 169 | 5.2 |

- as_of = 2026-07-20 23:59:59+00 (windows end at the latest matching reading at or before it)
- R2_rain_7d: metric 5.2 vs threshold 20 → does not fire
- Raw readings: [data/A004_R2_rain_7d.csv](data/A004_R2_rain_7d.csv) (169 rows)

---

## A005 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a temperature anomaly at Lucretili on 2026-05-14?  
**Reference:** No. R9a_temp_lt: metric 19 vs threshold 20 (window ending 2026-05-14 23:55 UTC); R9b_temp_st: max 1h change 0.1 vs threshold 5 (ending 2026-05-14 23:55 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-14 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 147 | 2 | 21 | 19 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 134 | 6.7 | 21.1 | 14.4 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 139 | 6 | 20 | 14 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 19 | 9.6 | 22.7 | 13.1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 130 | 7 | 20 | 13 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 123 | 7 | 20 | 13 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 127 | 7 | 20 | 13 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 5 | 7 | 20 | 13 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 4 | 7 | 20 | 13 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 4 | 7 | 20 | 13 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 12 | 7 | 17 | 10 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 9 | 6 | 15 | 9 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 9 | 6 | 15 | 9 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 11 | 13.1 | 21.2 | 8.1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 9 | 9 | 15 | 6 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 19 | 10 | 14 | 4 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 10 | 8.5 | 12.1 | 3.6 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-14 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 6 | 0.1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 8 | 0 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 7 | 0 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 7 | 0 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 6 | 0 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 7 | 0 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 1 | None |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 1 | None |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 1 | None |

- as_of = 2026-05-14 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 19 vs threshold 20 → does not fire
- R9b_temp_st: metric 0.1 vs threshold 5 → does not fire
- Raw readings: [data/A005_R9a_temp_lt.csv](data/A005_R9a_temp_lt.csv) (911 rows)
- Raw readings: [data/A005_R9b_temp_st.csv](data/A005_R9b_temp_st.csv) (47 rows)

---

## A006 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a temperature anomaly at Lucretili on 2026-05-16?  
**Reference:** No. R9a_temp_lt: metric 16 vs threshold 20 (window ending 2026-05-16 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-05-16 23:55 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-16 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 213 | 1 | 17 | 16 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 11 | 3 | 18 | 15 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 11 | 3 | 18 | 15 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 10 | 3 | 18 | 15 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 221 | 5 | 17 | 12 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 15 | 4 | 14 | 10 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 16 | 4 | 14 | 10 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 208 | 7 | 16 | 9 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 210 | 7 | 16 | 9 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 18 | 5 | 14 | 9 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 211 | 7 | 16 | 9 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 220 | 4.6 | 13 | 8.4 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 22 | 7.8 | 14.9 | 7.1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 18 | 6 | 11 | 5 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 17 | 11.4 | 15.5 | 4.1 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 16 | 6.7 | 9.6 | 2.9 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 19 | 9 | 11 | 2 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-16 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 1 | None |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 1 | None |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 1 | None |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 1 | None |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 1 | None |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 1 | None |

- as_of = 2026-05-16 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 16 vs threshold 20 → does not fire
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A006_R9a_temp_lt.csv](data/A006_R9a_temp_lt.csv) (1456 rows)
- Raw readings: [data/A006_R9b_temp_st.csv](data/A006_R9b_temp_st.csv) (89 rows)

---

## A007 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a temperature anomaly at Lucretili on 2026-06-12?  
**Reference:** Yes. R9a_temp_lt: metric 25 vs threshold 20 (window ending 2026-06-12 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-06-12 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-12 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 9 | 34 | 25 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 15 | 40 | 25 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 15 | 38 | 23 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 15 | 38 | 23 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 15 | 38 | 23 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 288 | 12.8 | 34.9 | 22.1 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 16.2 | 38 | 21.8 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 45 | 13 | 33 | 20 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 268 | 13 | 33 | 20 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 45 | 13 | 33 | 20 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 45 | 13 | 33 | 20 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 289 | 13 | 30 | 17 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 289 | 13 | 30 | 17 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 289 | 13 | 29 | 16 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 289 | 15 | 30 | 15 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 289 | 19 | 32.3 | 13.3 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 289 | 17 | 24 | 7 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 289 | 15.1 | 21.7 | 6.6 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-12 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.1 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-06-12 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 25 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A007_R9a_temp_lt.csv](data/A007_R9a_temp_lt.csv) (4183 rows)
- Raw readings: [data/A007_R9b_temp_st.csv](data/A007_R9b_temp_st.csv) (189 rows)

---

## A008 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a temperature anomaly at Lucretili on 2026-06-28?  
**Reference:** Yes. R9a_temp_lt: metric 26 vs threshold 20 (window ending 2026-06-28 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-06-28 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-28 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 15 | 41 | 26 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 31 | 21 | 45 | 24 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 31 | 21 | 45 | 24 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 31 | 21 | 45 | 24 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 20 | 43 | 23 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 25.3 | 46.6 | 21.3 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 288 | 21.7 | 41.2 | 19.5 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 20 | 38 | 18 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 20 | 38 | 18 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 20 | 38 | 18 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 288 | 21 | 37 | 16 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 288 | 22 | 38 | 16 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 288 | 22 | 38 | 16 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 287 | 25 | 37 | 12 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 91 | 22 | 34 | 12 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 288 | 28 | 39.9 | 11.9 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 288 | 24 | 30 | 6 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 283 | 22.6 | 28 | 5.4 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-28 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.4 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.2 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 0 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 0 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 0 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-06-28 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 26 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A008_R9a_temp_lt.csv](data/A008_R9a_temp_lt.csv) (3951 rows)
- Raw readings: [data/A008_R9b_temp_st.csv](data/A008_R9b_temp_st.csv) (183 rows)

---

## A009 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a temperature anomaly at Lucretili on 2026-07-20?  
**Reference:** Yes. R9a_temp_lt: metric 24 vs threshold 20 (window ending 2026-07-20 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-07-20 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-20 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 17 | 41 | 24 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 21 | 22 | 44 | 22 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 21 | 22 | 44 | 22 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 21 | 22 | 44 | 22 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 22 | 43 | 21 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 224 | 22 | 43 | 21 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 25.1 | 45.9 | 20.8 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 289 | 22 | 38 | 16 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 21 | 37 | 16 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 21 | 37 | 16 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 21 | 37 | 16 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 289 | 21 | 37 | 16 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 289 | 22 | 38 | 16 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 289 | 27.8 | 41.1 | 13.3 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 289 | 25 | 38 | 13 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 289 | 25 | 32 | 7 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 280 | 23.3 | 29.2 | 5.9 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-20 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.3 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 0 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 1 | None |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-07-20 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 24 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A009_R9a_temp_lt.csv](data/A009_R9a_temp_lt.csv) (3770 rows)
- Raw readings: [data/A009_R9b_temp_st.csv](data/A009_R9b_temp_st.csv) (173 rows)

---

## A010 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a vibration anomaly at Schenkenberg on 2026-05-15?  
**Reference:** Cannot be determined. R3_vib_zscore: no readings; R4_pga: no readings  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-05-15 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-15 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

- as_of = 2026-05-15 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: no readings (or no series with enough data) — not evaluated
- R4_pga: no readings (or no series with enough data) — not evaluated

---

## A011 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a vibration anomaly at Schenkenberg on 2026-05-18?  
**Reference:** Cannot be determined. R3_vib_zscore: no readings; R4_pga: no readings  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-05-18 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-18 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

- as_of = 2026-05-18 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: no readings (or no series with enough data) — not evaluated
- R4_pga: no readings (or no series with enough data) — not evaluated

---

## A012 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a vibration anomaly at Schenkenberg on 2026-05-19?  
**Reference:** Cannot be determined. R3_vib_zscore: no readings; R4_pga: no readings  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-05-19 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-19 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

- as_of = 2026-05-19 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: no readings (or no series with enough data) — not evaluated
- R4_pga: no readings (or no series with enough data) — not evaluated

---

## A013 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a vibration anomaly at Schenkenberg on 2026-05-20?  
**Reference:** Cannot be determined. R3_vib_zscore: no readings; R4_pga: no readings  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-05-20 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-20 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

- as_of = 2026-05-20 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: no readings (or no series with enough data) — not evaluated
- R4_pga: no readings (or no series with enough data) — not evaluated

---

## A014 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a vibration anomaly at Schenkenberg on 2026-05-22?  
**Reference:** No. R3_vib_zscore: max z-score 0.127 vs threshold 4.5; R4_pga: max z-score 0.125 vs threshold 0.5  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-05-22 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 3dff8100-55c1-11f1-9208-83a949003bcf | rmsComposed | 241 | 8.69046 | 66.0671 | 0.3 | 2026-05-22 23:33:00 | 0.126999 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 238 | 12.4063 | 92.1902 | 0.9 | 2026-05-22 23:33:00 | 0.12481 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 239 | 24.1297 | 191.352 | 0.6 | 2026-05-22 23:33:00 | 0.122965 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 239 | 14.2799 | 115.554 | 0.6 | 2026-05-22 23:33:00 | 0.118385 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 237 | 11.8941 | 100.265 | 0.9 | 2026-05-22 23:33:00 | 0.10965 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-22 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 238 | 12.4063 | 92.1902 | 0.9 | 2026-05-22 23:33:00 | 0.12481 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 239 | 24.1297 | 191.352 | 0.6 | 2026-05-22 23:33:00 | 0.122965 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 239 | 14.2799 | 115.554 | 0.6 | 2026-05-22 23:33:00 | 0.118385 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 237 | 11.8941 | 100.265 | 0.9 | 2026-05-22 23:33:00 | 0.10965 |

- as_of = 2026-05-22 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 0.126999 vs threshold 4.5 → does not fire
- R4_pga: metric 0.12481 vs threshold 0.5 → does not fire
- Raw readings: [data/A014_R3_vib_zscore.csv](data/A014_R3_vib_zscore.csv) (1194 rows)
- Raw readings: [data/A014_R4_pga.csv](data/A014_R4_pga.csv) (953 rows)

---

## A015 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a vibration anomaly at Schenkenberg on 2026-06-08?  
**Reference:** Yes. R3_vib_zscore: max z-score 6.364 vs threshold 4.5; R4_pga: max z-score 6.364 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-06-08 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 351 | 0.1 | 3.15787e-16 | 0.1 | 2026-06-08 23:30:00 | 2.0655 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 351 | 0.1 | 3.15787e-16 | 0.1 | 2026-06-08 23:30:00 | 2.0655 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 351 | 0.1 | 3.15787e-16 | 0.1 | 2026-06-08 23:30:00 | 2.0655 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 517 | 0.1 | 5.178e-16 | 0.1 | 2026-06-08 23:30:00 | 1.71529 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 517 | 0.1 | 5.178e-16 | 0.1 | 2026-06-08 23:30:00 | 1.71529 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 517 | 0.1 | 5.178e-16 | 0.1 | 2026-06-08 23:30:00 | 1.71529 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 530 | 0.1 | 5.30522e-16 | 0.1 | 2026-06-08 23:30:00 | 1.70032 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsZAxis | 530 | 0.1 | 5.30522e-16 | 0.1 | 2026-06-08 23:30:00 | 1.70032 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 530 | 0.1 | 5.30522e-16 | 0.1 | 2026-06-08 23:30:00 | 1.70032 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 517 | 0.480658 | 0.111666 | 0.3 | 2026-06-08 23:30:00 | 1.61785 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 351 | 0.554131 | 0.0977162 | 0.4 | 2026-06-08 23:30:00 | 1.57733 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 351 | 0.373504 | 0.0540019 | 0.3 | 2026-06-08 23:30:00 | 1.36114 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 517 | 0.371373 | 0.0530743 | 0.3 | 2026-06-08 23:30:00 | 1.34478 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 351 | 0.373789 | 0.0564592 | 0.3 | 2026-06-08 23:30:00 | 1.30695 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-08 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 517 | 0.480658 | 0.111666 | 0.3 | 2026-06-08 23:30:00 | 1.61785 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 351 | 0.554131 | 0.0977162 | 0.4 | 2026-06-08 23:30:00 | 1.57733 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 351 | 0.373504 | 0.0540019 | 0.3 | 2026-06-08 23:30:00 | 1.36114 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 517 | 0.371373 | 0.0530743 | 0.3 | 2026-06-08 23:30:00 | 1.34478 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 351 | 0.373789 | 0.0564592 | 0.3 | 2026-06-08 23:30:00 | 1.30695 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 530 | 0.52566 | 0.0997262 | 0.4 | 2026-06-08 23:30:00 | 1.26005 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 517 | 0.368665 | 0.0575512 | 0.3 | 2026-06-08 23:30:00 | 1.19312 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 530 | 0.364151 | 0.0576075 | 0.3 | 2026-06-08 23:30:00 | 1.11359 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 530 | 0.365283 | 0.0598931 | 0.3 | 2026-06-08 23:30:00 | 1.08999 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

- as_of = 2026-06-08 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 6.36396 vs threshold 4.5 → fires
- R4_pga: metric 6.36396 vs threshold 0.5 → fires
- Raw readings: [data/A015_R3_vib_zscore.csv](data/A015_R3_vib_zscore.csv) (11385 rows)
- Raw readings: [data/A015_R4_pga.csv](data/A015_R4_pga.csv) (6440 rows)

---

## A016 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a vibration anomaly at Schenkenberg on 2026-06-17?  
**Reference:** Yes. R3_vib_zscore: max z-score 6.364 vs threshold 4.5; R4_pga: max z-score 6.364 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-06-17 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 960 | 0.1 | 6.48e-16 | 0.1 | 2026-06-17 23:30:00 | 1.90606 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsZAxis | 960 | 0.1 | 6.48e-16 | 0.1 | 2026-06-17 23:30:00 | 1.90606 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 960 | 0.1 | 6.48e-16 | 0.1 | 2026-06-17 23:30:00 | 1.90606 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 530 | 0.1 | 5.30522e-16 | 0.1 | 2026-06-17 23:30:00 | 1.70032 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 530 | 0.1 | 5.30522e-16 | 0.1 | 2026-06-17 23:30:00 | 1.70032 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 530 | 0.1 | 5.30522e-16 | 0.1 | 2026-06-17 23:30:00 | 1.70032 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 530 | 0.503396 | 0.107404 | 0.4 | 2026-06-17 23:30:00 | 0.962684 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 766 | 0.3453 | 0.0597873 | 0.3 | 2026-06-17 20:00:00 | 0.757691 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 960 | 0.47125 | 0.0966442 | 0.4 | 2026-06-17 23:30:00 | 0.73724 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 530 | 0.34566 | 0.0628718 | 0.3 | 2026-06-17 23:30:00 | 0.726246 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 530 | 0.343774 | 0.0639052 | 0.3 | 2026-06-17 23:30:00 | 0.684977 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 766 | 0.342689 | 0.0631429 | 0.3 | 2026-06-17 20:00:00 | 0.676075 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 960 | 0.335938 | 0.055623 | 0.3 | 2026-06-17 23:30:00 | 0.646091 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 960 | 0.334375 | 0.0553928 | 0.3 | 2026-06-17 23:30:00 | 0.620568 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-17 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 530 | 0.503396 | 0.107404 | 0.4 | 2026-06-17 23:30:00 | 0.962684 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 766 | 0.3453 | 0.0597873 | 0.3 | 2026-06-17 20:00:00 | 0.757691 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 960 | 0.47125 | 0.0966442 | 0.4 | 2026-06-17 23:30:00 | 0.73724 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 530 | 0.34566 | 0.0628718 | 0.3 | 2026-06-17 23:30:00 | 0.726246 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 530 | 0.343774 | 0.0639052 | 0.3 | 2026-06-17 23:30:00 | 0.684977 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 766 | 0.342689 | 0.0631429 | 0.3 | 2026-06-17 20:00:00 | 0.676075 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 960 | 0.335938 | 0.055623 | 0.3 | 2026-06-17 23:30:00 | 0.646091 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 960 | 0.334375 | 0.0553928 | 0.3 | 2026-06-17 23:30:00 | 0.620568 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 766 | 0.439426 | 0.112932 | 0.4 | 2026-06-17 20:00:00 | 0.349108 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

- as_of = 2026-06-17 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 6.36396 vs threshold 4.5 → fires
- R4_pga: metric 6.36396 vs threshold 0.5 → fires
- Raw readings: [data/A016_R3_vib_zscore.csv](data/A016_R3_vib_zscore.csv) (16533 rows)
- Raw readings: [data/A016_R4_pga.csv](data/A016_R4_pga.csv) (9014 rows)

---

## A017 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a vibration anomaly at Schenkenberg on 2026-08-03?  
**Reference:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-08-03 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 932 | 0.337661 | 0.0757516 | 0.9 | 2026-07-14 00:00:00 | 7.42346 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 1171 | 0.1 | 9.23665e-16 | 0.1 | 2026-08-03 18:30:00 | 2.20863 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 1171 | 0.1 | 9.23665e-16 | 0.1 | 2026-08-03 18:30:00 | 2.20863 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 1171 | 0.1 | 9.23665e-16 | 0.1 | 2026-08-03 18:30:00 | 2.20863 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 1945 | 0.1 | 1.97014e-15 | 0.1 | 2026-08-03 20:00:00 | 1.76806 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 1945 | 0.1 | 1.97014e-15 | 0.1 | 2026-08-03 20:00:00 | 1.76806 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 1945 | 0.1 | 1.97014e-15 | 0.1 | 2026-08-03 20:00:00 | 1.76806 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1945 | 0.43054 | 0.0742605 | 0.4 | 2026-08-03 20:00:00 | 0.411253 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 3151 | 0.1 | 2.43015e-15 | 0.1 | 2026-08-03 23:30:00 | 0.411168 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 3151 | 0.1 | 2.43015e-15 | 0.1 | 2026-08-03 23:30:00 | 0.411168 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 3151 | 0.427991 | 0.0697076 | 0.4 | 2026-08-03 23:30:00 | 0.40155 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 3151 | 0.310536 | 0.0359404 | 0.3 | 2026-08-03 23:30:00 | 0.293161 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 3151 | 0.31006 | 0.0362958 | 0.3 | 2026-08-03 23:30:00 | 0.277175 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1945 | 0.306581 | 0.0464457 | 0.3 | 2026-08-03 20:00:00 | 0.141692 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1171 | 0.406063 | 0.0475439 | 0.4 | 2026-08-03 18:30:00 | 0.127528 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-03 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 932 | 0.337661 | 0.0757516 | 0.9 | 2026-07-14 00:00:00 | 7.42346 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1945 | 0.43054 | 0.0742605 | 0.4 | 2026-08-03 20:00:00 | 0.411253 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 3151 | 0.427991 | 0.0697076 | 0.4 | 2026-08-03 23:30:00 | 0.40155 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 3151 | 0.310536 | 0.0359404 | 0.3 | 2026-08-03 23:30:00 | 0.293161 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 3151 | 0.31006 | 0.0362958 | 0.3 | 2026-08-03 23:30:00 | 0.277175 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1945 | 0.306581 | 0.0464457 | 0.3 | 2026-08-03 20:00:00 | 0.141692 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1171 | 0.406063 | 0.0475439 | 0.4 | 2026-08-03 18:30:00 | 0.127528 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 1945 | 0.305398 | 0.0481713 | 0.3 | 2026-08-03 20:00:00 | 0.112068 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 1171 | 0.301025 | 0.0371804 | 0.3 | 2026-08-03 18:30:00 | 0.027562 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 1171 | 0.299146 | 0.038538 | 0.3 | 2026-08-03 18:30:00 | 0.0221592 |

- as_of = 2026-08-03 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 7.42346 vs threshold 4.5 → fires
- R4_pga: metric 7.42346 vs threshold 0.5 → fires
- Raw readings: [data/A017_R3_vib_zscore.csv](data/A017_R3_vib_zscore.csv) (45693 rows)
- Raw readings: [data/A017_R4_pga.csv](data/A017_R4_pga.csv) (23594 rows)

---

## A018 · verdict_on_date

**Question:** According to the AD-RT expert rules, was there a visitor count anomaly at Lucretili on 2026-08-01?  
**Reference:** No. R5_visitors: latest reading 0 at 2026-08-01 23:55 UTC vs threshold 3  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors';
```
| threshold_value | threshold_json |
|---|---|
| 3 | {"R5_visitors_peak": 3} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-01 23:59:59+00')
SELECT r.sensor_id, o.property_id, o.result_time, o.value AS metric FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL
  AND o.result_time = anchor.t ORDER BY metric DESC;
```
| sensor_id | property_id | result_time | metric |
|---|---|---|---|
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | pulse_counter | 2026-08-01 23:55:00 | 0 |

- as_of = 2026-08-01 23:59:59+00 (windows end at the latest matching reading at or before it)
- R5_visitors: metric 0 vs threshold 3 → does not fire
- Raw readings: [data/A018_R5_visitors.csv](data/A018_R5_visitors.csv) (1 rows)

---

## A019 · verdict_on_date

**Question:** Did the rainfall at Ranverso exceed its AD-RT threshold on 2026-06-24?  
**Reference:** No. R2_rain_7d: metric 0.4 vs threshold 20 (window ending 2026-06-24 15:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-24 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 167 | 0.4 |

- as_of = 2026-06-24 23:59:59+00 (windows end at the latest matching reading at or before it)
- R2_rain_7d: metric 0.4 vs threshold 20 → does not fire
- Raw readings: [data/A019_R2_rain_7d.csv](data/A019_R2_rain_7d.csv) (167 rows)

---

## A020 · verdict_on_date

**Question:** Did the rainfall at Ranverso exceed its AD-RT threshold on 2026-07-04?  
**Reference:** No. R2_rain_7d: metric 0.8 vs threshold 20 (window ending 2026-07-04 23:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-04 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 163 | 0.8 |

- as_of = 2026-07-04 23:59:59+00 (windows end at the latest matching reading at or before it)
- R2_rain_7d: metric 0.8 vs threshold 20 → does not fire
- Raw readings: [data/A020_R2_rain_7d.csv](data/A020_R2_rain_7d.csv) (163 rows)

---

## A021 · verdict_on_date

**Question:** Did the temperature at Lucretili exceed its AD-RT threshold on 2026-05-24?  
**Reference:** Yes. R9a_temp_lt: metric 26 vs threshold 20 (window ending 2026-05-24 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-05-24 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-24 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 8 | 34 | 26 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 18 | 13 | 38 | 25 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 18 | 13 | 38 | 25 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 18 | 13 | 38 | 25 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 13 | 37 | 24 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 16.5 | 37.8 | 21.3 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 289 | 13 | 33.6 | 20.6 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 14 | 34 | 20 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 14 | 34 | 20 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 14 | 34 | 20 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 11 | 14 | 34 | 20 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 24 | 13 | 28 | 15 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 24 | 13 | 28 | 15 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 24 | 13 | 28 | 15 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 24 | 19.5 | 32 | 12.5 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 24 | 16 | 28 | 12 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 24 | 14.6 | 20.7 | 6.1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 24 | 17 | 23 | 6 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-24 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 1 | None |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 1 | None |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 1 | None |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 1 | None |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 1 | None |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 1 | None |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 1 | None |

- as_of = 2026-05-24 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 26 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A021_R9a_temp_lt.csv](data/A021_R9a_temp_lt.csv) (1991 rows)
- Raw readings: [data/A021_R9b_temp_st.csv](data/A021_R9b_temp_st.csv) (89 rows)

---

## A022 · verdict_on_date

**Question:** Did the temperature at Lucretili exceed its AD-RT threshold on 2026-06-03?  
**Reference:** No. R9a_temp_lt: metric 20 vs threshold 20 (window ending 2026-06-03 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-06-03 23:55 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-03 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 286 | 10 | 30 | 20 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 286 | 14 | 33 | 19 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 15 | 33.9 | 18.9 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 287 | 11.9 | 30.1 | 18.2 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 151 | 10 | 24 | 14 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 285 | 12 | 25 | 13 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 23 | 12 | 24 | 12 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 286 | 12 | 24 | 12 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 286 | 12 | 24 | 12 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 286 | 14 | 26 | 12 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 23 | 12 | 24 | 12 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 23 | 12 | 24 | 12 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 286 | 14 | 26 | 12 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 286 | 14 | 26 | 12 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 285 | 14 | 25 | 11 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 282 | 18.1 | 28.4 | 10.3 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 277 | 16 | 20 | 4 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 23 | 14.6 | 17.9 | 3.3 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-03 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 0 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 1 | None |

- as_of = 2026-06-03 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 20 vs threshold 20 → does not fire
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A022_R9a_temp_lt.csv](data/A022_R9a_temp_lt.csv) (3685 rows)
- Raw readings: [data/A022_R9b_temp_st.csv](data/A022_R9b_temp_st.csv) (177 rows)

---

## A023 · verdict_on_date

**Question:** Did the temperature at Lucretili exceed its AD-RT threshold on 2026-06-05?  
**Reference:** Yes. R9a_temp_lt: metric 24 vs threshold 20 (window ending 2026-06-05 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-06-05 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-05 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 8 | 32 | 24 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 12 | 34 | 22 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 34 | 11 | 28 | 17 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 13 | 30 | 17 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 13 | 30 | 17 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 34 | 11 | 28 | 17 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 13 | 30 | 17 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 34 | 11 | 28 | 17 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 218 | 11 | 26 | 15 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 289 | 12 | 24 | 12 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 289 | 12 | 24 | 12 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 289 | 12 | 24 | 12 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 15.1 | 25.7 | 10.6 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 289 | 12.1 | 22.6 | 10.5 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 288 | 15 | 22 | 7 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 289 | 18.5 | 25.2 | 6.7 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 289 | 16 | 20 | 4 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 289 | 14.2 | 17.8 | 3.6 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-05 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.3 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.1 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-06-05 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 24 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A023_R9a_temp_lt.csv](data/A023_R9a_temp_lt.csv) (4100 rows)
- Raw readings: [data/A023_R9b_temp_st.csv](data/A023_R9b_temp_st.csv) (170 rows)

---

## A024 · verdict_on_date

**Question:** Did the temperature at Lucretili exceed its AD-RT threshold on 2026-07-17?  
**Reference:** Yes. R9a_temp_lt: metric 25 vs threshold 20 (window ending 2026-07-17 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-07-17 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-17 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 16 | 41 | 25 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 34 | 22 | 44 | 22 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 34 | 22 | 44 | 22 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 34 | 22 | 44 | 22 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 22 | 43 | 21 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 26.1 | 44.5 | 18.4 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 21 | 38 | 17 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 21 | 38 | 17 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 21 | 38 | 17 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 196 | 23 | 40 | 17 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 282 | 23 | 38 | 15 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 282 | 23 | 38 | 15 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 287 | 22 | 37 | 15 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 289 | 29.1 | 40.4 | 11.3 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 287 | 26 | 37 | 11 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 285 | 25 | 31 | 6 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 279 | 24 | 29.1 | 5.1 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 56 | 22.8 | 23.7 | 0.9 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-17 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 1 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 1 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 1 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.4 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.2 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-07-17 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 25 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A024_R9a_temp_lt.csv](data/A024_R9a_temp_lt.csv) (3814 rows)
- Raw readings: [data/A024_R9b_temp_st.csv](data/A024_R9b_temp_st.csv) (176 rows)

---

## A025 · verdict_on_date

**Question:** Did the temperature at Lucretili exceed its AD-RT threshold on 2026-08-11?  
**Reference:** Yes. R9a_temp_lt: metric 27 vs threshold 20 (window ending 2026-08-11 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-08-11 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-11 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 277 | 14 | 41 | 27 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 39 | 23 | 49 | 26 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 39 | 23 | 49 | 26 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 39 | 23 | 49 | 26 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 277 | 19 | 42 | 23 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 23 | 26.1 | 48.7 | 22.6 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 178 | 24 | 45 | 21 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 277 | 19 | 38 | 19 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 277 | 19 | 38 | 19 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 277 | 19 | 38 | 19 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 277 | 23 | 41 | 18 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 277 | 23 | 41 | 18 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 277 | 29.4 | 45.6 | 16.2 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 277 | 23 | 39 | 16 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 277 | 25 | 40 | 15 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 277 | 26 | 33 | 7 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 276 | 24.3 | 31.3 | 7 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-11 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 10 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.3 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 0 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-08-11 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 27 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A025_R9a_temp_lt.csv](data/A025_R9a_temp_lt.csv) (3641 rows)
- Raw readings: [data/A025_R9b_temp_st.csv](data/A025_R9b_temp_st.csv) (173 rows)

---

## A026 · verdict_on_date

**Question:** Did the vibration at Schenkenberg exceed its AD-RT threshold on 2026-05-23?  
**Reference:** No. R3_vib_zscore: max z-score 0.116 vs threshold 4.5; R4_pga: max z-score 0.112 vs threshold 0.5  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-05-23 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 3dff8100-55c1-11f1-9208-83a949003bcf | rmsComposed | 289 | 7.29896 | 60.4122 | 0.3 | 2026-05-23 23:30:00 | 0.115854 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 287 | 20.2077 | 174.838 | 0.6 | 2026-05-23 23:30:00 | 0.112147 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 286 | 10.5199 | 84.2038 | 1.1 | 2026-05-23 23:30:00 | 0.111871 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 287 | 12.0021 | 105.572 | 0.7 | 2026-05-23 23:30:00 | 0.107056 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 285 | 10.0923 | 91.5205 | 1.1 | 2026-05-23 23:30:00 | 0.0982542 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-23 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 287 | 20.2077 | 174.838 | 0.6 | 2026-05-23 23:30:00 | 0.112147 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 286 | 10.5199 | 84.2038 | 1.1 | 2026-05-23 23:30:00 | 0.111871 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 287 | 12.0021 | 105.572 | 0.7 | 2026-05-23 23:30:00 | 0.107056 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 285 | 10.0923 | 91.5205 | 1.1 | 2026-05-23 23:30:00 | 0.0982542 |

- as_of = 2026-05-23 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 0.115854 vs threshold 4.5 → does not fire
- R4_pga: metric 0.112147 vs threshold 0.5 → does not fire
- Raw readings: [data/A026_R3_vib_zscore.csv](data/A026_R3_vib_zscore.csv) (1434 rows)
- Raw readings: [data/A026_R4_pga.csv](data/A026_R4_pga.csv) (1145 rows)

---

## A027 · verdict_on_date

**Question:** Did the vibration at Schenkenberg exceed its AD-RT threshold on 2026-06-24?  
**Reference:** Yes. R3_vib_zscore: max z-score 6.364 vs threshold 4.5; R4_pga: max z-score 6.364 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-06-24 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 725 | 0.33131 | 0.0603353 | 0.2 | 2026-06-24 23:30:00 | 2.17634 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 1289 | 0.1 | 1.10592e-15 | 0.1 | 2026-06-24 23:30:00 | 2.13327 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsZAxis | 1289 | 0.1 | 1.10592e-15 | 0.1 | 2026-06-24 23:30:00 | 2.13327 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 1289 | 0.1 | 1.10592e-15 | 0.1 | 2026-06-24 23:30:00 | 2.13327 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 803 | 0.435866 | 0.111968 | 0.3 | 2026-06-24 20:00:00 | 1.21343 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 725 | 0.47669 | 0.102493 | 0.4 | 2026-06-24 23:30:00 | 0.74824 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 803 | 0.343213 | 0.0591609 | 0.3 | 2026-06-24 20:00:00 | 0.730431 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 803 | 0.340473 | 0.0626781 | 0.3 | 2026-06-24 20:00:00 | 0.645732 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 1289 | 0.455237 | 0.0888996 | 0.4 | 2026-06-24 23:30:00 | 0.621337 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 803 | 0.1 | 5.96228e-16 | 0.1 | 2026-06-24 20:00:00 | 0.605175 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 803 | 0.1 | 5.96228e-16 | 0.1 | 2026-06-24 20:00:00 | 0.605175 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 803 | 0.1 | 5.96228e-16 | 0.1 | 2026-06-24 20:00:00 | 0.605175 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 1289 | 0.326687 | 0.0506127 | 0.3 | 2026-06-24 23:30:00 | 0.527286 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 725 | 0.331034 | 0.0593264 | 0.3 | 2026-06-24 23:30:00 | 0.523114 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-24 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 725 | 0.33131 | 0.0603353 | 0.2 | 2026-06-24 23:30:00 | 2.17634 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 803 | 0.435866 | 0.111968 | 0.3 | 2026-06-24 20:00:00 | 1.21343 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 725 | 0.47669 | 0.102493 | 0.4 | 2026-06-24 23:30:00 | 0.74824 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 803 | 0.343213 | 0.0591609 | 0.3 | 2026-06-24 20:00:00 | 0.730431 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 803 | 0.340473 | 0.0626781 | 0.3 | 2026-06-24 20:00:00 | 0.645732 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 1289 | 0.455237 | 0.0888996 | 0.4 | 2026-06-24 23:30:00 | 0.621337 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 1289 | 0.326687 | 0.0506127 | 0.3 | 2026-06-24 23:30:00 | 0.527286 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 725 | 0.331034 | 0.0593264 | 0.3 | 2026-06-24 23:30:00 | 0.523114 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 1289 | 0.325679 | 0.0502903 | 0.3 | 2026-06-24 23:30:00 | 0.510612 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

- as_of = 2026-06-24 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 6.36396 vs threshold 4.5 → fires
- R4_pga: metric 6.36396 vs threshold 0.5 → fires
- Raw readings: [data/A027_R3_vib_zscore.csv](data/A027_R3_vib_zscore.csv) (19899 rows)
- Raw readings: [data/A027_R4_pga.csv](data/A027_R4_pga.csv) (10697 rows)

---

## A028 · verdict_on_date

**Question:** Did the vibration at Schenkenberg exceed its AD-RT threshold on 2026-06-25?  
**Reference:** Yes. R3_vib_zscore: max z-score 6.364 vs threshold 4.5; R4_pga: max z-score 6.364 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-06-25 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 1337 | 0.1 | 1.17888e-15 | 0.1 | 2026-06-25 23:30:00 | 2.10719 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsZAxis | 1337 | 0.1 | 1.17888e-15 | 0.1 | 2026-06-25 23:30:00 | 2.10719 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 1337 | 0.1 | 1.17888e-15 | 0.1 | 2026-06-25 23:30:00 | 2.10719 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 808 | 0.342946 | 0.0590749 | 0.3 | 2026-06-25 16:00:00 | 0.726968 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 755 | 0.473642 | 0.101548 | 0.4 | 2026-06-25 19:30:00 | 0.725201 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 808 | 0.1 | 5.95151e-16 | 0.1 | 2026-06-25 16:00:00 | 0.676225 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 808 | 0.1 | 5.95151e-16 | 0.1 | 2026-06-25 16:00:00 | 0.676225 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 808 | 0.1 | 5.95151e-16 | 0.1 | 2026-06-25 16:00:00 | 0.676225 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 808 | 0.340223 | 0.0625644 | 0.3 | 2026-06-25 16:00:00 | 0.642902 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 1337 | 0.453553 | 0.0878805 | 0.5 | 2026-06-25 23:30:00 | 0.528528 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 1337 | 0.325729 | 0.0499432 | 0.3 | 2026-06-25 23:30:00 | 0.51517 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 755 | 0.329536 | 0.0588109 | 0.3 | 2026-06-25 19:30:00 | 0.502227 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 755 | 0.329934 | 0.059618 | 0.3 | 2026-06-25 19:30:00 | 0.502093 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 1337 | 0.324832 | 0.0496479 | 0.3 | 2026-06-25 23:30:00 | 0.500157 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-25 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 808 | 0.342946 | 0.0590749 | 0.3 | 2026-06-25 16:00:00 | 0.726968 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 755 | 0.473642 | 0.101548 | 0.4 | 2026-06-25 19:30:00 | 0.725201 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 808 | 0.340223 | 0.0625644 | 0.3 | 2026-06-25 16:00:00 | 0.642902 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 1337 | 0.453553 | 0.0878805 | 0.5 | 2026-06-25 23:30:00 | 0.528528 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 1337 | 0.325729 | 0.0499432 | 0.3 | 2026-06-25 23:30:00 | 0.51517 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 755 | 0.329536 | 0.0588109 | 0.3 | 2026-06-25 19:30:00 | 0.502227 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 755 | 0.329934 | 0.059618 | 0.3 | 2026-06-25 19:30:00 | 0.502093 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 1337 | 0.324832 | 0.0496479 | 0.3 | 2026-06-25 23:30:00 | 0.500157 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 808 | 0.435396 | 0.111846 | 0.4 | 2026-06-25 16:00:00 | 0.316472 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

- as_of = 2026-06-25 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 6.36396 vs threshold 4.5 → fires
- R4_pga: metric 6.36396 vs threshold 0.5 → fires
- Raw readings: [data/A028_R3_vib_zscore.csv](data/A028_R3_vib_zscore.csv) (20397 rows)
- Raw readings: [data/A028_R4_pga.csv](data/A028_R4_pga.csv) (10946 rows)

---

## A029 · verdict_on_date

**Question:** Did the vibration at Schenkenberg exceed its AD-RT threshold on 2026-06-27?  
**Reference:** Yes. R3_vib_zscore: max z-score 6.364 vs threshold 4.5; R4_pga: max z-score 6.364 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-06-27 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 1433 | 0.1 | 1.32156e-15 | 0.1 | 2026-06-27 23:30:00 | 2.03721 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 1433 | 0.1 | 1.32156e-15 | 0.1 | 2026-06-27 23:30:00 | 2.03721 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsZAxis | 1433 | 0.1 | 1.32156e-15 | 0.1 | 2026-06-27 23:30:00 | 2.03721 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 819 | 0.1 | 5.93308e-16 | 0.1 | 2026-06-27 20:00:00 | 0.795278 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 819 | 0.1 | 5.93308e-16 | 0.1 | 2026-06-27 20:00:00 | 0.795278 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 819 | 0.1 | 5.93308e-16 | 0.1 | 2026-06-27 20:00:00 | 0.795278 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 819 | 0.342369 | 0.0588847 | 0.3 | 2026-06-27 20:00:00 | 0.719521 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 798 | 0.469925 | 0.100114 | 0.4 | 2026-06-27 14:30:00 | 0.698452 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 819 | 0.339683 | 0.0623151 | 0.3 | 2026-06-27 20:00:00 | 0.636805 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 1433 | 0.450244 | 0.0859348 | 0.4 | 2026-06-27 23:30:00 | 0.584678 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 798 | 0.1 | 5.97445e-16 | 0.1 | 2026-06-27 14:30:00 | 0.557485 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 798 | 0.1 | 5.97445e-16 | 0.1 | 2026-06-27 14:30:00 | 0.557485 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 798 | 0.1 | 5.97445e-16 | 0.1 | 2026-06-27 14:30:00 | 0.557485 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 1433 | 0.324006 | 0.0488115 | 0.3 | 2026-06-27 23:30:00 | 0.491802 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-27 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 819 | 0.342369 | 0.0588847 | 0.3 | 2026-06-27 20:00:00 | 0.719521 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 798 | 0.469925 | 0.100114 | 0.4 | 2026-06-27 14:30:00 | 0.698452 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 819 | 0.339683 | 0.0623151 | 0.3 | 2026-06-27 20:00:00 | 0.636805 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 1433 | 0.450244 | 0.0859348 | 0.4 | 2026-06-27 23:30:00 | 0.584678 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 1433 | 0.324006 | 0.0488115 | 0.3 | 2026-06-27 23:30:00 | 0.491802 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 798 | 0.32782 | 0.0577611 | 0.3 | 2026-06-27 14:30:00 | 0.481631 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 798 | 0.328195 | 0.0585497 | 0.3 | 2026-06-27 14:30:00 | 0.481565 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 1433 | 0.323168 | 0.0483562 | 0.3 | 2026-06-27 23:30:00 | 0.479115 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 819 | 0.434921 | 0.111167 | 0.4 | 2026-06-27 20:00:00 | 0.314128 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

- as_of = 2026-06-27 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 6.36396 vs threshold 4.5 → fires
- R4_pga: metric 6.36396 vs threshold 0.5 → fires
- Raw readings: [data/A029_R3_vib_zscore.csv](data/A029_R3_vib_zscore.csv) (21297 rows)
- Raw readings: [data/A029_R4_pga.csv](data/A029_R4_pga.csv) (11396 rows)

---

## A030 · verdict_on_date

**Question:** Did the vibration at Schenkenberg exceed its AD-RT threshold on 2026-07-29?  
**Reference:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-07-29 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 932 | 0.337661 | 0.0757516 | 0.9 | 2026-07-14 00:00:00 | 7.42346 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 1041 | 0.1 | 7.37463e-16 | 0.1 | 2026-07-29 23:30:00 | 2.14528 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 1041 | 0.1 | 7.37463e-16 | 0.1 | 2026-07-29 23:30:00 | 2.14528 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 1041 | 0.1 | 7.37463e-16 | 0.1 | 2026-07-29 23:30:00 | 2.14528 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 1807 | 0.1 | 1.81473e-15 | 0.1 | 2026-07-29 23:30:00 | 1.82771 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 1807 | 0.1 | 1.81473e-15 | 0.1 | 2026-07-29 23:30:00 | 1.82771 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 1807 | 0.1 | 1.81473e-15 | 0.1 | 2026-07-29 23:30:00 | 1.82771 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1807 | 0.432319 | 0.0759102 | 0.4 | 2026-07-29 23:30:00 | 0.42575 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2921 | 0.428928 | 0.0695896 | 0.4 | 2026-07-29 23:30:00 | 0.415701 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2921 | 0.311503 | 0.0369753 | 0.3 | 2026-07-29 23:30:00 | 0.311098 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2921 | 0.310852 | 0.0374923 | 0.3 | 2026-07-29 23:30:00 | 0.289458 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 2921 | 0.1 | 2.51981e-15 | 0.1 | 2026-07-29 23:30:00 | 0.286389 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 2921 | 0.1 | 2.51981e-15 | 0.1 | 2026-07-29 23:30:00 | 0.286389 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1807 | 0.307637 | 0.0473691 | 0.3 | 2026-07-29 23:30:00 | 0.161222 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1041 | 0.407012 | 0.0497719 | 0.4 | 2026-07-29 23:30:00 | 0.140893 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-29 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 932 | 0.337661 | 0.0757516 | 0.9 | 2026-07-14 00:00:00 | 7.42346 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1807 | 0.432319 | 0.0759102 | 0.4 | 2026-07-29 23:30:00 | 0.42575 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2921 | 0.428928 | 0.0695896 | 0.4 | 2026-07-29 23:30:00 | 0.415701 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2921 | 0.311503 | 0.0369753 | 0.3 | 2026-07-29 23:30:00 | 0.311098 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2921 | 0.310852 | 0.0374923 | 0.3 | 2026-07-29 23:30:00 | 0.289458 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1807 | 0.307637 | 0.0473691 | 0.3 | 2026-07-29 23:30:00 | 0.161222 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1041 | 0.407012 | 0.0497719 | 0.4 | 2026-07-29 23:30:00 | 0.140893 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 1807 | 0.306143 | 0.0495794 | 0.3 | 2026-07-29 23:30:00 | 0.123898 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 1041 | 0.301537 | 0.0389283 | 0.3 | 2026-07-29 23:30:00 | 0.0394825 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 1041 | 0.299904 | 0.0398121 | 0.3 | 2026-07-29 23:30:00 | 0.00241287 |

- as_of = 2026-07-29 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 7.42346 vs threshold 4.5 → fires
- R4_pga: metric 7.42346 vs threshold 0.5 → fires
- Raw readings: [data/A030_R3_vib_zscore.csv](data/A030_R3_vib_zscore.csv) (42705 rows)
- Raw readings: [data/A030_R4_pga.csv](data/A030_R4_pga.csv) (22100 rows)

---

## A031 · verdict_on_date

**Question:** Was the rainfall at Lucretili anomalous on 2026-05-16 according to its AD-RT rules?  
**Reference:** No. R6a_rain: metric 0 vs threshold 20 (window ending 2026-05-16 23:00 UTC); R6b_rain_cum7d: metric 0 vs threshold 100 (window ending 2026-05-16 23:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6a_rain';
```
| threshold_value | threshold_json |
|---|---|
| None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-16 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n_24h,
       avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour') AS mean_1h,
       avg(o.value) AS mean_24h,
       greatest(avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour'), avg(o.value)) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n_24h | mean_1h | mean_24h | metric |
|---|---|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 15 | 0 | 0 | 0 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6b_rain_cum7d';
```
| threshold_value | threshold_json |
|---|---|
| 100 | {"R6b_rain_cum7d": 100} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-16 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 24 | 0 |

- as_of = 2026-05-16 23:59:59+00 (windows end at the latest matching reading at or before it)
- R6a_rain: metric 0 vs threshold 20 → does not fire
- R6b_rain_cum7d: metric 0 vs threshold 100 → does not fire
- Raw readings: [data/A031_R6a_rain.csv](data/A031_R6a_rain.csv) (15 rows)
- Raw readings: [data/A031_R6b_rain_cum7d.csv](data/A031_R6b_rain_cum7d.csv) (24 rows)

---

## A032 · verdict_on_date

**Question:** Was the rainfall at Ranverso anomalous on 2026-07-29 according to its AD-RT rules?  
**Reference:** No. R2_rain_7d: metric 0 vs threshold 20 (window ending 2026-07-29 23:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-29 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 169 | 0 |

- as_of = 2026-07-29 23:59:59+00 (windows end at the latest matching reading at or before it)
- R2_rain_7d: metric 0 vs threshold 20 → does not fire
- Raw readings: [data/A032_R2_rain_7d.csv](data/A032_R2_rain_7d.csv) (169 rows)

---

## A033 · verdict_on_date

**Question:** Was the temperature at Lucretili anomalous on 2026-06-15 according to its AD-RT rules?  
**Reference:** Yes. R9a_temp_lt: metric 27 vs threshold 20 (window ending 2026-06-15 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-06-15 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-15 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 6 | 33 | 27 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 13 | 35 | 22 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 43 | 14 | 35 | 21 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 43 | 14 | 35 | 21 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 43 | 14 | 35 | 21 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 18 | 37 | 19 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 266 | 15 | 34 | 19 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 287 | 15.1 | 33.7 | 18.6 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 13 | 30 | 17 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 13 | 30 | 17 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 13 | 30 | 17 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 281 | 14 | 30 | 16 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 269 | 14 | 30 | 16 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 269 | 14 | 30 | 16 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 283 | 17 | 30 | 13 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 284 | 21.2 | 32 | 10.8 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 273 | 18 | 24 | 6 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 203 | 16.8 | 22.2 | 5.4 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-15 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 12 | 0.4 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 11 | 0.3 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-06-15 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 27 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A033_R9a_temp_lt.csv](data/A033_R9a_temp_lt.csv) (4013 rows)
- Raw readings: [data/A033_R9b_temp_st.csv](data/A033_R9b_temp_st.csv) (186 rows)

---

## A034 · verdict_on_date

**Question:** Was the temperature at Lucretili anomalous on 2026-07-02 according to its AD-RT rules?  
**Reference:** No. R9a_temp_lt: metric 18 vs threshold 20 (window ending 2026-07-02 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-07-02 23:55 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-02 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 267 | 16 | 34 | 18 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 267 | 13 | 31 | 18 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 288 | 12.7 | 30.5 | 17.8 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 16.6 | 32.8 | 16.2 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 268 | 17 | 31 | 14 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 268 | 17 | 31 | 14 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 268 | 17 | 31 | 14 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 269 | 14 | 27 | 13 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 269 | 14 | 27 | 13 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 287 | 14 | 26 | 12 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 284 | 15 | 27 | 12 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 181 | 12 | 24 | 12 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 28 | 13 | 24 | 11 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 28 | 13 | 24 | 11 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 28 | 13 | 24 | 11 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 286 | 19 | 27.7 | 8.7 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 242 | 15.6 | 21.7 | 6.1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 242 | 19 | 24 | 5 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-02 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 12 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 12 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 11 | 0.1 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-07-02 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 18 vs threshold 20 → does not fire
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A034_R9a_temp_lt.csv](data/A034_R9a_temp_lt.csv) (3794 rows)
- Raw readings: [data/A034_R9b_temp_st.csv](data/A034_R9b_temp_st.csv) (185 rows)

---

## A035 · verdict_on_date

**Question:** Was the temperature at Lucretili anomalous on 2026-07-03 according to its AD-RT rules?  
**Reference:** Yes. R9a_temp_lt: metric 25 vs threshold 20 (window ending 2026-07-03 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-07-03 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-03 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 31 | 16 | 41 | 25 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 31 | 16 | 41 | 25 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 31 | 16 | 41 | 25 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 286 | 14 | 37 | 23 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 223 | 16 | 37 | 21 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 285 | 17 | 37 | 20 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 288 | 16.7 | 36.2 | 19.5 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 19.7 | 38.6 | 18.9 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 286 | 18 | 36 | 18 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 286 | 18 | 36 | 18 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 286 | 18 | 36 | 18 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 288 | 16 | 32 | 16 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 259 | 17 | 33 | 16 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 259 | 17 | 33 | 16 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 284 | 19 | 32 | 13 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 285 | 22.6 | 35.1 | 12.5 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 239 | 18.1 | 24 | 5.9 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 234 | 20 | 25 | 5 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-03 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 11 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 9 | 1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 12 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 12 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 10 | 0.1 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-07-03 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 25 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A035_R9a_temp_lt.csv](data/A035_R9a_temp_lt.csv) (3905 rows)
- Raw readings: [data/A035_R9b_temp_st.csv](data/A035_R9b_temp_st.csv) (178 rows)

---

## A036 · verdict_on_date

**Question:** Was the temperature at Lucretili anomalous on 2026-07-09 according to its AD-RT rules?  
**Reference:** Yes. R9a_temp_lt: metric 27 vs threshold 20 (window ending 2026-07-09 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-07-09 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-09 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 12 | 39 | 27 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 31 | 18 | 43 | 25 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 31 | 18 | 43 | 25 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 31 | 18 | 43 | 25 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 36 | 19 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 122 | 19 | 38 | 19 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 21.3 | 39.8 | 18.5 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 289 | 18.1 | 36 | 17.9 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 270 | 18 | 34 | 16 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 270 | 18 | 34 | 16 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 288 | 18 | 33 | 15 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 32 | 15 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 32 | 15 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 32 | 15 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 287 | 24.1 | 35.4 | 11.3 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 286 | 21 | 32 | 11 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 285 | 21 | 27 | 6 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 259 | 19.5 | 24.8 | 5.3 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-09 23:59:59+00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 7 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 12 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 9 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 9 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 12 | 1 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 11 | 0.4 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 12 | 0.3 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-07-09 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 27 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/A036_R9a_temp_lt.csv](data/A036_R9a_temp_lt.csv) (3918 rows)
- Raw readings: [data/A036_R9b_temp_st.csv](data/A036_R9b_temp_st.csv) (170 rows)

---

## A037 · verdict_on_date

**Question:** Was the vibration at Schenkenberg anomalous on 2026-05-14 according to its AD-RT rules?  
**Reference:** Cannot be determined. R3_vib_zscore: no readings; R4_pga: no readings  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-05-14 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-14 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
_(no rows)_

- as_of = 2026-05-14 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: no readings (or no series with enough data) — not evaluated
- R4_pga: no readings (or no series with enough data) — not evaluated

---

## A038 · verdict_on_date

**Question:** Was the vibration at Schenkenberg anomalous on 2026-05-24 according to its AD-RT rules?  
**Reference:** No. R3_vib_zscore: max z-score 0.107 vs threshold 4.5; R4_pga: max z-score 0.104 vs threshold 0.5  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-05-24 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 3dff8100-55c1-11f1-9208-83a949003bcf | rmsComposed | 337 | 6.30297 | 55.998 | 0.3 | 2026-05-24 23:30:00 | 0.1072 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 335 | 17.4113 | 161.973 | 0.6 | 2026-05-24 23:30:00 | 0.103791 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 334 | 9.17784 | 77.9875 | 1.1 | 2026-05-24 23:30:00 | 0.103579 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 335 | 10.3824 | 97.7966 | 0.7 | 2026-05-24 23:30:00 | 0.0990053 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 333 | 8.81261 | 84.7254 | 1.2 | 2026-05-24 23:30:00 | 0.0898504 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-24 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 335 | 17.4113 | 161.973 | 0.6 | 2026-05-24 23:30:00 | 0.103791 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 334 | 9.17784 | 77.9875 | 1.1 | 2026-05-24 23:30:00 | 0.103579 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 335 | 10.3824 | 97.7966 | 0.7 | 2026-05-24 23:30:00 | 0.0990053 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 333 | 8.81261 | 84.7254 | 1.2 | 2026-05-24 23:30:00 | 0.0898504 |

- as_of = 2026-05-24 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 0.1072 vs threshold 4.5 → does not fire
- R4_pga: metric 0.103791 vs threshold 0.5 → does not fire
- Raw readings: [data/A038_R3_vib_zscore.csv](data/A038_R3_vib_zscore.csv) (1674 rows)
- Raw readings: [data/A038_R4_pga.csv](data/A038_R4_pga.csv) (1337 rows)

---

## A039 · verdict_on_date

**Question:** Was the vibration at Schenkenberg anomalous on 2026-05-27 according to its AD-RT rules?  
**Reference:** No. R3_vib_zscore: max z-score 0.09 vs threshold 4.5; R4_pga: max z-score 0.087 vs threshold 0.5  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-05-27 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 3dff8100-55c1-11f1-9208-83a949003bcf | rmsComposed | 479 | 4.52756 | 47.0495 | 0.3 | 2026-05-27 23:30:00 | 0.0898535 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 476 | 6.78929 | 65.4301 | 1.1 | 2026-05-27 23:30:00 | 0.0869522 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 477 | 12.4258 | 135.955 | 0.7 | 2026-05-27 23:30:00 | 0.0862474 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 477 | 7.48994 | 82.0775 | 0.7 | 2026-05-27 23:30:00 | 0.0827259 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 475 | 6.53663 | 71.0253 | 1.1 | 2026-05-27 23:30:00 | 0.076545 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-27 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 476 | 6.78929 | 65.4301 | 1.1 | 2026-05-27 23:30:00 | 0.0869522 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 477 | 12.4258 | 135.955 | 0.7 | 2026-05-27 23:30:00 | 0.0862474 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 477 | 7.48994 | 82.0775 | 0.7 | 2026-05-27 23:30:00 | 0.0827259 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 475 | 6.53663 | 71.0253 | 1.1 | 2026-05-27 23:30:00 | 0.076545 |

- as_of = 2026-05-27 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 0.0898535 vs threshold 4.5 → does not fire
- R4_pga: metric 0.0869522 vs threshold 0.5 → does not fire
- Raw readings: [data/A039_R3_vib_zscore.csv](data/A039_R3_vib_zscore.csv) (2384 rows)
- Raw readings: [data/A039_R4_pga.csv](data/A039_R4_pga.csv) (1905 rows)

---

## A040 · verdict_on_date

**Question:** Was the vibration at Schenkenberg anomalous on 2026-06-05 according to its AD-RT rules?  
**Reference:** Yes. R3_vib_zscore: max z-score 6.364 vs threshold 4.5; R4_pga: max z-score 6.364 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-06-05 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 315 | 0.383492 | 0.0462621 | 0.2 | 2026-06-05 12:00:00 | 3.96635 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 397 | 0.394962 | 0.0329079 | 0.3 | 2026-06-05 23:30:00 | 2.88569 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 397 | 0.392947 | 0.0382308 | 0.3 | 2026-06-05 23:30:00 | 2.43121 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 397 | 0.516877 | 0.0990754 | 0.3 | 2026-06-05 23:30:00 | 2.18901 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 315 | 0.1 | 2.62461e-16 | 0.1 | 2026-06-05 12:00:00 | 2.11503 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 315 | 0.1 | 2.62461e-16 | 0.1 | 2026-06-05 12:00:00 | 2.11503 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 315 | 0.1 | 2.62461e-16 | 0.1 | 2026-06-05 12:00:00 | 2.11503 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 398 | 0.564573 | 0.0831309 | 0.4 | 2026-06-05 23:30:00 | 1.97968 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 315 | 0.571111 | 0.0881397 | 0.4 | 2026-06-05 12:00:00 | 1.94136 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 397 | 0.1 | 3.79758e-16 | 0.1 | 2026-06-05 23:30:00 | 1.93682 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 397 | 0.1 | 3.79758e-16 | 0.1 | 2026-06-05 23:30:00 | 1.93682 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 397 | 0.1 | 3.79758e-16 | 0.1 | 2026-06-05 23:30:00 | 1.93682 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsZAxis | 398 | 0.1 | 3.81055e-16 | 0.1 | 2026-06-05 23:30:00 | 1.93023 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 398 | 0.1 | 3.81055e-16 | 0.1 | 2026-06-05 23:30:00 | 1.93023 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-05 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 315 | 0.383492 | 0.0462621 | 0.2 | 2026-06-05 12:00:00 | 3.96635 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 397 | 0.394962 | 0.0329079 | 0.3 | 2026-06-05 23:30:00 | 2.88569 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 397 | 0.392947 | 0.0382308 | 0.3 | 2026-06-05 23:30:00 | 2.43121 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 397 | 0.516877 | 0.0990754 | 0.3 | 2026-06-05 23:30:00 | 2.18901 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 398 | 0.564573 | 0.0831309 | 0.4 | 2026-06-05 23:30:00 | 1.97968 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 315 | 0.571111 | 0.0881397 | 0.4 | 2026-06-05 12:00:00 | 1.94136 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 398 | 0.386181 | 0.048443 | 0.3 | 2026-06-05 23:30:00 | 1.77902 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 398 | 0.388191 | 0.0499874 | 0.3 | 2026-06-05 23:30:00 | 1.76426 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 315 | 0.38381 | 0.0493587 | 0.3 | 2026-06-05 12:00:00 | 1.69797 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

- as_of = 2026-06-05 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 6.36396 vs threshold 4.5 → fires
- R4_pga: metric 6.36396 vs threshold 0.5 → fires
- Raw readings: [data/A040_R3_vib_zscore.csv](data/A040_R3_vib_zscore.csv) (9657 rows)
- Raw readings: [data/A040_R4_pga.csv](data/A040_R4_pga.csv) (5576 rows)

---

## A041 · verdict_on_date

**Question:** Was the vibration at Schenkenberg anomalous on 2026-06-28 according to its AD-RT rules?  
**Reference:** Yes. R3_vib_zscore: max z-score 6.364 vs threshold 4.5; R4_pga: max z-score 6.364 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-06-28 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 801 | 0.327965 | 0.0586317 | 0.2 | 2026-06-28 22:00:00 | 2.18252 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 83 | 0.1 | 8.07762e-17 | 0.1 | 2026-06-05 12:00:00 | 2.06167 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 1480 | 0.1 | 1.38927e-15 | 0.1 | 2026-06-28 23:30:00 | 2.00784 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsZAxis | 1480 | 0.1 | 1.38927e-15 | 0.1 | 2026-06-28 23:30:00 | 2.00784 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 1480 | 0.1 | 1.38927e-15 | 0.1 | 2026-06-28 23:30:00 | 2.00784 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 825 | 0.1 | 5.92621e-16 | 0.1 | 2026-06-28 20:00:00 | 0.843035 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 825 | 0.1 | 5.92621e-16 | 0.1 | 2026-06-28 20:00:00 | 0.843035 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 825 | 0.1 | 5.92621e-16 | 0.1 | 2026-06-28 20:00:00 | 0.843035 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 825 | 0.342303 | 0.0590185 | 0.3 | 2026-06-28 20:00:00 | 0.716776 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 801 | 0.469663 | 0.100018 | 0.4 | 2026-06-28 22:00:00 | 0.696507 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 825 | 0.339394 | 0.0621796 | 0.3 | 2026-06-28 20:00:00 | 0.633551 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 801 | 0.1 | 5.96696e-16 | 0.1 | 2026-06-28 22:00:00 | 0.581443 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 801 | 0.1 | 5.96696e-16 | 0.1 | 2026-06-28 22:00:00 | 0.581443 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 801 | 0.1 | 5.96696e-16 | 0.1 | 2026-06-28 22:00:00 | 0.581443 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 1480 | 0.449054 | 0.0850226 | 0.4 | 2026-06-28 23:30:00 | 0.576953 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-28 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 83 | 0.39759 | 0.0153348 | 0.3 | 2026-06-05 12:00:00 | 6.36396 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 83 | 0.4 | 0.0268866 | 0.3 | 2026-06-05 12:00:00 | 3.71932 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 83 | 0.540964 | 0.0560468 | 0.4 | 2026-06-05 12:00:00 | 2.51511 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 801 | 0.327965 | 0.0586317 | 0.2 | 2026-06-28 22:00:00 | 2.18252 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 825 | 0.342303 | 0.0590185 | 0.3 | 2026-06-28 20:00:00 | 0.716776 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 801 | 0.469663 | 0.100018 | 0.4 | 2026-06-28 22:00:00 | 0.696507 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 825 | 0.339394 | 0.0621796 | 0.3 | 2026-06-28 20:00:00 | 0.633551 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 1480 | 0.449054 | 0.0850226 | 0.4 | 2026-06-28 23:30:00 | 0.576953 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 1480 | 0.323243 | 0.0482143 | 0.3 | 2026-06-28 23:30:00 | 0.482082 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 801 | 0.327715 | 0.0576779 | 0.3 | 2026-06-28 22:00:00 | 0.480519 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 1480 | 0.322365 | 0.0479986 | 0.3 | 2026-06-28 23:30:00 | 0.465948 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 825 | 0.435152 | 0.111195 | 0.4 | 2026-06-28 20:00:00 | 0.316124 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

- as_of = 2026-06-28 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 6.36396 vs threshold 4.5 → fires
- R4_pga: metric 6.36396 vs threshold 0.5 → fires
- Raw readings: [data/A041_R3_vib_zscore.csv](data/A041_R3_vib_zscore.csv) (21633 rows)
- Raw readings: [data/A041_R4_pga.csv](data/A041_R4_pga.csv) (11564 rows)

---

## A042 · verdict_on_date

**Question:** Was the vibration at Schenkenberg anomalous on 2026-07-17 according to its AD-RT rules?  
**Reference:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-07-17 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 932 | 0.337661 | 0.0757516 | 0.9 | 2026-07-14 00:00:00 | 7.42346 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 1524 | 0.1 | 1.45121e-15 | 0.1 | 2026-07-17 23:00:00 | 1.97952 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 1524 | 0.1 | 1.45121e-15 | 0.1 | 2026-07-17 23:00:00 | 1.97952 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 1524 | 0.1 | 1.45121e-15 | 0.1 | 2026-07-17 23:00:00 | 1.97952 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 2348 | 0.1 | 2.3556e-15 | 0.1 | 2026-07-17 23:30:00 | 1.63781 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 2348 | 0.1 | 2.3556e-15 | 0.1 | 2026-07-17 23:30:00 | 1.63781 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1524 | 0.437467 | 0.0811281 | 0.4 | 2026-07-17 23:00:00 | 0.461827 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2348 | 0.434412 | 0.0756558 | 0.4 | 2026-07-17 23:30:00 | 0.454853 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2348 | 0.314395 | 0.0406162 | 0.3 | 2026-07-17 23:30:00 | 0.354421 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2348 | 0.314012 | 0.040593 | 0.3 | 2026-07-17 23:30:00 | 0.345181 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 728 | 0.1 | 6.23236e-16 | 0.1 | 2026-07-17 19:00:00 | 0.289475 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 728 | 0.1 | 6.23236e-16 | 0.1 | 2026-07-17 19:00:00 | 0.289475 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 728 | 0.1 | 6.23236e-16 | 0.1 | 2026-07-17 19:00:00 | 0.289475 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 728 | 0.413324 | 0.0547316 | 0.4 | 2026-07-17 19:00:00 | 0.243446 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1524 | 0.310892 | 0.0492675 | 0.3 | 2026-07-17 23:00:00 | 0.221087 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-17 23:59:59+00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 932 | 0.337661 | 0.0757516 | 0.9 | 2026-07-14 00:00:00 | 7.42346 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1524 | 0.437467 | 0.0811281 | 0.4 | 2026-07-17 23:00:00 | 0.461827 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2348 | 0.434412 | 0.0756558 | 0.4 | 2026-07-17 23:30:00 | 0.454853 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2348 | 0.314395 | 0.0406162 | 0.3 | 2026-07-17 23:30:00 | 0.354421 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2348 | 0.314012 | 0.040593 | 0.3 | 2026-07-17 23:30:00 | 0.345181 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 728 | 0.413324 | 0.0547316 | 0.4 | 2026-07-17 19:00:00 | 0.243446 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1524 | 0.310892 | 0.0492675 | 0.3 | 2026-07-17 23:00:00 | 0.221087 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 1524 | 0.310105 | 0.050745 | 0.3 | 2026-07-17 23:00:00 | 0.199133 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 728 | 0.305632 | 0.0420444 | 0.3 | 2026-07-17 19:00:00 | 0.13395 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 728 | 0.304258 | 0.0425299 | 0.3 | 2026-07-17 19:00:00 | 0.100124 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

- as_of = 2026-07-17 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 7.42346 vs threshold 4.5 → fires
- R4_pga: metric 7.42346 vs threshold 0.5 → fires
- Raw readings: [data/A042_R3_vib_zscore.csv](data/A042_R3_vib_zscore.csv) (35691 rows)
- Raw readings: [data/A042_R4_pga.csv](data/A042_R4_pga.csv) (18593 rows)

---

## A043 · verdict_on_date

**Question:** Was the visitor count at Lucretili anomalous on 2026-05-19 according to its AD-RT rules?  
**Reference:** No. R5_visitors: latest reading 0 at 2026-05-19 23:55 UTC vs threshold 3  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors';
```
| threshold_value | threshold_json |
|---|---|
| 3 | {"R5_visitors_peak": 3} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-19 23:59:59+00')
SELECT r.sensor_id, o.property_id, o.result_time, o.value AS metric FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL
  AND o.result_time = anchor.t ORDER BY metric DESC;
```
| sensor_id | property_id | result_time | metric |
|---|---|---|---|
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | pulse_counter | 2026-05-19 23:55:00 | 0 |

- as_of = 2026-05-19 23:59:59+00 (windows end at the latest matching reading at or before it)
- R5_visitors: metric 0 vs threshold 3 → does not fire
- Raw readings: [data/A043_R5_visitors.csv](data/A043_R5_visitors.csv) (1 rows)

---

## A044 · verdict_on_date

**Question:** Was the visitor count at Lucretili anomalous on 2026-06-03 according to its AD-RT rules?  
**Reference:** No. R5_visitors: latest reading 0 at 2026-06-03 23:55 UTC vs threshold 3  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors';
```
| threshold_value | threshold_json |
|---|---|
| 3 | {"R5_visitors_peak": 3} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-03 23:59:59+00')
SELECT r.sensor_id, o.property_id, o.result_time, o.value AS metric FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL
  AND o.result_time = anchor.t ORDER BY metric DESC;
```
| sensor_id | property_id | result_time | metric |
|---|---|---|---|
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | pulse_counter | 2026-06-03 23:55:00 | 0 |

- as_of = 2026-06-03 23:59:59+00 (windows end at the latest matching reading at or before it)
- R5_visitors: metric 0 vs threshold 3 → does not fire
- Raw readings: [data/A044_R5_visitors.csv](data/A044_R5_visitors.csv) (1 rows)

---

## A045 · verdict_on_date

**Question:** Was the visitor count at Lucretili anomalous on 2026-06-23 according to its AD-RT rules?  
**Reference:** No. R5_visitors: latest reading 0 at 2026-06-23 23:55 UTC vs threshold 3  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors';
```
| threshold_value | threshold_json |
|---|---|
| 3 | {"R5_visitors_peak": 3} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-23 23:59:59+00')
SELECT r.sensor_id, o.property_id, o.result_time, o.value AS metric FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL
  AND o.result_time = anchor.t ORDER BY metric DESC;
```
| sensor_id | property_id | result_time | metric |
|---|---|---|---|
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | pulse_counter | 2026-06-23 23:55:00 | 0 |

- as_of = 2026-06-23 23:59:59+00 (windows end at the latest matching reading at or before it)
- R5_visitors: metric 0 vs threshold 3 → does not fire
- Raw readings: [data/A045_R5_visitors.csv](data/A045_R5_visitors.csv) (1 rows)

---

## A046 · verdict_latest

**Question:** Based on the latest data, is there a rainfall anomaly at Lucretili according to its AD-RT rules?  
**Reference:** No. R6a_rain: metric 0 vs threshold 20 (window ending 2026-08-12 08:00 UTC); R6b_rain_cum7d: metric 0 vs threshold 100 (window ending 2026-08-12 08:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6a_rain';
```
| threshold_value | threshold_json |
|---|---|
| None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-12T09:15:00+00:00')
SELECT r.sensor_id, o.property_id, count(*) AS n_24h,
       avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour') AS mean_1h,
       avg(o.value) AS mean_24h,
       greatest(avg(o.value) FILTER (WHERE o.result_time >= anchor.t - interval '1 hour'), avg(o.value)) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n_24h | mean_1h | mean_24h | metric |
|---|---|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 43 | 0 | 0 | 0 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6b_rain_cum7d';
```
| threshold_value | threshold_json |
|---|---|
| 100 | {"R6b_rain_cum7d": 100} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-12T09:15:00+00:00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 237 | 0 |

- as_of = 2026-08-12T09:15:00+00:00 (windows end at the latest matching reading at or before it)
- R6a_rain: metric 0 vs threshold 20 → does not fire
- R6b_rain_cum7d: metric 0 vs threshold 100 → does not fire
- Raw readings: [data/A046_R6a_rain.csv](data/A046_R6a_rain.csv) (43 rows)
- Raw readings: [data/A046_R6b_rain_cum7d.csv](data/A046_R6b_rain_cum7d.csv) (237 rows)

---

## A047 · verdict_latest

**Question:** Based on the latest data, is there a rainfall anomaly at Ranverso according to its AD-RT rules?  
**Reference:** No. R2_rain_7d: metric 0.6 vs threshold 20 (window ending 2026-08-12 09:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-12T09:15:00+00:00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 208 | 0.6 |

- as_of = 2026-08-12T09:15:00+00:00 (windows end at the latest matching reading at or before it)
- R2_rain_7d: metric 0.6 vs threshold 20 → does not fire
- Raw readings: [data/A047_R2_rain_7d.csv](data/A047_R2_rain_7d.csv) (208 rows)

---

## A048 · verdict_latest

**Question:** Based on the latest data, is there a temperature anomaly at Lucretili according to its AD-RT rules?  
**Reference:** Yes. R9a_temp_lt: metric 27 vs threshold 20 (window ending 2026-08-12 09:15 UTC); R9b_temp_st: max 1h change 2 vs threshold 5 (ending 2026-08-12 09:15 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-12T09:15:00+00:00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 277 | 14 | 41 | 27 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 40 | 24 | 49 | 25 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 40 | 24 | 49 | 25 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 40 | 24 | 49 | 25 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 277 | 19 | 42 | 23 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 23 | 27.2 | 48.7 | 21.5 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 182 | 24 | 45 | 21 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 277 | 19 | 38 | 19 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 277 | 19 | 38 | 19 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 277 | 19 | 38 | 19 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 277 | 25 | 41 | 16 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 277 | 25 | 41 | 16 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 277 | 30.5 | 45.6 | 15.1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 276 | 24 | 39 | 15 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 277 | 27 | 40 | 13 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 276 | 25.2 | 31.3 | 6.1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 277 | 27 | 33 | 6 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-12T09:15:00+00:00')
, w AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value,
        o.value - lag(o.value) OVER (PARTITION BY r.sensor_id, o.property_id ORDER BY o.result_time) AS diff
      FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
        AND o.result_time BETWEEN anchor.t - interval '1 hours' AND anchor.t)
SELECT sensor_id, property_id, count(*) AS n, max(abs(diff)) AS metric FROM w
GROUP BY 1, 2 ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 2 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 12 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.2 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-08-12T09:15:00+00:00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 27 vs threshold 20 → fires
- R9b_temp_st: metric 2 vs threshold 5 → does not fire
- Raw readings: [data/A048_R9a_temp_lt.csv](data/A048_R9a_temp_lt.csv) (3647 rows)
- Raw readings: [data/A048_R9b_temp_st.csv](data/A048_R9b_temp_st.csv) (156 rows)

---

## A049 · verdict_latest

**Question:** Based on the latest data, is there a vibration anomaly at Schenkenberg according to its AD-RT rules?  
**Reference:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-08-12T09:15:00+00:00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 932 | 0.337661 | 0.0757516 | 0.9 | 2026-07-14 00:00:00 | 7.42346 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1312 | 0.404649 | 0.0460451 | 0.3 | 2026-08-12 08:00:00 | 2.27276 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 1312 | 0.1 | 1.14097e-15 | 0.1 | 2026-08-12 08:00:00 | 2.11639 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 1312 | 0.1 | 1.14097e-15 | 0.1 | 2026-08-12 08:00:00 | 2.11639 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 1312 | 0.1 | 1.14097e-15 | 0.1 | 2026-08-12 08:00:00 | 2.11639 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 2088 | 0.1 | 2.11774e-15 | 0.1 | 2026-08-12 08:00:00 | 1.71691 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 2088 | 0.1 | 2.11774e-15 | 0.1 | 2026-08-12 08:00:00 | 1.71691 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 2088 | 0.1 | 2.11774e-15 | 0.1 | 2026-08-12 08:00:00 | 1.71691 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 3540 | 0.1 | 2.42045e-15 | 0.1 | 2026-08-12 09:00:00 | 1.39899 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 3540 | 0.1 | 2.42045e-15 | 0.1 | 2026-08-12 09:00:00 | 1.39899 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 2088 | 0.428592 | 0.0721955 | 0.4 | 2026-08-12 08:00:00 | 0.396035 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 3540 | 0.425706 | 0.066767 | 0.4 | 2026-08-12 09:00:00 | 0.385014 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 3540 | 0.309379 | 0.0341508 | 0.3 | 2026-08-12 09:00:00 | 0.274621 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 3540 | 0.308955 | 0.0345517 | 0.3 | 2026-08-12 09:00:00 | 0.259171 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 2088 | 0.305364 | 0.0458003 | 0.3 | 2026-08-12 08:00:00 | 0.117117 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-12T09:15:00+00:00'),
st AS (SELECT sensor_id, property_id, count(*) AS n, avg(value) AS mean, stddev_pop(value) AS sd FROM s GROUP BY 1, 2),
lt AS (SELECT DISTINCT ON (sensor_id, property_id) sensor_id, property_id, value AS latest, result_time
       FROM s ORDER BY sensor_id, property_id, result_time DESC)
SELECT st.sensor_id, st.property_id, st.n, st.mean, st.sd, lt.latest, lt.result_time,
       abs(lt.latest - st.mean) / NULLIF(st.sd, 0) AS metric
FROM st JOIN lt USING (sensor_id, property_id) ORDER BY metric DESC NULLS LAST;
```
| sensor_id | property_id | n | mean | sd | latest | result_time | metric |
|---|---|---|---|---|---|---|---|
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaXAxis | 932 | 0.337661 | 0.0757516 | 0.9 | 2026-07-14 00:00:00 | 7.42346 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1312 | 0.404649 | 0.0460451 | 0.3 | 2026-08-12 08:00:00 | 2.27276 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 2088 | 0.428592 | 0.0721955 | 0.4 | 2026-08-12 08:00:00 | 0.396035 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 3540 | 0.425706 | 0.066767 | 0.4 | 2026-08-12 09:00:00 | 0.385014 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 3540 | 0.309379 | 0.0341508 | 0.3 | 2026-08-12 09:00:00 | 0.274621 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 3540 | 0.308955 | 0.0345517 | 0.3 | 2026-08-12 09:00:00 | 0.259171 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 2088 | 0.305364 | 0.0458003 | 0.3 | 2026-08-12 08:00:00 | 0.117117 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 2088 | 0.304502 | 0.0471287 | 0.3 | 2026-08-12 08:00:00 | 0.0955239 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 1312 | 0.298628 | 0.0372198 | 0.3 | 2026-08-12 08:00:00 | 0.0368608 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 1312 | 0.30061 | 0.035565 | 0.3 | 2026-08-12 08:00:00 | 0.0171448 |

- as_of = 2026-08-12T09:15:00+00:00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 7.42346 vs threshold 4.5 → fires
- R4_pga: metric 7.42346 vs threshold 0.5 → fires
- Raw readings: [data/A049_R3_vib_zscore.csv](data/A049_R3_vib_zscore.csv) (49731 rows)
- Raw readings: [data/A049_R4_pga.csv](data/A049_R4_pga.csv) (25613 rows)

---

## A050 · verdict_latest

**Question:** Based on the latest data, is there a visitor count anomaly at Lucretili according to its AD-RT rules?  
**Reference:** No. R5_visitors: latest reading 0 at 2026-08-12 09:15 UTC vs threshold 3  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors';
```
| threshold_value | threshold_json |
|---|---|
| 3 | {"R5_visitors_peak": 3} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-12T09:15:00+00:00')
SELECT r.sensor_id, o.property_id, o.result_time, o.value AS metric FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL
  AND o.result_time = anchor.t ORDER BY metric DESC;
```
| sensor_id | property_id | result_time | metric |
|---|---|---|---|
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | pulse_counter | 2026-08-12 09:15:00 | 0 |

- as_of = 2026-08-12T09:15:00+00:00 (windows end at the latest matching reading at or before it)
- R5_visitors: metric 0 vs threshold 3 → does not fire
- Raw readings: [data/A050_R5_visitors.csv](data/A050_R5_visitors.csv) (1 rows)

---

## A051 · verdict_no_data

**Question:** According to the AD-RT expert rules, was there a combined low temperature and high humidity anomaly at Schenkenberg on 2026-06-24?  
**Reference:** Cannot be determined: the snapshot has no combined low temperature and high humidity readings at Schenkenberg for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%hum%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'schenkenberg' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_temp_hum | AD-RT Schenkenberg policy - low temperature and high humidity | None | {"R1_hum_high": 90, "R1_temp_low": 0} |
| R2_crack_step | AD-RT Schenkenberg policy - crack step | 0.1 | {"R2_crack_step": 0.1} |
| R3_vib_zscore | AD-RT Schenkenberg policy - vibration z-score | 4.5 | {"R3_vib_zscore": 4.5} |
| R4_pga | AD-RT Schenkenberg policy - PGA | 0.5 | {"R4_pga": 0.5} |

- Expected: first query returns no rows (no combined low temperature and high humidity readings). Second query: the site's AD-RT rules — check which concern combined low temperature and high humidity.

---

## A052 · verdict_no_data

**Question:** According to the AD-RT expert rules, was there a rainfall anomaly at Delos on 2026-06-01?  
**Reference:** Cannot be determined: the snapshot has no rainfall readings at Delos for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND (lower(o.property_id) LIKE '%rain%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'delos' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1a_rain_1h | AD-RT Delos policy - rainfall 1h | 10 | {"R1a_rain_1h": 10} |
| R1b_rain_3h | AD-RT Delos policy - rainfall 3h | 20 | {"R1b_rain_3h": 20} |
| R2_wind | AD-RT Delos policy - wind | 12 | {"R2_wind": 12} |
| R3_hum_cross | AD-RT Delos policy - humidity crossings | None | {"R3_cross": 9, "R3_hum_th": 75} |

- Expected: first query returns no rows (no rainfall readings). Second query: the site's AD-RT rules — check which concern rainfall.

---

## A053 · verdict_no_data

**Question:** According to the AD-RT expert rules, was there a soil moisture anomaly at Ranverso on 2026-06-21?  
**Reference:** Cannot be determined: the snapshot has no soil moisture readings at Ranverso for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND (lower(o.property_id) LIKE '%moisture%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'ranverso' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_hum_inside | AD-RT Ranverso policy - indoor humidity | 80 | {"R1_hum_inside": 80} |
| R2_rain_7d | AD-RT Ranverso policy - rainfall 7d | 20 | {"R2_rain_7d_diff": 20} |
| R3_temp_nodiff | AD-RT Ranverso policy - soil and air temperature coupling | 2 | {"R3_temp_nodiff": 2} |
| R4a_soil_high | AD-RT Ranverso policy - soil moisture high | 60 | {"R4a_soil_high": 60} |
| R4b_soil_low | AD-RT Ranverso policy - soil moisture low | 5 | {"R4b_soil_low": 5} |

- Expected: first query returns no rows (no soil moisture readings). Second query: the site's AD-RT rules — check which concern soil moisture.

---

## A054 · verdict_no_data

**Question:** According to the AD-RT expert rules, was there a vibration (PPV) anomaly at Baltanas on 2026-05-25?  
**Reference:** Cannot be determined: the snapshot has no vibration (PPV) readings at Baltanas for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND (lower(o.property_id) LIKE '%ppv%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_ppv | AD-RT Baltanas policy - vibration PPV | 0.25 | {"R1_ppv": 0.25} |
| R2_hum_daily_range | AD-RT Baltanas policy - humidity daily range | 10 | {"R2_hum_daily_range": 10} |
| R3_gnss_change | AD-RT Baltanas policy - GNSS drift | 3 | {"R3_gnss_change": 3} |
| R4a_soil_high | AD-RT Baltanas policy - soil moisture high | 70 | {"R4a_soil_high": 70} |
| R4b_soil_range | AD-RT Baltanas policy - soil moisture daily range | 3 | {"R4b_soil_daily_range": 3} |
| R5a_airflow_const | AD-RT Baltanas policy - airflow constancy | 0.05 | {"R5a_airflow_const": 0.05} |
| R5b_airflow_range | AD-RT Baltanas policy - airflow range | 0.35 | {"R5b_airflow_range": 0.35} |
| R6_rain_1h | AD-RT Baltanas policy - rainfall 1h | 10 | {"R6_rain_1h": 10} |

- Expected: first query returns no rows (no vibration (PPV) readings). Second query: the site's AD-RT rules — check which concern vibration (PPV).

---

## A055 · verdict_no_data

**Question:** Did the airflow at Baltanas exceed its AD-RT threshold on 2026-05-23?  
**Reference:** Cannot be determined: the snapshot has no airflow readings at Baltanas for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND (lower(o.property_id) LIKE '%airflow%' OR lower(o.property_id) LIKE '%air_flow%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_ppv | AD-RT Baltanas policy - vibration PPV | 0.25 | {"R1_ppv": 0.25} |
| R2_hum_daily_range | AD-RT Baltanas policy - humidity daily range | 10 | {"R2_hum_daily_range": 10} |
| R3_gnss_change | AD-RT Baltanas policy - GNSS drift | 3 | {"R3_gnss_change": 3} |
| R4a_soil_high | AD-RT Baltanas policy - soil moisture high | 70 | {"R4a_soil_high": 70} |
| R4b_soil_range | AD-RT Baltanas policy - soil moisture daily range | 3 | {"R4b_soil_daily_range": 3} |
| R5a_airflow_const | AD-RT Baltanas policy - airflow constancy | 0.05 | {"R5a_airflow_const": 0.05} |
| R5b_airflow_range | AD-RT Baltanas policy - airflow range | 0.35 | {"R5b_airflow_range": 0.35} |
| R6_rain_1h | AD-RT Baltanas policy - rainfall 1h | 10 | {"R6_rain_1h": 10} |

- Expected: first query returns no rows (no airflow readings). Second query: the site's AD-RT rules — check which concern airflow.

---

## A056 · verdict_no_data

**Question:** Did the crack width at Schenkenberg exceed its AD-RT threshold on 2026-06-02?  
**Reference:** Cannot be determined: the snapshot has no crack width readings at Schenkenberg for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%crack%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'schenkenberg' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_temp_hum | AD-RT Schenkenberg policy - low temperature and high humidity | None | {"R1_hum_high": 90, "R1_temp_low": 0} |
| R2_crack_step | AD-RT Schenkenberg policy - crack step | 0.1 | {"R2_crack_step": 0.1} |
| R3_vib_zscore | AD-RT Schenkenberg policy - vibration z-score | 4.5 | {"R3_vib_zscore": 4.5} |
| R4_pga | AD-RT Schenkenberg policy - PGA | 0.5 | {"R4_pga": 0.5} |

- Expected: first query returns no rows (no crack width readings). Second query: the site's AD-RT rules — check which concern crack width.

---

## A057 · verdict_no_data

**Question:** Did the humidity at Delos exceed its AD-RT threshold on 2026-05-29?  
**Reference:** Cannot be determined: the snapshot has no humidity readings at Delos for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND (lower(o.property_id) LIKE '%hum%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'delos' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1a_rain_1h | AD-RT Delos policy - rainfall 1h | 10 | {"R1a_rain_1h": 10} |
| R1b_rain_3h | AD-RT Delos policy - rainfall 3h | 20 | {"R1b_rain_3h": 20} |
| R2_wind | AD-RT Delos policy - wind | 12 | {"R2_wind": 12} |
| R3_hum_cross | AD-RT Delos policy - humidity crossings | None | {"R3_cross": 9, "R3_hum_th": 75} |

- Expected: first query returns no rows (no humidity readings). Second query: the site's AD-RT rules — check which concern humidity.

---

## A058 · verdict_no_data

**Question:** Did the soil moisture at Baltanas exceed its AD-RT threshold on 2026-06-20?  
**Reference:** Cannot be determined: the snapshot has no soil moisture readings at Baltanas for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND (lower(o.property_id) LIKE '%moisture%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_ppv | AD-RT Baltanas policy - vibration PPV | 0.25 | {"R1_ppv": 0.25} |
| R2_hum_daily_range | AD-RT Baltanas policy - humidity daily range | 10 | {"R2_hum_daily_range": 10} |
| R3_gnss_change | AD-RT Baltanas policy - GNSS drift | 3 | {"R3_gnss_change": 3} |
| R4a_soil_high | AD-RT Baltanas policy - soil moisture high | 70 | {"R4a_soil_high": 70} |
| R4b_soil_range | AD-RT Baltanas policy - soil moisture daily range | 3 | {"R4b_soil_daily_range": 3} |
| R5a_airflow_const | AD-RT Baltanas policy - airflow constancy | 0.05 | {"R5a_airflow_const": 0.05} |
| R5b_airflow_range | AD-RT Baltanas policy - airflow range | 0.35 | {"R5b_airflow_range": 0.35} |
| R6_rain_1h | AD-RT Baltanas policy - rainfall 1h | 10 | {"R6_rain_1h": 10} |

- Expected: first query returns no rows (no soil moisture readings). Second query: the site's AD-RT rules — check which concern soil moisture.

---

## A059 · verdict_no_data

**Question:** Did the tilt at Lucretili exceed its AD-RT threshold on 2026-06-15?  
**Reference:** Cannot be determined: the snapshot has no tilt readings at Lucretili for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND (lower(o.property_id) LIKE '%tilt%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R10_solar_zscore | AD-RT Lucretili policy - GNSS z-score | 1 | {"R10_solar_zscore": 1.0} |
| R1a_crack_step | AD-RT Lucretili policy - crack step | 0.7 | {"R1a_crack_step": 0.7} |
| R1b_crack_offset | AD-RT Lucretili policy - crack offset | 0.9 | {"R1b_crack_offset": 0.9} |
| R2a_tilt_step | AD-RT Lucretili policy - tilt step | 0.7 | {"R2a_tilt_step": 0.7} |
| R2b_tilt_offset | AD-RT Lucretili policy - tilt offset | 0.9 | {"R2b_tilt_offset": 0.9} |
| R3_vib_zscore | AD-RT Lucretili policy - vibration z-score | 7 | {"R3_vib_zscore": 7} |
| R4a_hum_spike_6h | AD-RT Lucretili policy - humidity spike | 98 | {"R4a_hum_spike_6h": 98} |
| R4b_hum_persist_7d | AD-RT Lucretili policy - humidity persistence | 90 | {"R4b_hum_persist_7d": 90} |
| R4c_hum_rapid_1h | AD-RT Lucretili policy - humidity rapid change | 20 | {"R4c_hum_rapid_1h": 20} |
| R5_visitors | AD-RT Lucretili policy - visitor peak | 3 | {"R5_visitors_peak": 3} |
| R6a_rain | AD-RT Lucretili policy - rainfall short window | None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |
| R6b_rain_cum7d | AD-RT Lucretili policy - rainfall 7d | 100 | {"R6b_rain_cum7d": 100} |
| R7_wind | AD-RT Lucretili policy - wind peak ratio | 6 | {"R7a_wind_peak_ratio": 6} |
| R8_baro | AD-RT Lucretili policy - barometer range | 300 | {"R8_baro_range": 300} |
| R9a_temp_lt | AD-RT Lucretili policy - daily temperature range | 20 | {"R9a_temp_lt": 20} |
| R9b_temp_st | AD-RT Lucretili policy - rapid temperature change | 5 | {"R9b_temp_st": 5} |

- Expected: first query returns no rows (no tilt readings). Second query: the site's AD-RT rules — check which concern tilt.

---

## A060 · verdict_no_data

**Question:** Did the wind speed at Delos exceed its AD-RT threshold on 2026-08-09?  
**Reference:** Cannot be determined: the snapshot has no wind speed readings at Delos for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND (lower(o.property_id) LIKE '%wind%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'delos' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1a_rain_1h | AD-RT Delos policy - rainfall 1h | 10 | {"R1a_rain_1h": 10} |
| R1b_rain_3h | AD-RT Delos policy - rainfall 3h | 20 | {"R1b_rain_3h": 20} |
| R2_wind | AD-RT Delos policy - wind | 12 | {"R2_wind": 12} |
| R3_hum_cross | AD-RT Delos policy - humidity crossings | None | {"R3_cross": 9, "R3_hum_th": 75} |

- Expected: first query returns no rows (no wind speed readings). Second query: the site's AD-RT rules — check which concern wind speed.

---

## A061 · verdict_no_data

**Question:** Did the wind speed at Lucretili exceed its AD-RT threshold on 2026-05-24?  
**Reference:** Cannot be determined: the snapshot has no wind speed readings at Lucretili for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND (lower(o.property_id) LIKE '%wind%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R10_solar_zscore | AD-RT Lucretili policy - GNSS z-score | 1 | {"R10_solar_zscore": 1.0} |
| R1a_crack_step | AD-RT Lucretili policy - crack step | 0.7 | {"R1a_crack_step": 0.7} |
| R1b_crack_offset | AD-RT Lucretili policy - crack offset | 0.9 | {"R1b_crack_offset": 0.9} |
| R2a_tilt_step | AD-RT Lucretili policy - tilt step | 0.7 | {"R2a_tilt_step": 0.7} |
| R2b_tilt_offset | AD-RT Lucretili policy - tilt offset | 0.9 | {"R2b_tilt_offset": 0.9} |
| R3_vib_zscore | AD-RT Lucretili policy - vibration z-score | 7 | {"R3_vib_zscore": 7} |
| R4a_hum_spike_6h | AD-RT Lucretili policy - humidity spike | 98 | {"R4a_hum_spike_6h": 98} |
| R4b_hum_persist_7d | AD-RT Lucretili policy - humidity persistence | 90 | {"R4b_hum_persist_7d": 90} |
| R4c_hum_rapid_1h | AD-RT Lucretili policy - humidity rapid change | 20 | {"R4c_hum_rapid_1h": 20} |
| R5_visitors | AD-RT Lucretili policy - visitor peak | 3 | {"R5_visitors_peak": 3} |
| R6a_rain | AD-RT Lucretili policy - rainfall short window | None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |
| R6b_rain_cum7d | AD-RT Lucretili policy - rainfall 7d | 100 | {"R6b_rain_cum7d": 100} |
| R7_wind | AD-RT Lucretili policy - wind peak ratio | 6 | {"R7a_wind_peak_ratio": 6} |
| R8_baro | AD-RT Lucretili policy - barometer range | 300 | {"R8_baro_range": 300} |
| R9a_temp_lt | AD-RT Lucretili policy - daily temperature range | 20 | {"R9a_temp_lt": 20} |
| R9b_temp_st | AD-RT Lucretili policy - rapid temperature change | 5 | {"R9b_temp_st": 5} |

- Expected: first query returns no rows (no wind speed readings). Second query: the site's AD-RT rules — check which concern wind speed.

---

## A062 · verdict_no_data

**Question:** Was the barometric pressure at Lucretili anomalous on 2026-06-06 according to its AD-RT rules?  
**Reference:** Cannot be determined: the snapshot has no barometric pressure readings at Lucretili for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND (lower(o.property_id) LIKE '%baro%' OR lower(o.property_id) LIKE '%pressure%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R10_solar_zscore | AD-RT Lucretili policy - GNSS z-score | 1 | {"R10_solar_zscore": 1.0} |
| R1a_crack_step | AD-RT Lucretili policy - crack step | 0.7 | {"R1a_crack_step": 0.7} |
| R1b_crack_offset | AD-RT Lucretili policy - crack offset | 0.9 | {"R1b_crack_offset": 0.9} |
| R2a_tilt_step | AD-RT Lucretili policy - tilt step | 0.7 | {"R2a_tilt_step": 0.7} |
| R2b_tilt_offset | AD-RT Lucretili policy - tilt offset | 0.9 | {"R2b_tilt_offset": 0.9} |
| R3_vib_zscore | AD-RT Lucretili policy - vibration z-score | 7 | {"R3_vib_zscore": 7} |
| R4a_hum_spike_6h | AD-RT Lucretili policy - humidity spike | 98 | {"R4a_hum_spike_6h": 98} |
| R4b_hum_persist_7d | AD-RT Lucretili policy - humidity persistence | 90 | {"R4b_hum_persist_7d": 90} |
| R4c_hum_rapid_1h | AD-RT Lucretili policy - humidity rapid change | 20 | {"R4c_hum_rapid_1h": 20} |
| R5_visitors | AD-RT Lucretili policy - visitor peak | 3 | {"R5_visitors_peak": 3} |
| R6a_rain | AD-RT Lucretili policy - rainfall short window | None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |
| R6b_rain_cum7d | AD-RT Lucretili policy - rainfall 7d | 100 | {"R6b_rain_cum7d": 100} |
| R7_wind | AD-RT Lucretili policy - wind peak ratio | 6 | {"R7a_wind_peak_ratio": 6} |
| R8_baro | AD-RT Lucretili policy - barometer range | 300 | {"R8_baro_range": 300} |
| R9a_temp_lt | AD-RT Lucretili policy - daily temperature range | 20 | {"R9a_temp_lt": 20} |
| R9b_temp_st | AD-RT Lucretili policy - rapid temperature change | 5 | {"R9b_temp_st": 5} |

- Expected: first query returns no rows (no barometric pressure readings). Second query: the site's AD-RT rules — check which concern barometric pressure.

---

## A063 · verdict_no_data

**Question:** Was the crack width at Lucretili anomalous on 2026-07-20 according to its AD-RT rules?  
**Reference:** Cannot be determined: the snapshot has no crack width readings at Lucretili for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND (lower(o.property_id) LIKE '%crack%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R10_solar_zscore | AD-RT Lucretili policy - GNSS z-score | 1 | {"R10_solar_zscore": 1.0} |
| R1a_crack_step | AD-RT Lucretili policy - crack step | 0.7 | {"R1a_crack_step": 0.7} |
| R1b_crack_offset | AD-RT Lucretili policy - crack offset | 0.9 | {"R1b_crack_offset": 0.9} |
| R2a_tilt_step | AD-RT Lucretili policy - tilt step | 0.7 | {"R2a_tilt_step": 0.7} |
| R2b_tilt_offset | AD-RT Lucretili policy - tilt offset | 0.9 | {"R2b_tilt_offset": 0.9} |
| R3_vib_zscore | AD-RT Lucretili policy - vibration z-score | 7 | {"R3_vib_zscore": 7} |
| R4a_hum_spike_6h | AD-RT Lucretili policy - humidity spike | 98 | {"R4a_hum_spike_6h": 98} |
| R4b_hum_persist_7d | AD-RT Lucretili policy - humidity persistence | 90 | {"R4b_hum_persist_7d": 90} |
| R4c_hum_rapid_1h | AD-RT Lucretili policy - humidity rapid change | 20 | {"R4c_hum_rapid_1h": 20} |
| R5_visitors | AD-RT Lucretili policy - visitor peak | 3 | {"R5_visitors_peak": 3} |
| R6a_rain | AD-RT Lucretili policy - rainfall short window | None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |
| R6b_rain_cum7d | AD-RT Lucretili policy - rainfall 7d | 100 | {"R6b_rain_cum7d": 100} |
| R7_wind | AD-RT Lucretili policy - wind peak ratio | 6 | {"R7a_wind_peak_ratio": 6} |
| R8_baro | AD-RT Lucretili policy - barometer range | 300 | {"R8_baro_range": 300} |
| R9a_temp_lt | AD-RT Lucretili policy - daily temperature range | 20 | {"R9a_temp_lt": 20} |
| R9b_temp_st | AD-RT Lucretili policy - rapid temperature change | 5 | {"R9b_temp_st": 5} |

- Expected: first query returns no rows (no crack width readings). Second query: the site's AD-RT rules — check which concern crack width.

---

## A064 · verdict_no_data

**Question:** Was the humidity at Baltanas anomalous on 2026-07-28 according to its AD-RT rules?  
**Reference:** Cannot be determined: the snapshot has no humidity readings at Baltanas for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND (lower(o.property_id) LIKE '%hum%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_ppv | AD-RT Baltanas policy - vibration PPV | 0.25 | {"R1_ppv": 0.25} |
| R2_hum_daily_range | AD-RT Baltanas policy - humidity daily range | 10 | {"R2_hum_daily_range": 10} |
| R3_gnss_change | AD-RT Baltanas policy - GNSS drift | 3 | {"R3_gnss_change": 3} |
| R4a_soil_high | AD-RT Baltanas policy - soil moisture high | 70 | {"R4a_soil_high": 70} |
| R4b_soil_range | AD-RT Baltanas policy - soil moisture daily range | 3 | {"R4b_soil_daily_range": 3} |
| R5a_airflow_const | AD-RT Baltanas policy - airflow constancy | 0.05 | {"R5a_airflow_const": 0.05} |
| R5b_airflow_range | AD-RT Baltanas policy - airflow range | 0.35 | {"R5b_airflow_range": 0.35} |
| R6_rain_1h | AD-RT Baltanas policy - rainfall 1h | 10 | {"R6_rain_1h": 10} |

- Expected: first query returns no rows (no humidity readings). Second query: the site's AD-RT rules — check which concern humidity.

---

## A065 · verdict_no_data

**Question:** Was the humidity at Ranverso anomalous on 2026-08-04 according to its AD-RT rules?  
**Reference:** Cannot be determined: the snapshot has no humidity readings at Ranverso for its AD-RT rule(s).  
**Recomputed:** `Cannot be determined` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND (lower(o.property_id) LIKE '%hum%');
```
_(no rows)_

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'ranverso' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_hum_inside | AD-RT Ranverso policy - indoor humidity | 80 | {"R1_hum_inside": 80} |
| R2_rain_7d | AD-RT Ranverso policy - rainfall 7d | 20 | {"R2_rain_7d_diff": 20} |
| R3_temp_nodiff | AD-RT Ranverso policy - soil and air temperature coupling | 2 | {"R3_temp_nodiff": 2} |
| R4a_soil_high | AD-RT Ranverso policy - soil moisture high | 60 | {"R4a_soil_high": 60} |
| R4b_soil_low | AD-RT Ranverso policy - soil moisture low | 5 | {"R4b_soil_low": 5} |

- Expected: first query returns no rows (no humidity readings). Second query: the site's AD-RT rules — check which concern humidity.

---

## A066 · verdict_no_rule

**Question:** Has the soil temperature at Baltanas exceeded its AD-RT threshold?  
**Reference:** Cannot be determined: no AD-RT rule is defined for soil temperature at Baltanas.  
**Recomputed:** `Cannot be determined` → **MANUAL**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_ppv | AD-RT Baltanas policy - vibration PPV | 0.25 | {"R1_ppv": 0.25} |
| R2_hum_daily_range | AD-RT Baltanas policy - humidity daily range | 10 | {"R2_hum_daily_range": 10} |
| R3_gnss_change | AD-RT Baltanas policy - GNSS drift | 3 | {"R3_gnss_change": 3} |
| R4a_soil_high | AD-RT Baltanas policy - soil moisture high | 70 | {"R4a_soil_high": 70} |
| R4b_soil_range | AD-RT Baltanas policy - soil moisture daily range | 3 | {"R4b_soil_daily_range": 3} |
| R5a_airflow_const | AD-RT Baltanas policy - airflow constancy | 0.05 | {"R5a_airflow_const": 0.05} |
| R5b_airflow_range | AD-RT Baltanas policy - airflow range | 0.35 | {"R5b_airflow_range": 0.35} |
| R6_rain_1h | AD-RT Baltanas policy - rainfall 1h | 10 | {"R6_rain_1h": 10} |

- Check that none of these rules is about soil temperature.

---

## A067 · verdict_no_rule

**Question:** Has the temperature at Baltanas exceeded its AD-RT threshold?  
**Reference:** Cannot be determined: no AD-RT rule is defined for temperature at Baltanas.  
**Recomputed:** `Cannot be determined` → **MANUAL**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_ppv | AD-RT Baltanas policy - vibration PPV | 0.25 | {"R1_ppv": 0.25} |
| R2_hum_daily_range | AD-RT Baltanas policy - humidity daily range | 10 | {"R2_hum_daily_range": 10} |
| R3_gnss_change | AD-RT Baltanas policy - GNSS drift | 3 | {"R3_gnss_change": 3} |
| R4a_soil_high | AD-RT Baltanas policy - soil moisture high | 70 | {"R4a_soil_high": 70} |
| R4b_soil_range | AD-RT Baltanas policy - soil moisture daily range | 3 | {"R4b_soil_daily_range": 3} |
| R5a_airflow_const | AD-RT Baltanas policy - airflow constancy | 0.05 | {"R5a_airflow_const": 0.05} |
| R5b_airflow_range | AD-RT Baltanas policy - airflow range | 0.35 | {"R5b_airflow_range": 0.35} |
| R6_rain_1h | AD-RT Baltanas policy - rainfall 1h | 10 | {"R6_rain_1h": 10} |

- Check that none of these rules is about temperature.

---

## A068 · verdict_no_rule

**Question:** Has the temperature at Delos exceeded its AD-RT threshold?  
**Reference:** Cannot be determined: no AD-RT rule is defined for temperature at Delos.  
**Recomputed:** `Cannot be determined` → **MANUAL**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'delos' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1a_rain_1h | AD-RT Delos policy - rainfall 1h | 10 | {"R1a_rain_1h": 10} |
| R1b_rain_3h | AD-RT Delos policy - rainfall 3h | 20 | {"R1b_rain_3h": 20} |
| R2_wind | AD-RT Delos policy - wind | 12 | {"R2_wind": 12} |
| R3_hum_cross | AD-RT Delos policy - humidity crossings | None | {"R3_cross": 9, "R3_hum_th": 75} |

- Check that none of these rules is about temperature.

---

## A069 · verdict_no_rule

**Question:** Has the temperature at Ranverso exceeded its AD-RT threshold?  
**Reference:** Cannot be determined: no AD-RT rule sets a threshold on the temperature at Ranverso. Its only temperature-related rule, R3_temp_nodiff (threshold 2), checks whether the soil temperature tracks the outdoor air temperature, not the temperature itself, and the snapshot has no soil-temperature readings at Ranverso to evaluate it.  
**Recomputed:** `Cannot be determined` → **MANUAL**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'ranverso' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_hum_inside | AD-RT Ranverso policy - indoor humidity | 80 | {"R1_hum_inside": 80} |
| R2_rain_7d | AD-RT Ranverso policy - rainfall 7d | 20 | {"R2_rain_7d_diff": 20} |
| R3_temp_nodiff | AD-RT Ranverso policy - soil and air temperature coupling | 2 | {"R3_temp_nodiff": 2} |
| R4a_soil_high | AD-RT Ranverso policy - soil moisture high | 60 | {"R4a_soil_high": 60} |
| R4b_soil_low | AD-RT Ranverso policy - soil moisture low | 5 | {"R4b_soil_low": 5} |

- Check that none of these rules is about temperature.

**Partner review (2026-10-20):** R3_temp_nodiff concerns temperature (soil vs. outdoor air temperature,
threshold 2, confirmed in the partner database and NB5.3 Table 1 of ARGUS D5.3), so the explanation was
revised to tell it apart from a threshold on the temperature itself. The verdict stays *Cannot be
determined*: no rule thresholds the temperature value, and R3_temp_nodiff cannot be evaluated, as the
snapshot's only temperature quantity at Ranverso is `temperature` (18,924 observations) and it has no
soil-temperature series (`soilmoisture_temp`) to pair it with. `reference_value` is unchanged, so no score changes.

---

## A070 · verdict_no_rule

**Question:** Has the voltage at Delos exceeded its AD-RT threshold?  
**Reference:** Cannot be determined: no AD-RT rule is defined for voltage at Delos.  
**Recomputed:** `Cannot be determined` → **MANUAL**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'delos' AND left(label, 5) = 'AD-RT' ORDER BY rule_id;
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1a_rain_1h | AD-RT Delos policy - rainfall 1h | 10 | {"R1a_rain_1h": 10} |
| R1b_rain_3h | AD-RT Delos policy - rainfall 3h | 20 | {"R1b_rain_3h": 20} |
| R2_wind | AD-RT Delos policy - wind | 12 | {"R2_wind": 12} |
| R3_hum_cross | AD-RT Delos policy - humidity crossings | None | {"R3_cross": 9, "R3_hum_th": 75} |

- Check that none of these rules is about voltage.

---

## A071 · threshold_lookup

**Question:** What threshold does the AD-RT 1-hour and 24-hour rainfall rule at Lucretili use?  
**Reference:** Rule R6a_rain: R6a_rain_1h = 5, R6a_rain_24h = 20.  
**Recomputed:** `{'R6a_rain_1h': 5, 'R6a_rain_24h': 20}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R6a_rain' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R6a_rain | AD-RT Lucretili policy - rainfall short window | None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |


---

## A072 · threshold_lookup

**Question:** What threshold does the AD-RT 6-hour barometric pressure range rule at Lucretili use?  
**Reference:** Rule R8_baro: R8_baro_range = 300.  
**Recomputed:** `{'R8_baro_range': 300}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R8_baro' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R8_baro | AD-RT Lucretili policy - barometer range | 300 | {"R8_baro_range": 300} |


---

## A073 · threshold_lookup

**Question:** What threshold does the AD-RT 6-hour humidity spike rule at Lucretili use?  
**Reference:** Rule R4a_hum_spike_6h: R4a_hum_spike_6h = 98.  
**Recomputed:** `{'R4a_hum_spike_6h': 98}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R4a_hum_spike_6h' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R4a_hum_spike_6h | AD-RT Lucretili policy - humidity spike | 98 | {"R4a_hum_spike_6h": 98} |


---

## A074 · threshold_lookup

**Question:** What threshold does the AD-RT 7-day cumulative rainfall rule at Lucretili use?  
**Reference:** Rule R6b_rain_cum7d: R6b_rain_cum7d = 100.  
**Recomputed:** `{'R6b_rain_cum7d': 100}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R6b_rain_cum7d' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R6b_rain_cum7d | AD-RT Lucretili policy - rainfall 7d | 100 | {"R6b_rain_cum7d": 100} |


---

## A075 · threshold_lookup

**Question:** What threshold does the AD-RT 7-day humidity persistence rule at Lucretili use?  
**Reference:** Rule R4b_hum_persist_7d: R4b_hum_persist_7d = 90.  
**Recomputed:** `{'R4b_hum_persist_7d': 90}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R4b_hum_persist_7d' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R4b_hum_persist_7d | AD-RT Lucretili policy - humidity persistence | 90 | {"R4b_hum_persist_7d": 90} |


---

## A076 · threshold_lookup

**Question:** What threshold does the AD-RT 7-day rainfall rule at Ranverso use?  
**Reference:** Rule R2_rain_7d: R2_rain_7d_diff = 20.  
**Recomputed:** `{'R2_rain_7d_diff': 20}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R2_rain_7d | AD-RT Ranverso policy - rainfall 7d | 20 | {"R2_rain_7d_diff": 20} |


---

## A077 · threshold_lookup

**Question:** What threshold does the AD-RT airflow constancy rule at Baltanas use?  
**Reference:** Rule R5a_airflow_const: R5a_airflow_const = 0.05.  
**Recomputed:** `{'R5a_airflow_const': 0.05}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND rule_id = 'R5a_airflow_const' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R5a_airflow_const | AD-RT Baltanas policy - airflow constancy | 0.05 | {"R5a_airflow_const": 0.05} |


---

## A078 · threshold_lookup

**Question:** What threshold does the AD-RT airflow range rule at Baltanas use?  
**Reference:** Rule R5b_airflow_range: R5b_airflow_range = 0.35.  
**Recomputed:** `{'R5b_airflow_range': 0.35}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND rule_id = 'R5b_airflow_range' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R5b_airflow_range | AD-RT Baltanas policy - airflow range | 0.35 | {"R5b_airflow_range": 0.35} |


---

## A079 · threshold_lookup

**Question:** What threshold does the AD-RT crack offset rule at Lucretili use?  
**Reference:** Rule R1b_crack_offset: R1b_crack_offset = 0.9.  
**Recomputed:** `{'R1b_crack_offset': 0.9}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R1b_crack_offset' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1b_crack_offset | AD-RT Lucretili policy - crack offset | 0.9 | {"R1b_crack_offset": 0.9} |


---

## A080 · threshold_lookup

**Question:** What threshold does the AD-RT crack step rule at Schenkenberg use?  
**Reference:** Rule R2_crack_step: R2_crack_step = 0.1.  
**Recomputed:** `{'R2_crack_step': 0.1}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'schenkenberg' AND rule_id = 'R2_crack_step' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R2_crack_step | AD-RT Schenkenberg policy - crack step | 0.1 | {"R2_crack_step": 0.1} |


---

## A081 · threshold_lookup

**Question:** What threshold does the AD-RT daily humidity range rule at Baltanas use?  
**Reference:** Rule R2_hum_daily_range: R2_hum_daily_range = 10.  
**Recomputed:** `{'R2_hum_daily_range': 10}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND rule_id = 'R2_hum_daily_range' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R2_hum_daily_range | AD-RT Baltanas policy - humidity daily range | 10 | {"R2_hum_daily_range": 10} |


---

## A082 · threshold_lookup

**Question:** What threshold does the AD-RT daily temperature range rule at Lucretili use?  
**Reference:** Rule R9a_temp_lt: R9a_temp_lt = 20.  
**Recomputed:** `{'R9a_temp_lt': 20}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R9a_temp_lt | AD-RT Lucretili policy - daily temperature range | 20 | {"R9a_temp_lt": 20} |


---

## A083 · threshold_lookup

**Question:** What threshold does the AD-RT day-over-day GNSS position change rule at Baltanas use?  
**Reference:** Rule R3_gnss_change: R3_gnss_change = 3.  
**Recomputed:** `{'R3_gnss_change': 3}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND rule_id = 'R3_gnss_change' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R3_gnss_change | AD-RT Baltanas policy - GNSS drift | 3 | {"R3_gnss_change": 3} |


---

## A084 · threshold_lookup

**Question:** What threshold does the AD-RT high soil moisture rule at Baltanas use?  
**Reference:** Rule R4a_soil_high: R4a_soil_high = 70.  
**Recomputed:** `{'R4a_soil_high': 70}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND rule_id = 'R4a_soil_high' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R4a_soil_high | AD-RT Baltanas policy - soil moisture high | 70 | {"R4a_soil_high": 70} |


---

## A085 · threshold_lookup

**Question:** What threshold does the AD-RT high soil moisture rule at Ranverso use?  
**Reference:** Rule R4a_soil_high: R4a_soil_high = 60.  
**Recomputed:** `{'R4a_soil_high': 60}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'ranverso' AND rule_id = 'R4a_soil_high' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R4a_soil_high | AD-RT Ranverso policy - soil moisture high | 60 | {"R4a_soil_high": 60} |


---

## A086 · threshold_lookup

**Question:** What threshold does the AD-RT humidity threshold crossings rule at Delos use?  
**Reference:** Rule R3_hum_cross: R3_cross = 9, R3_hum_th = 75.  
**Recomputed:** `{'R3_cross': 9, 'R3_hum_th': 75}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'delos' AND rule_id = 'R3_hum_cross' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R3_hum_cross | AD-RT Delos policy - humidity crossings | None | {"R3_cross": 9, "R3_hum_th": 75} |


---

## A087 · threshold_lookup

**Question:** What threshold does the AD-RT indoor humidity rule at Ranverso use?  
**Reference:** Rule R1_hum_inside: R1_hum_inside = 80.  
**Recomputed:** `{'R1_hum_inside': 80}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'ranverso' AND rule_id = 'R1_hum_inside' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_hum_inside | AD-RT Ranverso policy - indoor humidity | 80 | {"R1_hum_inside": 80} |


---

## A088 · threshold_lookup

**Question:** What threshold does the AD-RT low soil moisture rule at Ranverso use?  
**Reference:** Rule R4b_soil_low: R4b_soil_low = 5.  
**Recomputed:** `{'R4b_soil_low': 5}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'ranverso' AND rule_id = 'R4b_soil_low' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R4b_soil_low | AD-RT Ranverso policy - soil moisture low | 5 | {"R4b_soil_low": 5} |


---

## A089 · threshold_lookup

**Question:** What threshold does the AD-RT low temperature with high humidity rule at Schenkenberg use?  
**Reference:** Rule R1_temp_hum: R1_hum_high = 90, R1_temp_low = 0.  
**Recomputed:** `{'R1_hum_high': 90, 'R1_temp_low': 0}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'schenkenberg' AND rule_id = 'R1_temp_hum' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_temp_hum | AD-RT Schenkenberg policy - low temperature and high humidity | None | {"R1_hum_high": 90, "R1_temp_low": 0} |


---

## A090 · threshold_lookup

**Question:** What threshold does the AD-RT peak ground acceleration (PGA) rule at Schenkenberg use?  
**Reference:** Rule R4_pga: R4_pga = 0.5.  
**Recomputed:** `{'R4_pga': 0.5}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R4_pga | AD-RT Schenkenberg policy - PGA | 0.5 | {"R4_pga": 0.5} |


---

## A091 · threshold_lookup

**Question:** What threshold does the AD-RT peak particle velocity (PPV) rule at Baltanas use?  
**Reference:** Rule R1_ppv: R1_ppv = 0.25.  
**Recomputed:** `{'R1_ppv': 0.25}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND rule_id = 'R1_ppv' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R1_ppv | AD-RT Baltanas policy - vibration PPV | 0.25 | {"R1_ppv": 0.25} |


---

## A092 · threshold_lookup

**Question:** What threshold does the AD-RT rapid 1-hour humidity change rule at Lucretili use?  
**Reference:** Rule R4c_hum_rapid_1h: R4c_hum_rapid_1h = 20.  
**Recomputed:** `{'R4c_hum_rapid_1h': 20}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R4c_hum_rapid_1h' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R4c_hum_rapid_1h | AD-RT Lucretili policy - humidity rapid change | 20 | {"R4c_hum_rapid_1h": 20} |


---

## A093 · threshold_lookup

**Question:** What threshold does the AD-RT short-term (1-hour) temperature change rule at Lucretili use?  
**Reference:** Rule R9b_temp_st: R9b_temp_st = 5.  
**Recomputed:** `{'R9b_temp_st': 5}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R9b_temp_st | AD-RT Lucretili policy - rapid temperature change | 5 | {"R9b_temp_st": 5} |


---

## A094 · threshold_lookup

**Question:** What threshold does the AD-RT soil/air temperature difference rule at Ranverso use?  
**Reference:** Rule R3_temp_nodiff: R3_temp_nodiff = 2.  
**Recomputed:** `{'R3_temp_nodiff': 2}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'ranverso' AND rule_id = 'R3_temp_nodiff' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R3_temp_nodiff | AD-RT Ranverso policy - soil and air temperature coupling | 2 | {"R3_temp_nodiff": 2} |


---

## A095 · threshold_lookup

**Question:** What threshold does the AD-RT tilt offset rule at Lucretili use?  
**Reference:** Rule R2b_tilt_offset: R2b_tilt_offset = 0.9.  
**Recomputed:** `{'R2b_tilt_offset': 0.9}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R2b_tilt_offset' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R2b_tilt_offset | AD-RT Lucretili policy - tilt offset | 0.9 | {"R2b_tilt_offset": 0.9} |


---

## A096 · threshold_lookup

**Question:** What threshold does the AD-RT tilt step rule at Lucretili use?  
**Reference:** Rule R2a_tilt_step: R2a_tilt_step = 0.7.  
**Recomputed:** `{'R2a_tilt_step': 0.7}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R2a_tilt_step' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R2a_tilt_step | AD-RT Lucretili policy - tilt step | 0.7 | {"R2a_tilt_step": 0.7} |


---

## A097 · threshold_lookup

**Question:** What threshold does the AD-RT vibration z-score rule at Schenkenberg use?  
**Reference:** Rule R3_vib_zscore: R3_vib_zscore = 4.5.  
**Recomputed:** `{'R3_vib_zscore': 4.5}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R3_vib_zscore | AD-RT Schenkenberg policy - vibration z-score | 4.5 | {"R3_vib_zscore": 4.5} |


---

## A098 · threshold_lookup

**Question:** What threshold does the AD-RT visitor peak rule at Lucretili use?  
**Reference:** Rule R5_visitors: R5_visitors_peak = 3.  
**Recomputed:** `{'R5_visitors_peak': 3}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R5_visitors | AD-RT Lucretili policy - visitor peak | 3 | {"R5_visitors_peak": 3} |


---

## A099 · threshold_lookup

**Question:** What threshold does the AD-RT wind peak ratio rule at Lucretili use?  
**Reference:** Rule R7_wind: R7a_wind_peak_ratio = 6.  
**Recomputed:** `{'R7a_wind_peak_ratio': 6}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'lucretili' AND rule_id = 'R7_wind' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R7_wind | AD-RT Lucretili policy - wind peak ratio | 6 | {"R7a_wind_peak_ratio": 6} |


---

## A100 · threshold_lookup

**Question:** What threshold does the AD-RT wind speed rule at Delos use?  
**Reference:** Rule R2_wind: R2_wind = 12.  
**Recomputed:** `{'R2_wind': 12}` → **MATCH**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'delos' AND rule_id = 'R2_wind' AND left(label, 5) = 'AD-RT';
```
| rule_id | label | threshold_value | threshold_json |
|---|---|---|---|
| R2_wind | AD-RT Delos policy - wind | 12 | {"R2_wind": 12} |


---
