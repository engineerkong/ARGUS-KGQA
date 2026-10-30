# Verification — basic

Run `SET TIME ZONE 'UTC';` in psql first (`psql -h localhost -U argus -d argus_snapshot`).

## B001 · node_count

**Question:** How many sensor nodes are installed at Baltanas?  
**Reference:** 15 sensor nodes.  
**Recomputed:** `15` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'baltanas';
```
| nodes |
|---|
| 15 |


---

## B002 · node_count

**Question:** How many sensor nodes are installed at Delos?  
**Reference:** 19 sensor nodes.  
**Recomputed:** `19` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'delos';
```
| nodes |
|---|
| 19 |


---

## B003 · node_count

**Question:** How many sensor nodes are installed at Lucretili?  
**Reference:** 15 sensor nodes.  
**Recomputed:** `15` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'lucretili';
```
| nodes |
|---|
| 15 |


---

## B004 · node_count

**Question:** How many sensor nodes are installed at Ranverso?  
**Reference:** 13 sensor nodes.  
**Recomputed:** `13` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'ranverso';
```
| nodes |
|---|
| 13 |


---

## B005 · node_count

**Question:** How many sensor nodes are installed at Schenkenberg?  
**Reference:** 9 sensor nodes.  
**Recomputed:** `9` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'schenkenberg';
```
| nodes |
|---|
| 9 |


---

## B006 · sensor_count

**Question:** How many sensors have reported readings at Baltanas?  
**Reference:** 35 sensors.  
**Recomputed:** `35` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'baltanas';
```
| sensors |
|---|
| 35 |


---

## B007 · sensor_count

**Question:** How many sensors have reported readings at Delos?  
**Reference:** 30 sensors.  
**Recomputed:** `30` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'delos';
```
| sensors |
|---|
| 30 |


---

## B008 · sensor_count

**Question:** How many sensors have reported readings at Lucretili?  
**Reference:** 20 sensors.  
**Recomputed:** `20` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'lucretili';
```
| sensors |
|---|
| 20 |


---

## B009 · sensor_count

**Question:** How many sensors have reported readings at Ranverso?  
**Reference:** 19 sensors.  
**Recomputed:** `19` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'ranverso';
```
| sensors |
|---|
| 19 |


---

## B010 · sensor_count

**Question:** How many sensors have reported readings at Schenkenberg?  
**Reference:** 14 sensors.  
**Recomputed:** `14` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'schenkenberg';
```
| sensors |
|---|
| 14 |


---

## B011 · reading_count

**Question:** How many readings are stored for Baltanas?  
**Reference:** 709170 readings.  
**Recomputed:** `709170` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'baltanas';
```
| readings |
|---|
| 709170 |


---

## B012 · reading_count

**Question:** How many readings are stored for Delos?  
**Reference:** 225945 readings.  
**Recomputed:** `225945` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'delos';
```
| readings |
|---|
| 225945 |


---

## B013 · reading_count

**Question:** How many readings are stored for Lucretili?  
**Reference:** 574578 readings.  
**Recomputed:** `574578` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili';
```
| readings |
|---|
| 574578 |


---

## B014 · reading_count

**Question:** How many readings are stored for Ranverso?  
**Reference:** 108150 readings.  
**Recomputed:** `108150` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'ranverso';
```
| readings |
|---|
| 108150 |


---

## B015 · reading_count

**Question:** How many readings are stored for Schenkenberg?  
**Reference:** 59713 readings.  
**Recomputed:** `59713` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'schenkenberg';
```
| readings |
|---|
| 59713 |


---

## B016 · quantity_count

**Question:** How many different physical quantities are measured at Baltanas?  
**Reference:** 67 quantities.  
**Recomputed:** `67` → **MATCH**

```sql
SELECT count(DISTINCT o.property_id) AS quantities FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'baltanas';
```
| quantities |
|---|
| 67 |

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'baltanas'
GROUP BY 1 ORDER BY 2 DESC;
```
| property_id | count |
|---|---|
| temperature | 435215 |
| voltage | 182636 |
| voltage_polynomial_4 | 137289 |
| thermistor | 127203 |
| pulse_counter | 127179 |
| yAxis | 53645 |
| xAxis | 53645 |
| zAxis | 53643 |
| activeTime | 50862 |
| overThresholdEvents | 50862 |
| backgroundEvent | 50862 |
| underThresholdEvents | 50862 |
| duration | 50862 |
| freqYAxis | 50861 |
| freqXAxis | 50861 |
| freqZAxis | 50861 |
| composedAxis | 50860 |
| soil_water_potential | 50850 |
| installation_pitch_angle | 50850 |
| soil_temperature | 50734 |

