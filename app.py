import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🏏 IPL Data Analysis Dashboard")

# LOAD DATA

matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

# DATA CLEANING

matches = matches.dropna(subset=['season'])
deliveries = deliveries.fillna({'dismissal_kind': '', 'player_dismissed': ''})

# 🏆 TOP WINNING TEAMS (PANDAS)

st.subheader("🏆 Top Winning Teams")

top_winners = matches['winner'].value_counts().head(10)
st.dataframe(top_winners)

# 🎯 TOSS IMPACT (PANDAS)

st.subheader("🎯 Toss Impact on Winning")

toss_win = matches[matches['toss_winner'] == matches['winner']]
win_rate = len(toss_win) / len(matches) * 100

st.write(f"Toss Winning Team also Won Match: {win_rate:.2f}%")

# 📈 RUN STATISTICS

st.subheader("📈 Run Statistics")

st.write("Max Runs in a Ball:", deliveries['batsman_runs'].max())
st.write("Average Runs per Ball:", deliveries['batsman_runs'].mean())
st.write("Total Runs:", deliveries['batsman_runs'].sum())


# 1. LINE PLOT → Matches per Season

st.subheader("1. Matches per Season Trend")

season_count = matches['season'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))  # 👈 bigger size

ax.plot(season_count.index, season_count.values, marker='o')

ax.set_title("IPL Matches Trend Over Seasons")
ax.set_xlabel("Season")
ax.set_ylabel("Matches")

plt.xticks(rotation=45)  # 👈 rotate labels for clarity

st.pyplot(fig)

# 2. BAR PLOT → Top Run Scorers

st.subheader("2. Top 10 Run Scorers")

top_scorers = deliveries.groupby("batter")["batsman_runs"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots()
sns.barplot(x=top_scorers.values, y=top_scorers.index, ax=ax)
ax.set_title("Top 10 Run Scorers (Orange Cap)")
ax.set_xlabel("Runs")

st.pyplot(fig)

# 3. PIE CHART → Toss Decision

st.subheader("3. Toss Decision Distribution")

toss = matches['toss_decision'].value_counts()

fig, ax = plt.subplots()
ax.pie(toss.values, labels=toss.index, autopct='%1.1f%%')

st.pyplot(fig)

# 4. HISTOGRAM → Runs per Ball

st.subheader("4. Runs per Ball Distribution")

fig, ax = plt.subplots()
ax.hist(deliveries['batsman_runs'], bins=7, edgecolor='black')
ax.set_title("Distribution of Runs per Ball")
ax.set_xlabel("Runs")
ax.set_ylabel("Frequency")

st.pyplot(fig)

# 5. HEATMAP → Batter vs Over

st.subheader("5. Batting Heatmap")

heatmap_data = deliveries.pivot_table(
    index="batter",
    columns="over",
    values="batsman_runs",
    aggfunc="sum"
).fillna(0)

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(heatmap_data.iloc[:10, :10], cmap="YlGnBu", ax=ax)
ax.set_title("Top Batters vs Overs")

st.pyplot(fig)

# 6. SCATTER → Balls vs Runs

st.subheader("6. Balls vs Runs")

player_runs = deliveries.groupby("batter").agg(
    balls=("ball", "count"),
    runs=("batsman_runs", "sum")
).reset_index()

fig, ax = plt.subplots()
ax.scatter(player_runs['balls'], player_runs['runs'])
ax.set_title("Balls Faced vs Runs Scored")
ax.set_xlabel("Balls")
ax.set_ylabel("Runs")

st.pyplot(fig)

# SUCCESS MESSAGE

st.success("✅ IPL Dashboard Loaded Successfully!")