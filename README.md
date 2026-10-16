# Wikipedia Pageview Forecasting



A multi-horizon time-series forecasting project that uses Wikipedia pageview data to predict future traffic for individual articles.



---



## 1. Project Goal



Build a forecasting system that can answer:



> **"Given the historical pageviews of a Wikipedia article, how many views should we expect over the next N days?"**



The project will focus on:



- Time-series analysis

- Seasonality and trend detection

- Multi-horizon forecasting

- Model comparison

- Forecast uncertainty

- Anomaly/spike detection

- A clean prediction pipeline that can eventually be exposed through an API/UI



---



# 2. Data Source



### Wikimedia Pageviews API



Use the Wikimedia REST API to collect historical pageview data.



### Initial target



Start with a small set of articles, then expand.



Example:



```text

Python_(programming_language)

Machine_learning

Artificial_intelligence

Linux

Data_science

```



### Data fields



Expected structure:



```text

project

article

granularity

timestamp

access

agent

views

```



---



# 3. Current Data Pipeline



```text

Wikimedia API

      ↓

Raw JSON

      ↓

Data Cleaning

      ↓

Pandas DataFrame

      ↓

Processed CSV

      ↓

EDA

      ↓

Feature Engineering

      ↓

Forecasting Models

      ↓

Evaluation

      ↓

Final Forecast

```



Current files:



```text

data/

├── data.json

└── processed.csv

```



---



# 4. Phase 1 — Data Collection



## Tasks



- [x] Connect to Wikimedia Pageviews API

- [x] Handle API authentication/request requirements

- [x] Add appropriate User-Agent

- [x] Download pageview data

- [x] Save raw API response

- [x] Parse JSON into Pandas

- [x] Convert timestamps

- [x] Export processed CSV



### Future improvements



- [ ] Build reusable API client

- [ ] Support multiple articles

- [ ] Support custom date ranges

- [ ] Add retry logic

- [ ] Handle API rate limits

- [ ] Cache downloaded data

- [ ] Automate dataset updates



---



# 5. Phase 2 — Exploratory Data Analysis



Understand the structure and behavior of Wikipedia traffic before modeling.



## 5.1 Basic Statistics



Analyze:



- Mean views

- Median views

- Minimum views

- Maximum views

- Standard deviation

- Percentiles



Questions:



- How volatile is the traffic?

- Are there extreme spikes?

- Is the distribution heavily skewed?



---



## 5.2 Time-Series Visualization



Plot:



```text

Date → Views

```



For each article.



Investigate:



- Long-term trends

- Sudden spikes

- Sudden drops

- Periodic behavior

- Stable vs volatile articles



---



## 5.3 Seasonality



Investigate:



### Weekly seasonality



Do views behave differently on:



- Monday

- Tuesday

- ...

- Sunday



### Monthly/annual seasonality



Check whether traffic changes depending on:



- Month

- Season

- Holidays

- Major recurring events



---



## 5.4 Rolling Statistics



Calculate:



- 7-day rolling mean

- 14-day rolling mean

- 30-day rolling mean

- Rolling standard deviation



Example:



```python

df["rolling_7"] = df["views"].rolling(7).mean()

```



Use these to identify underlying trends.



---



# 6. Phase 3 — Data Preprocessing



Before training models:



- [ ] Sort by timestamp

- [ ] Remove duplicate timestamps

- [ ] Handle missing values

- [ ] Detect invalid values

- [ ] Check for missing dates

- [ ] Resample if necessary

- [ ] Ensure continuous daily frequency



---



## 6.1 Outliers



Wikipedia traffic can contain massive spikes.



Determine whether a spike is:



1. A genuine event

2. An API/data issue

3. An anomaly that should be retained



Do **not automatically remove spikes**.



For forecasting, genuine spikes may contain useful information.



---



## 6.2 Transformations



Experiment with:



### Raw views



```text

y = views

```



### Log transformation



```text

y = log1p(views)

```



Compare model performance on both.



---



# 7. Phase 4 — Feature Engineering



Create time-series features.



## Calendar Features



```text

day_of_week

day_of_month

month

week_of_year

quarter

day_of_year

is_weekend

```



---



## Lag Features



Create historical dependencies:



```text

lag_1

lag_2

lag_3

lag_7

lag_14

lag_21

lag_28

```



Example:



```python

df["lag_7"] = df["views"].shift(7)

```



---



## Rolling Features



```text

rolling_mean_7

rolling_mean_14

rolling_mean_28



rolling_std_7

rolling_std_14

rolling_std_28

```



---



## Trend Features



Potential features:



```text

days_since_start

trend

growth_rate

```



---



# 8. Phase 5 — Train/Validation/Test Split



**Never randomly split the time series.**



Use chronological splitting.