_… 47 more rows_


---

## B017 · quantity_count

**Question:** How many different physical quantities are measured at Lucretili?  
**Reference:** 39 quantities.  
**Recomputed:** `39` → **MATCH**

```sql
SELECT count(DISTINCT o.property_id) AS quantities FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili';
```
| quantities |
|---|
| 39 |

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili'
GROUP BY 1 ORDER BY 2 DESC;
```
| property_id | count |
|---|---|
| temperature | 318576 |
| voltage_1 | 179935 |
| voltage | 179933 |
| axis_z | 58484 |
| axis_y_std | 58484 |
| axis_x_std | 58484 |
| axis_y | 58484 |
| axis_x | 58484 |
| axis_z_std | 58484 |
| thermistor | 49866 |
| counter_in | 29879 |
| counter_out | 29879 |
| counter_acc_out | 29876 |
| counter_acc_in | 29876 |
| pulse_counter | 28150 |
| thermistor_ysi44005 | 24649 |
| wind_speed_1 | 17474 |
| wind_direction_1 | 17474 |
| hum1 | 17474 |
| light | 17474 |

_… 19 more rows_


---

## B018 · quantity_count

**Question:** How many different physical quantities are measured at Ranverso?  
**Reference:** 54 quantities.  
**Recomputed:** `54` → **MATCH**

```sql
SELECT count(DISTINCT o.property_id) AS quantities FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso';
```
| quantities |
|---|
| 54 |

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso'
GROUP BY 1 ORDER BY 2 DESC;
```
| property_id | count |
|---|---|
| temp1 | 39124 |
| hum1 | 39124 |
| temperature | 18924 |
| cumulative energy | 17588 |
| cumulative counts | 17588 |
| hit count | 17588 |
| moisture | 15301 |
| temp2 | 15301 |
| hum2 | 15301 |
| voltage | 14793 |
| co2 | 13797 |
| nox | 13797 |
| pm1 | 13797 |
| pm10 | 13797 |
| no2 | 13797 |
| co | 13797 |
| nh3 | 13797 |
| so2 | 13797 |
| pm2_5 | 13797 |
| pm4 | 13797 |

_… 34 more rows_


---

## B019 · quantity_count

**Question:** How many different physical quantities are measured at Schenkenberg?  
**Reference:** 55 quantities.  
**Recomputed:** `55` → **MATCH**

