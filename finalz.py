import streamlit as st
import altair as alt
import pandas as pd

class Job:
    def __init__(self, id, deadline, profit):
        self.id = id
        self.deadline = deadline
        self.profit = profit

def job_sequencing_greedy(jobs):
    jobs.sort(key=lambda x: x.profit, reverse=True)
    max_deadline = max(jobs, key=lambda x: x.deadline).deadline
    timeslot = [-1] * (max_deadline + 1)
    filled_time_slots = 0
    max_profit = 0
    selected_jobs = []

    for job in jobs:
        k = min(max_deadline, job.deadline)
        while k >= 1:
            if timeslot[k] == -1:
                timeslot[k] = job
                filled_time_slots += 1
                max_profit += job.profit
                selected_jobs.append(job)  # Append the whole job object
                break
            k -= 1

        if filled_time_slots == max_deadline:
            break

    return max_profit, selected_jobs


def job_sequencing_dynamic_programming(jobs):
    max_deadline = max(jobs, key=lambda x: x.deadline).deadline
    dp = [0] * (max_deadline + 1)

    jobs.sort(key=lambda x: x.profit, reverse=True)
    selected_jobs = []

    for job in jobs:
        for j in range(job.deadline, 0, -1):
            if dp[j] == 0:
                dp[j] = job.profit
                selected_jobs.append(job)  # Append the whole job object
                break

    max_profit = sum(dp)
    return max_profit, selected_jobs

def visualize_job_sequence(selected_jobs):
    df = pd.DataFrame([(job.id, job.deadline, job.profit) for job in selected_jobs], columns=['Job ID', 'Deadline', 'Profit'])
    chart = alt.Chart(df).mark_bar().encode(
        x='Deadline',
        y='Job ID',
        color='Profit'
    ).properties(
        title='Job Sequence Visualization'
    )
    st.altair_chart(chart, use_container_width=True)

def main():
    st.title("Job Sequencing Algorithms")

    st.sidebar.title("Options")
    algorithm_choice = st.sidebar.radio("Choose Algorithm", ("Greedy", "Dynamic Programming"))

    num_jobs = st.number_input("Enter the number of jobs", min_value=1, step=1, value=1)

    jobs = []
    for i in range(num_jobs):
        id = st.text_input(f"Job ID for job {i+1}")
        deadline = st.number_input(f"Deadline for job {i+1}", min_value=1, step=1)
        profit = st.number_input(f"Profit for job {i+1}", min_value=0, step=1)
        jobs.append(Job(id, deadline, profit))

    if st.button("Calculate"):
        if algorithm_choice == "Greedy":
            max_profit, selected_jobs = job_sequencing_greedy(jobs)
        
        elif algorithm_choice == "Dynamic Programming":
            max_profit, selected_jobs = job_sequencing_dynamic_programming(jobs)

        st.write(f"Max Profit using {algorithm_choice}: {max_profit}")
        st.write("Selected Jobs in Sequence:", [job.id for job in selected_jobs])
        visualize_job_sequence(selected_jobs)

if __name__ == "__main__":
    main()
