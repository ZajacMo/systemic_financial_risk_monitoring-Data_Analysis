# Systemic Financial Risk Monitoring - Data Analysis

[![GitHub license](https://img.shields.io/github/license/ZajacMo/systemic_financial_risk_monitoring-Data_Analysis)](LICENSE)
[中文](README_CN.md)

## Project Introduction

This project aims to build a comprehensive systemic financial risk monitoring framework to analyze the risk status of China's financial market through multiple dimensions. The system integrates data from five dimensions: stock market, bond market, foreign exchange market, money market, and derivatives market. It utilizes methods such as Principal Component Analysis (PCA) and Markov regime switching to construct systemic financial risk pressure indices, and conducts risk regime identification and probability analysis.

## System Architecture

```
systemic_financial_risk_monitoring-Data_Analysis/
├── db/                  # Data storage directory
│   ├── data_股票市场维度.xlsx (Stock Market Dimension)
│   ├── data_债券市场维度.xlsx (Bond Market Dimension)
│   ├── data_外汇市场维度.xlsx (Foreign Exchange Market Dimension)
│   ├── data_货币市场维度.xlsx (Money Market Dimension)
│   └── data_衍生品市场维度.xlsx (Derivatives Market Dimension)
├── systemic_financial_risk_monitoring/  # Core code directory
│   ├── main.py          # Main program entry
│   ├── algorithm.py     # Algorithm implementation
│   ├── preprocessing.py # Data preprocessing
│   └── draw_img.py      # Image plotting
├── output/              # Output results directory
│   ├── img/             # Generated charts
│   ├── corr_*.xlsx      # Correlation analysis results
│   ├── loading_*.xlsx   # Factor loading results
│   └── contrib_*.xlsx   # Factor contribution results
├── docs/                # Documentation directory
└── LICENSE              # License file
```

## Core Features

### 1. Data Preprocessing Module
- Data cleaning and formatting
- Index volatility calculation (GARCH model)
- Data standardization and dimension unification
- Cumulative distribution ranking

### 2. Algorithm Analysis Module
- Principal Component Analysis (PCA): Dimensionality reduction and feature extraction
- Weighted synthesis of sub-market indices
- Systemic financial risk index construction
- Markov regime switching analysis
- Risk probability density estimation

### 3. Visualization Module
- Single line chart plotting (market pressure indices)
- Double line chart plotting (risk regime probabilities)
- Histogram plotting (probability density distribution)
- SVG format output support

## Technology Stack

- **Programming Language**: Python 3.8+
- **Data Analysis Libraries**: pandas, numpy, scipy
- **Statistical Analysis**: statsmodels
- **Volatility Model**: arch
- **Visualization**: matplotlib

## Key Indicator System

### Stock Market Dimension
- P/E Ratio Q
- Turnover Rate R
- Short/Long Ratio S
- Absolute Return Volatility U

### Bond Market Dimension
- Treasury Term Premium
- Comprehensive Risk Premium
- CSI Composite Bond Index Volatility

### Foreign Exchange Market Dimension
- RMB Exchange Rate Market Distortion
- USD/CNY Central Parity Rate Volatility

### Money Market Dimension
- Liquidity Premium
- Interbank Repo Rate Volatility
- SHIBOR Volatility

### Derivatives Market Dimension
- Stock Index Futures Price Deviation
- CSI 300 Index Futures Daily Log Return Volatility

## Usage

1. Ensure all necessary dependencies are installed:
```bash
pip install pandas numpy scipy statsmodels arch matplotlib
```

2. Prepare data files and place them in the `db` directory according to the required format

3. Run the main program:
```bash
cd systemic_financial_risk_monitoring
python main.py
```

4. Results will be output to the `output` directory, including:
   - Correlation matrices for each market dimension
   - Factor loading matrices
   - Factor contributions
   - Pressure index charts
   - Risk probability analysis results

## Model Implementation Details

### Principal Component Analysis (PCA)
- Select principal components with explained variance greater than 80% by calculating eigenvalues and eigenvectors
- Calculate factor loading matrices and factor contributions to determine key indicators

### Index Synthesis Method
- Synthesize sub-market indices using weighted average method based on key indicators selected in each market
- Integrate sub-market indices, considering correlations, to construct the final systemic financial risk pressure index

### Markov Regime Switching
- Use a two-state Markov switching model to identify "medium-low risk" and "high risk" regimes
- Calculate probability density distributions for each regime

## Project Value

1. **Risk Monitoring**: Real-time monitoring of systemic risk conditions in financial markets
2. **Early Warning**: Early warning of potential risks through risk regime switching analysis
3. **Policy Reference**: Providing data support for financial regulation and macroeconomic policy formulation
4. **Investment Decision**: Offering risk reference indicators for investment strategy development

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details