```sql
SELECT count(DISTINCT o.property_id) AS quantities FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg';
```
| quantities |
|---|
| 55 |

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg'
GROUP BY 1 ORDER BY 2 DESC;
```
| property_id | count |
|---|---|
| temp1 | 32650 |
| temperature | 26859 |
| wind_peak_1 | 17897 |
| hum1 | 17897 |
| light | 17897 |
| baro | 17897 |
| wind_speed_1 | 17897 |
| rain_1 | 17897 |
| rain_acc | 17897 |
| wind_direction_1 | 17897 |
| uv | 17897 |
| ec | 14753 |
| moisture | 14753 |
| activeTime | 11964 |
| backgroundEvent | 11964 |
| overThresholdEvents | 11961 |
| pgaXAxis | 8372 |
| pgaYAxis | 8372 |
| pgaZAxis | 8371 |
| axis_x | 8098 |

_… 35 more rows_


---

## B020 · avg_quantity

**Question:** What is the average composed RMS acceleration (rmsComposed) recorded at Schenkenberg?  
**Reference:** 4.334 mg.  
**Recomputed:** `4.333864541832807` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'rmsComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 4.33386 | 777 | 0.3 | 502 | mg_acc |


---

## B021 · avg_quantity

**Question:** What is the average composed peak ground acceleration (pgaComposed) recorded at Schenkenberg?  
**Reference:** 6.288 mg.  
**Recomputed:** `6.288152610441712` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'pgaComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 6.28815 | 1238.6 | 0.9 | 498 | mg_acc |


---

## B022 · avg_quantity

**Question:** What is the average potentiometer displacement observed at Delos?  
**Reference:** 22.623.  
**Recomputed:** `22.623179094883824` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'potentiometer_displacement' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 22.6232 | 49.5 | 0.869739 | 4218 | None |


---

## B023 · avg_quantity

**Question:** What is the average rainfall observed at Ranverso?  
**Reference:** 0.012.  
**Recomputed:** `0.011753643629525155` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.0117536 | 6.8 | 0 | 2127 | None |


---

## B024 · avg_quantity

**Question:** What is the average soil temperature observed at Baltanas?  
**Reference:** 28.216.  
**Recomputed:** `28.21560235739415` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 28.2156 | 38.51 | 18.7 | 50734 | None |


---

## B025 · avg_quantity

**Question:** What is the average soil water potential recorded at Baltanas?  
**Reference:** 93.517.  
**Recomputed:** `93.5171354178962` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_water_potential' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 93.5171 | 94.767 | -42.424 | 50850 | None |


---

## B026 · avg_quantity

**Question:** What is the average temperature measured at Schenkenberg?  
**Reference:** 23.672 °C.  
**Recomputed:** `23.672202985963796` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |


---

## B027 · avg_quantity

**Question:** What is the average temperature observed at Delos?  
**Reference:** 26.087.  
**Recomputed:** `26.087030199753844` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |


---

## B028 · avg_quantity

**Question:** What is the average temperature recorded at Baltanas?  
**Reference:** 21.722 °C.  
**Recomputed:** `21.721905265213753` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |


---

## B029 · avg_quantity

**Question:** What is the average temperature recorded at Ranverso?  
**Reference:** 24.209 °C.  
**Recomputed:** `24.20859226379202` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |


---

## B030 · avg_quantity

**Question:** What is the average voltage measured at Lucretili?  
**Reference:** 0.142.  
**Recomputed:** `0.1416362646084936` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.141636 | 4.61947 | 0.0036663 | 179933 | None |


---

## B031 · avg_quantity

**Question:** What is the average voltage observed at Baltanas?  
**Reference:** 0.903 V.  
**Recomputed:** `0.9029327876239512` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.902933 | 3.72243 | -0.0011721 | 182636 | V |


---

## B032 · avg_quantity

**Question:** What is the average voltage observed at Delos?  
**Reference:** 2.387 V.  
**Recomputed:** `2.387406240001124` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 2.38741 | 13104 | -0.0016764 | 35824 | V |


---

## B033 · avg_quantity

**Question:** What is the average voltage observed at Ranverso?  
**Reference:** 1.543.  
**Recomputed:** `1.5432252862908102` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.54323 | 4.42806 | 0.0010206 | 14793 | None |


---

## B034 · max_quantity

**Question:** What is the maximum composed RMS acceleration (rmsComposed) measured at Schenkenberg?  
**Reference:** 777 mg.  
**Recomputed:** `777.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'rmsComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 4.33386 | 777 | 0.3 | 502 | mg_acc |


---

## B035 · max_quantity

**Question:** What is the maximum composed peak ground acceleration (pgaComposed) measured at Schenkenberg?  
**Reference:** 1238.6 mg.  
**Recomputed:** `1238.6` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'pgaComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 6.28815 | 1238.6 | 0.9 | 498 | mg_acc |


---

## B036 · max_quantity

**Question:** What is the maximum potentiometer displacement recorded at Delos?  
**Reference:** 49.5.  
**Recomputed:** `49.50000644` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'potentiometer_displacement' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 22.6232 | 49.5 | 0.869739 | 4218 | None |


---

## B037 · max_quantity

**Question:** What is the maximum rainfall measured at Ranverso?  
**Reference:** 6.8.  
**Recomputed:** `6.8` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.0117536 | 6.8 | 0 | 2127 | None |


