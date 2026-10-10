# Verification — basic

Run `SET TIME ZONE 'UTC';` in psql first (`psql -h localhost -U argus -d argus_snapshot`).

## B001 · node_count

**Question:** How many sensor nodes are installed at Baltanas?  
**Reference:** 13 sensor nodes.  
**Recomputed:** `13` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'baltanas';
```
| nodes |
|---|
| 13 |


---

## B002 · node_count

**Question:** How many sensor nodes are installed at Delos?  
**Reference:** 15 sensor nodes.  
**Recomputed:** `15` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'delos';
```
| nodes |
|---|
| 15 |


---

## B003 · node_count

**Question:** How many sensor nodes are installed at Lucretili?  
**Reference:** 13 sensor nodes.  
**Recomputed:** `13` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'lucretili';
```
| nodes |
|---|
| 13 |


---

## B004 · node_count

**Question:** How many sensor nodes are installed at Ranverso?  
**Reference:** 7 sensor nodes.  
**Recomputed:** `7` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'ranverso';
```
| nodes |
|---|
| 7 |


---

## B005 · node_count

**Question:** How many sensor nodes are installed at Schenkenberg?  
**Reference:** 7 sensor nodes.  
**Recomputed:** `7` → **MATCH**

```sql
SELECT count(DISTINCT node_id) AS nodes FROM readings WHERE site_id = 'schenkenberg';
```
| nodes |
|---|
| 7 |


---

## B006 · sensor_count

**Question:** How many sensors have reported readings at Baltanas?  
**Reference:** 33 sensors.  
**Recomputed:** `33` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'baltanas';
```
| sensors |
|---|
| 33 |


---

## B007 · sensor_count

**Question:** How many sensors have reported readings at Delos?  
**Reference:** 26 sensors.  
**Recomputed:** `26` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'delos';
```
| sensors |
|---|
| 26 |


---

## B008 · sensor_count

**Question:** How many sensors have reported readings at Lucretili?  
**Reference:** 18 sensors.  
**Recomputed:** `18` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'lucretili';
```
| sensors |
|---|
| 18 |


---

## B009 · sensor_count

**Question:** How many sensors have reported readings at Ranverso?  
**Reference:** 13 sensors.  
**Recomputed:** `13` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'ranverso';
```
| sensors |
|---|
| 13 |


---

## B010 · sensor_count

**Question:** How many sensors have reported readings at Schenkenberg?  
**Reference:** 12 sensors.  
**Recomputed:** `12` → **MATCH**

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'schenkenberg';
```
| sensors |
|---|
| 12 |


---

## B011 · reading_count

**Question:** How many readings are stored for Baltanas?  
**Reference:** 676272 readings.  
**Recomputed:** `676272` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'baltanas';
```
| readings |
|---|
| 676272 |


---

## B012 · reading_count

**Question:** How many readings are stored for Delos?  
**Reference:** 113789 readings.  
**Recomputed:** `113789` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'delos';
```
| readings |
|---|
| 113789 |


---

## B013 · reading_count

**Question:** How many readings are stored for Lucretili?  
**Reference:** 526071 readings.  
**Recomputed:** `526071` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili';
```
| readings |
|---|
| 526071 |


---

## B014 · reading_count

**Question:** How many readings are stored for Ranverso?  
**Reference:** 50695 readings.  
**Recomputed:** `50695` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'ranverso';
```
| readings |
|---|
| 50695 |


---

## B015 · reading_count

**Question:** How many readings are stored for Schenkenberg?  
**Reference:** 26859 readings.  
**Recomputed:** `26859` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'schenkenberg';
```
| readings |
|---|
| 26859 |


---

## B016 · quantity_count

**Question:** How many different physical quantities are measured at Baltanas?  
**Reference:** 55 quantities.  
**Recomputed:** `55` → **MATCH**

