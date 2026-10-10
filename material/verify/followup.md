# Verification — followup

Run `SET TIME ZONE 'UTC';` in psql first (`psql -h localhost -U argus -d argus_snapshot`).

## F001 · what_about_site

**Turn 1:** What is the average temperature at Schenkenberg?  
**Answer given in history:** The average temperature at Schenkenberg is 23.672 °C.  
**Recomputed:** `23.672202985963786`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |

**Question:** What about Baltanas?  
**Reference:** 21.722 °C.  
**Recomputed:** `21.721905265213728` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |


---

## F002 · what_about_site

**Turn 1:** What is the average temperature at Delos?  
**Answer given in history:** The average temperature at Delos is 26.087.  
**Recomputed:** `26.08703019975385`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |

**Question:** What about Baltanas?  
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

## F003 · what_about_site

**Turn 1:** What is the average voltage at Ranverso?  
**Answer given in history:** The average voltage at Ranverso is 1.543.  
**Recomputed:** `1.5432252862908102`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.54323 | 4.42806 | 0.0010206 | 14793 | None |

**Question:** What about Baltanas?  
**Reference:** 0.935.  
**Recomputed:** `0.9349161758575465` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.934916 | 3.72243 | -0.0011721 | 167572 | None |


---

## F004 · what_about_site

**Turn 1:** What is the average temperature at Schenkenberg?  
**Answer given in history:** The average temperature at Schenkenberg is 23.672 °C.  
**Recomputed:** `23.672202985963786`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |

**Question:** What about Delos?  
**Reference:** 26.087.  
**Recomputed:** `26.087030199753862` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |


---

## F005 · what_about_site

**Turn 1:** What is the average temperature at Ranverso?  
**Answer given in history:** The average temperature at Ranverso is 24.209 °C.  
**Recomputed:** `24.208592263792028`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Question:** What about Delos?  
**Reference:** 26.087.  
**Recomputed:** `26.08703019975385` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |


---

## F006 · what_about_site

**Turn 1:** What is the average temperature at Baltanas?  
**Answer given in history:** The average temperature at Baltanas is 21.722 °C.  
**Recomputed:** `21.721905265213753`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |

**Question:** What about Delos?  
**Reference:** 26.087.  
**Recomputed:** `26.087030199753862` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |


---

## F007 · what_about_site

**Turn 1:** What is the average voltage at Lucretili?  
**Answer given in history:** The average voltage at Lucretili is 0.142.  
**Recomputed:** `0.1416362646084932`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.141636 | 4.61947 | 0.0036663 | 179933 | None |

**Question:** What about Delos?  
**Reference:** 1.656.  
**Recomputed:** `1.6559220909441192` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.65592 | 4.94471 | -0.0016764 | 35822 | None |


---

## F008 · what_about_site

**Turn 1:** What is the average voltage at Baltanas?  
**Answer given in history:** The average voltage at Baltanas is 0.935.  
**Recomputed:** `0.9349161758575444`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.934916 | 3.72243 | -0.0011721 | 167572 | None |

**Question:** What about Lucretili?  
**Reference:** 0.142.  
**Recomputed:** `0.14163626460849402` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.141636 | 4.61947 | 0.0036663 | 179933 | None |


---

## F009 · what_about_site

**Turn 1:** What is the average voltage at Baltanas?  
**Answer given in history:** The average voltage at Baltanas is 0.935.  
**Recomputed:** `0.9349161758575425`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.934916 | 3.72243 | -0.0011721 | 167572 | None |

**Question:** What about Ranverso?  
**Reference:** 1.543.  
**Recomputed:** `1.54322528629081` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.54323 | 4.42806 | 0.0010206 | 14793 | None |


---

## F010 · what_about_site

**Turn 1:** What is the average temperature at Delos?  
**Answer given in history:** The average temperature at Delos is 26.087.  
**Recomputed:** `26.08703019975386`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |

**Question:** What about Ranverso?  
**Reference:** 24.209 °C.  
**Recomputed:** `24.20859226379203` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |


---

## F011 · what_about_site

**Turn 1:** What is the average voltage at Delos?  
**Answer given in history:** The average voltage at Delos is 1.656.  
**Recomputed:** `1.6559220909441181`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.65592 | 4.94471 | -0.0016764 | 35822 | None |

**Question:** What about Ranverso?  
**Reference:** 1.543.  
**Recomputed:** `1.5432252862908111` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.54323 | 4.42806 | 0.0010206 | 14793 | None |


---

## F012 · what_about_site

**Turn 1:** What is the average temperature at Ranverso?  
**Answer given in history:** The average temperature at Ranverso is 24.209 °C.  
**Recomputed:** `24.208592263792017`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Question:** What about Schenkenberg?  
**Reference:** 23.672 °C.  
**Recomputed:** `23.672202985963786` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |


---

## F013 · and_the_minimum

**Turn 1:** What is the maximum temperature recorded at Schenkenberg?  
**Answer given in history:** The maximum is 48.3 °C.  
**Recomputed:** `48.3`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |

**Question:** And the minimum?  
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

## F014 · and_the_minimum

**Turn 1:** What is the maximum temperature recorded at Baltanas?  
**Answer given in history:** The maximum is 44.6 °C.  
**Recomputed:** `44.6`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |

**Question:** And the minimum?  
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

## F015 · and_the_minimum

**Turn 1:** What is the maximum composed RMS acceleration (rmsComposed) recorded at Schenkenberg?  
**Answer given in history:** The maximum is 777 mg.  
**Recomputed:** `777.0`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'rmsComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 4.33386 | 777 | 0.3 | 502 | mg_acc |

**Question:** And the minimum?  
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

## F016 · and_the_minimum

**Turn 1:** What is the maximum temperature recorded at Ranverso?  
**Answer given in history:** The maximum is 40 °C.  
**Recomputed:** `40.0`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Question:** And the minimum?  
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

## F017 · and_the_minimum

**Turn 1:** What is the maximum composed peak ground acceleration (pgaComposed) recorded at Schenkenberg?  
**Answer given in history:** The maximum is 1238.6 mg.  
**Recomputed:** `1238.6`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'pgaComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 6.28815 | 1238.6 | 0.9 | 498 | mg_acc |

**Question:** And the minimum?  
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

## F018 · and_the_minimum

**Turn 1:** What is the maximum voltage recorded at Ranverso?  
**Answer given in history:** The maximum is 4.428.  
**Recomputed:** `4.4280627`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.54323 | 4.42806 | 0.0010206 | 14793 | None |

**Question:** And the minimum?  
**Reference:** 0.001.  
**Recomputed:** `0.0010206` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.54323 | 4.42806 | 0.0010206 | 14793 | None |


---

## F019 · and_the_minimum

**Turn 1:** What is the maximum temperature recorded at Lucretili?  
**Answer given in history:** The maximum is 50 °C.  
**Recomputed:** `50.0`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |

**Question:** And the minimum?  
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

## F020 · and_the_minimum

**Turn 1:** What is the maximum rainfall recorded at Ranverso?  
**Answer given in history:** The maximum is 6.8.  
**Recomputed:** `6.8`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.0117536 | 6.8 | 0 | 2127 | None |

**Question:** And the minimum?  
**Reference:** 0.  
**Recomputed:** `0.0` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'rainfall' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.0117536 | 6.8 | 0 | 2127 | None |


---

## F021 · and_the_minimum

**Turn 1:** What is the maximum voltage recorded at Delos?  
**Answer given in history:** The maximum is 4.945.  
**Recomputed:** `4.944706`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.65592 | 4.94471 | -0.0016764 | 35822 | None |

**Question:** And the minimum?  
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

## F022 · and_the_minimum

**Turn 1:** What is the maximum temperature recorded at Delos?  
**Answer given in history:** The maximum is 54.2.  
**Recomputed:** `54.2`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |

**Question:** And the minimum?  
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

## F023 · when_recorded

**Turn 1:** What is the maximum voltage recorded at Baltanas?  
**Answer given in history:** The maximum is 3.722.  
**Recomputed:** `3.722426`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 0.934916 | 3.72243 | -0.0011721 | 167572 | None |

**Question:** When was it recorded?  
**Reference:** 2026-07-01 23:15 UTC.  
**Recomputed:** `2026-07-01 23:15 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'voltage' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 3.72243 | 2026-07-01 23:15:00 | 60bddba0-c94f-11f0-9e79-07375f067697 |
| 3.72242 | 2026-07-01 23:10:00 | 60bddba0-c94f-11f0-9e79-07375f067697 |
| 3.7224 | 2026-07-02 23:20:00 | 60bddba0-c94f-11f0-9e79-07375f067697 |
| 3.72239 | 2026-07-01 23:30:00 | 60bddba0-c94f-11f0-9e79-07375f067697 |
| 3.72231 | 2026-07-04 08:30:00 | 60bddba0-c94f-11f0-9e79-07375f067697 |


---

## F024 · when_recorded

**Turn 1:** What is the maximum temperature recorded at Baltanas?  
**Answer given in history:** The maximum is 44.6 °C.  
**Recomputed:** `44.6`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |

**Question:** When was it recorded?  
**Reference:** 2026-07-07 12:00 UTC.  
**Recomputed:** `2026-07-07 12:00 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 44.6 | 2026-07-07 12:00:00 | 82e0d400-784e-11f0-9283-e956b63ef652 |
| 44.3 | 2026-07-06 14:00:00 | 82e0d400-784e-11f0-9283-e956b63ef652 |
| 44.2 | 2026-07-05 14:00:00 | 82e0d400-784e-11f0-9283-e956b63ef652 |
| 44.1 | 2026-06-23 16:00:00 | 17063d10-7835-11f0-9283-e956b63ef652 |
| 44 | 2026-07-06 16:00:00 | 82e0d400-784e-11f0-9283-e956b63ef652 |


---

## F025 · when_recorded

