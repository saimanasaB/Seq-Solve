import streamlit as st
import pandas as pd
import altair as alt


def job_sequencing_knapsack(jobs, max_deadline):
    jobs.sort(key=lambda x: x[2] / x[1], reverse=True)  # Sort by profit-to-deadline ratio in descending order
    dp = [0] * (max_deadline + 1)

    for job in jobs:
        deadline = job[1]
        for j in range(deadline, 0, -1):
            if dp[j] == 0:
                dp[j] = job[2]
            else:
                dp[j] = max(dp[j], dp[j - 1] + job[2])

    return dp[max_deadline]


def job_sequencing_backtracking(jobs, current_sequence, current_profit, current_time_slot):
    if not jobs:
        return current_sequence, current_profit

    max_sequence, max_profit = current_sequence, current_profit

    for job in jobs:
        job_id, deadline, profit = job
        if current_time_slot < deadline:
            new_sequence = current_sequence.copy()
            new_sequence[current_time_slot] = job_id
            new_profit = current_profit + profit
            new_time_slot = current_time_slot + 1
            new_jobs = [j for j in jobs if j != job]
            sequence, profit = job_sequencing_backtracking(new_jobs, new_sequence, new_profit, new_time_slot)
            if profit > max_profit:
                max_sequence, max_profit = sequence, profit

    return max_sequence, max_profit


def job_sequencing_dynamic_programming(jobs):
    jobs.sort(key=lambda x: x[1])  # Sort by deadline
    max_deadline = max(jobs, key=lambda x: x[1])[1]
    dp = [[0] * (max_deadline + 1) for _ in range(len(jobs) + 1)]

    for i in range(1, len(jobs) + 1):
        for j in range(1, max_deadline + 1):
            job_id, deadline, profit = jobs[i - 1]
            if j >= deadline:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - deadline] + profit)
            else:
                dp[i][j] = dp[i - 1][j]

    max_profit = dp[len(jobs)][max_deadline]

    return max_profit


def job_sequencing_ndf(jobs):
    jobs.sort(key=lambda x: x[1])  # Sort by deadline
    max_deadline = max(jobs, key=lambda x: x[1])[1]
    sequence = [0] * max_deadline
    total_profit = 0

    for job in jobs:
        deadline = job[1]
        for i in range(deadline - 1, -1, -1):
            if sequence[i] == 0:
                sequence[i] = job[0]
                total_profit += job[2]
                break

    return sequence, total_profit


def job_sequencing_spt(jobs):
    jobs.sort(key=lambda x: x[2])  # Sort by processing time (profit)
    max_deadline = max(jobs, key=lambda x: x[1])[1]
    sequence = [0] * max_deadline
    total_profit = 0

    for job in jobs:
        deadline = job[1]
        for i in range(deadline - 1, -1, -1):
            if sequence[i] == 0:
                sequence[i] = job[0]
                total_profit += job[2]
                break

    return sequence, total_profit


def plot_distribution(jobs):
    deadline_counts = jobs['Deadline'].value_counts().sort_index()
    profit_counts = jobs['Profit'].value_counts().sort_index()

    df_deadline = pd.DataFrame({'Deadline': deadline_counts.index, 'Count': deadline_counts.values})
    df_profit = pd.DataFrame({'Profit': profit_counts.index, 'Count': profit_counts.values})

    chart_deadline = alt.Chart(df_deadline).mark_bar().encode(
        x='Deadline:O',
        y='Count:Q',
        tooltip=['Deadline', 'Count']
    ).properties(
        title='Deadline Distribution'
    )

    chart_profit = alt.Chart(df_profit).mark_bar().encode(
        x='Profit:O',
        y='Count:Q',
        tooltip=['Profit', 'Count']
    ).properties(
        title='Profit Distribution'
    )

    st.altair_chart(chart_deadline, use_container_width=True)
    st.altair_chart(chart_profit, use_container_width=True)


def main():
    st.title("Job Sequencing Problem Solver")

    algorithm = st.radio("Select Algorithm",
                         ("Knapsack", "Backtracking", "Dynamic Programming", "NDF", "SPT"))

    num_jobs = st.number_input("Enter number of jobs", min_value=1, step=1, value=1)

    jobs = pd.DataFrame(columns=['Job ID', 'Deadline', 'Profit', 'Description'])

    for i in range(num_jobs):
        job_id = st.text_input(f"Job {i + 1} ID", key=f"job_id_{i}")
        deadline = st.number_input(f"Job {i + 1} Deadline", min_value=1, step=1, key=f"deadline_{i}")
        profit = st.number_input(f"Job {i + 1} Profit", min_value=0, step=1, key=f"profit_{i}")
        description = st.text_area(f"Job {i + 1} Description", key=f"description_{i}")
        jobs = jobs.append({'Job ID': job_id, 'Deadline': deadline, 'Profit': profit, 'Description': description},
                           ignore_index=True)

    # Validate inputs
    if jobs.empty or any(jobs['Job ID'].duplicated()):
        st.warning("Please ensure each job has a unique ID.")
        return

    plot_distribution(jobs)

    if st.button("Solve"):
        jobs_tuples = [tuple(x) for x in jobs.values]
        max_deadline = max(jobs['Deadline'])

        if algorithm == "Knapsack":
            total_profit = job_sequencing_knapsack(jobs_tuples, max_deadline)
            st.write("Knapsack Algorithm:")
            st.write("Total Profit:", total_profit)
        elif algorithm == "Backtracking":
            sequence, total_profit = job_sequencing_backtracking(jobs_tuples, [0] * max_deadline, 0, 0)
            st.write("Backtracking Algorithm:")
            st.write("Job Sequence:", sequence)
            st.write("Total Profit:", total_profit)
        elif algorithm == "Dynamic Programming":
            total_profit = job_sequencing_dynamic_programming(jobs_tuples)
            st.write("Dynamic Programming Algorithm:")
            st.write("Total Profit:", total_profit)
        elif algorithm == "NDF":
            sequence, total_profit = job_sequencing_ndf(jobs_tuples)
            st.write("Nearest Deadline First (NDF) Algorithm:")
            st.write("Job Sequence:", sequence)
            st.write("Total Profit:", total_profit