```sql
SELECT count(DISTINCT o.property_id) AS quantities FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'baltanas';
```
| quantities |
|---|
| 55 |

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'baltanas'
GROUP BY 1 ORDER BY 2 DESC;
```
| property_id | count |
|---|---|
| temperature | 435215 |
| voltage | 167572 |
| voltage_polynomial_4 | 137289 |
| thermistor | 127203 |
| pulse_counter | 127179 |
| yAxis | 53645 |
| xAxis | 53645 |
| zAxis | 53643 |
| underThresholdEvents | 50862 |
| duration | 50862 |
| backgroundEvent | 50862 |
| overThresholdEvents | 50862 |
| activeTime | 50862 |
| freqXAxis | 50861 |
| freqYAxis | 50861 |
| freqZAxis | 50861 |
| composedAxis | 50860 |
| soil_water_potential | 50850 |
| installation_pitch_angle | 50850 |
| soil_temperature | 50734 |

_… 35 more rows_


---

## B017 · quantity_count

**Question:** How many different physical quantities are measured at Lucretili?  
**Reference:** 25 quantities.  
**Recomputed:** `25` → **MATCH**

```sql
SELECT count(DISTINCT o.property_id) AS quantities FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili';
```
| quantities |
|---|
| 25 |

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
| axis_x_std | 58484 |
| axis_y | 58484 |
| axis_y_std | 58484 |
| axis_z_std | 58484 |
| axis_x | 58484 |
| thermistor | 49866 |
| pulse_counter | 28150 |
| thermistor_ysi44005 | 24649 |
| rainfall | 2911 |
| zAxis | 2143 |
| backgroundEvent | 2143 |
| duration | 2143 |
| freqXAxis | 2143 |
| freqYAxis | 2143 |
| freqZAxis | 2143 |
| overThresholdEvents | 2143 |

_… 5 more rows_


---

## B018 · quantity_count

**Question:** How many different physical quantities are measured at Ranverso?  
**Reference:** 26 quantities.  
**Recomputed:** `26` → **MATCH**

```sql
SELECT count(DISTINCT o.property_id) AS quantities FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso';
```
| quantities |
|---|
| 26 |

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso'
GROUP BY 1 ORDER BY 2 DESC;
```
| property_id | count |
|---|---|
| temperature | 18924 |
| voltage | 14793 |
| voltage_1 | 12672 |
| thermistor_ysi44005 | 6339 |
| thermistor | 6336 |
| pulse_counter | 2131 |
| rainfall | 2127 |
| voltage_polynomial_4 | 2124 |
| zAxis | 2088 |
| backgroundEvent | 2088 |
| composedAxis | 2088 |
| duration | 2088 |
| freqYAxis | 2088 |
| freqZAxis | 2088 |
| overThresholdEvents | 2088 |
| underThresholdEvents | 2088 |
| xAxis | 2088 |
| yAxis | 2088 |
| activeTime | 2088 |
| axis_y_std | 2085 |

_… 6 more rows_


---

## B019 · quantity_count

**Question:** How many different physical quantities are measured at Schenkenberg?  
**Reference:** 43 quantities.  
**Recomputed:** `43` → **MATCH**

```sql
SELECT count(DISTINCT o.property_id) AS quantities FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg';
```
| quantities |
|---|
| 43 |

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg'
GROUP BY 1 ORDER BY 2 DESC;
```
| property_id | count |
|---|---|
| temperature | 26859 |
| activeTime | 11964 |
| backgroundEvent | 11964 |
| overThresholdEvents | 11961 |
| pgaYAxis | 8372 |
| pgaXAxis | 8372 |
| pgaZAxis | 8371 |
| axis_z | 8098 |
| axis_x | 8098 |
| axis_x_std | 8098 |
| axis_y | 8098 |
| axis_y_std | 8098 |
| axis_z_std | 8098 |
| freq2Xaxis | 7872 |
| freq2Yaxis | 7872 |
| freq2Zaxis | 7872 |
| freq3Xaxis | 7872 |
| freq3Yaxis | 7872 |
| freq3Zaxis | 7872 |
| freq4Xaxis | 7872 |

_… 23 more rows_


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
**Recomputed:** `22.623179094883845` → **MATCH**

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
**Recomputed:** `0.011753643629525154` → **MATCH**

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
**Recomputed:** `28.215602357394136` → **MATCH**

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
**Recomputed:** `93.51713541789607` → **MATCH**

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
**Recomputed:** `23.672202985963782` → **MATCH**

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
**Recomputed:** `26.08703019975384` → **MATCH**

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
**Recomputed:** `21.72190526521377` → **MATCH**

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
**Recomputed:** `24.208592263792024` → **MATCH**

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
**Recomputed:** `0.1416362646084934` → **MATCH**

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
**Reference:** 0.935.  
**Recomputed:** `0.9349161758575463` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.934916 | 3.72243 | -0.0011721 | 167572 | None |


---

## B032 · avg_quantity

**Question:** What is the average voltage observed at Delos?  
**Reference:** 1.656.  
**Recomputed:** `1.6559220909441201` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.65592 | 4.94471 | -0.0016764 | 35822 | None |


---

## B033 · avg_quantity

**Question:** What is the average voltage observed at Ranverso?  
**Reference:** 1.543.  
**Recomputed:** `1.543225286290811` → **MATCH**

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
**Reference:** 4.945.  
**Recomputed:** `4.944706` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.65592 | 4.94471 | -0.0016764 | 35822 | None |


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
**Reference:** 3.722.  
**Recomputed:** `3.722426` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.934916 | 3.72243 | -0.0011721 | 167572 | None |


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
**Reference:** -0.001.  
**Recomputed:** `-0.0011721` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.934916 | 3.72243 | -0.0011721 | 167572 | None |


---

## B059 · min_quantity

**Question:** What is the minimum voltage recorded at Delos?  
**Reference:** -0.002.  
**Recomputed:** `-0.0016764` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.65592 | 4.94471 | -0.0016764 | 35822 | None |


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
**Reference:** 167572 observations.  
**Recomputed:** `167572` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.934916 | 3.72243 | -0.0011721 | 167572 | None |


---

## B073 · obs_count

**Question:** How many voltage observations exist for Delos?  
**Reference:** 35822 observations.  
**Recomputed:** `35822` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.65592 | 4.94471 | -0.0016764 | 35822 | None |


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
**Reference:** 9 sensors.  
**Recomputed:** `9` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage';
```
| sensors |
|---|
| 9 |