---

## B038 · max_quantity

**Question:** What is the maximum soil temperature measured at Baltanas?  
**Reference:** 38.51.  
**Recomputed:** `38.51` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 28.2156 | 38.51 | 18.7 | 50734 | None |


---

## B039 · max_quantity

**Question:** What is the maximum soil water potential recorded at Baltanas?  
**Reference:** 94.767.  
**Recomputed:** `94.767` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_water_potential' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 93.5171 | 94.767 | -42.424 | 50850 | None |


---

## B040 · max_quantity

**Question:** What is the maximum temperature measured at Baltanas?  
**Reference:** 44.6 °C.  
**Recomputed:** `44.6` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |


---

## B041 · max_quantity

**Question:** What is the maximum temperature measured at Lucretili?  
**Reference:** 50 °C.  
**Recomputed:** `50.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |


---

## B042 · max_quantity

**Question:** What is the maximum temperature measured at Ranverso?  
**Reference:** 40 °C.  
**Recomputed:** `40.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |


---

## B043 · max_quantity

**Question:** What is the maximum temperature measured at Schenkenberg?  
**Reference:** 48.3 °C.  
**Recomputed:** `48.3` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |


---

## B044 · max_quantity

**Question:** What is the maximum temperature recorded at Delos?  
**Reference:** 54.2.  
**Recomputed:** `54.2` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |


---

## B045 · max_quantity

**Question:** What is the maximum voltage measured at Delos?  
**Reference:** 13104 V.  
**Recomputed:** `13104.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 2.38741 | 13104 | -0.0016764 | 35824 | V |


---

## B046 · max_quantity

**Question:** What is the maximum voltage measured at Ranverso?  
**Reference:** 4.428.  
**Recomputed:** `4.4280627` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.54323 | 4.42806 | 0.0010206 | 14793 | None |


---

## B047 · max_quantity

**Question:** What is the maximum voltage observed at Baltanas?  
**Reference:** 3.722 V.  
**Recomputed:** `3.722426` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.902933 | 3.72243 | -0.0011721 | 182636 | V |


---

## B048 · min_quantity

**Question:** What is the minimum composed RMS acceleration (rmsComposed) observed at Schenkenberg?  
**Reference:** 0.3 mg.  
**Recomputed:** `0.3` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'rmsComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 4.33386 | 777 | 0.3 | 502 | mg_acc |


---

## B049 · min_quantity

**Question:** What is the minimum composed peak ground acceleration (pgaComposed) measured at Schenkenberg?  
**Reference:** 0.9 mg.  
**Recomputed:** `0.9` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'pgaComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 6.28815 | 1238.6 | 0.9 | 498 | mg_acc |


---

## B050 · min_quantity

**Question:** What is the minimum potentiometer displacement recorded at Delos?  
**Reference:** 0.87.  
**Recomputed:** `0.869739059999995` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'potentiometer_displacement' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 22.6232 | 49.5 | 0.869739 | 4218 | None |


---

## B051 · min_quantity

**Question:** What is the minimum soil temperature recorded at Baltanas?  
**Reference:** 18.7.  
**Recomputed:** `18.7` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 28.2156 | 38.51 | 18.7 | 50734 | None |


---

## B052 · min_quantity

**Question:** What is the minimum soil water potential recorded at Baltanas?  
**Reference:** -42.424.  
**Recomputed:** `-42.424` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_water_potential' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 93.5171 | 94.767 | -42.424 | 50850 | None |


---

## B053 · min_quantity

**Question:** What is the minimum temperature measured at Schenkenberg?  
**Reference:** 9.2 °C.  
**Recomputed:** `9.2` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |


---

## B054 · min_quantity

**Question:** What is the minimum temperature observed at Baltanas?  
**Reference:** -0.6 °C.  
**Recomputed:** `-0.6` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |


---

## B055 · min_quantity

**Question:** What is the minimum temperature observed at Delos?  
**Reference:** 11.5.  
**Recomputed:** `11.5` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |


---

## B056 · min_quantity

**Question:** What is the minimum temperature observed at Lucretili?  
**Reference:** 0 °C.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |


---

## B057 · min_quantity

**Question:** What is the minimum temperature recorded at Ranverso?  
**Reference:** 2 °C.  
**Recomputed:** `2.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |


