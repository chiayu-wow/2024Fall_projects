# **IS 597 - Programming & Quality in Analytics: Final Project**

## **Project Title**
### **Monte Carlo Simulation of Wildfire Propagation in Forested Areas**

## **Team Members**
- **Chia Yu Wang**  
- **Guan Hong Lin**

---

## **Project Overview**

This project aims to model and simulate the spread of wildfires under varying environmental conditions using Monte Carlo simulations. By adjusting parameters such as tree species, humidity, temperature, wind speed, and proximity to water bodies, the model predicts wildfire behavior and dynamics. The ultimate goal is to enhance our understanding of wildfire propagation and provide insights for better management and response strategies.

---

## **Hypotheses and Validation**

### **Hypotheses**
1. **Impact of Ignition Point Location:**  
   Wildfires starting in bushland will result in a burned area approximately **50% larger** compared to ignition in forested areas composed of willow, pine, and oak trees.
   
2. **Humidity and Water Proximity:**  
   Areas near water bodies, with higher humidity levels, will exhibit significantly reduced wildfire spread probabilities.

3. **Effect of Wind Speed:**  
   As wind speed increases, wildfire spread accelerates, leading to shorter burn durations for a given area.

### **Validation**
1. **Empirical Data Comparison:**  
   Historical wildfire patterns reveal significant differences in wildfire propagation influenced by seasonal variations in temperature and humidity.  
2. **Simulation Results:**  
   Results from our simulations are compared against expected trends to validate the model's accuracy.

---

## **Model Design**

We simulate the **Mendocino Complex Fire (July 2018)**, the largest wildfire in California's history, which burned approximately **459,123 acres**. To closely replicate the scenario:

### **Grid and Burn Rate Design**

A 50×50 grid represents the simulated area, where each cell covers 46 chains (1 chain = 66 feet). This results in a total simulation area of 529,000 acres, slightly larger than the actual event.
In this simulation, each grid cell represents a **46-chain (1 chain = 66 feet)** square. The decision to set the grid cell size to **46 chains** is based on the burn rate of the fastest-burning vegetation type, **bush**, which spreads at a rate of **46 chains per hour**. By aligning the grid cell size with the burn rate of bush, we ensure that:

- **Fastest Burn Rate (Bush):**  
   A bushfire can burn through an entire grid cell in approximately **1 hour**, making it the fastest vegetation to spread fire across the simulation.  
- **Slower Burn Rates (Other Vegetation):**  
   For tree species such as **pine**, **oak**, and **willow**, the burn rate is slower, requiring multiple time steps to fully burn through a single grid cell. This effectively represents their lower flammability and spread rates in real-world conditions.


### **Propagation Logic**
- The fire starts in the **center** of the grid.  
- Burn probabilities are calculated based on environmental factors such as humidity, temperature, and wind conditions.  
- If the calculated burn probability exceeds a randomly generated threshold, the fire spreads to adjacent cells.  
- Fire spreads only in **four directions (N, S, W, E)** to simplify the simulation.

### **References**
- [Fire Behavior Measures](https://nwfirescience.org/sites/default/files/publications/FIREFACTS_Measures%20of%20fire%20behavior%20FINAL.pdf)  
- [Largest Wildfires in U.S. History](https://wfca.com/wildfire-articles/biggest-wildfires-in-us-history/)

---

## **Simulation Variables**

1. **Fire Spread Rate:**  
   - Each cell represents a distance of **46 chains** (~1 mile).  
   - Burn rate: according to the Northwest Fire Science Consortium, the rate of fire move across the landscape is **1 chain per hour**.  and when wildfire burn on bush, the rate become 46 chain per hour, burning through dense ponderosa pine with heavy surface fuels spreads at a
much slower rate of 5 chains/hour .


2. **Tree Types:**  
   - **Flammability:** Varies by species (e.g., pine, oak, willow, bush).  
   - **Burn Rate:** Specific rates for each tree type.  

3. **Water Bodies:**  
   - Lakes, rivers, and streams act as natural firebreaks, reducing fire spread probabilities.  

4. **Humidity:**  
   - Higher humidity lowers burn probability.  

5. **Temperature:**  
   - Elevated temperatures increase burn probability.  

6. **Wind Conditions:**  
   - **Wind Speed:**  
     - Simulated based on real-world conditions and categorized by the Beaufort scale:
       | Beaufort Scale | Wind Speed (mph) | Wind Speed (chain/hr) |
       |----------------|-------------------|-----------------------|
       | 0 (Calm)       | 0-1               | 0-181.08              |
       | 1 (Light Air)  | 2-3               | 362.16-543.24         |
       | 2 (Light Breeze)| 4-7              | 724.32-1272.48        |
       | ...            | ...               | ...                   |
       | 12 (Hurricane) | 73+               | 14016.48+             |

   - **Wind Direction:**  
     - Includes **North (N), South (S), West (W), East (E)**.  

---




## Hypothesis 1
### Hypothesis : The burned area is expected to increase by approximately 50% when the ignition point originates from bushland compared to forested areas composed of willow, pine, and oak trees.

1. Independent variable : ignition point location (bush or non-bush)
2. Dependent variable : burned area, duration
3. Controlled variables : tree type, water bodies, humidity, temperature, wind condition

We conducted the simulation 50 times for each of two scenarios: one where the ignition point was on a bush, and another where it was in a forest (willow, oak, or pine trees). Subsequently, we analyzed how the statistical results differed between these two scenarios.
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis1_001.png)
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis1_002.png)

