"""
ESX Market Dashboard
Interactive analytics & valuation dashboard for the Ethiopian Securities Exchange (ESX)
Built by Natnael Seyum Haile
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="ESX Market Dashboard", layout="wide")
st.title("🇪🇹 ESX Market Dashboard")
st.markdown("**Analytics & valuation for the Ethiopian Securities Exchange**")

LISTED_COMPANIES = pd.DataFrame([
    {"Ticker": "WGBX", "Company": "Wegagen Bank S.C.", "Sector": "Banking",
     "Listed": "2025-01-10", "Method": "Listing by introduction"},
    {"Ticker": "GADAA", "Company": "Gadaa Bank S.C.", "Sector": "Banking",
     "Listed": "2025", "Method": "Listing by introduction"},
    {"Ticker": "AWASH", "Company": "Awash Bank S.C.", "Sector": "Banking",
     "Listed": "2026-04", "Method": "Listing by introduction"},
    {"Ticker": "TELE", "Company": "Ethio Telecom S.C.", "Sector": "Telecom",
     "Listed": "2026-05-26", "Method": "Public offering"},
    {"Ticker": "ABAYB", "Company": "Abay Bank S.C.", "Sector": "Banking",
     "Listed": "2026-06-30", "Method": "Listing by introduction"},
])

WEGAGEN = {
    "net_profit_birr": 2_777_510_000,
    "total_equity_birr": 12_807_973_000,
    "shares_outstanding": 6_200_000,
    "par_value": 1_000,
    "roe_pct": 25.3,
    "npl_pct": 3.8,
    "last_price": 1_050.31,
    "price_as_of": "2026-03-10",
}

page = st.sidebar.selectbox("Navigate", [
    "Market Overview", "Valuation Models", "Credit Risk", "Portfolio Simulator", "About",
])

if page == "Market Overview":
    st.header("Market Snapshot")
    st.caption("Listed companies as of the ESX 2025/26 fiscal year (source: esx.et)")
    st.dataframe(LISTED_COMPANIES, use_container_width=True, hide_index=True)
    st.metric("Companies Listed", len(LISTED_COMPANIES))
    st.info("ESX does not publish a public market-data API. This table is manually "
            "curated from ESX's own disclosure directory and will be updated as new "
            "companies list.")

elif page == "Valuation Models":
    st.header("Equity Valuation Tool")
    company = st.selectbox("Select company", ["Wegagen Bank S.C. (WGBX)"])

    if company.startswith("Wegagen"):
        w = WEGAGEN
        eps = w["net_profit_birr"] / w["shares_outstanding"]
        bvps = w["total_equity_birr"] / w["shares_outstanding"]
        pe = w["last_price"] / eps
        pb = w["last_price"] / bvps

        st.subheader("Fundamentals — FY2024/25 (year ended 30 June 2025)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("EPS (Birr)", f"{eps:,.0f}")
        c2.metric("Book Value/Share (Birr)", f"{bvps:,.0f}")
        c3.metric("P/E", f"{pe:.2f}x")
        c4.metric("P/B", f"{pb:.2f}x")
        st.caption(f"Last price: {w['last_price']:,.2f} ETB as of {w['price_as_of']} "
                   f"(ESX main board). ROE {w['roe_pct']}%, NPL ratio {w['npl_pct']}%.")

        st.markdown("---")
        st.subheader("Dividend Discount Model (Gordon Growth)")
        st.caption("Wegagen's dividend per share is not yet confirmed from a public source, "
                   "so it's left as an input below rather than assumed — adjust to test scenarios.")

        col1, col2 = st.columns(2)
        with col1:
            dps = st.number_input("Estimated dividend per share (Birr)", min_value=0.0,
                                   value=float(round(eps * 0.3)), step=10.0,
                                   help="Default assumes a 30% payout ratio — edit if you have a confirmed figure.")
            req_return = st.slider("Required rate of return (%)", 10.0, 35.0, 20.0, 0.5)
        with col2:
            growth = st.slider("Terminal dividend growth rate (%)", 0.0, 20.0, 8.0, 0.5)
            st.metric("Implied ROE (sanity check)", f"{w['roe_pct']}%")

        if req_return > growth:
            ddm_value = dps * (1 + growth / 100) / (req_return / 100 - growth / 100)
            st.metric("DDM Fair Value (Birr/share)", f"{ddm_value:,.0f}",
                       delta=f"{ddm_value - w['last_price']:,.0f} vs. last price")
            if ddm_value > w["last_price"]:
                st.success("Model implies undervaluation at current inputs.")
            else:
                st.warning("Model implies overvaluation at current inputs.")
        else:
            st.error("Required return must exceed growth rate for the model to converge.")

        st.markdown("---")
        st.caption("Sources: Wegagen Bank FY2024/25 Annual Report (esx.et/directory), "
                   "Capital Market Ethiopia (capitalmarketethiopia.com), ESX main board pricing.")

    st.info("Additional companies (Gadaa, Awash, Ethio Telecom, Abay Bank) will be "
            "added as their audited financials become available on esx.et.")

elif page == "Credit Risk":
    st.header("EthioScore Credit Engine")
    st.warning("Not yet built. Will integrate scoring logic from the separate "
               "EthioScore project once the interface between the two is defined.")

elif page == "Portfolio Simulator":
    st.header("Portfolio Simulator")
    st.warning("Not yet built.")

else:
    st.header("About")
    st.markdown("Built by **Natnael Seyum Haile**. Tracks Ethiopian Securities Exchange "
                "listings and provides equity valuation tools using publicly disclosed "
                "financial data. Companion project to EthioBank Intelligence Hub and EthioScore.")

st.sidebar.markdown("---")
st.sidebar.caption("Built by Natnael Seyum Haile")