---

## B058 · min_quantity

**Question:** What is the minimum voltage measured at Baltanas?  
**Reference:** -0.001 V.  
**Recomputed:** `-0.0011721` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.902933 | 3.72243 | -0.0011721 | 182636 | V |


---

## B059 · min_quantity

**Question:** What is the minimum voltage recorded at Delos?  
**Reference:** -0.002 V.  
**Recomputed:** `-0.0016764` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 2.38741 | 13104 | -0.0016764 | 35824 | V |


---

## B060 · min_quantity

**Question:** What is the minimum voltage recorded at Lucretili?  
**Reference:** 0.004.  
**Recomputed:** `0.0036663` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.141636 | 4.61947 | 0.0036663 | 179933 | None |


---

## B061 · obs_count

**Question:** How many composed RMS acceleration (rmsComposed) observations exist for Schenkenberg?  
**Reference:** 502 observations.  
**Recomputed:** `502` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'rmsComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 4.33386 | 777 | 0.3 | 502 | mg_acc |


---

## B062 · obs_count

**Question:** How many composed peak ground acceleration (pgaComposed) observations exist for Schenkenberg?  
**Reference:** 498 observations.  
**Recomputed:** `498` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'pgaComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 6.28815 | 1238.6 | 0.9 | 498 | mg_acc |


---

## B063 · obs_count

**Question:** How many potentiometer displacement observations exist for Delos?  
**Reference:** 4218 observations.  
**Recomputed:** `4218` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'potentiometer_displacement' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 22.6232 | 49.5 | 0.869739 | 4218 | None |


---

## B064 · obs_count

**Question:** How many rainfall observations exist for Ranverso?  
**Reference:** 2127 observations.  
**Recomputed:** `2127` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.0117536 | 6.8 | 0 | 2127 | None |


---

## B065 · obs_count

**Question:** How many soil temperature observations exist for Baltanas?  
**Reference:** 50734 observations.  
**Recomputed:** `50734` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 28.2156 | 38.51 | 18.7 | 50734 | None |


---

## B066 · obs_count

**Question:** How many soil water potential observations exist for Baltanas?  
**Reference:** 50850 observations.  
**Recomputed:** `50850` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_water_potential' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 93.5171 | 94.767 | -42.424 | 50850 | None |


---

## B067 · obs_count

**Question:** How many temperature observations exist for Baltanas?  
**Reference:** 435215 observations.  
**Recomputed:** `435215` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |


---

## B068 · obs_count

**Question:** How many temperature observations exist for Delos?  
**Reference:** 21126 observations.  
**Recomputed:** `21126` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |


---

## B069 · obs_count

**Question:** How many temperature observations exist for Lucretili?  
**Reference:** 318576 observations.  
**Recomputed:** `318576` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |


---

## B070 · obs_count

**Question:** How many temperature observations exist for Ranverso?  
**Reference:** 18924 observations.  
**Recomputed:** `18924` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |


---

## B071 · obs_count

**Question:** How many temperature observations exist for Schenkenberg?  
**Reference:** 26859 observations.  
**Recomputed:** `26859` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |


---

## B072 · obs_count

**Question:** How many voltage observations exist for Baltanas?  
**Reference:** 182636 observations.  
**Recomputed:** `182636` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.902933 | 3.72243 | -0.0011721 | 182636 | V |


---

## B073 · obs_count

**Question:** How many voltage observations exist for Delos?  
**Reference:** 35824 observations.  
**Recomputed:** `35824` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 2.38741 | 13104 | -0.0016764 | 35824 | V |


---

## B074 · obs_count

**Question:** How many voltage observations exist for Lucretili?  
**Reference:** 179933 observations.  
**Recomputed:** `179933` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.141636 | 4.61947 | 0.0036663 | 179933 | None |


---

## B075 · obs_count