**Turn 1:** What is the maximum soil temperature recorded at Baltanas?  
**Answer given in history:** The maximum is 38.51.  
**Recomputed:** `38.51`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'soil_temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 28.2156 | 38.51 | 18.7 | 50734 | None |

**Question:** When was it recorded?  
**Reference:** 2026-06-07 09:35 UTC.  
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

## F026 · when_recorded

**Turn 1:** What is the maximum composed RMS acceleration (rmsComposed) recorded at Schenkenberg?  
**Answer given in history:** The maximum is 777 mg.  
**Recomputed:** `777.0`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'rmsComposed' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 4.33386 | 777 | 0.3 | 502 | mg_acc |

**Question:** When was it recorded?  
**Reference:** 2026-05-22 09:33 UTC.  
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

## F027 · when_recorded

**Turn 1:** What is the maximum temperature recorded at Schenkenberg?  
**Answer given in history:** The maximum is 48.3 °C.  
**Recomputed:** `48.3`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |

**Question:** When was it recorded?  
**Reference:** 2026-06-28 12:00 UTC.  
**Recomputed:** `2026-06-28 12:00 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 48.3 | 2026-06-28 12:00:00 | be175380-1305-11f1-9e79-07375f067697 |
| 48.2 | 2026-06-27 13:30:00 | be175380-1305-11f1-9e79-07375f067697 |
| 48.2 | 2026-08-04 13:30:00 | be175380-1305-11f1-9e79-07375f067697 |
| 48 | 2026-06-27 13:00:00 | be175380-1305-11f1-9e79-07375f067697 |
| 48 | 2026-06-28 12:30:00 | be175380-1305-11f1-9e79-07375f067697 |


---

## F028 · when_recorded

**Turn 1:** What is the maximum temperature recorded at Lucretili?  
**Answer given in history:** The maximum is 50 °C.  
**Recomputed:** `50.0`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |

**Question:** When was it recorded?  
**Reference:** 2026-07-31 11:30 UTC.  
**Recomputed:** `2026-07-31 11:30 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 50 | 2026-07-31 11:30:00 | 8250dd80-8269-11f0-9283-e956b63ef652 |
| 50 | 2026-07-31 11:30:00 | 0cf22310-81be-11f0-9283-e956b63ef652 |
| 50 | 2026-07-31 11:30:00 | 82508f60-8269-11f0-b6dc-556f88243956 |
| 50 | 2026-08-01 11:30:00 | 0cf22310-81be-11f0-9283-e956b63ef652 |
| 50 | 2026-08-01 11:30:00 | 8250dd80-8269-11f0-9283-e956b63ef652 |

- The maximum occurs more than once; the reference uses the earliest.

---

## F029 · when_recorded

**Turn 1:** What is the maximum temperature recorded at Delos?  
**Answer given in history:** The maximum is 54.2.  
**Recomputed:** `54.2`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |

**Question:** When was it recorded?  
**Reference:** 2026-07-22 11:00 UTC.  
**Recomputed:** `2026-07-22 11:00 UTC` → **MATCH**

```sql
SELECT o.value, o.result_time, r.sensor_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL
ORDER BY o.value DESC, o.result_time ASC LIMIT 5;
```
| value | result_time | sensor_id |
|---|---|---|
| 54.2 | 2026-07-22 11:00:00 | ca7161c0-679d-11f0-8a4b-6bd692b5baa4 |
| 53.8 | 2026-07-04 13:00:00 | ca7161c0-679d-11f0-8a4b-6bd692b5baa4 |
| 53.8 | 2026-07-22 10:00:00 | ca7161c0-679d-11f0-8a4b-6bd692b5baa4 |
| 53.8 | 2026-07-22 12:00:00 | ca7161c0-679d-11f0-8a4b-6bd692b5baa4 |
| 53.6 | 2026-06-12 12:00:00 | ca7161c0-679d-11f0-8a4b-6bd692b5baa4 |


---

## F030 · when_recorded

**Turn 1:** What is the maximum potentiometer displacement recorded at Delos?  
**Answer given in history:** The maximum is 49.5.  
**Recomputed:** `49.50000644`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'potentiometer_displacement' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 22.6232 | 49.5 | 0.869739 | 4218 | None |

**Question:** When was it recorded?  
**Reference:** 2026-06-04 02:00 UTC.  
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

## F031 · when_recorded

**Turn 1:** What is the maximum voltage recorded at Ranverso?  
**Answer given in history:** The maximum is 4.428.  
**Recomputed:** `4.4280627`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'voltage' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 1.54323 | 4.42806 | 0.0010206 | 14793 | None |

**Question:** When was it recorded?  
**Reference:** 2026-06-03 01:00 UTC.  
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

## F032 · among_these

**Turn 1:** How many sensors have reported readings at Schenkenberg?  
**Answer given in history:** 12 sensors.  
**Recomputed:** `12`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'schenkenberg';
```
| sensors |
|---|
| 12 |

**Question:** Among these, how many measure composed RMS acceleration (rmsComposed)?  
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

## F033 · among_these

**Turn 1:** How many sensors have reported readings at Schenkenberg?  
**Answer given in history:** 12 sensors.  
**Recomputed:** `12`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'schenkenberg';
```
| sensors |
|---|
| 12 |

**Question:** Among these, how many measure composed peak ground acceleration (pgaComposed)?  
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

## F034 · among_these

**Turn 1:** How many sensors have reported readings at Delos?  
**Answer given in history:** 26 sensors.  
**Recomputed:** `26`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'delos';
```
| sensors |
|---|
| 26 |

**Question:** Among these, how many measure potentiometer displacement?  
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

## F035 · among_these

**Turn 1:** How many sensors have reported readings at Ranverso?  
**Answer given in history:** 13 sensors.  
**Recomputed:** `13`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'ranverso';
```
| sensors |
|---|
| 13 |

**Question:** Among these, how many measure rainfall?  
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

## F036 · among_these

**Turn 1:** How many sensors have reported readings at Baltanas?  
**Answer given in history:** 33 sensors.  
**Recomputed:** `33`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'baltanas';
```
| sensors |
|---|
| 33 |

**Question:** Among these, how many measure soil water potential?  
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

## F037 · among_these

**Turn 1:** How many sensors have reported readings at Lucretili?  
**Answer given in history:** 18 sensors.  
**Recomputed:** `18`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'lucretili';
```
| sensors |
|---|
| 18 |

**Question:** Among these, how many measure temperature?  
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

## F038 · among_these

**Turn 1:** How many sensors have reported readings at Schenkenberg?  
**Answer given in history:** 12 sensors.  
**Recomputed:** `12`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'schenkenberg';
```
| sensors |
|---|
| 12 |

**Question:** Among these, how many measure temperature?  
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

## F039 · among_these

**Turn 1:** How many sensors have reported readings at Delos?  
**Answer given in history:** 26 sensors.  
**Recomputed:** `26`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'delos';
```
| sensors |
|---|
| 26 |

**Question:** Among these, how many measure temperature?  
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

## F040 · among_these

**Turn 1:** How many sensors have reported readings at Ranverso?  
**Answer given in history:** 13 sensors.  
**Recomputed:** `13`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'ranverso';
```
| sensors |
|---|
| 13 |

**Question:** Among these, how many measure voltage?  
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

## F041 · among_these

**Turn 1:** How many sensors have reported readings at Delos?  
**Answer given in history:** 26 sensors.  
**Recomputed:** `26`

```sql
SELECT count(DISTINCT sensor_id) AS sensors FROM readings WHERE site_id = 'delos';
```
| sensors |
|---|
| 26 |

**Question:** Among these, how many measure voltage?  
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

## F042 · and_the_lowest

**Turn 1:** Which sensor node at Lucretili is at the highest altitude?  
**Answer given in history:** LS-177310 Crackmeter Montefalco, at 896.06 m.  
**Recomputed:** `LS-177310 Crackmeter Montefalco`

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

**Question:** And which one is the lowest?  
**Reference:** LS-177237 Pyranometer Villa Orazio, at 424.63 m.  
**Recomputed:** `LS-177237 Pyranometer Villa Orazio` → **MATCH**

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'lucretili' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt ASC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-177237 Pyranometer Villa Orazio | 42.0664 | 12.9011 | 424.63 |
| LS-174156 Crackmeter Villa Orazio | 42.0665 | 12.9013 | 425.63 |
| LS-177287 Crackmeter Villa Orazio | 42.0664 | 12.9013 | 426.1 |


---

## F043 · and_the_lowest

**Turn 1:** Which sensor node at Ranverso is at the highest altitude?  
**Answer given in history:** LS-170894, at 339.42 m.  
**Recomputed:** `LS-170894`

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

**Question:** And which one is the lowest?  
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

## F044 · and_the_lowest

**Turn 1:** Which sensor node at Baltanas is at the highest altitude?  
**Answer given in history:** AF4, at 798.42 m.  
**Recomputed:** `AF4`

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

**Question:** And which one is the lowest?  
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

## F045 · and_the_lowest

**Turn 1:** Which sensor node at Schenkenberg is at the highest altitude?  
**Answer given in history:** LS-152914, at 643.53 m.  
**Recomputed:** `LS-152914`

```sql
WITH n AS (SELECT DISTINCT n.node_id, n.label, n.latitude::float8 AS lat, n.longitude::float8 AS lon,
                  n.altitude::float8 AS alt
           FROM nodes n JOIN readings r USING (node_id)
           WHERE r.site_id = 'schenkenberg' AND n.latitude IS NOT NULL)
