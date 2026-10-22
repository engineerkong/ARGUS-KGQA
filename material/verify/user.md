# Verification — user questions

80 questions from ask_events.jsonl (real questions routed to the knowledge graph, and two sensor-data questions the router had sent to fallback), answered on the snapshot. COMPUTED: the reference is the SQL result shown. MANUAL: a long list or a question that needs interpretation — the reference is computed, its scoring is judged by hand.

Dropped: 25 (too vague to have one answer ("sensor values that may need attention")); 27 (not about the KG (how sensors are used in heritage preservation)); 29 (not about the KG (greeting / general knowledge about Delos)); 37 (not about the KG (general knowledge about Delos and the project)); 44 (too vague ("locations associated with Delos instruments")); 48 (not about the KG (about the system's architecture)); 99 (an Interactive-KBQA demo (Baltanas 1-hour rainfall threshold), excluded as in the benchmark).

Exact duplicates merged (question → kept copy): 49→4, 50→31, 51→33, 52→42, 53→35, 55→36, 63→21, 65→35, 66→33, 67→36, 68→56, 69→57, 70→58, 71→59, 72→60, 73→61, 74→62, 75→64.

In psql, run `SET TIME ZONE 'UTC';` first.

---

## U001 · per_site

**Question:** How many sensors are deployed per site?  
**Reference:** Baltanas 33; Delos 26; Lucretili 18; Ranverso 13; Schenkenberg 12.  
**Must state:** [33, 26, 18, 13, 12]  
**Scoring:** all → **COMPUTED**

```sql
SELECT r.site_id, count(DISTINCT r.sensor_id) FROM readings r WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1 ORDER BY 1;
```

---

## U002 · total

**Question:** How many readings are available in total?  
**Reference:** 1,674,205 readings in the knowledge graph (1,393,686 at the five pilot sites).  
**Must state:** [1674205, 1393686]  
**Scoring:** any → **COMPUTED**

```sql
SELECT count(*) FROM readings;

SELECT count(*) FROM readings WHERE site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']);
```

---

## U003 · latest_site

**Question:** what are the most recent readings in delos?  
**Reference:** Latest readings at Delos: 2026-08-12 09:00 UTC — H. Fournoi_pole mounted_outdoors thermistor 8495.726; H. Fournoi_pole mounted_outdoors thermistor_ysi44005 28.708; H. Fournoi_pole mounted_outdoors voltage 0.555; H. Fournoi_pole mounted_outdoors voltage 2.559; H. Fournoi_pole mounted_outdoors voltage 3.327; H. Fournoi_pole mounted_outdoors voltage_1 166.526; H. Fournoi_pole mounted_outdoors voltage_1 66.536; H. Fournoi_pole mounted_outdoors voltage_polynomial_4 14.794; H. Fournoi_wall attached 1 temperature 29; H. Fournoi_wall attached 1 voltage 0.71; H. Fournoi_wall attached 1 voltage_1 76.355; H. Masks_Dolphins mosaic_pole mounted thermistor 8711.498 … and 66 more.  
**Must state:** ['2026-08-12 09:00']  
**Scoring:** all → **COMPUTED**

```sql
SELECT max(o.result_time) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE o.value IS NOT NULL AND r.site_id = 'delos';

SELECT n.label, se.label, o.property_id, o.value FROM observations o
JOIN readings r USING (reading_id) JOIN nodes n USING (node_id) JOIN sensors se USING (sensor_id)
WHERE o.value IS NOT NULL AND r.site_id = 'delos' AND o.result_time = '2026-08-12T09:00:00+00:00' ORDER BY 1, 3;
```

---

## U004 · per_site

**Question:** How many readings are available per site?  
**Reference:** Baltanas 676,272; Delos 113,789; Lucretili 526,071; Ranverso 50,695; Schenkenberg 26,859.  
**Must state:** [676272, 113789, 526071, 50695, 26859]  
**Scoring:** all → **COMPUTED**

```sql
SELECT r.site_id, count(*) FROM readings r WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1 ORDER BY 1;
```

---

## U005 · argmax_site

**Question:** Which site has the most readings?  
**Reference:** Baltanas (676,272 readings).  
**Must state:** ['Baltanas']  
**Scoring:** all → **COMPUTED**

```sql
SELECT r.site_id, count(*) FROM readings r WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1 ORDER BY 1;
```

---

## U006 · per_site_avg

**Question:** What is the average voltage per site?  
**Reference:** Baltanas 0.935; Delos 1.656; Lucretili 0.142; Ranverso 1.543; Schenkenberg 0.026.  
**Must state:** [0.935, 1.656, 0.142, 1.543, 0.026]  
**Scoring:** all → **COMPUTED**

```sql
SELECT r.site_id, avg(o.value) FROM observations o JOIN readings r USING (reading_id)
WHERE o.property_id = 'voltage' AND o.value IS NOT NULL AND r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg'])
GROUP BY 1 ORDER BY 1;
```

---

## U007 · verdict

**Question:** Check Baltanas vibration PPV anomaly using the AD-RT vibration policy.  
**Reference:** Cannot be determined. R1_ppv: no readings in the snapshot  
**Must state:** ['Cannot be determined']  
**Scoring:** verdict → **COMPUTED**

```sql
-- AD-RT rule evaluation (build_benchmark.RuleEngine) at Baltanas, rules ['R1_ppv'], latest data (windows ending 2026-08-12 09:15 UTC); see verify/anomaly.md for the rule SQL
```

---

## U008 · latest_overall

**Question:** What are the latest 20 readings?  
**Reference:** The latest 20 readings run from 2026-08-12 09:15 to 2026-08-12 09:15 UTC, at Baltanas, Lucretili.  
**Must state:** ['2026-08-12 09:15']  
**Scoring:** all → **COMPUTED** (readings with observations (the KG's latest data); the list is in the SQL result)

```sql
SELECT r.result_time, r.site_id, n.label FROM readings r JOIN nodes n USING (node_id)
WHERE EXISTS (SELECT 1 FROM observations o WHERE o.reading_id = r.reading_id)
ORDER BY r.result_time DESC LIMIT 20;
```

---

## U009 · threats

**Question:** What are the risks for Delos Island based on Argus Database?  
**Reference:** 52 threats (risk scenarios) concern Delos: ABC risk scenario: delos-fournoi.air-pollution.site v1; ABC risk scenario: delos-fournoi.architectural-stability.site v1; ABC risk scenario: delos-fournoi.flooding.site v1; ABC risk scenario: delos-fournoi.freeze-thaw-cycles.site v1; ABC risk scenario: delos-fournoi.gravitational-slope-movements.site v1; ABC risk scenario: delos-fournoi.heatwaves.site v1; ABC risk scenario: delos-fournoi.high-temperature.site v1; ABC risk scenario: delos-fournoi.low-temperature.site v1; ABC risk scenario: delos-fournoi.prolonged-dry-periods.site v1; ABC risk scenario: delos-fournoi.rainfall.site v1; ABC risk scenario: delos-fournoi.rh-fluctuations.site v1; ABC risk scenario: delos-fournoi.salinity.site v1; ABC risk scenario: delos-fournoi.seismic.site v1; ABC risk scenario: delos-fournoi.soil-erosion.site v1; ABC risk scenario: delos-fournoi.storm.site v1; ABC risk scenario: delos-fournoi.subsidence.site v1; ABC risk scenario: delos-fournoi.water-rise.site v1; ABC risk scenario: delos-fournoi.wind-erosion.site v1; ABC risk scenario: delos-masks.air-pollution.site v1; ABC risk scenario: delos-masks.architectural-stability.site v1; ABC risk scenario: delos-masks.flooding.site v1; ABC risk scenario: delos-masks.freeze-thaw-cycles.site v1; ABC risk scenario: delos-masks.gravitational-slope-movements.site v1; ABC risk scenario: delos-masks.heatwaves.site v1; ABC risk scenario: delos-masks.high-temperature.site v1; ABC risk scenario: delos-masks.low-temperature.site v1; ABC risk scenario: delos-masks.prolonged-dry-periods.site v1; ABC risk scenario: delos-masks.rainfall.site v1; ABC risk scenario: delos-masks.rh-fluctuations.site v1; ABC risk scenario: delos-masks.salinity.site v1; ABC risk scenario: delos-masks.seismic.site v1; ABC risk scenario: delos-masks.soil-erosion.site v1; ABC risk scenario: delos-masks.storm.site v1; ABC risk scenario: delos-masks.subsidence.site v1; ABC risk scenario: delos-masks.water-rise.site v1; ABC risk scenario: delos-masks.wind-erosion.site v1; IRA fusion policy: delos-fournoi.flooding.site v1; IRA fusion policy: delos-fournoi.rainfall.site v1; IRA fusion policy: delos-fournoi.rh-fluctuations.site v1; IRA fusion policy: delos-fournoi.seismic.site v1; IRA fusion policy: delos-fournoi.soil-erosion.site v1; IRA fusion policy: delos-fournoi.storm.site v1; IRA fusion policy: delos-fournoi.water-rise.site v1; IRA fusion policy: delos-fournoi.wind-erosion.site v1; IRA fusion policy: delos-masks.flooding.site v1; IRA fusion policy: delos-masks.rainfall.site v1; IRA fusion policy: delos-masks.rh-fluctuations.site v1; IRA fusion policy: delos-masks.seismic.site v1; IRA fusion policy: delos-masks.soil-erosion.site v1; IRA fusion policy: delos-masks.storm.site v1; IRA fusion policy: delos-masks.water-rise.site v1; IRA fusion policy: delos-masks.wind-erosion.site v1.  
**Must state:** ['ABC risk scenario: delos-fournoi.air-pollution.site v1', 'ABC risk scenario: delos-fournoi.architectural-stability.site v1', 'ABC risk scenario: delos-fournoi.flooding.site v1', 'ABC risk scenario: delos-fournoi.freeze-thaw-cycles.site v1', 'ABC risk scenario: delos-fournoi.gravitational-slope-movements.site v1', 'ABC risk scenario: delos-fournoi.heatwaves.site v1', 'ABC risk scenario: delos-fournoi.high-temperature.site v1', 'ABC risk scenario: delos-fournoi.low-temperature.site v1', 'ABC risk scenario: delos-fournoi.prolonged-dry-periods.site v1', 'ABC risk scenario: delos-fournoi.rainfall.site v1', 'ABC risk scenario: delos-fournoi.rh-fluctuations.site v1', 'ABC risk scenario: delos-fournoi.salinity.site v1', 'ABC risk scenario: delos-fournoi.seismic.site v1', 'ABC risk scenario: delos-fournoi.soil-erosion.site v1', 'ABC risk scenario: delos-fournoi.storm.site v1', 'ABC risk scenario: delos-fournoi.subsidence.site v1', 'ABC risk scenario: delos-fournoi.water-rise.site v1', 'ABC risk scenario: delos-fournoi.wind-erosion.site v1', 'ABC risk scenario: delos-masks.air-pollution.site v1', 'ABC risk scenario: delos-masks.architectural-stability.site v1', 'ABC risk scenario: delos-masks.flooding.site v1', 'ABC risk scenario: delos-masks.freeze-thaw-cycles.site v1', 'ABC risk scenario: delos-masks.gravitational-slope-movements.site v1', 'ABC risk scenario: delos-masks.heatwaves.site v1', 'ABC risk scenario: delos-masks.high-temperature.site v1', 'ABC risk scenario: delos-masks.low-temperature.site v1', 'ABC risk scenario: delos-masks.prolonged-dry-periods.site v1', 'ABC risk scenario: delos-masks.rainfall.site v1', 'ABC risk scenario: delos-masks.rh-fluctuations.site v1', 'ABC risk scenario: delos-masks.salinity.site v1', 'ABC risk scenario: delos-masks.seismic.site v1', 'ABC risk scenario: delos-masks.soil-erosion.site v1', 'ABC risk scenario: delos-masks.storm.site v1', 'ABC risk scenario: delos-masks.subsidence.site v1', 'ABC risk scenario: delos-masks.water-rise.site v1', 'ABC risk scenario: delos-masks.wind-erosion.site v1', 'IRA fusion policy: delos-fournoi.flooding.site v1', 'IRA fusion policy: delos-fournoi.rainfall.site v1', 'IRA fusion policy: delos-fournoi.rh-fluctuations.site v1', 'IRA fusion policy: delos-fournoi.seismic.site v1', 'IRA fusion policy: delos-fournoi.soil-erosion.site v1', 'IRA fusion policy: delos-fournoi.storm.site v1', 'IRA fusion policy: delos-fournoi.water-rise.site v1', 'IRA fusion policy: delos-fournoi.wind-erosion.site v1', 'IRA fusion policy: delos-masks.flooding.site v1', 'IRA fusion policy: delos-masks.rainfall.site v1', 'IRA fusion policy: delos-masks.rh-fluctuations.site v1', 'IRA fusion policy: delos-masks.seismic.site v1', 'IRA fusion policy: delos-masks.soil-erosion.site v1', 'IRA fusion policy: delos-masks.storm.site v1', 'IRA fusion policy: delos-masks.water-rise.site v1', 'IRA fusion policy: delos-masks.wind-erosion.site v1']  
**Scoring:** manual → **MANUAL** (52 risk scenarios: judged by hand)

```sql
SELECT label FROM threats WHERE label ILIKE '%delos%' ORDER BY 1;
```

---

## U010 · nodes_per_site

**Question:** Which nodes are available per site?  
**Reference:** Baltanas (13): Acc-2A, Acc-3A, AF1, AF2, AF3, AF4, Gases, GNSS_Base, GNSS-Rover, P_WL, sensor, WP1, WP2; Delos (15): H. Fournoi_pole mounted_outdoors, H. Fournoi_wall attached 1, H. Masks_Dolphins mosaic_pole mounted, H. Masks_Dyonisios mosaic_pole mounted, H. Masks_Dyonisios &panter mosaic_flow meter, H. Masks_Dyonisios &panter mosaic_pole mounted 2, H. Masks_Mask mosaic_pole mounted, H. Masks_Mask mosaic_pole mounted 2, H. Masks_Mask mosaic_window, H. Masks_Masks mosaic_flow meter, LS-150900, LS-153157, LS-153242, LS-153295, Outdoors area H. Masks_Mask_pole mounted; Lucretili (13): LS-152608 - Tiltmeter Conventillo, LS-152816 Tiltmeter Conventillo, LS-152931 Tiltemeter Conventillo, LS-153061 - Tiltmeter Conventillo, LS-174156 Crackmeter Villa Orazio, LS-177237 Pyranometer Villa Orazio, LS-177239 - Humidity sensor Conventillo, LS-177253 Crackmeter Conventillo, LS-177266 - Crackmeter Conventillo, LS-177281 Humidity-Temperature Montefalco, LS-177287 Crackmeter Villa Orazio, LS-177310 Crackmeter Montefalco, LS-177320 CrackMeter Conventillo; Ranverso (7): LS-143276, LS-149248, LS-149361, LS-168442, LS-170894, LS-174188, LS-177315; Schenkenberg (7): LS-149796, LS-152479, LS-152555, LS-152899, LS-152914, LS-159070, LS-175480.  
**Must state:** [13, 15, 13, 7, 7]  
**Scoring:** manual → **MANUAL** (58 node names: judged by hand (must lists the node count per site))

```sql
SELECT r.site_id, count(DISTINCT n.node_id), string_agg(DISTINCT n.label, ', ')
FROM nodes n JOIN readings r USING (node_id) WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1 ORDER BY 1;
```

---

## U011 · verdict

**Question:** Check Baltanas soil moisture anomaly using the soil moisture policy.  
**Reference:** Cannot be determined. R4a_soil_high: no readings in the snapshot; R4b_soil_range: no readings in the snapshot  
**Must state:** ['Cannot be determined']  
**Scoring:** verdict → **COMPUTED**

```sql
-- AD-RT rule evaluation (build_benchmark.RuleEngine) at Baltanas, rules ['R4a_soil_high', 'R4b_soil_range'], latest data (windows ending 2026-08-12 09:15 UTC); see verify/anomaly.md for the rule SQL
```

---

## U012 · latest_site

**Question:** whats the situation in Temperature in the House of Masks  
**Reference:** Latest temperature at the House of Masks: 2026-08-12 09:00 UTC — H. Masks_Dyonisios &panter mosaic_flow meter temperature 25; H. Masks_Mask mosaic_pole mounted temperature 25; H. Masks_Mask mosaic_window temperature 26; H. Masks_Masks mosaic_flow meter temperature 25; Outdoors area H. Masks_Mask_pole mounted temperature 27.  
**Must state:** ['2026-08-12 09:00']  
**Scoring:** all → **COMPUTED**

```sql
SELECT max(o.result_time) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE o.value IS NOT NULL AND r.site_id = 'delos' AND o.property_id = 'temperature' AND (n.label ILIKE 'H. Masks%' OR n.label ILIKE '%H. Masks_Mask%');

SELECT n.label, se.label, o.property_id, o.value FROM observations o
JOIN readings r USING (reading_id) JOIN nodes n USING (node_id) JOIN sensors se USING (sensor_id)
WHERE o.value IS NOT NULL AND r.site_id = 'delos' AND o.property_id = 'temperature' AND (n.label ILIKE 'H. Masks%' OR n.label ILIKE '%H. Masks_Mask%') AND o.result_time = '2026-08-12T09:00:00+00:00' ORDER BY 1, 3;
```

---

## U013 · count_sensors_q

**Question:** How many temperature sensors do we have installed in The House Masks in Delos?  
**Reference:** 5 sensors measure temperature at the House of Masks.  
**Must state:** [5]  
**Scoring:** all → **COMPUTED**

```sql
SELECT count(DISTINCT r.sensor_id) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE TRUE AND r.site_id = 'delos' AND o.property_id = 'temperature' AND (n.label ILIKE 'H. Masks%' OR n.label ILIKE '%H. Masks_Mask%');
```

---

## U014 · count_sensors_q

**Question:** How many of those installed sensors in Delos are for temperature?  
**Earlier turn:** How many temperature sensors do we have installed in The House Masks in Delos?  
**Reference:** 10 sensors measure temperature at Delos.  
**Must state:** [10]  
**Scoring:** all → **COMPUTED**

```sql
SELECT count(DISTINCT r.sensor_id) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE TRUE AND r.site_id = 'delos' AND o.property_id = 'temperature';
```

---

## U015 · per_quantity

**Question:** How many readings are available per observed quantity?  
**Reference:** 89 quantities; the most frequent: temperature 820,700; voltage 404,917; voltage_1 222,104; thermistor 196,017; pulse_counter 157,460; voltage_polynomial_4 145,760; axis_y_std 77,126; axis_z 77,126; axis_z_std 77,126; axis_x_std 77,126 … (full list in the SQL result).  
**Must state:** ['temperature', 'voltage', 'voltage_1']  
**Scoring:** manual → **MANUAL** (89 quantities: judged by hand)

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1 ORDER BY 2 DESC;
```

---

## U016 · latest_site

**Question:** Give me the last temperature measurements for Delos Island.  
**Reference:** Latest temperature at Delos: 2026-08-12 09:00 UTC — H. Fournoi_wall attached 1 temperature 29; H. Masks_Dyonisios &panter mosaic_flow meter temperature 25; H. Masks_Mask mosaic_pole mounted temperature 25; H. Masks_Mask mosaic_window temperature 26; H. Masks_Masks mosaic_flow meter temperature 25; LS-150900 temperature 40.7; LS-153157 temperature 28.3; LS-153242 temperature 26.7; LS-153295 temperature 40.6; Outdoors area H. Masks_Mask_pole mounted temperature 27.  
**Must state:** ['2026-08-12 09:00']  
**Scoring:** all → **COMPUTED**

```sql
SELECT max(o.result_time) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE o.value IS NOT NULL AND r.site_id = 'delos' AND o.property_id = 'temperature';

SELECT n.label, se.label, o.property_id, o.value FROM observations o
JOIN readings r USING (reading_id) JOIN nodes n USING (node_id) JOIN sensors se USING (sensor_id)
WHERE o.value IS NOT NULL AND r.site_id = 'delos' AND o.property_id = 'temperature' AND o.result_time = '2026-08-12T09:00:00+00:00' ORDER BY 1, 3;
```

---

## U017 · count_sensors_q

**Question:** How many temperature sensors are there in Delos?  
**Reference:** 10 sensors measure temperature at Delos.  
**Must state:** [10]  
**Scoring:** all → **COMPUTED**

```sql
SELECT count(DISTINCT r.sensor_id) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE TRUE AND r.site_id = 'delos' AND o.property_id = 'temperature';
```

---

## U018 · list_sensors_q

**Question:** Give me the names of the temperature sensors in Delos.  
**Reference:** 10 sensors measure temperature at Delos: ls-109315hw-voltsingle-1, ls-149368hw-potentiometer-1, ls-149405hw-voltsingle-1, ls-149423hw-potentiometer-1, ls-149460hw-voltsingle-1, ls-149678hw-voltsingle-1, ls-150900hw-1, ls-153157hw-1, ls-153242hw-1, ls-153295hw-1.  
**Must state:** ['ls-109315hw-voltsingle-1', 'ls-149368hw-potentiometer-1', 'ls-149405hw-voltsingle-1', 'ls-149423hw-potentiometer-1', 'ls-149460hw-voltsingle-1', 'ls-149678hw-voltsingle-1', 'ls-150900hw-1', 'ls-153157hw-1', 'ls-153242hw-1', 'ls-153295hw-1']  
**Scoring:** all → **COMPUTED**

```sql
SELECT DISTINCT r.site_id, r.sensor_id, se.label FROM observations o
JOIN readings r USING (reading_id) JOIN sensors se USING (sensor_id) WHERE TRUE AND r.site_id = 'delos' AND o.property_id = 'temperature' ORDER BY 1, 3;
```

---

## U019 · verdict

**Question:** Check Delos wind anomaly using the wind policy.  
**Reference:** Cannot be determined. R2_wind: no readings in the snapshot  
**Must state:** ['Cannot be determined']  
**Scoring:** verdict → **COMPUTED**

```sql
-- AD-RT rule evaluation (build_benchmark.RuleEngine) at Delos, rules ['R2_wind'], latest data (windows ending 2026-08-12 09:15 UTC); see verify/anomaly.md for the rule SQL
```

---

## U020 · verdict

**Question:** Check Baltanas vibration PPV anomaly using the vibration policy.  
**Reference:** Cannot be determined. R1_ppv: no readings in the snapshot  
**Must state:** ['Cannot be determined']  
**Scoring:** verdict → **COMPUTED**

```sql
-- AD-RT rule evaluation (build_benchmark.RuleEngine) at Baltanas, rules ['R1_ppv'], latest data (windows ending 2026-08-12 09:15 UTC); see verify/anomaly.md for the rule SQL
```

---

## U021 · quantities

**Question:** Do you have any measurements for the House of Masks?  
**Reference:** 8 quantities are measured at the House of Masks: potentiometer, potentiometer_displacement, temperature, thermistor, thermistor_ysi44005, voltage, voltage_1, voltage_polynomial_4.  
**Must state:** ['potentiometer', 'potentiometer_displacement', 'temperature', 'thermistor', 'thermistor_ysi44005', 'voltage', 'voltage_1', 'voltage_polynomial_4']  
**Scoring:** all → **COMPUTED**

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE TRUE AND r.site_id = 'delos' AND (n.label ILIKE 'H. Masks%' OR n.label ILIKE '%H. Masks_Mask%') GROUP BY 1 ORDER BY 1;
```

---

## U022 · count_sensors

**Question:** how many sensors are there in delos?  
**Reference:** 26 sensors have readings at Delos.  
**Must state:** [26]  
**Scoring:** all → **COMPUTED**

```sql
SELECT count(DISTINCT sensor_id) FROM readings WHERE site_id = 'delos';
```

---

## U023 · list_sensors_q

**Question:** which sensor is about temperature?  
**Earlier turn:** how many sensors are there in delos?  
**Reference:** 10 sensors measure temperature at Delos: ls-109315hw-voltsingle-1, ls-149368hw-potentiometer-1, ls-149405hw-voltsingle-1, ls-149423hw-potentiometer-1, ls-149460hw-voltsingle-1, ls-149678hw-voltsingle-1, ls-150900hw-1, ls-153157hw-1, ls-153242hw-1, ls-153295hw-1.  
**Must state:** ['ls-109315hw-voltsingle-1', 'ls-149368hw-potentiometer-1', 'ls-149405hw-voltsingle-1', 'ls-149423hw-potentiometer-1', 'ls-149460hw-voltsingle-1', 'ls-149678hw-voltsingle-1', 'ls-150900hw-1', 'ls-153157hw-1', 'ls-153242hw-1', 'ls-153295hw-1']  
**Scoring:** all → **COMPUTED**

```sql
SELECT DISTINCT r.site_id, r.sensor_id, se.label FROM observations o
JOIN readings r USING (reading_id) JOIN sensors se USING (sensor_id) WHERE TRUE AND r.site_id = 'delos' AND o.property_id = 'temperature' ORDER BY 1, 3;
```

---

## U024 · verdict

**Question:** Check Delos rainfall anomaly using the rainfall 1 hour policy.  
**Reference:** Cannot be determined. R1a_rain_1h: no readings in the snapshot  
**Must state:** ['Cannot be determined']  
**Scoring:** verdict → **COMPUTED**

```sql
-- AD-RT rule evaluation (build_benchmark.RuleEngine) at Delos, rules ['R1a_rain_1h'], latest data (windows ending 2026-08-12 09:15 UTC); see verify/anomaly.md for the rule SQL
```

---

## U025 · latest_time

**Question:** What is the latest reading timestamp overall?  
**Reference:** 2026-08-12 09:15 UTC (latest observation; the latest reading record, a LoRaWAN reading without values, is 2026-08-12 09:36 UTC).  
**Must state:** ['2026-08-12 09:15', '2026-08-12 09:36']  
**Scoring:** any → **COMPUTED**

```sql
SELECT max(result_time) FROM observations;

SELECT max(result_time) FROM readings;
```

---

## U026 · verdict

**Question:** Check Baltanas rainfall anomaly using the rainfall 1 hour policy.  
**Reference:** Cannot be determined. R6_rain_1h: no readings in the snapshot  
**Must state:** ['Cannot be determined']  
**Scoring:** verdict → **COMPUTED**

```sql
-- AD-RT rule evaluation (build_benchmark.RuleEngine) at Baltanas, rules ['R6_rain_1h'], latest data (windows ending 2026-08-12 09:15 UTC); see verify/anomaly.md for the rule SQL
```

---

## U027 · latest_per_site

**Question:** give me live temperature data from all ARGUS sites  
**Reference:** Latest temperature per site: Baltanas 2026-08-12 09:15 UTC; Delos 2026-08-12 09:00 UTC; Lucretili 2026-08-12 09:15 UTC; Ranverso 2026-08-12 09:00 UTC; Schenkenberg 2026-08-12 09:00 UTC.  
**Must state:** ['2026-08-12 09:15', '2026-08-12 09:00', '2026-08-12 09:15', '2026-08-12 09:00', '2026-08-12 09:00']  
**Scoring:** all → **COMPUTED** (the values at those times are in the SQL result)

```sql
SELECT r.site_id, max(o.result_time) FROM observations o JOIN readings r USING (reading_id)
WHERE o.property_id = 'temperature' AND o.value IS NOT NULL AND r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg'])
GROUP BY 1 ORDER BY 1;
```

---

## U028 · latest_site

**Question:** give me the latest temperature data from Delos  
**Reference:** Latest temperature at Delos: 2026-08-12 09:00 UTC — H. Fournoi_wall attached 1 temperature 29; H. Masks_Dyonisios &panter mosaic_flow meter temperature 25; H. Masks_Mask mosaic_pole mounted temperature 25; H. Masks_Mask mosaic_window temperature 26; H. Masks_Masks mosaic_flow meter temperature 25; LS-150900 temperature 40.7; LS-153157 temperature 28.3; LS-153242 temperature 26.7; LS-153295 temperature 40.6; Outdoors area H. Masks_Mask_pole mounted temperature 27.  
**Must state:** ['2026-08-12 09:00']  
**Scoring:** all → **COMPUTED**

```sql
SELECT max(o.result_time) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE o.value IS NOT NULL AND r.site_id = 'delos' AND o.property_id = 'temperature';

SELECT n.label, se.label, o.property_id, o.value FROM observations o
JOIN readings r USING (reading_id) JOIN nodes n USING (node_id) JOIN sensors se USING (sensor_id)
WHERE o.value IS NOT NULL AND r.site_id = 'delos' AND o.property_id = 'temperature' AND o.result_time = '2026-08-12T09:00:00+00:00' ORDER BY 1, 3;
```

---

## U029 · no_data

**Question:** latest wind dir from baltanas  
**Reference:** No wind direction data at Baltanas in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U030 · no_data

**Question:** give me live wind data from all ARGUS sites  
**Reference:** No wind data in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U031 · per_site_stats

**Question:** Show live temperature statistics per site  
**Reference:** Baltanas: 435,215 observations, min -0.6, mean 21.722, max 44.6; Delos: 21,126 observations, min 11.5, mean 26.087, max 54.2; Lucretili: 318,576 observations, min 0, mean 23.639, max 50; Ranverso: 18,924 observations, min 2, mean 24.209, max 40; Schenkenberg: 26,859 observations, min 9.2, mean 23.672, max 48.3.  
**Must state:** [21.722, 26.087, 23.639, 24.209, 23.672]  
**Scoring:** manual → **MANUAL** ("statistics" is open: the reference gives count, min, mean and max per site; judged by hand)

```sql
SELECT r.site_id, count(*), min(o.value), avg(o.value), max(o.value)
FROM observations o JOIN readings r USING (reading_id)
WHERE o.property_id = 'temperature' AND o.value IS NOT NULL AND r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg'])
GROUP BY 1 ORDER BY 1;
```

---

## U032 · no_data

**Question:** Do you have any crack displacement measurements at Ranverso?  
**Reference:** No crack displacement data at Ranverso in the snapshot.  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U033 · no_data

**Question:** give me latest rainfall data from Baltanas  
**Reference:** No rainfall data at Baltanas in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U034 · list_sensors

**Question:** Which sensors are available at the baltanas site?  
**Reference:** 33 sensors (30 distinct names): Acc-2A, Acc-3A, GNSS-Rover, GNSS_Base, ls-130314hw-meter-teros32-2, ls-130432hw-meter-teros32-2, ls-149367hw-pulse-3, ls-149367hw-thermistor-2, ls-149367hw-voltsingle-1, ls-149402hw-pulse-3, ls-149402hw-thermistor-2, ls-149402hw-voltsingle-1, ls-149421hw-pulse-3, ls-149421hw-thermistor-2, ls-149421hw-voltsingle-1, ls-149443hw-pulse-3, ls-149443hw-thermistor-2, ls-149443hw-voltsingle-1, ls-149780hw-pulse-3, ls-149780hw-thermistor-2, ls-149780hw-voltsingle-1, ls-151810hw-voltage-1, ls-151810hw-voltage-2, ls-151810hw-voltage-3, ls-151810hw-voltage-4, shellydw2-AAB1AC, shellyht-6B6DEE, shellyht-701EE3, shellyht-7020C8, shellyht-CAAE03.  
**Must state:** ['Acc-2A', 'Acc-3A', 'GNSS-Rover', 'GNSS_Base', 'ls-130314hw-meter-teros32-2', 'ls-130432hw-meter-teros32-2', 'ls-149367hw-pulse-3', 'ls-149367hw-thermistor-2', 'ls-149367hw-voltsingle-1', 'ls-149402hw-pulse-3', 'ls-149402hw-thermistor-2', 'ls-149402hw-voltsingle-1', 'ls-149421hw-pulse-3', 'ls-149421hw-thermistor-2', 'ls-149421hw-voltsingle-1', 'ls-149443hw-pulse-3', 'ls-149443hw-thermistor-2', 'ls-149443hw-voltsingle-1', 'ls-149780hw-pulse-3', 'ls-149780hw-thermistor-2', 'ls-149780hw-voltsingle-1', 'ls-151810hw-voltage-1', 'ls-151810hw-voltage-2', 'ls-151810hw-voltage-3', 'ls-151810hw-voltage-4', 'shellydw2-AAB1AC', 'shellyht-6B6DEE', 'shellyht-701EE3', 'shellyht-7020C8', 'shellyht-CAAE03']  
**Scoring:** manual → **MANUAL** (30 sensors: judged by hand)

```sql
SELECT DISTINCT r.sensor_id, se.label FROM readings r JOIN sensors se USING (sensor_id)
WHERE r.site_id = 'baltanas' ORDER BY 2;
```

---

## U035 · node_locations

**Question:** Where are the sensor nodes at the baltanas site?  
**Reference:** 12 located nodes: Acc-2A (41.938432, -4.243868, 797.59 m); Acc-3A (41.937933, -4.243313, 796.89 m); AF1 (41.938408, -4.243822, 797.42 m); AF2 (41.938453, -4.243799, 797.51 m); AF3 (41.938472, -4.243900, 797.92 m); AF4 (41.938544, -4.243940, 798.42 m); Gases (41.938538, -4.243314, 797.16 m); GNSS_Base (41.937244, -4.247576, 779.90 m); GNSS-Rover (41.938386, -4.243841, 797.29 m); P_WL (41.938435, -4.243858, 797.58 m); WP1 (41.938482, -4.243839, 797.84 m); WP2 (41.938454, -4.243845, 797.67 m).  
**Must state:** ['Acc-2A', 'Acc-3A', 'AF1', 'AF2', 'AF3', 'AF4', 'Gases', 'GNSS_Base', 'GNSS-Rover', 'P_WL', 'WP1', 'WP2']  
**Scoring:** manual → **MANUAL** (12 nodes with coordinates: judged by hand)

```sql
SELECT DISTINCT n.label, n.latitude, n.longitude, n.altitude FROM nodes n
JOIN readings r USING (node_id) WHERE r.site_id = 'baltanas' ORDER BY 1;
```

---

## U036 · range_compare

**Question:** How does the voltage range at delos compare to baltanas?  
**Reference:** Delos -0.002 to 4.945; Baltanas -0.001 to 3.722.  
**Must state:** [-0.002, 4.945, -0.001, 3.722]  
**Scoring:** all → **COMPUTED**

```sql
SELECT r.site_id, min(o.value), max(o.value) FROM observations o JOIN readings r USING (reading_id)
WHERE o.property_id = 'voltage' AND o.value IS NOT NULL AND r.site_id = ANY(ARRAY['delos', 'baltanas']) GROUP BY 1;
```

---

## U037 · verdict

**Question:** Has the temperature range at lucretili exceeded its threshold?  
**Reference:** Yes. R9a_temp_lt: metric 27 vs threshold 20 (window ending 2026-08-12 09:15 UTC)  
**Must state:** ['Yes']  
**Scoring:** verdict → **COMPUTED**

```sql
-- AD-RT rule evaluation (build_benchmark.RuleEngine) at Lucretili, rules ['R9a_temp_lt'], latest data (windows ending 2026-08-12 09:15 UTC); see verify/anomaly.md for the rule SQL
```

---

## U038 · range_compare

**Question:** How does the rainfall range at Delos compare to Baltanas?  
**Reference:** Delos: no rainfall data in the snapshot; Baltanas: no rainfall data in the snapshot.  
**Must state:** —  
**Scoring:** negative → **COMPUTED** (neither site has data)

```sql
SELECT r.site_id, min(o.value), max(o.value) FROM observations o JOIN readings r USING (reading_id)
WHERE o.property_id = 'rainfall' AND o.value IS NOT NULL AND r.site_id = ANY(ARRAY['delos', 'baltanas']) GROUP BY 1;
```

---

## U039 · no_data

**Question:** Which instruments measure wind direction?  
**Reference:** No wind direction data in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U040 · unanswerable

**Question:** Which instruments are installed in Room 214?  
**Reference:** Cannot be answered from the knowledge graph: rooms are not modelled in the knowledge graph.  
**Must state:** —  
**Scoring:** decline → **COMPUTED**

---

## U041 · device_types

**Question:** Which device types exist in the live ARGUS KG?  
**Reference:** Node (device) models: LS-G6-PICO (25); LS-G6-TIL90-X (10); LSG7ACL-BILH-VIB (8); LS-G6-VOLT-4-FCC (7); LSG7GNS-SXLH (2); MAPIR Survey 3 (RGN) (2); LS-G6-DIG-2-FCC (2); Spotwave_vallen (1).  
**Must state:** ['LS-G6-PICO', 'LS-G6-TIL90-X', 'LSG7ACL-BILH-VIB', 'LS-G6-VOLT-4-FCC', 'LSG7GNS-SXLH', 'MAPIR Survey 3 (RGN)', 'LS-G6-DIG-2-FCC', 'Spotwave_vallen']  
**Scoring:** manual → **MANUAL** ("device types" read as node models; judged by hand)

```sql
SELECT model, count(*) FROM nodes WHERE model IS NOT NULL GROUP BY 1 ORDER BY 2 DESC;
```

---

## U042 · unanswerable

**Question:** Which measurement protocols are used by each installed instrument?  
**Reference:** Cannot be answered from the knowledge graph: measurement protocols are not modelled in the knowledge graph.  
**Must state:** —  
**Scoring:** decline → **COMPUTED**

---

## U043 · no_rule

**Question:** Check wind anomaly at Schenkenberg using the wind policy.  
**Reference:** Cannot be determined: no AD-RT rule is defined for wind at Schenkenberg (its rules: R1_temp_hum, R2_crack_step, R3_vib_zscore, R4_pga).  
**Must state:** ['Cannot be determined']  
**Scoring:** verdict → **COMPUTED**

```sql
SELECT rule_id FROM policies WHERE site_id = 'schenkenberg' AND left(label, 5) = 'AD-RT' ORDER BY 1;
```

---

## U044 · no_data

**Question:** Give me the latest wind direction from Baltanas.  
**Reference:** No wind direction data at Baltanas in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U045 · no_data

**Question:** What are the latest humidity readings from Ranverso?  
**Reference:** No humidity data at Ranverso in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U046 · no_data

**Question:** Show me the latest soil moisture data from Delos.  
**Reference:** No soil moisture data at Delos in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U047 · total

**Question:** How many observations are available in the live ARGUS KG?  
**Reference:** 3,737,747 observations in the knowledge graph (3,684,898 at the five pilot sites).  
**Must state:** [3737747, 3684898]  
**Scoring:** any → **COMPUTED**

```sql
SELECT count(*) FROM observations;

SELECT count(*) FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']);
```

---

## U048 · count_readings

**Question:** How many readings are available for Delos Island?  
**Reference:** 113,789 readings.  
**Must state:** [113789]  
**Scoring:** all → **COMPUTED**

```sql
SELECT count(*) FROM readings WHERE site_id = 'delos';
```

---

## U049 · quantities

**Question:** What measurements are available at Baltanas?  
**Reference:** 55 quantities are measured at Baltanas: activeTime, alt, applied, backgroundEvent, channel_error_2, channel_error_4, cn0, composedAxis, deviation, duration, eastwest_displacement_millimeters, fixBeforeCorrections, freqXAxis, freqYAxis, freqZAxis, hasFix, haversine_distance_absolute_horizontal_displacement_millimeters, horizontal, installation_pitch_angle, installation_roll_angle, inUse, inView, lat, latLon, length, lon, northsouth_displacement_millimeters, numPerSample, numSamples, overThresholdEvents, pulse_counter, rssiAvg, rssiStdDev, samplesNoFix, snrAvg, snrStdDev, soil_temperature, soil_water_potential, temperature, thermistor, timeToFirst, timeToFix, underThresholdEvents, unexpectedPackets, updated, vertical, vertical_displacement_millimeters, voltage, voltage_polynomial_4, xAxis, xAxisStd, yAxis, yAxisStd, zAxis, zAxisStd.  
**Must state:** ['activeTime', 'alt', 'applied', 'backgroundEvent', 'channel_error_2', 'channel_error_4', 'cn0', 'composedAxis', 'deviation', 'duration', 'eastwest_displacement_millimeters', 'fixBeforeCorrections', 'freqXAxis', 'freqYAxis', 'freqZAxis', 'hasFix', 'haversine_distance_absolute_horizontal_displacement_millimeters', 'horizontal', 'installation_pitch_angle', 'installation_roll_angle', 'inUse', 'inView', 'lat', 'latLon', 'length', 'lon', 'northsouth_displacement_millimeters', 'numPerSample', 'numSamples', 'overThresholdEvents', 'pulse_counter', 'rssiAvg', 'rssiStdDev', 'samplesNoFix', 'snrAvg', 'snrStdDev', 'soil_temperature', 'soil_water_potential', 'temperature', 'thermistor', 'timeToFirst', 'timeToFix', 'underThresholdEvents', 'unexpectedPackets', 'updated', 'vertical', 'vertical_displacement_millimeters', 'voltage', 'voltage_polynomial_4', 'xAxis', 'xAxisStd', 'yAxis', 'yAxisStd', 'zAxis', 'zAxisStd']  
**Scoring:** manual → **MANUAL** (55 quantities: judged by hand)

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE TRUE AND r.site_id = 'baltanas' GROUP BY 1 ORDER BY 1;
```

---

## U050 · quantities

**Question:** What measurements are available at Ranverso?  
**Reference:** 26 quantities are measured at Ranverso: activeTime, axis_x, axis_x_std, axis_y, axis_y_std, axis_z, axis_z_std, backgroundEvent, composedAxis, duration, freqXAxis, freqYAxis, freqZAxis, overThresholdEvents, pulse_counter, rainfall, temperature, thermistor, thermistor_ysi44005, underThresholdEvents, voltage, voltage_1, voltage_polynomial_4, xAxis, yAxis, zAxis.  
**Must state:** ['activeTime', 'axis_x', 'axis_x_std', 'axis_y', 'axis_y_std', 'axis_z', 'axis_z_std', 'backgroundEvent', 'composedAxis', 'duration', 'freqXAxis', 'freqYAxis', 'freqZAxis', 'overThresholdEvents', 'pulse_counter', 'rainfall', 'temperature', 'thermistor', 'thermistor_ysi44005', 'underThresholdEvents', 'voltage', 'voltage_1', 'voltage_polynomial_4', 'xAxis', 'yAxis', 'zAxis']  
**Scoring:** manual → **MANUAL** (26 quantities: judged by hand)

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
JOIN nodes n USING (node_id) WHERE TRUE AND r.site_id = 'ranverso' GROUP BY 1 ORDER BY 1;
```

---

## U051 · crack

**Question:** Does crack displacement exist in the ARGUS database?  
**Reference:** No quantity is called crack displacement. Displacement is measured by potentiometers at Delos, House of Masks (potentiometer on H. Masks_Mask mosaic_pole mounted | H. Masks_Mask mosaic_window; potentiometer_displacement on H. Masks_Mask mosaic_pole mounted | H. Masks_Mask mosaic_window). Lucretili has crackmeter nodes (LS-174156 Crackmeter Villa Orazio, LS-177253 Crackmeter Conventillo, LS-177266 - Crackmeter Conventillo, LS-177287 Crackmeter Villa Orazio, LS-177310 Crackmeter Montefalco, LS-177320 CrackMeter Conventillo) but no displacement values.  
**Must state:** ['potentiometer_displacement']  
**Scoring:** manual → **MANUAL** (whether potentiometer displacement counts as crack displacement needs the partner's confirmation)

```sql
SELECT r.site_id, o.property_id, string_agg(DISTINCT n.label, ' | '),
string_agg(DISTINCT se.label, ' | '), count(*)
FROM observations o JOIN readings r USING (reading_id) JOIN nodes n USING (node_id)
JOIN sensors se USING (sensor_id)
WHERE o.property_id ILIKE '%potentiometer%' GROUP BY 1, 2;

SELECT DISTINCT r.site_id, n.label FROM nodes n JOIN readings r USING (node_id)
WHERE n.label ILIKE '%crack%' ORDER BY 2;
```

---

## U052 · crack

**Question:** Where is crack displacement measured?  
**Reference:** No quantity is called crack displacement. Displacement is measured by potentiometers at Delos, House of Masks (potentiometer on H. Masks_Mask mosaic_pole mounted | H. Masks_Mask mosaic_window; potentiometer_displacement on H. Masks_Mask mosaic_pole mounted | H. Masks_Mask mosaic_window). Lucretili has crackmeter nodes (LS-174156 Crackmeter Villa Orazio, LS-177253 Crackmeter Conventillo, LS-177266 - Crackmeter Conventillo, LS-177287 Crackmeter Villa Orazio, LS-177310 Crackmeter Montefalco, LS-177320 CrackMeter Conventillo) but no displacement values.  
**Must state:** ['potentiometer_displacement']  
**Scoring:** manual → **MANUAL** (whether potentiometer displacement counts as crack displacement needs the partner's confirmation)

```sql
SELECT r.site_id, o.property_id, string_agg(DISTINCT n.label, ' | '),
string_agg(DISTINCT se.label, ' | '), count(*)
FROM observations o JOIN readings r USING (reading_id) JOIN nodes n USING (node_id)
JOIN sensors se USING (sensor_id)
WHERE o.property_id ILIKE '%potentiometer%' GROUP BY 1, 2;

SELECT DISTINCT r.site_id, n.label FROM nodes n JOIN readings r USING (node_id)
WHERE n.label ILIKE '%crack%' ORDER BY 2;
```

---

## U053 · range_compare

**Question:** Compare the temperature range between Delos and Schenkenberg.  
**Reference:** Delos 11.5 to 54.2; Schenkenberg 9.2 to 48.3.  
**Must state:** [11.5, 54.2, 9.2, 48.3]  
**Scoring:** all → **COMPUTED**

```sql
SELECT r.site_id, min(o.value), max(o.value) FROM observations o JOIN readings r USING (reading_id)
WHERE o.property_id = 'temperature' AND o.value IS NOT NULL AND r.site_id = ANY(ARRAY['delos', 'schenkenberg']) GROUP BY 1;
```

---

## U054 · no_data

**Question:** What is the humidity range at Ranverso?  
**Reference:** No humidity data at Ranverso in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U055 · no_data

**Question:** What is the average rainfall at Baltanas?  
**Reference:** No rainfall data at Baltanas in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U056 · argmax_site

**Question:** Which site has the most observations?  
**Reference:** Baltanas (1,925,908 observations).  
**Must state:** ['Baltanas']  
**Scoring:** all → **COMPUTED**

```sql
SELECT r.site_id, count(*) FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1 ORDER BY 1;
```

---

## U057 · per_quantity

**Question:** How many observations are available per measurement?  
**Reference:** 89 quantities; the most frequent: temperature 820,700; voltage 404,917; voltage_1 222,104; thermistor 196,017; pulse_counter 157,460; voltage_polynomial_4 145,760; axis_y_std 77,126; axis_z 77,126; axis_z_std 77,126; axis_x_std 77,126 … (full list in the SQL result).  
**Must state:** ['temperature', 'voltage', 'voltage_1']  
**Scoring:** manual → **MANUAL** (89 quantities: judged by hand)

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1 ORDER BY 2 DESC;
```

---

## U058 · top_quantity

**Question:** Which measurements have the most readings?  
**Reference:** temperature (820,700 observations), then voltage (404,917), voltage_1 (222,104), thermistor (196,017), pulse_counter (157,460).  
**Must state:** ['temperature']  
**Scoring:** all → **COMPUTED**

```sql
SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1 ORDER BY 2 DESC LIMIT 5;
```

---

## U059 · no_data

**Question:** How many wind observations are available per site?  
**Reference:** No wind data in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U060 · latest_each_quantity

**Question:** What is the latest value for each measurement at Delos?  
**Reference:** axis_x -87.099 at 2026-08-12 09:00; axis_x_std 0 at 2026-08-12 09:00; axis_y -1.221 at 2026-08-12 09:00; axis_y_std 0 at 2026-08-12 09:00; axis_z -2.631 at 2026-08-12 09:00; axis_z_std 0 at 2026-08-12 09:00; potentiometer 924.481 at 2026-08-12 09:00; potentiometer_displacement 7.552 at 2026-08-12 09:00; temperature 25 at 2026-08-12 09:00; thermistor 8531.752 at 2026-08-12 09:00; thermistor_ysi44005 27.282 at 2026-08-12 09:00; voltage 0.588 at 2026-08-12 09:00; voltage_1 5741.629 at 2026-08-12 09:00; voltage_polynomial_4 0.387 at 2026-08-12 09:00 (UTC).  
**Must state:** ['axis_x', 'axis_x_std', 'axis_y', 'axis_y_std', 'axis_z', 'axis_z_std', 'potentiometer', 'potentiometer_displacement', 'temperature', 'thermistor', 'thermistor_ysi44005', 'voltage', 'voltage_1', 'voltage_polynomial_4']  
**Scoring:** manual → **MANUAL** (14 quantities (several sensors each): judged by hand)

```sql
SELECT DISTINCT ON (o.property_id) o.property_id, o.result_time, o.value
FROM observations o JOIN readings r USING (reading_id)
WHERE r.site_id = 'delos' AND o.value IS NOT NULL ORDER BY o.property_id, o.result_time DESC;
```

---

## U061 · list_sensors_q

**Question:** Which instruments measure air temperature?  
**Reference:** 68 sensors measure temperature at the five sites: Acc-2A (Baltanas), Acc-3A (Baltanas), GNSS_Base (Baltanas), GNSS-Rover (Baltanas), ls-149367hw-pulse-3 (Baltanas), ls-149367hw-thermistor-2 (Baltanas), ls-149367hw-voltsingle-1 (Baltanas), ls-149402hw-pulse-3 (Baltanas), ls-149402hw-thermistor-2 (Baltanas), ls-149402hw-voltsingle-1 (Baltanas), ls-149421hw-pulse-3 (Baltanas), ls-149421hw-thermistor-2 (Baltanas), ls-149421hw-voltsingle-1 (Baltanas), ls-149443hw-pulse-3 (Baltanas), ls-149443hw-thermistor-2 (Baltanas), ls-149443hw-voltsingle-1 (Baltanas), ls-149780hw-pulse-3 (Baltanas), ls-149780hw-thermistor-2 (Baltanas), ls-149780hw-voltsingle-1 (Baltanas), ls-109315hw-voltsingle-1 (Delos), ls-149368hw-potentiometer-1 (Delos), ls-149405hw-voltsingle-1 (Delos), ls-149423hw-potentiometer-1 (Delos), ls-149460hw-voltsingle-1 (Delos), ls-149678hw-voltsingle-1 (Delos), ls-150900hw-1 (Delos), ls-153157hw-1 (Delos), ls-153242hw-1 (Delos), ls-153295hw-1 (Delos), LS-152608 - Tiltmeter Conventillo (Lucretili), ls-152816hw-1 (Lucretili), ls-152931hw-1 (Lucretili), ls-153061hw-1 (Lucretili), ls-174156hw-pulse-3 (Lucretili), ls-174156hw-thermistor-2 (Lucretili), ls-174156hw-voltsingle-1 (Lucretili), ls-177237hw-voltsingle-1 (Lucretili), ls-177239hw-thermistor-2 (Lucretili), ls-177239hw-voltsingle-1 (Lucretili), ls-177253hw-voltsingle-1 (Lucretili), ls-177266hw-voltsingle-1 (Lucretili), ls-177281hw-pulse-3 (Lucretili), ls-177281hw-thermistor-2 (Lucretili), ls-177281hw-voltsingle-1 (Lucretili), ls-177287hw-voltsingle-1 (Lucretili), ls-177310hw-voltsingle-1 (Lucretili), ls-177320hw-voltsingle-1 (Lucretili), ls-143276hw-1 (Ranverso), ls-149248hw-voltsingle-1 (Ranverso), ls-149361hw-voltsingle-1 (Ranverso), LS-170894 (Ranverso), ls-174188hw-thermistor-2 (Ranverso), ls-174188hw-voltsingle-1 (Ranverso), ls-177315hw-pulse-3 (Ranverso), ls-177315hw-thermistor-2 (Ranverso), ls-177315hw-voltsingle-1 (Ranverso), ls-149796hw-voltsingle-1 (Schenkenberg), LS-152479 (Schenkenberg), LS-152479 (Schenkenberg), LS-152555 (Schenkenberg), LS-152555 (Schenkenberg), ls-152899hw-1 (Schenkenberg), ls-152914hw-1 (Schenkenberg), LS-159070 (Schenkenberg), LS-159070 (Schenkenberg), LS-175480 (Schenkenberg), LS-175480 (Schenkenberg), LS-175480 (Schenkenberg).  
**Must state:** ['Acc-2A', 'Acc-3A', 'GNSS_Base', 'GNSS-Rover', 'ls-149367hw-pulse-3', 'ls-149367hw-thermistor-2', 'ls-149367hw-voltsingle-1', 'ls-149402hw-pulse-3', 'ls-149402hw-thermistor-2', 'ls-149402hw-voltsingle-1', 'ls-149421hw-pulse-3', 'ls-149421hw-thermistor-2', 'ls-149421hw-voltsingle-1', 'ls-149443hw-pulse-3', 'ls-149443hw-thermistor-2', 'ls-149443hw-voltsingle-1', 'ls-149780hw-pulse-3', 'ls-149780hw-thermistor-2', 'ls-149780hw-voltsingle-1', 'ls-109315hw-voltsingle-1', 'ls-149368hw-potentiometer-1', 'ls-149405hw-voltsingle-1', 'ls-149423hw-potentiometer-1', 'ls-149460hw-voltsingle-1', 'ls-149678hw-voltsingle-1', 'ls-150900hw-1', 'ls-153157hw-1', 'ls-153242hw-1', 'ls-153295hw-1', 'LS-152608 - Tiltmeter Conventillo', 'ls-152816hw-1', 'ls-152931hw-1', 'ls-153061hw-1', 'ls-174156hw-pulse-3', 'ls-174156hw-thermistor-2', 'ls-174156hw-voltsingle-1', 'ls-177237hw-voltsingle-1', 'ls-177239hw-thermistor-2', 'ls-177239hw-voltsingle-1', 'ls-177253hw-voltsingle-1', 'ls-177266hw-voltsingle-1', 'ls-177281hw-pulse-3', 'ls-177281hw-thermistor-2', 'ls-177281hw-voltsingle-1', 'ls-177287hw-voltsingle-1', 'ls-177310hw-voltsingle-1', 'ls-177320hw-voltsingle-1', 'ls-143276hw-1', 'ls-149248hw-voltsingle-1', 'ls-149361hw-voltsingle-1', 'LS-170894', 'ls-174188hw-thermistor-2', 'ls-174188hw-voltsingle-1', 'ls-177315hw-pulse-3', 'ls-177315hw-thermistor-2', 'ls-177315hw-voltsingle-1', 'ls-149796hw-voltsingle-1', 'LS-152479', 'LS-152479', 'LS-152555', 'LS-152555', 'ls-152899hw-1', 'ls-152914hw-1', 'LS-159070', 'LS-159070', 'LS-175480', 'LS-175480', 'LS-175480']  
**Scoring:** manual → **MANUAL** (68 sensors: judged by hand)

```sql
SELECT DISTINCT r.site_id, r.sensor_id, se.label FROM observations o
JOIN readings r USING (reading_id) JOIN sensors se USING (sensor_id) WHERE TRUE AND r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) AND o.property_id = 'temperature' ORDER BY 1, 3;
```

---

## U062 · list_sensors_q

**Question:** Which instruments measure rainfall?  
**Reference:** 2 sensors measure rainfall at the five sites: ls-177281hw-pulse-3 (Lucretili), ls-177315hw-pulse-3 (Ranverso).  
**Must state:** ['ls-177281hw-pulse-3', 'ls-177315hw-pulse-3']  
**Scoring:** all → **COMPUTED**

```sql
SELECT DISTINCT r.site_id, r.sensor_id, se.label FROM observations o
JOIN readings r USING (reading_id) JOIN sensors se USING (sensor_id) WHERE TRUE AND r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) AND o.property_id = 'rainfall' ORDER BY 1, 3;
```

---

## U063 · no_data

**Question:** Which instruments measure soil moisture?  
**Reference:** No soil moisture data in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U064 · crack

**Question:** Which instruments measure crack displacement?  
**Reference:** No quantity is called crack displacement. Displacement is measured by potentiometers at Delos, House of Masks (potentiometer on H. Masks_Mask mosaic_pole mounted | H. Masks_Mask mosaic_window; potentiometer_displacement on H. Masks_Mask mosaic_pole mounted | H. Masks_Mask mosaic_window). Lucretili has crackmeter nodes (LS-174156 Crackmeter Villa Orazio, LS-177253 Crackmeter Conventillo, LS-177266 - Crackmeter Conventillo, LS-177287 Crackmeter Villa Orazio, LS-177310 Crackmeter Montefalco, LS-177320 CrackMeter Conventillo) but no displacement values.  
**Must state:** ['potentiometer_displacement']  
**Scoring:** manual → **MANUAL** (whether potentiometer displacement counts as crack displacement needs the partner's confirmation)

```sql
SELECT r.site_id, o.property_id, string_agg(DISTINCT n.label, ' | '),
string_agg(DISTINCT se.label, ' | '), count(*)
FROM observations o JOIN readings r USING (reading_id) JOIN nodes n USING (node_id)
JOIN sensors se USING (sensor_id)
WHERE o.property_id ILIKE '%potentiometer%' GROUP BY 1, 2;

SELECT DISTINCT r.site_id, n.label FROM nodes n JOIN readings r USING (node_id)
WHERE n.label ILIKE '%crack%' ORDER BY 2;
```

---

## U065 · nodes

**Question:** Which instruments are installed at the House of Masks?  
**Reference:** 9 sensor nodes: H. Masks_Dolphins mosaic_pole mounted, H. Masks_Dyonisios mosaic_pole mounted, H. Masks_Dyonisios &panter mosaic_flow meter, H. Masks_Dyonisios &panter mosaic_pole mounted 2, H. Masks_Mask mosaic_pole mounted, H. Masks_Mask mosaic_pole mounted 2, H. Masks_Mask mosaic_window, H. Masks_Masks mosaic_flow meter, Outdoors area H. Masks_Mask_pole mounted.  
**Must state:** ['H. Masks_Dolphins mosaic_pole mounted', 'H. Masks_Dyonisios mosaic_pole mounted', 'H. Masks_Dyonisios &panter mosaic_flow meter', 'H. Masks_Dyonisios &panter mosaic_pole mounted 2', 'H. Masks_Mask mosaic_pole mounted', 'H. Masks_Mask mosaic_pole mounted 2', 'H. Masks_Mask mosaic_window', 'H. Masks_Masks mosaic_flow meter', 'Outdoors area H. Masks_Mask_pole mounted']  
**Scoring:** all → **COMPUTED**

```sql
SELECT DISTINCT n.label FROM nodes n JOIN readings r USING (node_id)
WHERE r.site_id = 'delos' AND (n.label ILIKE 'H. Masks%' OR n.label ILIKE '%H. Masks_Mask%') ORDER BY 1;
```

---

## U066 · list_sensors

**Question:** Which sensors are available at Baltanas?  
**Reference:** 33 sensors (30 distinct names): Acc-2A, Acc-3A, GNSS-Rover, GNSS_Base, ls-130314hw-meter-teros32-2, ls-130432hw-meter-teros32-2, ls-149367hw-pulse-3, ls-149367hw-thermistor-2, ls-149367hw-voltsingle-1, ls-149402hw-pulse-3, ls-149402hw-thermistor-2, ls-149402hw-voltsingle-1, ls-149421hw-pulse-3, ls-149421hw-thermistor-2, ls-149421hw-voltsingle-1, ls-149443hw-pulse-3, ls-149443hw-thermistor-2, ls-149443hw-voltsingle-1, ls-149780hw-pulse-3, ls-149780hw-thermistor-2, ls-149780hw-voltsingle-1, ls-151810hw-voltage-1, ls-151810hw-voltage-2, ls-151810hw-voltage-3, ls-151810hw-voltage-4, shellydw2-AAB1AC, shellyht-6B6DEE, shellyht-701EE3, shellyht-7020C8, shellyht-CAAE03.  
**Must state:** ['Acc-2A', 'Acc-3A', 'GNSS-Rover', 'GNSS_Base', 'ls-130314hw-meter-teros32-2', 'ls-130432hw-meter-teros32-2', 'ls-149367hw-pulse-3', 'ls-149367hw-thermistor-2', 'ls-149367hw-voltsingle-1', 'ls-149402hw-pulse-3', 'ls-149402hw-thermistor-2', 'ls-149402hw-voltsingle-1', 'ls-149421hw-pulse-3', 'ls-149421hw-thermistor-2', 'ls-149421hw-voltsingle-1', 'ls-149443hw-pulse-3', 'ls-149443hw-thermistor-2', 'ls-149443hw-voltsingle-1', 'ls-149780hw-pulse-3', 'ls-149780hw-thermistor-2', 'ls-149780hw-voltsingle-1', 'ls-151810hw-voltage-1', 'ls-151810hw-voltage-2', 'ls-151810hw-voltage-3', 'ls-151810hw-voltage-4', 'shellydw2-AAB1AC', 'shellyht-6B6DEE', 'shellyht-701EE3', 'shellyht-7020C8', 'shellyht-CAAE03']  
**Scoring:** manual → **MANUAL** (30 sensors: judged by hand)

```sql
SELECT DISTINCT r.sensor_id, se.label FROM readings r JOIN sensors se USING (sensor_id)
WHERE r.site_id = 'baltanas' ORDER BY 2;
```

---

## U067 · list_sensors

**Question:** Which sensors are available at Delos?  
**Reference:** 26 sensors (26 distinct names): ls-109315hw-voltsingle-1, ls-149368hw-potentiometer-1, ls-149405hw-voltsingle-1, ls-149423hw-potentiometer-1, ls-149460hw-voltsingle-1, ls-149678hw-voltsingle-1, ls-150900hw-1, ls-151805hw-thermistor-2, ls-151805hw-voltage-1, ls-151805hw-voltage-3, ls-151809hw-thermistor-2, ls-151809hw-voltage-1, ls-151809hw-voltage-3, ls-151815hw-thermistor-2, ls-151815hw-voltage-1, ls-151815hw-voltage-3, ls-151815hw-voltage-4, ls-151836hw-thermistor-2, ls-151836hw-voltage-1, ls-151836hw-voltage-3, ls-153157hw-1, ls-153242hw-1, ls-153295hw-1, ls-168439hw-thermistor-2, ls-168439hw-voltage-1, ls-168439hw-voltage-3.  
**Must state:** ['ls-109315hw-voltsingle-1', 'ls-149368hw-potentiometer-1', 'ls-149405hw-voltsingle-1', 'ls-149423hw-potentiometer-1', 'ls-149460hw-voltsingle-1', 'ls-149678hw-voltsingle-1', 'ls-150900hw-1', 'ls-151805hw-thermistor-2', 'ls-151805hw-voltage-1', 'ls-151805hw-voltage-3', 'ls-151809hw-thermistor-2', 'ls-151809hw-voltage-1', 'ls-151809hw-voltage-3', 'ls-151815hw-thermistor-2', 'ls-151815hw-voltage-1', 'ls-151815hw-voltage-3', 'ls-151815hw-voltage-4', 'ls-151836hw-thermistor-2', 'ls-151836hw-voltage-1', 'ls-151836hw-voltage-3', 'ls-153157hw-1', 'ls-153242hw-1', 'ls-153295hw-1', 'ls-168439hw-thermistor-2', 'ls-168439hw-voltage-1', 'ls-168439hw-voltage-3']  
**Scoring:** manual → **MANUAL** (26 sensors: judged by hand)

```sql
SELECT DISTINCT r.sensor_id, se.label FROM readings r JOIN sensors se USING (sensor_id)
WHERE r.site_id = 'delos' ORDER BY 2;
```

---

## U068 · no_data

**Question:** Which installed instruments are associated with Weather Stations?  
**Reference:** No weather station data in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U069 · no_data

**Question:** What physical quantities are monitored by weather stations?  
**Reference:** No weather station data in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U070 · no_data

**Question:** Which sites have wind sensors?  
**Reference:** No wind data in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U071 · verdict

**Question:** Is there a rainfall anomaly at Baltanas?  
**Reference:** Cannot be determined. R6_rain_1h: no readings in the snapshot  
**Must state:** ['Cannot be determined']  
**Scoring:** verdict → **COMPUTED**

```sql
-- AD-RT rule evaluation (build_benchmark.RuleEngine) at Baltanas, rules ['R6_rain_1h'], latest data (windows ending 2026-08-12 09:15 UTC); see verify/anomaly.md for the rule SQL
```

---

## U072 · verdict

**Question:** Is the latest wind speed at Delos anomalous?  
**Reference:** Cannot be determined. R2_wind: no readings in the snapshot  
**Must state:** ['Cannot be determined']  
**Scoring:** verdict → **COMPUTED**

```sql
-- AD-RT rule evaluation (build_benchmark.RuleEngine) at Delos, rules ['R2_wind'], latest data (windows ending 2026-08-12 09:15 UTC); see verify/anomaly.md for the rule SQL
```

---

## U073 · policies

**Question:** Which AD-RT policies are available for Baltanas?  
**Reference:** 8 AD-RT policies: R1_ppv (vibration PPV); R2_hum_daily_range (humidity daily range); R3_gnss_change (GNSS drift); R4a_soil_high (soil moisture high); R4b_soil_range (soil moisture daily range); R5a_airflow_const (airflow constancy); R5b_airflow_range (airflow range); R6_rain_1h (rainfall 1h).  
**Must state:** ['R1_ppv', 'R2_hum_daily_range', 'R3_gnss_change', 'R4a_soil_high', 'R4b_soil_range', 'R5a_airflow_const', 'R5b_airflow_range', 'R6_rain_1h']  
**Scoring:** all → **COMPUTED**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'baltanas' AND left(label, 5) = 'AD-RT' ORDER BY 1;
```

---

## U074 · policy_for

**Question:** Which policy applies to rainfall at Baltanas?  
**Reference:** R6_rain_1h (AD-RT Baltanas policy - rainfall 1h).  
**Must state:** ['R6_rain_1h']  
**Scoring:** all → **COMPUTED**

```sql
SELECT rule_id, label, threshold_value FROM policies WHERE site_id = 'baltanas' AND rule_id = 'R6_rain_1h';
```

---

## U075 · policies

**Question:** Which policies are defined for Delos?  
**Reference:** 4 AD-RT policies: R1a_rain_1h (rainfall 1h); R1b_rain_3h (rainfall 3h); R2_wind (wind); R3_hum_cross (humidity crossings).  
**Must state:** ['R1a_rain_1h', 'R1b_rain_3h', 'R2_wind', 'R3_hum_cross']  
**Scoring:** all → **COMPUTED**

```sql
SELECT rule_id, label, threshold_value, threshold_json FROM policies
WHERE site_id = 'delos' AND left(label, 5) = 'AD-RT' ORDER BY 1;
```

---

## U076 · no_data

**Question:** Compare wind speed readings across ARGUS sites.  
**Reference:** No wind speed data in the snapshot (these channels come from LoRaWAN devices whose values were not ingested).  
**Must state:** —  
**Scoring:** negative → **COMPUTED**

---

## U077 · count_sensors

**Question:** how many sensors are there in delos pilot?  
**Reference:** 26 sensors have readings at Delos.  
**Must state:** [26]  
**Scoring:** all → **COMPUTED**

```sql
SELECT count(DISTINCT sensor_id) FROM readings WHERE site_id = 'delos';
```

---

## U078 · count_sensors

**Question:** how many sensors are in delos site  
**Reference:** 26 sensors have readings at Delos.  
**Must state:** [26]  
**Scoring:** all → **COMPUTED**

```sql
SELECT count(DISTINCT sensor_id) FROM readings WHERE site_id = 'delos';
```

---

## U079 · per_site

**Question:** How many devices are installed per ARGUS site?  
**Reference:** Baltanas 13; Delos 15; Lucretili 13; Ranverso 7; Schenkenberg 7.  
**Must state:** [13, 15, 13, 7, 7]  
**Scoring:** all → **COMPUTED**

```sql
SELECT r.site_id, count(DISTINCT r.node_id) FROM readings r WHERE r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1 ORDER BY 1;
```

---

## U080 · displacement_quantities

**Question:** Which displacement measurements are available?  
**Reference:** 5 displacement quantities: eastwest_displacement_millimeters at Baltanas (46 observations); haversine_distance_absolute_horizontal_displacement_millimeters at Baltanas (257 observations); northsouth_displacement_millimeters at Baltanas (287 observations); vertical_displacement_millimeters at Baltanas (209 observations); potentiometer_displacement at Delos (4,218 observations).  
**Must state:** ['eastwest_displacement_millimeters', 'haversine_distance_absolute_horizontal_displacement_millimeters', 'northsouth_displacement_millimeters', 'vertical_displacement_millimeters', 'potentiometer_displacement']  
**Scoring:** all → **COMPUTED**

```sql
SELECT r.site_id, o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
WHERE o.property_id ILIKE '%displacement%' AND r.site_id = ANY(ARRAY['baltanas', 'delos', 'lucretili', 'ranverso', 'schenkenberg']) GROUP BY 1, 2 ORDER BY 1, 2;
```

---