**Question:** How many voltage observations exist for Ranverso?  
**Reference:** 14793 observations.  
**Recomputed:** `14793` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.54323 | 4.42806 | 0.0010206 | 14793 | None |


---

## B076 · sensors_measuring

**Question:** How many sensors measure composed RMS acceleration (rmsComposed) at Schenkenberg?  
**Reference:** 1 sensor.  
**Recomputed:** `1` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'rmsComposed';
```
| sensors |
|---|
| 1 |


---

## B077 · sensors_measuring

**Question:** How many sensors measure composed peak ground acceleration (pgaComposed) at Schenkenberg?  
**Reference:** 1 sensor.  
**Recomputed:** `1` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'pgaComposed';
```
| sensors |
|---|
| 1 |


---

## B078 · sensors_measuring

**Question:** How many sensors measure potentiometer displacement at Delos?  
**Reference:** 2 sensors.  
**Recomputed:** `2` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'potentiometer_displacement';
```
| sensors |
|---|
| 2 |


---

## B079 · sensors_measuring

**Question:** How many sensors measure rainfall at Ranverso?  
**Reference:** 1 sensor.  
**Recomputed:** `1` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall';
```
| sensors |
|---|
| 1 |


---

## B080 · sensors_measuring

**Question:** How many sensors measure soil temperature at Baltanas?  
**Reference:** 2 sensors.  
**Recomputed:** `2` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature';
```
| sensors |
|---|
| 2 |


---

## B081 · sensors_measuring

**Question:** How many sensors measure soil water potential at Baltanas?  
**Reference:** 2 sensors.  
**Recomputed:** `2` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_water_potential';
```
| sensors |
|---|
| 2 |


---

## B082 · sensors_measuring

**Question:** How many sensors measure temperature at Baltanas?  
**Reference:** 19 sensors.  
**Recomputed:** `19` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature';
```
| sensors |
|---|
| 19 |


---

## B083 · sensors_measuring

**Question:** How many sensors measure temperature at Delos?  
**Reference:** 10 sensors.  
**Recomputed:** `10` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature';
```
| sensors |
|---|
| 10 |


---

## B084 · sensors_measuring

**Question:** How many sensors measure temperature at Lucretili?  
**Reference:** 18 sensors.  
**Recomputed:** `18` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature';
```
| sensors |
|---|
| 18 |


---

## B085 · sensors_measuring

**Question:** How many sensors measure temperature at Ranverso?  
**Reference:** 9 sensors.  
**Recomputed:** `9` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature';
```
| sensors |
|---|
| 9 |


---

## B086 · sensors_measuring

**Question:** How many sensors measure temperature at Schenkenberg?  
**Reference:** 12 sensors.  
**Recomputed:** `12` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature';
```
| sensors |
|---|
| 12 |


---

## B087 · sensors_measuring

**Question:** How many sensors measure voltage at Baltanas?  
**Reference:** 10 sensors.  
**Recomputed:** `10` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage';
```
| sensors |
|---|
| 10 |


---

## B088 · sensors_measuring

**Question:** How many sensors measure voltage at Delos?  
**Reference:** 16 sensors.  
**Recomputed:** `16` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage';
```
| sensors |
|---|
| 16 |


---

## B089 · sensors_measuring

**Question:** How many sensors measure voltage at Lucretili?  
**Reference:** 9 sensors.  
**Recomputed:** `9` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'voltage';
```
| sensors |
|---|
| 9 |


---

## B090 · sensors_measuring