---

## B088 · sensors_measuring

**Question:** How many sensors measure voltage at Delos?  
**Reference:** 15 sensors.  
**Recomputed:** `15` → **MATCH**

```sql
SELECT count(DISTINCT r.sensor_id) AS sensors FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage';
```
| sensors |
|---|
| 15 |


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

**Question:** Which heritage site has the highest average temperature?  
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

**Question:** Which heritage site has the lowest average temperature?  
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

**Question:** Which heritage site has the most readings?  
**Reference:** Baltanas (676272 readings).  
**Recomputed:** `Baltanas` → **MATCH**

```sql
SELECT site_id, count(*) AS readings FROM readings WHERE site_id IN ('baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg')
GROUP BY 1 ORDER BY 2 DESC;
```
| site_id | readings |
|---|---|
| baltanas | 676272 |
| lucretili | 526071 |
| delos | 113789 |
| ranverso | 50695 |
| schenkenberg | 26859 |


---

## B094 · site_compare

**Question:** Which heritage site has the most sensor nodes?  
**Reference:** Delos (15 nodes).  
**Recomputed:** `Delos` → **MATCH**

```sql
SELECT site_id, count(DISTINCT node_id) AS nodes FROM readings WHERE site_id IN ('baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg')
GROUP BY 1 ORDER BY 2 DESC;
```
| site_id | nodes |
|---|---|
| delos | 15 |
| baltanas | 13 |
| lucretili | 13 |
| ranverso | 7 |
| schenkenberg | 7 |


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

## B096 · unanswerable

**Question:** What is the average barometric pressure at Ranverso?  
**Reference:** Cannot be answered: the knowledge graph has no barometric pressure data for Ranverso.  
**Recomputed:** `None` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND (lower(o.property_id) LIKE '%baro%' OR lower(o.property_id) LIKE '%pressure%');
```
_(no rows)_

- Expected: no rows (no barometric pressure data at ranverso). Got 0 row(s).

---

## B097 · unanswerable

**Question:** What is the average relative humidity at Baltanas?  
**Reference:** Cannot be answered: the knowledge graph has no relative humidity data for Baltanas.  
**Recomputed:** `None` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND (lower(o.property_id) LIKE '%hum%');
```
_(no rows)_

- Expected: no rows (no relative humidity data at baltanas). Got 0 row(s).

---

## B098 · unanswerable

**Question:** What is the average relative humidity at Schenkenberg?  
**Reference:** Cannot be answered: the knowledge graph has no relative humidity data for Schenkenberg.  
**Recomputed:** `None` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%hum%');
```
_(no rows)_

- Expected: no rows (no relative humidity data at schenkenberg). Got 0 row(s).

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

## B100 · unanswerable

**Question:** What is the average wind speed at Delos?  
**Reference:** Cannot be answered: the knowledge graph has no wind speed data for Delos.  
**Recomputed:** `None` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND (lower(o.property_id) LIKE '%wind%');
```
_(no rows)_

- Expected: no rows (no wind speed data at delos). Got 0 row(s).

---