Example:



```text

|--------- Train ---------|---- Validation ----|---- Test ----|

        70%                     15%                 15%

```



Or:



```text

Past -------------------------------> Future



Train → Validation → Test

```



The test set must represent unseen future data.



---



# 9. Phase 6 — Baseline Models



Before using complicated ML models, establish strong baselines.



## Baseline 1 — Naive



Predict tomorrow as:



```text

y(t+1) = y(t)

```



---



## Baseline 2 — Weekly Naive



Predict using the value from 7 days ago:



```text

y(t+1) = y(t-6)

```



More generally:



```text

forecast = value from previous week

```



This is particularly important because Wikipedia traffic may contain weekly seasonality.



---



## Baseline 3 — Moving Average



Predict using the recent average:



```text

forecast = mean(last N observations)

```



Test:



```text

7-day

14-day

28-day

```



These baselines establish whether ML is actually providing value.



---



# 10. Phase 7 — Statistical Forecasting



Experiment with classical time-series models.



## ARIMA



Test:



```text

ARIMA

```



Understand:



- Autoregression

- Differencing

- Moving average



---



## SARIMA



If strong seasonality is present:



```text

SARIMA

```



Potential seasonal period:



```text

7 days

```



---



## Exponential Smoothing



Experiment with:



- Simple Exponential Smoothing

- Holt

- Holt-Winters



These provide useful comparisons against ML models.



---



# 11. Phase 8 — Machine Learning Models



Move to supervised ML using engineered lag/rolling features.



## Model 1 — Linear Regression



Simple benchmark.



```text

Features → Linear Regression → Forecast

```



---



## Model 2 — Random Forest



Use:



```text

lag features

calendar features

rolling statistics

```



---



## Model 3 — XGBoost



Likely one of the strongest candidates.



Features:



```text

lags

rolling statistics

calendar features

trend

```



Target:



```text

future pageviews

```



---



# 12. Phase 9 — Multi-Horizon Forecasting



This is one of the main goals of the project.



Instead of predicting only tomorrow, predict:



```text

t+1

t+2

t+3

...

t+7

```



Then extend to:



```text

7-day forecast

14-day forecast

30-day forecast

```



---



## Strategy A — Recursive Forecasting



Train:



```text

t → t+1

```



Then use the prediction as an input for:



```text

t+1 → t+2

```



Continue recursively.



### Advantage



Simple architecture.



### Problem



Prediction errors can accumulate.



---



## Strategy B — Direct Forecasting



Train separate models:



```text

Model 1 → t+1

Model 2 → t+2

Model 3 → t+3

...

Model 30 → t+30

```



### Advantage



Avoids recursive error accumulation.



### Problem



Requires multiple models.



---



## Strategy C — Multi-Output Forecasting



One model predicts:



```text

[t+1, t+2, ..., t+30]

```



This should also be investigated.



---



# 13. Phase 10 — Evaluation



Use time-series appropriate metrics.



## MAE



```text

Mean Absolute Error

```



Easy to interpret.



---



## RMSE



```text

Root Mean Squared Error

```



Penalizes large errors more heavily.



---



## MAPE



Use carefully because pageviews can potentially approach zero.



---



## sMAPE



Consider using:



```text

Symmetric MAPE

```



for more stable percentage-based evaluation.



---



## Model comparison



Create a table:



| Model | MAE | RMSE | sMAPE |

|---|---:|---:|---:|

| Naive | | | |

| Weekly Naive | | | |

| Moving Average | | | |

| ARIMA | | | |

| SARIMA | | | |

| Random Forest | | | |

| XGBoost | | | |



---



# 14. Phase 11 — Rolling / Walk-Forward Validation



Instead of evaluating only once, simulate real forecasting.



Example:



```text

Train → Predict

Train + 1 day → Predict

Train + 2 days → Predict

Train + 3 days → Predict

...

```



This gives a more realistic estimate of model performance.



---



# 15. Phase 12 — Prediction Intervals



Point forecasts aren't enough.



Instead of:



```text

Tomorrow = 14,532 views

```



aim for:



```text

Expected: 14,532

Lower:    11,200

Upper:    18,900

```



Eventually investigate:



- Prediction intervals

- Quantile regression

- Quantile XGBoost

- Conformal prediction



---



# 16. Phase 13 — Spike / Anomaly Detection



Wikipedia pageviews can suddenly explode because of:



- News

- Viral events

- Celebrity events

- Product launches

- Political events

- Software releases

- Major announcements



Build an anomaly detector that identifies:



```text

Normal traffic

      ↓

Unexpected spike

      ↓

Flag anomaly

```



Possible approaches:



- Rolling z-score

- IQR

- Isolation Forest

- Residual-based anomaly detection



---