**Question:** How many sensors measure voltage at Ranverso?  
**Reference:** 7 sensors.  
**Recomputed:** `7` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage';
```
| sensors |
|---|
| 7 |


---

## B091 · site_compare

**Question:** Among Baltanas, Delos, Lucretili, Ranverso and Schenkenberg, which site has the highest average temperature?  
**Reference:** Delos (26.087).  
**Recomputed:** `Delos` → **MATCH**

```sql
SELECT r.site_id, avg(o.value) AS avg_temperature FROM observations o JOIN readings r USING (reading_id)
WHERE o.property_id = 'temperature' AND o.value IS NOT NULL AND r.site_id IN ('baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg')
GROUP BY 1 ORDER BY 2 DESC;
```
| site_id | avg_temperature |
|---|---|
| delos | 26.087 |
| ranverso | 24.2086 |
| schenkenberg | 23.6722 |
| lucretili | 23.6386 |
| baltanas | 21.7219 |


---

## B092 · site_compare

**Question:** Among Baltanas, Delos, Lucretili, Ranverso and Schenkenberg, which site has the lowest average temperature?  
**Reference:** Baltanas (21.722).  
**Recomputed:** `Baltanas` → **MATCH**

```sql
SELECT r.site_id, avg(o.value) AS avg_temperature FROM observations o JOIN readings r USING (reading_id)
WHERE o.property_id = 'temperature' AND o.value IS NOT NULL AND r.site_id IN ('baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg')
GROUP BY 1 ORDER BY 2 ASC;
```
| site_id | avg_temperature |
|---|---|
| baltanas | 21.7219 |
| lucretili | 23.6386 |
| schenkenberg | 23.6722 |
| ranverso | 24.2086 |
| delos | 26.087 |


---

## B093 · site_compare

**Question:** Among Baltanas, Delos, Lucretili, Ranverso and Schenkenberg, which site has the most readings?  
**Reference:** Baltanas (709170 readings).  
**Recomputed:** `Baltanas` → **MATCH**

```sql
SELECT site_id, count(*) AS readings FROM readings WHERE site_id IN ('baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg')
GROUP BY 1 ORDER BY 2 DESC;
```
| site_id | readings |
|---|---|
| baltanas | 709170 |
| lucretili | 574578 |
| delos | 225945 |
| ranverso | 108150 |
| schenkenberg | 59713 |


---

## B094 · site_compare

**Question:** Among Baltanas, Delos, Lucretili, Ranverso and Schenkenberg, which site has the most sensor nodes?  
**Reference:** Delos (19 nodes).  
**Recomputed:** `Delos` → **MATCH**

```sql
SELECT site_id, count(DISTINCT node_id) AS nodes FROM readings WHERE site_id IN ('baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg')
GROUP BY 1 ORDER BY 2 DESC;
```
| site_id | nodes |
|---|---|
| delos | 19 |
| baltanas | 15 |
| lucretili | 15 |
| ranverso | 13 |
| schenkenberg | 9 |


---

## B095 · unanswerable

**Question:** What is the average CO2 concentration at Lucretili?  
**Reference:** Cannot be answered: the knowledge graph has no CO2 concentration data for Lucretili.  
**Recomputed:** `None` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND (lower(o.property_id) LIKE '%co2%');
```
_(no rows)_

- Expected: no rows (no CO2 concentration data at lucretili). Got 0 row(s).

---

## B096 · avg_quantity

**Question:** What is the average barometric pressure at Ranverso?  
**Reference:** 97614.262 Pa.  
**Recomputed:** `97614.26191901058` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'baro' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 97614.3 | 98300 | 94240 | 10026 | Pa |


---

## B097 · avg_quantity

**Question:** What is the average relative humidity at Baltanas?  
**Reference:** 42.292 %.  
**Recomputed:** `42.29167911116421` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'hum1' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 42.2917 | 91 | 9 | 16741 | % |


---

## B098 · avg_quantity

**Question:** What is the average relative humidity at Schenkenberg?  
**Reference:** 46.258 %.  
**Recomputed:** `46.25764094540985` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'hum1' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 46.2576 | 99 | 12 | 17897 | % |


---

## B099 · unanswerable

**Question:** What is the average solar radiation at Delos?  
**Reference:** Cannot be answered: the knowledge graph has no solar radiation data for Delos.  
**Recomputed:** `None` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND (lower(o.property_id) LIKE '%solar%' OR lower(o.property_id) LIKE '%radiation%');
```
_(no rows)_

- Expected: no rows (no solar radiation data at delos). Got 0 row(s).

---

## B100 · avg_quantity

**Question:** What is the average wind speed at Delos?  
**Reference:** 3.413 m/s.  
**Recomputed:** `3.412941829621858` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'wind_speed_1' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 3.41294 | 16.9 | 0 | 32422 | m/s |


---
