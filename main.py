import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title="StartUp Analysis")

df = pd.read_csv("cleaned_startup.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["month"] = df["date"].dt.month

def load_overall_analysis():
    st.title("Overall Analysis")

    # Total invested amount
    total = round(df['amount'].sum())
    # maximum amount infused in a startup
    max_funding=df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
    # Average ticket size
    avg_funding=df.groupby("startup")["amount"].sum().mean()
    # Total Funded startup
    total_funded = df["startup"].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total : ',str(total), 'Cr')
    with col2:
        st.metric('Max : ',str(max_funding), 'Cr')

    with col3:
        st.metric("Average Funding : ",str(round(avg_funding)),'Cr')

    with col4:
        st.metric("Total Funded StartUp : ",str(total_funded),'Startup')

def load_investor_details(investor):
    st.title(investor)
    # This show the recent 5 investement of the investor
    last5_df = df[df["investor"].str.contains(investor)].head()[
        ["date", "startup", "vertical", "city", "round", "amount"]
    ]
    st.subheader("Most recent investment")
    st.dataframe(last5_df)

    col1,col2,col3=st.columns(3)
    with col1:

        # Biggest investment
        big_df = (
            df[df["investor"].str.contains(investor)]
            .groupby("startup")["amount"]
            .sum()
            .sort_values(ascending=False)
        ).head()
        st.subheader("Biggest Investment")
        # st.dataframe(big_df)
        fig, ax=plt.subplots()
        ax.bar(big_df.index,big_df.values)

        st.pyplot(fig)

    with col2:
        vertical_series = df[df["investor"].str.contains(investor)].groupby("vertical")["amount"].sum().head()

        st.subheader("Sector Invested")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f%%')

        st.pyplot(fig1)
    
    # col3 = st.columns(1)
    with col3:
        df["year"] = df["date"].dt.year
        year_series=df[df["investor"].str.contains(investor)].groupby("year")[
            "amount"
        ].sum().head()
        st.subheader("YoY Investment")
        fig2, ax2 = plt.subplots()
        ax2.plot(year_series.index,year_series.values)

        st.pyplot(fig2)


st.sidebar.title("StartUp Funding analysis")

option = st.sidebar.selectbox("Select One", ["Overall Analysis", "StartUp", "Investor"])

if option == "Overall Analysis":
    # st.title("Overall Analysis")
    # st.balloons()
    btn0=st.sidebar.button("Show Overall Analysis")

    if btn0:
        load_overall_analysis()


elif option == "StartUp":
    st.sidebar.selectbox(
        "Select StartUp ", sorted(df["startup"].unique().tolist())
    )
    btn1 = st.sidebar.button("Find StartUp Details")
    st.title("StartUp Analysis")
else:
    selected_investor=st.sidebar.selectbox("Select StartUp ", sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)
    st.title("Investor Analysis ")
