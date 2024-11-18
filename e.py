import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(
    page_title="S&P 500 Sector ETF Dashboard",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Customizing the sidebar
st.sidebar.title("ETF Chart Selection")
st.sidebar.markdown("Select a sector ETF to explore its performance and compare metrics.")

# Create a radio button to select the ETF
selected_etf = st.sidebar.radio("Select a Sector Specific ETF", (
    ("XLC", "Communication Services"),
    ("XLY", "Consumer Discretionary"),
    ("XLP", "Consumer Staples"),
    ("XLE", "Energy"),
    ("XLF", "Financials"),
    ("XLV", "Health Care"),
    ("XLI", "Industrials"),
    ("XLK", "Information Technology"),
    ("XLB", "Materials"),
    ("XLRE", "Real Estate"),
    ("XLU", "Utilities")
))

# Main title with an icon
st.title("📊 S&P 500 Sector ETF Dashboard")

# Download the selected ETF's data and S&P 500 data
ticker1 = selected_etf[0]
ticker2 = "^GSPC"  # Always download S&P 500 data

etf_data1 = yf.Ticker(ticker1)
sp500_data = yf.Ticker(ticker2)

hist1 = etf_data1.history(period="1y")
hist2 = sp500_data.history(period="1y")

# Enhanced chart design
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
fig.patch.set_facecolor('#f9f9f9')

# Plot the selected ETF on the left subplot (ax1)
ax1.plot(hist1.index, hist1['Close'], label=f"{selected_etf[1]} ({ticker1})", color='teal', linewidth=2)
ax1.set_title(f"{selected_etf[1]} ({selected_etf[0]}) Closing Price", fontsize=16, color='teal')
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Closing Price', fontsize=12)
ax1.grid(True, alpha=0.5)
ax1.xaxis.set_major_locator(MaxNLocator(6))
ax1.legend()

# Plot S&P 500 on the right subplot (ax2)
ax2.plot(hist2.index, hist2['Close'], label="S&P 500", color='orange', linewidth=2)
ax2.set_title("S&P 500 Closing Price", fontsize=16, color='orange')
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('Closing Price', fontsize=12)
ax2.grid(True, alpha=0.5)
ax2.xaxis.set_major_locator(MaxNLocator(6))
ax2.legend()

st.pyplot(fig)

# ETF Comparison Section
st.subheader("📈 Sector ETF Comparison")

# Create a selectbox to choose the second ETF for comparison
selected_etf2 = st.selectbox("Select a Second ETF for Metric Comparison", (
    ("XLC", "Communication Services"),
    ("XLY", "Consumer Discretionary"),
    ("XLP", "Consumer Staples"),
    ("XLE", "Energy"),
    ("XLF", "Financials"),
    ("XLV", "Health Care"),
    ("XLI", "Industrials"),
    ("XLK", "Information Technology"),
    ("XLB", "Materials"),
    ("XLRE", "Real Estate"),
    ("XLU", "Utilities")
))

# Download the second ETF's data
etf_data2 = yf.Ticker(selected_etf2[0])
info1 = etf_data1.info
info2 = etf_data2.info

# Create a DataFrame to store the comparison data
comparison_data = {
    f"{selected_etf[1]} ({selected_etf[0]})": [info1.get('trailingPE', 'N/A'), info1.get('volume', 'N/A'), info1.get('fiftyTwoWeekHigh', 'N/A'), info1.get('fiftyTwoWeekLow', 'N/A')],
    f"{selected_etf2[1]} ({selected_etf2[0]})": [info2.get('trailingPE', 'N/A'), info2.get('volume', 'N/A'), info2.get('fiftyTwoWeekHigh', 'N/A'), info2.get('fiftyTwoWeekLow', 'N/A')]
}

# Styled dataframe (without metric column)
df = pd.DataFrame(comparison_data, index=['PE Ratio', 'Average Volume', '52-Week High', '52-Week Low'])

# Display the table
st.table(df)

# News Feed Section
st.subheader(f"📰 {selected_etf[1]} ({selected_etf[0]}) News Feed")

# Get news headlines using yfinance
news = etf_data1.news

# Display the news headlines if there are any
if news:
    for article in news:
        st.markdown(f"- [{article['title']}]({article['link']})")
else:
    st.write("No news found for this ETF.")