SELECT label, lat, lon, alt FROM n WHERE alt IS NOT NULL ORDER BY alt DESC LIMIT 3;
```
| label | lat | lon | alt |
|---|---|---|---|
| LS-152914 | 47.4421 | 8.10102 | 643.53 |
| LS-152555 | 47.4422 | 8.10108 | 643.52 |
| LS-152479 | 47.4421 | 8.10106 | 643.18 |

**Question:** And which one is the lowest?  
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

## F046 · and_the_lowest

**Turn 1:** Which sensor node at Delos is at the highest altitude?  
**Answer given in history:** LS-153242, at 43.48 m.  
**Recomputed:** `LS-153242`

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

**Question:** And which one is the lowest?  
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

## F047 · what_about_site_spatial

**Turn 1:** How far apart are the two most distant sensor nodes at Delos?  
**Answer given in history:** 1355.6 m, between H. Fournoi_wall attached 1 and LS-153157.  
**Recomputed:** `1355.6`

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

**Question:** What about at Baltanas?  
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

## F048 · what_about_site_spatial

**Turn 1:** How far apart are the two most distant sensor nodes at Schenkenberg?  
**Answer given in history:** 5.5 m, between LS-152555 and LS-175480.  
**Recomputed:** `5.5`

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

**Question:** What about at Delos?  
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

## F049 · what_about_site_spatial

**Turn 1:** How far apart are the two most distant sensor nodes at Schenkenberg?  
**Answer given in history:** 5.5 m, between LS-152555 and LS-175480.  
**Recomputed:** `5.5`

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

**Question:** What about at Lucretili?  
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

## F050 · what_about_site_spatial

**Turn 1:** How far apart are the two most distant sensor nodes at Baltanas?  
**Answer given in history:** 380.8 m, between Gases and GNSS_Base.  
**Recomputed:** `380.8`

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

**Question:** What about at Lucretili?  
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

## F051 · what_about_site_spatial

**Turn 1:** How far apart are the two most distant sensor nodes at Lucretili?  
**Answer given in history:** 8653.3 m, between LS-153061 - Tiltmeter Conventillo and LS-177310 Crackmeter Montefalco.  
**Recomputed:** `8653.3`

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

**Question:** What about at Ranverso?  
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

## F052 · what_about_site_spatial

**Turn 1:** How far apart are the two most distant sensor nodes at Baltanas?  
**Answer given in history:** 380.8 m, between Gases and GNSS_Base.  
**Recomputed:** `380.8`

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

**Question:** What about at Ranverso?  
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

## F053 · what_about_site_spatial

**Turn 1:** How far apart are the two most distant sensor nodes at Schenkenberg?  
**Answer given in history:** 5.5 m, between LS-152555 and LS-175480.  
**Recomputed:** `5.5`

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

**Question:** What about at Ranverso?  
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

## F054 · what_about_site_spatial

**Turn 1:** How far apart are the two most distant sensor nodes at Lucretili?  
**Answer given in history:** 8653.3 m, between LS-153061 - Tiltmeter Conventillo and LS-177310 Crackmeter Montefalco.  
**Recomputed:** `8653.3`

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

**Question:** What about at Schenkenberg?  
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

## F055 · next_day

**Turn 1:** What was the average temperature at Lucretili on 2026-06-09?  
**Answer given in history:** 21.503.  
**Recomputed:** `21.50324285371126`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-09' AND o.result_time < '2026-06-09'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 21.5032 | 39 | 8 | 4163 |

**Question:** And on the following day?  
**Reference:** 21.27.  
**Recomputed:** `21.26975961538461` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-10' AND o.result_time < '2026-06-10'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 21.2698 | 36 | 8 | 4160 |


---

## F056 · next_day

**Turn 1:** What was the average temperature at Baltanas on 2026-07-22?  
**Answer given in history:** 24.493.  
**Recomputed:** `24.49279902359643`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-22' AND o.result_time < '2026-07-22'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 24.4928 | 40.4 | 10 | 4916 |

**Question:** And on the following day?  
**Reference:** 24.908.  
**Recomputed:** `24.908150406504053` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-23' AND o.result_time < '2026-07-23'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 24.9082 | 39 | 10 | 4920 |


---

## F057 · next_day

**Turn 1:** What was the average temperature at Baltanas on 2026-08-04?  
**Answer given in history:** 23.591.  
**Recomputed:** `23.59085508168898`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-04' AND o.result_time < '2026-08-04'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 23.5909 | 34.7 | 10 | 4713 |

**Question:** And on the following day?  
**Reference:** 23.098.  
**Recomputed:** `23.097539244802746` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-05' AND o.result_time < '2026-08-05'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 23.0975 | 39.5 | 10 | 4714 |


---

## F058 · next_day

**Turn 1:** What was the average temperature at Schenkenberg on 2026-08-06?  
**Answer given in history:** 28.812.  
**Recomputed:** `28.812037037037044`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-06' AND o.result_time < '2026-08-06'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 28.812 | 43.5 | 21.3 | 108 |

**Question:** And on the following day?  
**Reference:** 28.817.  
**Recomputed:** `28.81652173913044` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-07' AND o.result_time < '2026-08-07'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 28.8165 | 43 | 17.9 | 115 |


---

## F059 · next_day

**Turn 1:** What was the average temperature at Baltanas on 2026-06-26?  
**Answer given in history:** 23.187.  
**Recomputed:** `23.187002437043077`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-26' AND o.result_time < '2026-06-26'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 23.187 | 37.3 | 9 | 4924 |

**Question:** And on the following day?  
**Reference:** 23.945.  
**Recomputed:** `23.944534577164884` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-27' AND o.result_time < '2026-06-27'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 23.9445 | 37.6 | 9 | 4931 |


---

## F060 · next_day

**Turn 1:** What was the average temperature at Schenkenberg on 2026-06-01?  
**Answer given in history:** 20.081.  
**Recomputed:** `20.081005586592163`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-01' AND o.result_time < '2026-06-01'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 20.081 | 36.7 | 14.4 | 537 |

**Question:** And on the following day?  
**Reference:** 17.686.  
**Recomputed:** `17.685934489402705` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-02' AND o.result_time < '2026-06-02'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 17.6859 | 33.2 | 12 | 519 |


---

## F061 · next_day

**Turn 1:** What was the average temperature at Ranverso on 2026-05-27?  
**Answer given in history:** 22.828.  
**Recomputed:** `22.827777777777783`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-27' AND o.result_time < '2026-05-27'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 22.8278 | 37 | 17 | 216 |

**Question:** And on the following day?  
**Reference:** 23.265.  
**Recomputed:** `23.26481481481482` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-05-28' AND o.result_time < '2026-05-28'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 23.2648 | 36 | 18 | 216 |


---

## F062 · next_day

**Turn 1:** What was the average temperature at Schenkenberg on 2026-06-19?  
**Answer given in history:** 29.542.  
**Recomputed:** `29.54239999999999`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-19' AND o.result_time < '2026-06-19'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 29.5424 | 46.8 | 19.4 | 125 |

**Question:** And on the following day?  
**Reference:** 30.13.  
**Recomputed:** `30.12962962962964` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-20' AND o.result_time < '2026-06-20'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 30.1296 | 43.3 | 18.1 | 135 |


---

## F063 · next_day

**Turn 1:** What was the average temperature at Ranverso on 2026-06-10?  
**Answer given in history:** 21.635.  
**Recomputed:** `21.634722222222223`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-10' AND o.result_time < '2026-06-10'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 21.6347 | 27 | 15 | 216 |

**Question:** And on the following day?  
**Reference:** 21.737.  
**Recomputed:** `21.73693693693694` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-06-11' AND o.result_time < '2026-06-11'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 21.7369 | 33 | 14 | 222 |


---

## F064 · next_day

**Turn 1:** What was the average temperature at Baltanas on 2026-07-06?  
**Answer given in history:** 26.049.  
**Recomputed:** `26.04888211382117`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-06' AND o.result_time < '2026-07-06'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 26.0489 | 44.3 | 10 | 4920 |

**Question:** And on the following day?  
**Reference:** 23.947.  
**Recomputed:** `23.946899776377283` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-07-07' AND o.result_time < '2026-07-07'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 23.9469 | 44.6 | 10 | 4919 |


---

## F065 · next_day

**Turn 1:** What was the average temperature at Baltanas on 2026-08-09?  
**Answer given in history:** 24.346.  
**Recomputed:** `24.345837746240207`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-09' AND o.result_time < '2026-08-09'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 24.3458 | 37.2 | 10 | 4721 |

**Question:** And on the following day?  
**Reference:** 23.981.  
**Recomputed:** `23.981120507399563` → **MATCH**

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL
  AND o.result_time >= '2026-08-10' AND o.result_time < '2026-08-10'::date + 1;
```
| avg | max | min | n |
|---|---|---|---|
| 23.9811 | 41.3 | 10 | 4730 |


---

## F066 · anomaly_other_date

**Turn 1:** Was the rainfall at Ranverso anomalous on 2026-05-23 according to its AD-RT rules?  
**Answer given in history:** No. R2_rain_7d: metric 1.6 vs threshold 20 (window ending 2026-05-23 23:00 UTC)  
**Recomputed:** `No`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-23 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 135 | 1.6 |