# 17. Phase 14 — External Signals



Potential future improvement:



Add external information that can explain traffic spikes.



Possible signals:



```text

Google Trends

News

Reddit activity

Wikipedia article metadata

Search trends

Event calendars

```



This turns the project from pure time-series forecasting into a more advanced **multivariate forecasting system**.



---



# 18. Phase 15 — Model Selection



After experimentation, select the best model based on:



- Overall error

- Performance at different horizons

- Stability

- Computational cost

- Ability to handle spikes

- Generalization across articles



Do not simply choose the model with the lowest single RMSE.



---



# 19. Phase 16 — Final Forecasting Pipeline



The final architecture should look approximately like:



```text

                 Wikipedia API

                       │

                       ▼

                Data Collection

                       │

                       ▼

                 Data Cleaning

                       │

                       ▼

               Feature Engineering

                       │

                       ▼

                Forecasting Model

                       │

              ┌────────┴────────┐

              ▼                 ▼

         Point Forecast    Prediction Interval

              │                 │

              └────────┬────────┘

                       ▼

                 Final Forecast

```



Input:



```text

Article: Python_(programming_language)

Horizon: 30 days

```



Output:



```text

Date          Prediction

2026-11-01    31,200

2026-11-02    30,800

2026-11-03    32,100

...

```



---



# 20. Future Application



Once the forecasting pipeline works, build a simple interface.



Possible stack:



```text

Frontend/UI

    ↓

Streamlit

    ↓

Forecasting API/Model

    ↓

Processed Dataset

```



User enters:



```text

Article

Forecast horizon

```



The application returns:



- Historical pageviews

- Forecast

- Confidence/prediction interval

- Trend

- Detected anomalies

- Model used



---



# 21. Project Structure



Proposed structure:



```text

wikipedia-forecasting/

│

├── data/

│   ├── raw/

│   │   └── data.json

│   │

│   └── processed/

│       └── processed.csv

│

├── notebooks/

│   ├── 01_data_collection.ipynb

│   ├── 02_eda.ipynb

│   ├── 03_feature_engineering.ipynb

│   ├── 04_baselines.ipynb

│   ├── 05_statistical_models.ipynb

│   ├── 06_ml_models.ipynb

│   └── 07_model_comparison.ipynb

│

├── src/

│   ├── data_collection.py

│   ├── preprocessing.py

│   ├── features.py

│   ├── baselines.py

│   ├── forecasting.py

│   ├── evaluation.py

│   └── anomaly_detection.py

│

├── models/

│

├── reports/

│

├── app/

│   └── app.py

│

├── requirements.txt

├── README.md

└── PLAN.md

```



---



# 22. Milestones



## Milestone 1 — Dataset



- [x] API connection

- [x] Raw data collection

- [x] DataFrame creation

- [x] Processed CSV



## Milestone 2 — Understanding the Data



- [ ] Complete EDA

- [ ] Identify trends

- [ ] Identify seasonality

- [ ] Investigate anomalies



## Milestone 3 — Baselines



- [ ] Naive

- [ ] Weekly Naive

- [ ] Moving Average



## Milestone 4 — Forecasting



- [ ] ARIMA

- [ ] SARIMA

- [ ] XGBoost

- [ ] Compare models



## Milestone 5 — Multi-Horizon



- [ ] 7-day

- [ ] 14-day

- [ ] 30-day

- [ ] Compare recursive vs direct forecasting



## Milestone 6 — Advanced



- [ ] Prediction intervals

- [ ] Anomaly detection

- [ ] Walk-forward validation

- [ ] External signals



## Milestone 7 — Product



- [ ] Streamlit interface

- [ ] Article search/input

- [ ] Interactive forecast graph

- [ ] Model metrics

- [ ] Deploy



---



# 23. Final Goal



The finished project should demonstrate that we can take:



```text

Historical Wikipedia pageviews

```



and turn them into:



```text

Reliable multi-horizon forecasts

        +

Uncertainty estimates

        +

Anomaly detection

        +

Interactive visualization

```



The project should prioritize **good forecasting methodology over simply using a more complicated model**.



The progression should be:



```text

Understand the data

        ↓

Build strong baselines

        ↓

Try statistical models

        ↓

Try ML models

        ↓

Evaluate properly

        ↓

Build multi-horizon forecasting

        ↓

Add uncertainty

        ↓

Add anomaly detection

        ↓

Build the application

```



---



## Current Priority



**Do not jump directly into LSTM/Transformers.**



First establish:



1. Clean dataset

2. EDA

3. Naive baselines

4. Weekly baseline

5. Feature engineering

6. XGBoost

7. Proper time-series validation

8. Multi-horizon forecasting

9. Model comparison



Only after this should more complex deep-learning approaches be considered.