### **Statistical Result**

From the simulation results:
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis1_01.png)
- **Burned Area Percentage:**
  - **Fire at Bushland:** Mean = 30.58%, Std = 17.68%
  - **Fire at Non-Bushland:** Mean = 26.28%, Std = 21.12%

Fires in bushland tend to spread slightly faster and burn a larger percentage of the area compared to non-bushland fires.
The burned area from fires ignited in bushland is, on average, **16.37% larger** than that from fires in non-bushland areas. This is significantly smaller than the hypothesized **50% increase**.
Thus, **the hypothesis is not fully supported** based on these simulation results. While fires in bushland do tend to burn larger areas, the difference is more modest than expected.

---

### **Plot**
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis1_02.png) 
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis1_03.png)
1. **Box Plot of Burned Area:**
   - The variability in burned area for non-bushland is higher, as shown by the broader whiskers in the box plot.
   - The median burned area for bushland fires is higher than for non-bushland, but the overlap in interquartile ranges indicates that the difference is not as pronounced as hypothesized.
2. **Box Plot of Duration:**
   - From the duration box plot, the distributions for bushland and non-bushland durations appear largely similar, with some overlap.
   - The median duration of bushland fires is slightly shorter than that of non-bushland fires, indicating that bushland fires burn more quickly.
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis1_04.png)
2. **Scatter Plot of Burned Area vs. Duration:**
   - Both categories show a positive correlation between burned area and duration, with bushland fires generally burning slightly more area for comparable durations.


---

### **Conclusion**
Fires originating in bushland tend to last slightly longer, likely due to the larger area burned.
The overlap in duration ranges indicates that fire behavior is influenced by other factors beyond the ignition point type.
The hypothesis that fires in bushland result in a **50% larger burned area** compared to non-bushland is **not supported** by this analysis. Instead, the actual increase in burned area is approximately **16.37%**. This suggests that while bushland ignition does increase fire spread, the effect is less pronounced than initially expected. 

## Hypothesis 2
### Hypothesis : The impact of humidity on the likelihood of wildfire spread in areas surrounding bodies of water

1. Independent variable :

   a. - Humidity levels in the surrounding area (e.g., high, medium, low humidity). This is manipulated to observe its effect on wildfire spread.
   
2. Dependent variable :
   
   a. - Likelihood of wildfire spread to areas surrounding bodies of water. This outcome is measured and depends on humidity levels.
   
3. Controlled variables :
   
   a. - Proximity to bodies of water:** The distance between the wildfire and the water body remains constant in the simulation.
   
   b. - Vegetation type and density:** Kept consistent in all areas.
   
   c. - Initial fire size and location:** The starting conditions for the wildfire are identical across scenarios.

### **Color Scale:**

- **Red:** High fire probability
- **Yellow:** Medium fire probability
- **Black:** Low fire probability
- **Blue Boxes:** Denote water bodies, which typically act as natural fire barriers.

### Result

![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis/Screenshot%202024-12-10%20at%2011.26.10%E2%80%AFAM.png)

The heatmap shows that areas near water bodies are less likely to experience fire spread. The fire probability near the water body is 0, indicating that increased humidity around water bodies significantly reduces the likelihood of wildfire spread.

![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis/Screenshot%202024-12-10%20at%2011.34.21%E2%80%AFAM.png)
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis/Screenshot%202024-12-10%20at%2011.34.32%E2%80%AFAM.png)

The statistical analysis supports this conclusion, with cells near the water body showing a lower mean fire probability. The median fire probability near the water body is 0, much lower than the median fire probability of cells farther from the water. This demonstrates that increased humidity near water bodies plays a significant role in reducing wildfire spread.
>>>>>>> origin/main


