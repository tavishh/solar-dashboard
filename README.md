# Solar Data Optimisation Analytics Dashboard

An interactive research dashboard visualising solar irradiance, multi-site PV power output, and geographic dispersion optimisation across **9 PV sites in Mauritius**.

Built as part of peer-reviewed research on grid stability and renewable energy optimisation.

**[▶ Live Demo](https://solar-dashboard-tavishh.streamlit.app/)** &nbsp;·&nbsp;

---

## Overview

This dashboard presents the results of a 3-stage GRG (Generalised Reduced Gradient) optimisation algorithm applied to geographically distributed PV systems. The core research question: can strategically weighting output from multiple spatially separated solar sites reduce grid intermittency caused by moving cloud cover?

**Answer: yes — by up to 67%.**

---

## Screen Capture

<img width="2518" height="919" alt="image" src="https://github.com/user-attachments/assets/0b86643a-a1c6-41ad-ad08-cbcbe948c32b" />

---
## Features

| Tab | Description |
|-----|-------------|
| Before vs After Optimization| Single-site (spiky) vs GRG-optimised combined output with ramp rate comparison |
| Irradiance by Site | Day-level irradiance curves per site with daily statistics |
| Monthly Overview | Heatmap of daily peak irradiance + monthly ramp rate trend |
| Research & Pipeline | Abstract data pipeline (raw → BSRN QC → GRG optimisation) + publications |

---

## Tech Stack

- **Python** — data processing and pipeline logic
- **Streamlit** — interactive web application framework
- **Plotly** — interactive charts and visualisations
- **Pandas / NumPy** — data ingestion and computation

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/tavishh/solar-dashboard.git
cd solar-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`. The January 2020 dataset is bundled in `data/`. You can also upload other monthly files (e.g. `03_March.xlsx`) via the sidebar.

---

## Deploy to Streamlit Community Cloud (Free)

1. Push this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set main file to `app.py`
4. Click **Deploy** — you'll get a public URL in ~2 minutes

---

## Data

- **Sites:** 9 PV installations across Mauritius (Curepipe, La Mivoie, Ferney, Mahebourg, Souillac, Goodlands, Rose Hill, Nicolay, Bramsthan)
- **Resolution:** 1-minute irradiance and power output readings
- **Volume:** ~840 readings/site/day · 200,000+ records per month
- **Quality:** 99.74% data validated against BSRN international standards
- **Format:** Excel workbook with one sheet per day + monthly summary

---

## Research & Publications

This dashboard visualises results from the following peer-reviewed work:

1. **Hookoom, T., Bangarigadu, K., Ramgolam, Y.K.** (2022). *Optimisation of Geographically Deployed PV Parks for Reduction of Intermittency to Enhance Grid Stability.* Renewable Energy Journal (Elsevier). 

2. **Ramgolam, Y., Bangarigadu, K., Hookoom, T.** (2020). *A Robust Methodology for Assessing the Effectiveness of Site Adaptation Techniques for Calibration of Solar Radiation Data.* Journal of Solar Energy Engineering, 143(3). ASME.

3. **Bangarigadu, K., Hookoom, T., Ramgolam, Y., Kune, N.** (2020). *Analysis of Solar Power and Energy Variability Through Site Adaptation of Satellite Data With Quality Controlled Measured Solar Radiation Data.* Journal of Solar Energy Engineering, 143(3). ASME.

4. **Ramiah, C., Bangarigadu, K., Hookoom, T., Ramgolam, Y.K.** (2023). *A Novel and Holistic Framework for The Selection of Performance Indicators To Appraise Photovoltaic Systems.* Solar World Congress 2023. [DOI: 10.18086/swc.2023.08.05](https://doi.org/10.18086/swc.2023.08.05)

5. **Hookoom, T., Bangarigadu, K., Ramiah, C., Ramgolam, Y.K.** (2024). *Strengthening health services with quality in a net zero transition.* Book Chapter — The Elgar Companion to Energy and Sustainability.

---

## Author

**Tavish Hookoom**  
[github.com/tavishh](https://github.com/tavishh)

---

*Raw research data is proprietary. Illustrative signals in the pipeline tab are synthetically generated. All statistics (99.74%, 200,000+ records, 67% reduction) are from published peer-reviewed work. Data provided is courtesy of Dr. Yatindra Ramgolam and the University of Mauritius.*
