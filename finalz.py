import streamlit as st
import altair as alt
import pandas as pd
import heapq

class Job:
    def __init__(self, id, deadline, profit):
        self.id = id
        self.deadline = deadline
        self.profit = profit

def job_sequencing_max_heap(jobs):
    if not jobs:
        return 0, []
    
    max_deadline = max(jobs, key=lambda x: x.deadline).deadline
    max_heap = []
    selected_jobs = []

    for job in jobs:
        heapq.heappush(max_heap, (-job.profit, job.deadline, job))

    timeslot = [-1] * (max_deadline + 1)
    max_profit = 0

    while max_heap:
        profit, deadline, job = heapq.heappop(max_heap)
        profit = -profit  # negate the profit again
        k = min(max_deadline, deadline)
        while k >= 1:
            if timeslot[k] == -1:
                timeslot[k] = job
                max_profit += profit
                selected_jobs.append(job)
                break
            k -= 1

    return max_profit, selected_jobs

def main():
    st.title("Job Sequencing Problem Solver")

    st.sidebar.title("Options")
    algorithm_choice = st.sidebar.radio("Choose Algorithm", ("Max Heap",))

    num_jobs = st.number_input("Enter the number of jobs", min_value=1, step=1, value=1)

    jobs = []
    for i in range(num_jobs):
        id = st.text_input(f"Job ID for job {i+1}")
        deadline = st.number_input(f"Deadline for job {i+1}", min_value=1, step=1)
        profit = st.number_input(f"Profit for job {i+1}", min_value=0, step=1)
        jobs.append(Job(id, deadline, profit))

    if st.button("Calculate"):
        if not any(job.id for job in jobs):
            st.warning("Please enter Job IDs for all jobs.")
        elif any(job.deadline < 1 for job in jobs):
            st.warning("Deadline must be at least 1 for all jobs.")
        elif any(job.profit < 0 for job in jobs):
            st.warning("Profit cannot be negative.")
        else:
            if algorithm_choice == "Max Heap":
                max_profit, selected_jobs = job_sequencing_max_heap(jobs)

            st.write(f"Max Profit using {algorithm_choice}: {max_profit}")
            st.write("Selected Jobs in Sequence:", [job.id for job in selected_jobs])

    # Comparative Analysis
    st.sidebar.subheader("Comparative Analysis")
    show_analysis = st.sidebar.checkbox("Show Comparative Analysis")
    if show_analysis:
        st.subheader("Comparative Analysis of Algorithms")
        max_heap_profit, _ = job_sequencing_max_heap(jobs)
        analysis_data = pd.DataFrame({
            'Algorithm': ['Max Heap'],
            'Max Profit': [max_heap_profit]
        })
        st.write(analysis_data)

if __name__ == "__main__":
    main()