**Question:** What about on 2026-05-26?  
**Reference:** No. R2_rain_7d: metric 0 vs threshold 20 (window ending 2026-05-26 23:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-05-26 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 168 | 0 |

- as_of = 2026-05-26 23:59:59+00 (windows end at the latest matching reading at or before it)
- R2_rain_7d: metric 0 vs threshold 20 → does not fire
- Raw readings: [data/F066_R2_rain_7d.csv](data/F066_R2_rain_7d.csv) (168 rows)

---

## F067 · anomaly_other_date

**Turn 1:** Was the visitor count at Lucretili anomalous on 2026-06-06 according to its AD-RT rules?  
**Answer given in history:** No. R5_visitors: latest reading 0 at 2026-06-06 23:55 UTC vs threshold 3  
**Recomputed:** `No`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors';
```
| threshold_value | threshold_json |
|---|---|
| 3 | {"R5_visitors_peak": 3} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-06 23:59:59+00')
SELECT r.sensor_id, o.property_id, o.result_time, o.value AS metric FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL
  AND o.result_time = anchor.t ORDER BY metric DESC;
```
| sensor_id | property_id | result_time | metric |
|---|---|---|---|
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | pulse_counter | 2026-06-06 23:55:00 | 0 |

**Question:** What about on 2026-06-09?  
**Reference:** No. R5_visitors: latest reading 0 at 2026-06-09 23:55 UTC vs threshold 3  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors';
```
| threshold_value | threshold_json |
|---|---|
| 3 | {"R5_visitors_peak": 3} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-09 23:59:59+00')
SELECT r.sensor_id, o.property_id, o.result_time, o.value AS metric FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL
  AND o.result_time = anchor.t ORDER BY metric DESC;
```
| sensor_id | property_id | result_time | metric |
|---|---|---|---|
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | pulse_counter | 2026-06-09 23:55:00 | 0 |

- as_of = 2026-06-09 23:59:59+00 (windows end at the latest matching reading at or before it)
- R5_visitors: metric 0 vs threshold 3 → does not fire
- Raw readings: [data/F067_R5_visitors.csv](data/F067_R5_visitors.csv) (1 rows)

---

## F068 · anomaly_other_date

**Turn 1:** Was the temperature at Lucretili anomalous on 2026-06-13 according to its AD-RT rules?  
**Answer given in history:** Yes. R9a_temp_lt: metric 28 vs threshold 20 (window ending 2026-06-13 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-06-13 23:55 UTC)  
**Recomputed:** `Yes`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-13 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 7 | 35 | 28 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 13 | 40 | 27 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 46 | 14 | 36 | 22 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 14 | 36 | 22 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 46 | 14 | 36 | 22 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 46 | 14 | 36 | 22 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 14 | 36 | 22 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 14 | 36 | 22 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 17.9 | 39.5 | 21.6 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 276 | 15 | 36 | 21 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 289 | 14.9 | 35.5 | 20.6 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 288 | 14 | 31 | 17 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 288 | 14 | 31 | 17 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 288 | 14 | 30 | 16 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 289 | 17 | 31 | 14 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 289 | 21 | 34.1 | 13.1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 289 | 17 | 25 | 8 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 289 | 16.3 | 23.1 | 6.8 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-13 23:59:59+00')
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
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.3 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 0 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

**Question:** What about on 2026-06-21?  
**Reference:** Yes. R9a_temp_lt: metric 27 vs threshold 20 (window ending 2026-06-21 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-06-21 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-21 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 13 | 40 | 27 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 41 | 20 | 44 | 24 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 41 | 20 | 44 | 24 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 41 | 20 | 44 | 24 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 19 | 42 | 23 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 245 | 20 | 41 | 21 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 24.3 | 45.1 | 20.8 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 18 | 38 | 20 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 18 | 38 | 20 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 18 | 38 | 20 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 289 | 21.1 | 40.5 | 19.4 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 285 | 21 | 37 | 16 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 285 | 21 | 37 | 16 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 287 | 21 | 36 | 15 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 288 | 24 | 37 | 13 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 289 | 27.3 | 39.4 | 12.1 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 275 | 21.8 | 28.2 | 6.4 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 289 | 24 | 30 | 6 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-21 23:59:59+00')
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
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 1 |
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
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.3 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-06-21 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 27 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/F068_R9a_temp_lt.csv](data/F068_R9a_temp_lt.csv) (4124 rows)
- Raw readings: [data/F068_R9b_temp_st.csv](data/F068_R9b_temp_st.csv) (189 rows)

---

## F069 · anomaly_other_date

**Turn 1:** Was the temperature at Lucretili anomalous on 2026-06-25 according to its AD-RT rules?  
**Answer given in history:** Yes. R9a_temp_lt: metric 27 vs threshold 20 (window ending 2026-06-25 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-06-25 23:55 UTC)  
**Recomputed:** `Yes`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-25 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 12 | 39 | 27 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 45 | 19 | 41 | 22 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 45 | 19 | 41 | 22 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 45 | 19 | 41 | 22 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 22 | 22.5 | 43.5 | 21 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 288 | 19.1 | 39 | 19.9 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 274 | 19 | 38 | 19 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 16 | 33 | 17 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 289 | 19 | 35 | 16 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 289 | 19 | 35 | 16 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 16 | 31 | 15 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 16 | 31 | 15 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 16 | 31 | 15 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 289 | 19 | 34 | 15 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 289 | 22 | 35 | 13 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 288 | 25.2 | 36.7 | 11.5 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 288 | 22 | 28 | 6 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 284 | 20 | 25.3 | 5.3 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-25 23:59:59+00')
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
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.2 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.2 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 0 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 0 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

**Question:** What about on 2026-06-30?  
**Reference:** Yes. R9a_temp_lt: metric 27 vs threshold 20 (window ending 2026-06-30 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-06-30 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-30 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 13 | 40 | 27 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 34 | 18 | 43 | 25 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 34 | 18 | 43 | 25 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 34 | 18 | 43 | 25 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 23 | 23.1 | 41.8 | 18.7 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 289 | 20.1 | 38.3 | 18.2 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 34 | 17 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 288 | 19 | 35 | 16 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 33 | 16 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 33 | 16 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 33 | 16 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 276 | 20 | 36 | 16 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 276 | 20 | 36 | 16 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 135 | 18 | 31 | 13 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 287 | 24 | 36 | 12 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 288 | 26.5 | 37.8 | 11.3 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 287 | 23 | 29 | 6 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 265 | 21.6 | 27.2 | 5.6 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-06-30 23:59:59+00')
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
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.4 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.3 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 13 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-06-30 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 27 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/F069_R9a_temp_lt.csv](data/F069_R9a_temp_lt.csv) (3961 rows)
- Raw readings: [data/F069_R9b_temp_st.csv](data/F069_R9b_temp_st.csv) (189 rows)

---

## F070 · anomaly_other_date

**Turn 1:** Was the temperature at Lucretili anomalous on 2026-07-06 according to its AD-RT rules?  
**Answer given in history:** Yes. R9a_temp_lt: metric 25 vs threshold 20 (window ending 2026-07-06 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-07-06 23:55 UTC)  
**Recomputed:** `Yes`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-06 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 288 | 12 | 37 | 25 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 42 | 25 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 31 | 17 | 40 | 23 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 31 | 17 | 40 | 23 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 31 | 17 | 40 | 23 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 21 | 41 | 20 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 288 | 17.7 | 37.6 | 19.9 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 35 | 18 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 35 | 18 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 66 | 18 | 36 | 18 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 17 | 35 | 18 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 258 | 18 | 33 | 15 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 258 | 18 | 33 | 15 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 286 | 18 | 31 | 13 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 286 | 21 | 33 | 12 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 288 | 23.9 | 34.9 | 11 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 280 | 20 | 26 | 6 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 254 | 19.1 | 24.2 | 5.1 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-06 23:59:59+00')
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
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 5 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 13 | 1 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 13 | 1 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 13 | 1 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.4 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.3 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.1 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 2 | 0 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 0 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

**Question:** What about on 2026-07-14?  
**Reference:** Yes. R9a_temp_lt: metric 25 vs threshold 20 (window ending 2026-07-14 23:55 UTC); R9b_temp_st: max 1h change 1 vs threshold 5 (ending 2026-07-14 23:55 UTC)  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9a_temp_lt';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R9a_temp_lt": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-14 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, min(o.value), max(o.value), max(o.value) - min(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '24 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | min | max | metric |
|---|---|---|---|---|---|
| 9eefebd0-8191-11f0-9283-e956b63ef652 | temperature | 289 | 14 | 39 | 25 |
| 7c201440-8196-11f0-9a67-6d25b7d467e7 | temperature | 289 | 20 | 43 | 23 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 24 | 23.8 | 43.9 | 20.1 |
| 8250dd80-8269-11f0-9283-e956b63ef652 | temperature | 31 | 21 | 41 | 20 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 31 | 21 | 41 | 20 |
| 82508f60-8269-11f0-b6dc-556f88243956 | temperature | 31 | 21 | 41 | 20 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 289 | 20.6 | 39.8 | 19.2 |
| 5716e3f0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 19 | 38 | 19 |
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 19 | 38 | 19 |
| 5711b3d0-819a-11f0-9a67-6d25b7d467e7 | temperature | 289 | 19 | 38 | 19 |
| c0d43040-c86c-11f0-8080-e5362df2da58 | temperature | 187 | 22 | 38 | 16 |
| b52772f0-8327-11f0-9283-e956b63ef652 | temperature | 287 | 20 | 35 | 15 |
| 6d408f60-d103-11f0-9e79-07375f067697 | temperature | 283 | 21 | 36 | 15 |
| 6d46d0f0-d103-11f0-8484-ad77d9ec8692 | temperature | 283 | 21 | 36 | 15 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 288 | 23 | 36 | 13 |
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 287 | 26.5 | 39.3 | 12.8 |
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 288 | 23 | 30 | 7 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 275 | 21.6 | 27.8 | 6.2 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R9b_temp_st';
```
| threshold_value | threshold_json |
|---|---|
| 5 | {"R9b_temp_st": 5} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%temp%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-14 23:59:59+00')
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
| b8184060-831e-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 277491c0-833d-11f0-9283-e956b63ef652 | temperature | 13 | 1 |
| 0cf22310-81be-11f0-9283-e956b63ef652 | temperature | 2 | 1 |
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
| 0866de30-8335-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| 37c9dd80-833f-11f0-9283-e956b63ef652 | temperature | 13 | 0.3 |
| f3058610-83ff-11f0-9a67-6d25b7d467e7 | temperature | 13 | 0.2 |
| 8533f470-5c02-11f0-8a4b-6bd692b5baa4 | temperature | 1 | None |

- as_of = 2026-07-14 23:59:59+00 (windows end at the latest matching reading at or before it)
- R9a_temp_lt: metric 25 vs threshold 20 → fires
- R9b_temp_st: metric 1 vs threshold 5 → does not fire
- Raw readings: [data/F070_R9a_temp_lt.csv](data/F070_R9a_temp_lt.csv) (4029 rows)
- Raw readings: [data/F070_R9b_temp_st.csv](data/F070_R9b_temp_st.csv) (189 rows)

---

## F071 · anomaly_other_date

**Turn 1:** Was the rainfall at Ranverso anomalous on 2026-07-10 according to its AD-RT rules?  
**Answer given in history:** No. R2_rain_7d: metric 0 vs threshold 20 (window ending 2026-07-10 23:00 UTC)  
**Recomputed:** `No`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-10 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 169 | 0 |

**Question:** What about on 2026-07-16?  
**Reference:** No. R2_rain_7d: metric 8.2 vs threshold 20 (window ending 2026-07-16 23:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-16 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 169 | 8.2 |

- as_of = 2026-07-16 23:59:59+00 (windows end at the latest matching reading at or before it)
- R2_rain_7d: metric 8.2 vs threshold 20 → does not fire
- Raw readings: [data/F071_R2_rain_7d.csv](data/F071_R2_rain_7d.csv) (169 rows)

---

## F072 · anomaly_other_date

**Turn 1:** Was the rainfall at Ranverso anomalous on 2026-07-15 according to its AD-RT rules?  
**Answer given in history:** No. R2_rain_7d: metric 7.4 vs threshold 20 (window ending 2026-07-15 23:00 UTC)  
**Recomputed:** `No`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-15 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 169 | 7.4 |

**Question:** What about on 2026-07-22?  
**Reference:** No. R2_rain_7d: metric 1.6 vs threshold 20 (window ending 2026-07-22 23:00 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'ranverso' AND rule_id = 'R2_rain_7d';
```
| threshold_value | threshold_json |
|---|---|
| 20 | {"R2_rain_7d_diff": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-22 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'ranverso' AND lower(o.property_id) LIKE '%rain%' AND lower(o.property_id) NOT LIKE '%acc%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 9173cac0-8e53-11f0-9283-e956b63ef652 | rainfall | 168 | 1.6 |

- as_of = 2026-07-22 23:59:59+00 (windows end at the latest matching reading at or before it)
- R2_rain_7d: metric 1.6 vs threshold 20 → does not fire
- Raw readings: [data/F072_R2_rain_7d.csv](data/F072_R2_rain_7d.csv) (168 rows)

---

## F073 · anomaly_other_date

**Turn 1:** Was the vibration at Schenkenberg anomalous on 2026-07-23 according to its AD-RT rules?  
**Answer given in history:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-07-23 23:59:59+00'),
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
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 879 | 0.301251 | 0.0417019 | 0.2 | 2026-07-23 23:30:00 | 2.42798 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 1658 | 0.1 | 1.63114e-15 | 0.1 | 2026-07-23 23:30:00 | 1.89729 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 1658 | 0.1 | 1.63114e-15 | 0.1 | 2026-07-23 23:30:00 | 1.89729 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 1658 | 0.1 | 1.63114e-15 | 0.1 | 2026-07-23 23:30:00 | 1.89729 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 879 | 0.1 | 5.98255e-16 | 0.1 | 2026-07-23 23:30:00 | 1.36863 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 879 | 0.1 | 5.98255e-16 | 0.1 | 2026-07-23 23:30:00 | 1.36863 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 879 | 0.1 | 5.98255e-16 | 0.1 | 2026-07-23 23:30:00 | 1.36863 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 2634 | 0.1 | 2.56311e-15 | 0.1 | 2026-07-23 23:30:00 | 1.2778 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 2634 | 0.1 | 2.56311e-15 | 0.1 | 2026-07-23 23:30:00 | 1.2778 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2634 | 0.431359 | 0.0724077 | 0.5 | 2026-07-23 23:30:00 | 0.947977 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1658 | 0.43456 | 0.078472 | 0.4 | 2026-07-23 23:30:00 | 0.440408 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2634 | 0.312756 | 0.0387317 | 0.3 | 2026-07-23 23:30:00 | 0.329349 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2634 | 0.312225 | 0.0390002 | 0.3 | 2026-07-23 23:30:00 | 0.313453 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1658 | 0.309288 | 0.0482314 | 0.3 | 2026-07-23 23:30:00 | 0.192578 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-23 23:59:59+00'),
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
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 879 | 0.301251 | 0.0417019 | 0.2 | 2026-07-23 23:30:00 | 2.42798 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2634 | 0.431359 | 0.0724077 | 0.5 | 2026-07-23 23:30:00 | 0.947977 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1658 | 0.43456 | 0.078472 | 0.4 | 2026-07-23 23:30:00 | 0.440408 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2634 | 0.312756 | 0.0387317 | 0.3 | 2026-07-23 23:30:00 | 0.329349 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2634 | 0.312225 | 0.0390002 | 0.3 | 2026-07-23 23:30:00 | 0.313453 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1658 | 0.309288 | 0.0482314 | 0.3 | 2026-07-23 23:30:00 | 0.192578 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 879 | 0.409443 | 0.0519432 | 0.4 | 2026-07-23 23:30:00 | 0.181786 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 1658 | 0.307901 | 0.0503695 | 0.3 | 2026-07-23 23:30:00 | 0.156862 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 879 | 0.303185 | 0.0406304 | 0.3 | 2026-07-23 23:30:00 | 0.0784003 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

**Question:** What about on 2026-07-27?  
**Reference:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-07-27 23:59:59+00'),
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
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1757 | 0.308139 | 0.0476757 | 0.2 | 2026-07-27 23:30:00 | 2.26822 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 990 | 0.407677 | 0.0504691 | 0.3 | 2026-07-27 23:30:00 | 2.13352 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 990 | 0.1 | 6.77406e-16 | 0.1 | 2026-07-27 23:30:00 | 2.02818 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 990 | 0.1 | 6.77406e-16 | 0.1 | 2026-07-27 23:30:00 | 2.02818 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 990 | 0.1 | 6.77406e-16 | 0.1 | 2026-07-27 23:30:00 | 2.02818 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 1757 | 0.1 | 1.75501e-15 | 0.1 | 2026-07-27 23:30:00 | 1.85036 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 1757 | 0.1 | 1.75501e-15 | 0.1 | 2026-07-27 23:30:00 | 1.85036 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 1757 | 0.1 | 1.75501e-15 | 0.1 | 2026-07-27 23:30:00 | 1.85036 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 2826 | 0.1 | 2.55349e-15 | 0.1 | 2026-07-27 23:30:00 | 0.592397 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 2826 | 0.1 | 2.55349e-15 | 0.1 | 2026-07-27 23:30:00 | 0.592397 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1757 | 0.433182 | 0.0767715 | 0.4 | 2026-07-27 23:30:00 | 0.432212 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2826 | 0.429689 | 0.0704829 | 0.4 | 2026-07-27 23:30:00 | 0.421217 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2826 | 0.31189 | 0.0375304 | 0.3 | 2026-07-27 23:30:00 | 0.316799 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2826 | 0.311323 | 0.0378923 | 0.3 | 2026-07-27 23:30:00 | 0.298832 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-27 23:59:59+00'),
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
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1757 | 0.308139 | 0.0476757 | 0.2 | 2026-07-27 23:30:00 | 2.26822 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 990 | 0.407677 | 0.0504691 | 0.3 | 2026-07-27 23:30:00 | 2.13352 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1757 | 0.433182 | 0.0767715 | 0.4 | 2026-07-27 23:30:00 | 0.432212 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2826 | 0.429689 | 0.0704829 | 0.4 | 2026-07-27 23:30:00 | 0.421217 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2826 | 0.31189 | 0.0375304 | 0.3 | 2026-07-27 23:30:00 | 0.316799 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2826 | 0.311323 | 0.0378923 | 0.3 | 2026-07-27 23:30:00 | 0.298832 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 1757 | 0.306488 | 0.050077 | 0.3 | 2026-07-27 23:30:00 | 0.129567 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 990 | 0.301616 | 0.0399168 | 0.3 | 2026-07-27 23:30:00 | 0.0404883 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 990 | 0.300202 | 0.0404515 | 0.3 | 2026-07-27 23:30:00 | 0.00499414 |

- as_of = 2026-07-27 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 7.42346 vs threshold 4.5 → fires
- R4_pga: metric 7.42346 vs threshold 0.5 → fires
- Raw readings: [data/F073_R3_vib_zscore.csv](data/F073_R3_vib_zscore.csv) (41529 rows)
- Raw readings: [data/F073_R4_pga.csv](data/F073_R4_pga.csv) (21512 rows)

---

## F074 · anomaly_other_date

**Turn 1:** Was the vibration at Schenkenberg anomalous on 2026-07-23 according to its AD-RT rules?  
**Answer given in history:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-07-23 23:59:59+00'),
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
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 879 | 0.301251 | 0.0417019 | 0.2 | 2026-07-23 23:30:00 | 2.42798 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 1658 | 0.1 | 1.63114e-15 | 0.1 | 2026-07-23 23:30:00 | 1.89729 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 1658 | 0.1 | 1.63114e-15 | 0.1 | 2026-07-23 23:30:00 | 1.89729 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 1658 | 0.1 | 1.63114e-15 | 0.1 | 2026-07-23 23:30:00 | 1.89729 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 879 | 0.1 | 5.98255e-16 | 0.1 | 2026-07-23 23:30:00 | 1.36863 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 879 | 0.1 | 5.98255e-16 | 0.1 | 2026-07-23 23:30:00 | 1.36863 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 879 | 0.1 | 5.98255e-16 | 0.1 | 2026-07-23 23:30:00 | 1.36863 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 2634 | 0.1 | 2.56311e-15 | 0.1 | 2026-07-23 23:30:00 | 1.2778 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 2634 | 0.1 | 2.56311e-15 | 0.1 | 2026-07-23 23:30:00 | 1.2778 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2634 | 0.431359 | 0.0724077 | 0.5 | 2026-07-23 23:30:00 | 0.947977 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1658 | 0.43456 | 0.078472 | 0.4 | 2026-07-23 23:30:00 | 0.440408 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2634 | 0.312756 | 0.0387317 | 0.3 | 2026-07-23 23:30:00 | 0.329349 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2634 | 0.312225 | 0.0390002 | 0.3 | 2026-07-23 23:30:00 | 0.313453 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1658 | 0.309288 | 0.0482314 | 0.3 | 2026-07-23 23:30:00 | 0.192578 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-23 23:59:59+00'),
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
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 879 | 0.301251 | 0.0417019 | 0.2 | 2026-07-23 23:30:00 | 2.42798 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2634 | 0.431359 | 0.0724077 | 0.5 | 2026-07-23 23:30:00 | 0.947977 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1658 | 0.43456 | 0.078472 | 0.4 | 2026-07-23 23:30:00 | 0.440408 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2634 | 0.312756 | 0.0387317 | 0.3 | 2026-07-23 23:30:00 | 0.329349 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2634 | 0.312225 | 0.0390002 | 0.3 | 2026-07-23 23:30:00 | 0.313453 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1658 | 0.309288 | 0.0482314 | 0.3 | 2026-07-23 23:30:00 | 0.192578 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 879 | 0.409443 | 0.0519432 | 0.4 | 2026-07-23 23:30:00 | 0.181786 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 1658 | 0.307901 | 0.0503695 | 0.3 | 2026-07-23 23:30:00 | 0.156862 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 879 | 0.303185 | 0.0406304 | 0.3 | 2026-07-23 23:30:00 | 0.0784003 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |

**Question:** What about on 2026-07-30?  
**Reference:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-07-30 23:59:59+00'),
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
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2969 | 0.311216 | 0.0368721 | 0.2 | 2026-07-30 23:30:00 | 3.01626 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 1061 | 0.1 | 7.63694e-16 | 0.1 | 2026-07-30 22:30:00 | 2.16246 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 1061 | 0.1 | 7.63694e-16 | 0.1 | 2026-07-30 22:30:00 | 2.16246 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 1061 | 0.1 | 7.63694e-16 | 0.1 | 2026-07-30 22:30:00 | 2.16246 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 1830 | 0.1 | 1.84156e-15 | 0.1 | 2026-07-30 22:30:00 | 1.81615 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 1830 | 0.1 | 1.84156e-15 | 0.1 | 2026-07-30 22:30:00 | 1.81615 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 1830 | 0.1 | 1.84156e-15 | 0.1 | 2026-07-30 22:30:00 | 1.81615 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1830 | 0.432295 | 0.0761124 | 0.4 | 2026-07-30 22:30:00 | 0.424308 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2969 | 0.429101 | 0.0705216 | 0.4 | 2026-07-30 23:30:00 | 0.41265 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2969 | 0.310677 | 0.0372132 | 0.3 | 2026-07-30 23:30:00 | 0.286914 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1830 | 0.307486 | 0.0472607 | 0.3 | 2026-07-30 22:30:00 | 0.158405 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1061 | 0.406786 | 0.0496087 | 0.4 | 2026-07-30 22:30:00 | 0.136792 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 2969 | 0.1 | 2.50027e-15 | 0.1 | 2026-07-30 23:30:00 | 0.133212 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 2969 | 0.1 | 2.50027e-15 | 0.1 | 2026-07-30 23:30:00 | 0.133212 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-30 23:59:59+00'),
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
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 2969 | 0.311216 | 0.0368721 | 0.2 | 2026-07-30 23:30:00 | 3.01626 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1830 | 0.432295 | 0.0761124 | 0.4 | 2026-07-30 22:30:00 | 0.424308 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 2969 | 0.429101 | 0.0705216 | 0.4 | 2026-07-30 23:30:00 | 0.41265 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 2969 | 0.310677 | 0.0372132 | 0.3 | 2026-07-30 23:30:00 | 0.286914 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1830 | 0.307486 | 0.0472607 | 0.3 | 2026-07-30 22:30:00 | 0.158405 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1061 | 0.406786 | 0.0496087 | 0.4 | 2026-07-30 22:30:00 | 0.136792 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 1830 | 0.306066 | 0.0492716 | 0.3 | 2026-07-30 22:30:00 | 0.123105 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 1061 | 0.301508 | 0.0385602 | 0.3 | 2026-07-30 22:30:00 | 0.039108 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 1061 | 0.299906 | 0.0394351 | 0.3 | 2026-07-30 22:30:00 | 0.00239002 |

- as_of = 2026-07-30 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 7.42346 vs threshold 4.5 → fires
- R4_pga: metric 7.42346 vs threshold 0.5 → fires
- Raw readings: [data/F074_R3_vib_zscore.csv](data/F074_R3_vib_zscore.csv) (43251 rows)
- Raw readings: [data/F074_R4_pga.csv](data/F074_R4_pga.csv) (22373 rows)

---

## F075 · anomaly_other_date

**Turn 1:** Was the rainfall at Lucretili anomalous on 2026-07-22 according to its AD-RT rules?  
**Answer given in history:** No. R6a_rain: metric 0 vs threshold 20 (window ending 2026-07-22 23:30 UTC); R6b_rain_cum7d: metric 0 vs threshold 100 (window ending 2026-07-22 23:30 UTC)  
**Recomputed:** `No`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6a_rain';
```
| threshold_value | threshold_json |
|---|---|
| None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-22 23:59:59+00')
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
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 42 | 0 | 0 | 0 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6b_rain_cum7d';
```
| threshold_value | threshold_json |
|---|---|
| 100 | {"R6b_rain_cum7d": 100} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-22 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 226 | 0 |

**Question:** What about on 2026-07-31?  
**Reference:** No. R6a_rain: metric 0 vs threshold 20 (window ending 2026-07-31 23:30 UTC); R6b_rain_cum7d: metric 0 vs threshold 100 (window ending 2026-07-31 23:30 UTC)  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6a_rain';
```
| threshold_value | threshold_json |
|---|---|
| None | {"R6a_rain_1h": 5, "R6a_rain_24h": 20} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-31 23:59:59+00')
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
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 47 | 0 | 0 | 0 |

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R6b_rain_cum7d';
```
| threshold_value | threshold_json |
|---|---|
| 100 | {"R6b_rain_cum7d": 100} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL AND o.result_time <= '2026-07-31 23:59:59+00')
SELECT r.sensor_id, o.property_id, count(*) AS n, sum(o.value) AS metric
FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%rain%' AND o.value IS NOT NULL
  AND o.result_time BETWEEN anchor.t - interval '168 hours' AND anchor.t
GROUP BY 1, 2 ORDER BY metric DESC;
```
| sensor_id | property_id | n | metric |
|---|---|---|---|
| 8250dd80-8269-11f0-9283-e956b63ef652 | rainfall | 249 | 0 |

- as_of = 2026-07-31 23:59:59+00 (windows end at the latest matching reading at or before it)
- R6a_rain: metric 0 vs threshold 20 → does not fire
- R6b_rain_cum7d: metric 0 vs threshold 100 → does not fire
- Raw readings: [data/F075_R6a_rain.csv](data/F075_R6a_rain.csv) (47 rows)
- Raw readings: [data/F075_R6b_rain_cum7d.csv](data/F075_R6b_rain_cum7d.csv) (249 rows)

---

## F076 · anomaly_other_date

**Turn 1:** Was the visitor count at Lucretili anomalous on 2026-08-02 according to its AD-RT rules?  
**Answer given in history:** No. R5_visitors: latest reading 0 at 2026-08-02 23:55 UTC vs threshold 3  
**Recomputed:** `No`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors';
```
| threshold_value | threshold_json |
|---|---|
| 3 | {"R5_visitors_peak": 3} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-02 23:59:59+00')
SELECT r.sensor_id, o.property_id, o.result_time, o.value AS metric FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL
  AND o.result_time = anchor.t ORDER BY metric DESC;
```
| sensor_id | property_id | result_time | metric |
|---|---|---|---|
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | pulse_counter | 2026-08-02 23:55:00 | 0 |

**Question:** What about on 2026-08-07?  
**Reference:** No. R5_visitors: latest reading 0 at 2026-08-07 23:55 UTC vs threshold 3  
**Recomputed:** `No` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'lucretili' AND rule_id = 'R5_visitors';
```
| threshold_value | threshold_json |
|---|---|
| 3 | {"R5_visitors_peak": 3} |

```sql
WITH anchor AS (SELECT max(o.result_time) AS t FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-07 23:59:59+00')
SELECT r.sensor_id, o.property_id, o.result_time, o.value AS metric FROM anchor, observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'lucretili' AND lower(o.property_id) LIKE '%counter%' AND o.value IS NOT NULL
  AND o.result_time = anchor.t ORDER BY metric DESC;
```
| sensor_id | property_id | result_time | metric |
|---|---|---|---|
| 56fa0d20-819a-11f0-9a67-6d25b7d467e7 | pulse_counter | 2026-08-07 23:55:00 | 0 |

- as_of = 2026-08-07 23:59:59+00 (windows end at the latest matching reading at or before it)
- R5_visitors: metric 0 vs threshold 3 → does not fire
- Raw readings: [data/F076_R5_visitors.csv](data/F076_R5_visitors.csv) (1 rows)

---

## F077 · anomaly_other_date

**Turn 1:** Was the vibration at Schenkenberg anomalous on 2026-08-04 according to its AD-RT rules?  
**Answer given in history:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes`

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-08-04 23:59:59+00'),
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
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 1179 | 0.1 | 9.35909e-16 | 0.1 | 2026-08-04 10:00:00 | 2.20939 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 1179 | 0.1 | 9.35909e-16 | 0.1 | 2026-08-04 10:00:00 | 2.20939 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 1179 | 0.1 | 9.35909e-16 | 0.1 | 2026-08-04 10:00:00 | 2.20939 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 1957 | 0.1 | 1.98304e-15 | 0.1 | 2026-08-04 13:30:00 | 1.76355 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 1957 | 0.1 | 1.98304e-15 | 0.1 | 2026-08-04 13:30:00 | 1.76355 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 1957 | 0.1 | 1.98304e-15 | 0.1 | 2026-08-04 13:30:00 | 1.76355 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 3196 | 0.1 | 2.41686e-15 | 0.1 | 2026-08-04 23:30:00 | 0.539756 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 3196 | 0.1 | 2.41686e-15 | 0.1 | 2026-08-04 23:30:00 | 0.539756 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1957 | 0.430353 | 0.0740708 | 0.4 | 2026-08-04 13:30:00 | 0.409778 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 3196 | 0.427785 | 0.0694893 | 0.4 | 2026-08-04 23:30:00 | 0.399842 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 3196 | 0.310388 | 0.0357081 | 0.3 | 2026-08-04 23:30:00 | 0.290914 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 3196 | 0.30995 | 0.0360936 | 0.3 | 2026-08-04 23:30:00 | 0.27567 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1957 | 0.30649 | 0.0463683 | 0.3 | 2026-08-04 13:30:00 | 0.139956 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1179 | 0.406107 | 0.0474635 | 0.4 | 2026-08-04 10:00:00 | 0.128665 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-04 23:59:59+00'),
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
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 1957 | 0.430353 | 0.0740708 | 0.4 | 2026-08-04 13:30:00 | 0.409778 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 3196 | 0.427785 | 0.0694893 | 0.4 | 2026-08-04 23:30:00 | 0.399842 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 3196 | 0.310388 | 0.0357081 | 0.3 | 2026-08-04 23:30:00 | 0.290914 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 3196 | 0.30995 | 0.0360936 | 0.3 | 2026-08-04 23:30:00 | 0.27567 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 1957 | 0.30649 | 0.0463683 | 0.3 | 2026-08-04 13:30:00 | 0.139956 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1179 | 0.406107 | 0.0474635 | 0.4 | 2026-08-04 10:00:00 | 0.128665 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 1957 | 0.305365 | 0.0480252 | 0.3 | 2026-08-04 13:30:00 | 0.11172 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 1179 | 0.301018 | 0.0370541 | 0.3 | 2026-08-04 10:00:00 | 0.0274682 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 1179 | 0.299152 | 0.0384071 | 0.3 | 2026-08-04 10:00:00 | 0.0220838 |

**Question:** What about on 2026-08-11?  
**Reference:** Yes. R3_vib_zscore: max z-score 7.423 vs threshold 4.5; R4_pga: max z-score 7.423 vs threshold 0.5  
**Recomputed:** `Yes` → **MATCH**

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R3_vib_zscore';
```
| threshold_value | threshold_json |
|---|---|
| 4.5 | {"R3_vib_zscore": 4.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND (lower(o.property_id) LIKE '%pga%' OR lower(o.property_id) LIKE '%rms%') AND o.value IS NOT NULL AND o.result_time <= '2026-08-11 23:59:59+00'),
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
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsZAxis | 1297 | 0.1 | 1.11812e-15 | 0.1 | 2026-08-11 23:30:00 | 2.13481 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsYAxis | 1297 | 0.1 | 1.11812e-15 | 0.1 | 2026-08-11 23:30:00 | 2.13481 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | rmsXAxis | 1297 | 0.1 | 1.11812e-15 | 0.1 | 2026-08-11 23:30:00 | 2.13481 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsXAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsZAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | rmsYAxis | 932 | 0.1 | 6.255e-16 | 0.1 | 2026-07-14 00:00:00 | 1.75275 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsXAxis | 2076 | 0.1 | 2.10585e-15 | 0.1 | 2026-08-11 23:30:00 | 1.72002 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsYAxis | 2076 | 0.1 | 2.10585e-15 | 0.1 | 2026-08-11 23:30:00 | 1.72002 |
| 69755440-5b34-11f1-9208-83a949003bcf | rmsZAxis | 2076 | 0.1 | 2.10585e-15 | 0.1 | 2026-08-11 23:30:00 | 1.72002 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsYAxis | 3521 | 0.1 | 2.41459e-15 | 0.1 | 2026-08-11 23:30:00 | 1.3564 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | rmsXAxis | 3521 | 0.1 | 2.41459e-15 | 0.1 | 2026-08-11 23:30:00 | 1.3564 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaZAxis | 932 | 0.428863 | 0.110469 | 0.5 | 2026-07-14 00:00:00 | 0.643957 |
| e1a16c90-5a8c-11f1-9808-31317bce3c36 | pgaYAxis | 932 | 0.332511 | 0.0637266 | 0.3 | 2026-07-14 00:00:00 | 0.51016 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 2076 | 0.428757 | 0.0723711 | 0.4 | 2026-08-11 23:30:00 | 0.397358 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 3521 | 0.425845 | 0.0669201 | 0.4 | 2026-08-11 23:30:00 | 0.386206 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 3521 | 0.309429 | 0.0342359 | 0.3 | 2026-08-11 23:30:00 | 0.275417 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 3521 | 0.309003 | 0.0346386 | 0.3 | 2026-08-11 23:30:00 | 0.259916 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 2076 | 0.305539 | 0.0457558 | 0.3 | 2026-08-11 23:30:00 | 0.121067 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1297 | 0.405012 | 0.0459411 | 0.4 | 2026-08-11 23:30:00 | 0.109087 |

_… 9 more rows_

```sql
SELECT threshold_value, threshold_json FROM policies WHERE site_id = 'schenkenberg' AND rule_id = 'R4_pga';
```
| threshold_value | threshold_json |
|---|---|
| 0.5 | {"R4_pga": 0.5} |

```sql
WITH s AS (SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o JOIN readings r USING (reading_id) WHERE r.site_id = 'schenkenberg' AND lower(o.property_id) LIKE '%pga%' AND o.value IS NOT NULL AND o.result_time <= '2026-08-11 23:59:59+00'),
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
| 69755440-5b34-11f1-9208-83a949003bcf | pgaZAxis | 2076 | 0.428757 | 0.0723711 | 0.4 | 2026-08-11 23:30:00 | 0.397358 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaZAxis | 3521 | 0.425845 | 0.0669201 | 0.4 | 2026-08-11 23:30:00 | 0.386206 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaXAxis | 3521 | 0.309429 | 0.0342359 | 0.3 | 2026-08-11 23:30:00 | 0.275417 |
| 84d47f00-5a9d-11f1-9208-83a949003bcf | pgaYAxis | 3521 | 0.309003 | 0.0346386 | 0.3 | 2026-08-11 23:30:00 | 0.259916 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaYAxis | 2076 | 0.305539 | 0.0457558 | 0.3 | 2026-08-11 23:30:00 | 0.121067 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaZAxis | 1297 | 0.405012 | 0.0459411 | 0.4 | 2026-08-11 23:30:00 | 0.109087 |
| 69755440-5b34-11f1-9208-83a949003bcf | pgaXAxis | 2076 | 0.304576 | 0.0472078 | 0.3 | 2026-08-11 23:30:00 | 0.0969354 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaZAxis | 499 | 6.52806 | 63.9154 | 1.1 | 2026-05-28 11:30:00 | 0.0849256 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaXAxis | 500 | 11.8846 | 132.814 | 0.7 | 2026-05-28 11:30:00 | 0.0842123 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaYAxis | 500 | 7.176 | 80.1803 | 0.7 | 2026-05-28 11:30:00 | 0.080768 |
| 3dff8100-55c1-11f1-9208-83a949003bcf | pgaComposed | 498 | 6.28815 | 69.375 | 1.1 | 2026-05-28 11:30:00 | 0.0747842 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaXAxis | 1297 | 0.298843 | 0.0371318 | 0.3 | 2026-08-11 23:30:00 | 0.0311462 |
| 47a10ff0-5e48-11f1-9808-31317bce3c36 | pgaYAxis | 1297 | 0.300694 | 0.0356607 | 0.3 | 2026-08-11 23:30:00 | 0.0194587 |

- as_of = 2026-08-11 23:59:59+00 (windows end at the latest matching reading at or before it)
- R3_vib_zscore: metric 7.42346 vs threshold 4.5 → fires
- R4_pga: metric 7.42346 vs threshold 0.5 → fires
- Raw readings: [data/F077_R3_vib_zscore.csv](data/F077_R3_vib_zscore.csv) (49455 rows)
- Raw readings: [data/F077_R4_pga.csv](data/F077_R4_pga.csv) (25475 rows)

---

## F078 · next_month

**Turn 1:** How many readings were recorded at Lucretili in May 2026?  
**Answer given in history:** 60353 readings.  
**Recomputed:** `60353`

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili'
  AND result_time >= '2026-05-01' AND result_time < '2026-05-01'::date + interval '1 month';
```
| readings |
|---|
| 60353 |

**Question:** And in the following month?  
**Reference:** 198983 readings.  
**Recomputed:** `198983` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili'
  AND result_time >= '2026-06-01' AND result_time < '2026-06-01'::date + interval '1 month';
```
| readings |
|---|
| 198983 |


---

## F079 · next_month

**Turn 1:** How many readings were recorded at Delos in July 2026?  
**Answer given in history:** 40130 readings.  
**Recomputed:** `40130`

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'delos'
  AND result_time >= '2026-07-01' AND result_time < '2026-07-01'::date + interval '1 month';
```
| readings |
|---|
| 40130 |

**Question:** And in the following month?  
**Reference:** 14501 readings.  
**Recomputed:** `14501` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'delos'
  AND result_time >= '2026-08-01' AND result_time < '2026-08-01'::date + interval '1 month';
```
| readings |
|---|
| 14501 |


---

## F080 · next_month

**Turn 1:** How many readings were recorded at Delos in May 2026?  
**Answer given in history:** 20715 readings.  
**Recomputed:** `20715`

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'delos'
  AND result_time >= '2026-05-01' AND result_time < '2026-05-01'::date + interval '1 month';
```
| readings |
|---|
| 20715 |

**Question:** And in the following month?  
**Reference:** 38443 readings.  
**Recomputed:** `38443` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'delos'
  AND result_time >= '2026-06-01' AND result_time < '2026-06-01'::date + interval '1 month';
```
| readings |
|---|
| 38443 |


---

## F081 · next_month

**Turn 1:** How many readings were recorded at Lucretili in July 2026?  
**Answer given in history:** 199288 readings.  
**Recomputed:** `199288`

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili'
  AND result_time >= '2026-07-01' AND result_time < '2026-07-01'::date + interval '1 month';
```
| readings |
|---|
| 199288 |

**Question:** And in the following month?  
**Reference:** 67447 readings.  
**Recomputed:** `67447` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili'
  AND result_time >= '2026-08-01' AND result_time < '2026-08-01'::date + interval '1 month';
```
| readings |
|---|
| 67447 |


---

## F082 · next_month

**Turn 1:** How many readings were recorded at Baltanas in July 2026?  
**Answer given in history:** 220893 readings.  
**Recomputed:** `220893`

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'baltanas'
  AND result_time >= '2026-07-01' AND result_time < '2026-07-01'::date + interval '1 month';
```
| readings |
|---|
| 220893 |

**Question:** And in the following month?  
**Reference:** 77492 readings.  
**Recomputed:** `77492` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'baltanas'
  AND result_time >= '2026-08-01' AND result_time < '2026-08-01'::date + interval '1 month';
```
| readings |
|---|
| 77492 |


---

## F083 · next_month

**Turn 1:** How many readings were recorded at Delos in June 2026?  
**Answer given in history:** 38443 readings.  
**Recomputed:** `38443`

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'delos'
  AND result_time >= '2026-06-01' AND result_time < '2026-06-01'::date + interval '1 month';
```
| readings |
|---|
| 38443 |

**Question:** And in the following month?  
**Reference:** 40130 readings.  
**Recomputed:** `40130` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'delos'
  AND result_time >= '2026-07-01' AND result_time < '2026-07-01'::date + interval '1 month';
```
| readings |
|---|
| 40130 |


---

## F084 · next_month

**Turn 1:** How many readings were recorded at Lucretili in June 2026?  
**Answer given in history:** 198983 readings.  
**Recomputed:** `198983`

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili'
  AND result_time >= '2026-06-01' AND result_time < '2026-06-01'::date + interval '1 month';
```
| readings |
|---|
| 198983 |

**Question:** And in the following month?  
**Reference:** 199288 readings.  
**Recomputed:** `199288` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'lucretili'
  AND result_time >= '2026-07-01' AND result_time < '2026-07-01'::date + interval '1 month';
```
| readings |
|---|
| 199288 |


---

## F085 · next_month

**Turn 1:** How many readings were recorded at Baltanas in May 2026?  
**Answer given in history:** 141404 readings.  
**Recomputed:** `141404`

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'baltanas'
  AND result_time >= '2026-05-01' AND result_time < '2026-05-01'::date + interval '1 month';
```
| readings |
|---|
| 141404 |

**Question:** And in the following month?  
**Reference:** 236483 readings.  
**Recomputed:** `236483` → **MATCH**

```sql
SELECT count(*) AS readings FROM readings WHERE site_id = 'baltanas'
  AND result_time >= '2026-06-01' AND result_time < '2026-06-01'::date + interval '1 month';
```
| readings |
|---|
| 236483 |


---

## F086 · two_turn

**Turn 1:** What is the average temperature at Lucretili?  
**Answer given in history:** 23.639 °C.  
**Recomputed:** `23.638578549545585`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |

**Turn 2:** What about Baltanas?  
**Answer given in history:** 21.722 °C.  
**Recomputed:** `21.721905265213742`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |

**Question:** And the maximum there?  
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

## F087 · two_turn

**Turn 1:** What is the average temperature at Delos?  
**Answer given in history:** 26.087.  
**Recomputed:** `26.08703019975385`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |

**Turn 2:** What about Ranverso?  
**Answer given in history:** 24.209 °C.  
**Recomputed:** `24.208592263792024`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Question:** And the maximum there?  
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

## F088 · two_turn

**Turn 1:** What is the average temperature at Delos?  
**Answer given in history:** 26.087.  
**Recomputed:** `26.08703019975385`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |

**Turn 2:** What about Schenkenberg?  
**Answer given in history:** 23.672 °C.  
**Recomputed:** `23.672202985963786`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |

**Question:** And the maximum there?  
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

## F089 · two_turn

**Turn 1:** What is the average temperature at Baltanas?  
**Answer given in history:** 21.722 °C.  
**Recomputed:** `21.721905265213774`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |

**Turn 2:** What about Ranverso?  
**Answer given in history:** 24.209 °C.  
**Recomputed:** `24.208592263792017`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Question:** And the maximum there?  
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

## F090 · two_turn

**Turn 1:** What is the average temperature at Schenkenberg?  
**Answer given in history:** 23.672 °C.  
**Recomputed:** `23.672202985963782`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |

**Turn 2:** What about Ranverso?  
**Answer given in history:** 24.209 °C.  
**Recomputed:** `24.20859226379202`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Question:** And the maximum there?  
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

## F091 · two_turn

**Turn 1:** What is the average temperature at Ranverso?  
**Answer given in history:** 24.209 °C.  
**Recomputed:** `24.20859226379203`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Turn 2:** What about Lucretili?  
**Answer given in history:** 23.639 °C.  
**Recomputed:** `23.638578549545574`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |

**Question:** And the maximum there?  
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

## F092 · two_turn

**Turn 1:** What is the average temperature at Lucretili?  
**Answer given in history:** 23.639 °C.  
**Recomputed:** `23.63857854954565`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |

**Turn 2:** What about Ranverso?  
**Answer given in history:** 24.209 °C.  
**Recomputed:** `24.208592263792024`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Question:** And the maximum there?  
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

## F093 · two_turn

**Turn 1:** What is the average temperature at Schenkenberg?  
**Answer given in history:** 23.672 °C.  
**Recomputed:** `23.672202985963793`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |

**Turn 2:** What about Baltanas?  
**Answer given in history:** 21.722 °C.  
**Recomputed:** `21.721905265213746`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |

**Question:** And the maximum there?  
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

## F094 · two_turn

**Turn 1:** What is the average temperature at Ranverso?  
**Answer given in history:** 24.209 °C.  
**Recomputed:** `24.208592263792017`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Turn 2:** What about Delos?  
**Answer given in history:** 26.087.  
**Recomputed:** `26.08703019975385`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |

**Question:** And the maximum there?  
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

## F095 · two_turn

**Turn 1:** What is the average temperature at Ranverso?  
**Answer given in history:** 24.209 °C.  
**Recomputed:** `24.208592263792024`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'ranverso' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 24.2086 | 40 | 2 | 18924 | Cel |

**Turn 2:** What about Schenkenberg?  
**Answer given in history:** 23.672 °C.  
**Recomputed:** `23.672202985963793`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |

**Question:** And the maximum there?  
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

## F096 · two_turn

**Turn 1:** What is the average temperature at Lucretili?  
**Answer given in history:** 23.639 °C.  
**Recomputed:** `23.6385785495456`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |

**Turn 2:** What about Schenkenberg?  
**Answer given in history:** 23.672 °C.  
**Recomputed:** `23.672202985963786`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'schenkenberg' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6722 | 48.3 | 9.2 | 26859 | Cel |

**Question:** And the maximum there?  
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

## F097 · two_turn

**Turn 1:** What is the average temperature at Delos?  
**Answer given in history:** 26.087.  
**Recomputed:** `26.08703019975386`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |

**Turn 2:** What about Baltanas?  
**Answer given in history:** 21.722 °C.  
**Recomputed:** `21.721905265213763`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |

**Question:** And the maximum there?  
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

## F098 · unanswerable

**Turn 1:** What is the average temperature at Baltanas?  
**Answer given in history:** 21.722 °C.  
**Recomputed:** `21.721905265213753`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 21.7219 | 44.6 | -0.6 | 435215 | Cel |

**Question:** And the relative humidity?  
**Reference:** Cannot be answered: no humidity data at Baltanas.  
**Recomputed:** `None` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'baltanas' AND (lower(o.property_id) LIKE '%hum%');
```
_(no rows)_

- Expected: no rows (no relative humidity data at baltanas). Got 0 row(s).

---

## F099 · unanswerable

**Turn 1:** What is the average temperature at Lucretili?  
**Answer given in history:** 23.639 °C.  
**Recomputed:** `23.638578549545564`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 23.6386 | 50 | 0 | 318576 | Cel |

**Question:** And the relative humidity?  
**Reference:** Cannot be answered: no humidity data at Lucretili.  
**Recomputed:** `None` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'lucretili' AND (lower(o.property_id) LIKE '%hum%');
```
_(no rows)_

- Expected: no rows (no relative humidity data at lucretili). Got 0 row(s).

---

## F100 · unanswerable

**Turn 1:** What is the average temperature at Delos?  
**Answer given in history:** 26.087.  
**Recomputed:** `26.08703019975385`

```sql
SELECT avg(o.value) AS avg, max(o.value) AS max, min(o.value) AS min, count(*) AS n, max(o.unit) AS unit
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.property_id = 'temperature' AND o.value IS NOT NULL;
```
| avg | max | min | n | unit |
|---|---|---|---|---|
| 26.087 | 54.2 | 11.5 | 21126 | None |

**Question:** And the relative humidity?  
**Reference:** Cannot be answered: no humidity data at Delos.  
**Recomputed:** `None` → **MATCH**

```sql
SELECT DISTINCT o.property_id FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND (lower(o.property_id) LIKE '%hum%');
```
_(no rows)_

- Expected: no rows (no relative humidity data at delos). Got 0 row(s).

---
