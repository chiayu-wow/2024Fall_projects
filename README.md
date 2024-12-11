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
The impact of the ignition point location (vegetation type) on the burning area and duration of wildfires .... 
1. Independent variable : fire spread rate, burned probability(randomize)
2. Dependent variable : burned area, duration
3. Controlled variables : tree type, water bodies, humidity, temperature, wind condition
We run the simulation in two situation each 50 times. one is the ignition point is on bush, and the other is on the forest(willow, oak or pine tree). 
Afterward, we see how the statistic result varied from this two situation.
### Result

From the simulation results:

- **Burned Area Percentage:**
  - **Fire at Bushland:** Mean = 30.58%, Std = 17.68%
  - **Fire at Non-Bushland:** Mean = 26.28%, Std = 21.12%
  
- **Percentage Increase in Burned Area:**
  \[
  \text{Increase} = \frac{\text{Bush Mean Burned Area} - \text{Non-Bush Mean Burned Area}}{\text{Non-Bush Mean Burned Area}} \times 100\%
  \]
  Substituting the values:
  \[
  \text{Increase} = \frac{30.58 - 26.28}{26.28} \times 100\% = 16.37\%
  \]

#### **Conclusion of Burned Area Comparison**
The burned area from fires ignited in bushland is, on average, **16.37% larger** than that from fires in non-bushland areas. This is significantly smaller than the hypothesized **50% increase**.  

Thus, **the hypothesis is not fully supported** based on these simulation results. While fires in bushland do tend to burn larger areas, the difference is more modest than expected.

---

### **Visual Evidence**
1. **Box Plot of Burned Area:**
   - The median burned area for bushland fires is higher than for non-bushland, but the overlap in interquartile ranges indicates that the difference is not as pronounced as hypothesized.

2. **Scatter Plot of Burned Area vs. Duration:**
   - Both categories show a positive correlation between burned area and duration, with bushland fires generally burning slightly more area for comparable durations.

---

### **Possible Reasons for Discrepancy**
1. **Randomness in Fire Spread:**
   - The Monte Carlo simulation introduces stochastic elements, which may have reduced the observed differences between the two categories.

---

### **Conclusion**
The hypothesis that fires in bushland result in a **50% larger burned area** compared to non-bushland is **not supported** by this analysis. Instead, the actual increase in burned area is approximately **16.37%**. This suggests that while bushland ignition does increase fire spread, the effect is less pronounced than initially expected. Further analysis incorporating additional environmental variables may provide deeper insights.

## Hypothesis 2
### Hypothesis : 
(explanation)
1. Independent variable :
2. Dependent variable :
3. Controlled variables :
### Result
(plot)
(analyze description)
(conclusion)

## Hypothesis 3
### Hypothesis : The impact of humidity on the likelihood of wildfire spread in areas surrounding bodies of water

1. Independent variable :
   a. - Humidity levels in the surrounding area (e.g., high, medium, low humidity). This is manipulated to observe its effect on wildfire spread.
2. Dependent variable :
   a. - Likelihood of wildfire spread to areas surrounding bodies of water. This outcome is measured and depends on humidity levels.
5. Controlled variables :
   a. - Proximity to bodies of water:** The distance between the wildfire and the water body remains constant in the simulation.
   b. - Vegetation type and density:** Kept consistent in all areas.
   c. - Initial fire size and location:** The starting conditions for the wildfire are identical across scenarios.

### **Color Scale:**

- **Red:** High fire probability
- **Yellow:** Medium fire probability
- **Black:** Low fire probability
- **Blue Boxes:** Denote water bodies, which typically act as natural fire barriers.

### Result

The heatmap shows that areas near water bodies are less likely to experience fire spread. The fire probability near the water body is 0, indicating that increased humidity around water bodies significantly reduces the likelihood of wildfire spread.


The statistical analysis supports this conclusion, with cells near the water body showing a lower mean fire probability. The median fire probability near the water body is 0, much lower than the median fire probability of cells farther from the water. This demonstrates that increased humidity near water bodies plays a significant role in reducing wildfire spread.

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
# Winter vs. Summer Heatmaps

In winter, most areas remain unaffected, with only the fire’s starting point showing slightly elevated burn probabilities. In contrast, the summer heatmap shows widespread fire propagation, with most regions having nearly 100% burn probability.

Statistical comparisons reveal the mean fire spread is much higher in summer, and the median fire spread jumps from 0 in winter to 75 in summer. These findings confirm that seasonal variations, particularly temperature and humidity, significantly affect wildfire spread.

## Conclusion
1. ...

## Sources