## Hypothesis 3
### Hypothesis : As wind speed increases, wildfire spread accelerates, leading to shorter burn durations for a given area.

1. Independent variable : wind speed 
2. Dependent variable : burned area, duration
3. Controlled variables : wind direction,tree type, water bodies, humidity, temperature

We conducted the hypothesis test under four different wind speed conditions to observe how the burn patterns changed.

### **Burn Probability Heatmap**

![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_01.png)

wind = 0

![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_00.png)

wind = 5

![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_05.png)

wind = 10

![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_10.png)

wind = 20

![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_20.png)

wind = 30

![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_30.png)

As observed from the changes in burn patterns, transitioning from no wind (wind speed = 0) to strong wind (wind speed = 30), the fire spreads in all directions when there is no wind, avoiding only water bodies. However, as the wind speed increases, the burn pattern becomes more pronounced on the downwind side. Conversely, the upwind side shows reduced burning as the wind becomes stronger.


### **Statistical Results**

From the simulation results:  
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_stat.png)

- As wind speed increases, the burned area initially increases slightly (from 0 to 5 m/s) but then decreases steadily at higher wind speeds (10 m/s and above).
- The duration of the wildfire consistently decreases with increasing wind speed, supporting the hypothesis that higher wind speeds result in faster fire spread and shorter burn times.

---

### **Plot**
 
1. **Burned Area Distribution (Box Plot):**  
   ![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_box1.png) 
   - The variability in burned area is highest at 0 m/s, indicating more inconsistent fire spread in calm wind conditions.
   - The burned area slightly increases at 5 m/s but decreases significantly at higher wind speeds, suggesting that high wind speeds might create conditions where fires burn out more quickly.

2. **Duration Distribution (Box Plot):**  
   ![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_box2.png)  
   - Fire duration consistently decreases with increasing wind speed, reflecting faster fire spread and burnout at higher wind speeds.
   - The variability in fire duration is highest at 0 m/s and becomes minimal at 20 and 30 m/s, indicating more consistent fire behavior under strong wind conditions.

3. **Burned Area vs. Duration (Scatter Plot):**  
   ![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/hypothesis2_scatter.png)   
   - Higher wind speeds result in data points clustered in the lower-left quadrant, indicating smaller burned areas and shorter durations.
   - At 0 and 5 m/s, data points are more spread out, showing greater variability in fire behavior.

---

### **Conclusion**
The hypothesis that higher wind speeds lead to faster wildfire spread and shorter burn durations is **partially supported**:
- **Duration:** The duration consistently decreases with higher wind speeds, validating the hypothesis for burn time.  
- **Burned Area:** The burned area shows a non-linear relationship, increasing slightly at moderate wind speeds (5 m/s) but decreasing at higher wind speeds (10-30 m/s). This suggests that very high wind speeds may contribute to faster fire extinguishment due to more rapid fuel consumption or dispersal of fire. i


## Validation 1
### Validation : The impact of seasons (humidity & temperature) on wildfire spread

1. Independent variable :
   
   a. - Humidity levels (varied by season)
   
   b. - Temperature levels (varied by season)
   
2. Dependent variable :
   
   a. - Likelihood of fire ignition
   
3. Controlled variables :
    
   a. - Wind speed and direction (constant)
   
   b. - Vegetation type and density (constant)
   
   c. - Initial fire size and location (identical)
   
### Result
#### Winter vs. Summer Heatmaps

##### Winter
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/validation/Screenshot%202024-12-09%20at%2011.01.18%E2%80%AFPM.png)
#### Summer
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/validation/Screenshot%202024-12-09%20at%209.25.15%E2%80%AFPM.png)

In winter, most areas remain unaffected, with only the fire’s starting point showing slightly elevated burn probabilities. In contrast, the summer heatmap shows widespread fire propagation, with most regions having nearly 100% burn probability.

![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/validation/Screenshot%202024-12-10%20at%2012.08.35%E2%80%AFPM.png)
![image](https://github.com/chiayu-wow/2024Fall_projects/blob/main/image/validation/Screenshot%202024-12-10%20at%2012.00.50%E2%80%AFPM.png)

Statistical comparisons reveal the mean fire spread is much higher in summer, and the median fire spread jumps from 0 in winter to 75 in summer. These findings confirm that seasonal variations, particularly temperature and humidity, significantly affect wildfire spread.


## Sources
- [Fire Behavior Measures](https://nwfirescience.org/sites/default/files/publications/FIREFACTS_Measures%20of%20fire%20behavior%20FINAL.pdf)  
- [Wildfire Patterns](https://wfca.com/wildfire-articles/biggest-wildfires-in-us-history/)