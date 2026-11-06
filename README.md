# Group-14-TIL6022
This is the repository of Group 14 for the project under the TIL6022 course at TU Delft

Group 14: Bart Stevens, Chris van Bodegom, Freek Koch, Jiska Boersma, Sophia Bakker

# Railway Resilience During Large-Scale Events
## 1. Overview

This project investigates how the Dutch railway network responds to increased passenger demand during Kingsday.  
The analysis compares train services, delays and passenger volumes on Kingsday with comparable days.  

**Main research question:**  
> How resilient is the Dutch railway network's operational performance, measured by train delays and cancellations during King’s Day?

## 2. Data Sources & Reproduction

This repository contains: 
- Initial Datasets: 
1. Train Delay time data in 2024 [Rijden de Treinen](https://www.rijdendetreinen.nl/) 
2. Train disruption data in 2024 [Rijden de Treinen](https://www.rijdendetreinen.nl/) 
3. Passenger volume data  [https://translink.nl/open-data/]

- Filtered Datasets: 
1. Filtered Delay Time data of all the saturdays in 2024  (the code used for this filtering can be found under the name 'General Data filtering)

In Project_Group_14: The research questions and explanation on the analysis can be found
In the folder of Data analysis the different python code files for filtering, analysis and visualizations for each of the subquestions can be found. 


The project is developed in **Python** and uses standard data-analysis and visualisation libraries.

**Requirements packages installed:**
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `plotly`