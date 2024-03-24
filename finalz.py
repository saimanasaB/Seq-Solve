# Importing necessary libraries
import streamlit as st
import altair as alt
import pandas as pd
import heapq

# Definition of the Job class
class Job:
    def __init__(self, id, deadline, profit):
        self.id = id
        self.deadline = deadline
        self.profit = profit

# Knapsack algorithm for job sequencing
def job_sequencing_knapsack(jobs):
    # Sorting the jobs by profit (descending order)
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

# Dynamic Programming algorithm for job sequencing
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

# Max Heap algorithm for job sequencing
def job_sequencing_max_heap(jobs):
    max_deadline = max(jobs, key=lambda x: x.deadline).deadline
    max_heap = []
    selected_jobs = []

    for job in jobs:
        heapq.heappush(max_heap, (-job.profit, job.deadline, job))

    timeslot = [-1] * (max_deadline + 1)
    max_profit = 0

    while max_heap:
        profit, deadline, job = heapq.heappop(max_heap)
        k = min(max_deadline, deadline)
        while k >= 1:
            if timeslot[k] == -1:
                timeslot[k] = job
                max_profit -= profit
                selected_jobs.append(job)
                break
            k -= 1

    return max_profit, selected_jobs

# Branch and Bound algorithm for job sequencing
def job_sequencing_branch_and_bound(jobs):
    def dfs(deadline, profit, selected_jobs, index):
        nonlocal max_profit, max_selected_jobs
        
        if index == len(jobs) or deadline == 0:
            if profit > max_profit:
                max_profit = profit
                max_selected_jobs = selected_jobs[:]
            return
        
        if jobs[index].deadline >= deadline:
            dfs(deadline - 1, profit + jobs[index].profit, selected_jobs + [jobs[index]], index + 1)
        else:
            dfs(deadline, profit, selected_jobs, index + 1)
            dfs(deadline - 1, profit + jobs[index].profit, selected_jobs + [jobs[index]], index + 1)

    jobs.sort(key=lambda x: x.deadline)
    max_profit = 0
    max_selected_jobs = []
    dfs(max(jobs, key=lambda x: x.deadline).deadline, 0, [], 0)

    return max_profit, max_selected_jobs

# Visualization of job sequence
def visualize_job_sequence(selected_jobs):
    if not selected_jobs:
        st.warning("No jobs selected for visualization.")
        return
    
    df = pd.DataFrame([(job.id, job.deadline, job.profit) for job in selected_jobs], columns=['Job ID', 'Deadline', 'Profit'])
    chart = alt.Chart(df).mark_bar().encode(
        x='Deadline',
        y='Job ID',
        color='Profit'
    ).properties(
        title='Job Sequence Visualization'
    )
    st.altair_chart(chart, use_container_width=True)

# Main function
def main():
    st.title("Job Sequencing Problem Solver")

    # Sidebar for options
    st.sidebar.title("Options")
    algorithm_choice = st.sidebar.radio("Choose Algorithm", ("Knapsack", "Dynamic Programming", "Max Heap", "Branch and Bound"))

    # Input for job details
    num_jobs = st.number_input("Enter the number of jobs", min_value=1, step=1, value=1)
    jobs = []
    for i in range(num_jobs):
        id = st.text_input(f"Job ID for job {i+1}")
        deadline = st.number_input(f"Deadline for job {i+1}", min_value=1, step=1)
        profit = st.number_input(f"Profit for job {i+1}", min_value=0, step=1)
        jobs.append(Job(id, deadline, profit))

    # Calculation button
    if st.button("Calculate"):
        if not any(job.id for job in jobs):
            st.warning("Please enter Job IDs for all jobs.")
        elif any(job.deadline < 1 for job in jobs):
            st.warning("Deadline must be at least 1 for all jobs.")
        elif any(job.profit < 0 for job in jobs):
            st.warning("Profit cannot be negative.")
        else:
            # Algorithm selection
            if algorithm_choice == "Knapsack":
                # Knapsack algorithm
                max_profit, selected_jobs = job_sequencing_knapsack(jobs)
                # Complexity: O(n log n + n * max_deadline)
            elif algorithm_choice == "Dynamic Programming":
                # Dynamic Programming algorithm
                max_profit, selected_jobs = job_sequencing_dynamic_programming(jobs)
                # Complexity: O(n log n + n * max_deadline)
            elif algorithm_choice == "Max Heap":
                # Max Heap algorithm
                max_profit, selected_jobs = job_sequencing_max_heap(jobs)
                # Complexity: O(n + n * max_deadline)
            elif algorithm_choice == "Branch and Bound":
                # Branch and Bound algorithm
                max_profit, selected_jobs = job_sequencing_branch_and_bound(jobs)
                # Complexity: O(n log n + 2^n)

            # Display maximum profit and selected job sequence
            st.write(f"Max Profit using {algorithm_choice}: {max_profit}")
            st.write("Selected Jobs in Sequence:", [job.id for job in selected_jobs])
            # Visualize the job sequence
            visualize_job_sequence(selected_jobs)

    # Comparative Analysis
    st.sidebar.subheader("Comparative Analysis")
    show_analysis = st.sidebar.checkbox("Show Comparative Analysis")
    if show_analysis:
        # Calculate profits for all algorithms for analysis
        knapsack_profit, _ = job_sequencing_knapsack(jobs)
        dp_profit, _ = job_sequencing_dynamic_programming(jobs)
        max_heap_profit, _ = job_sequencing_max_heap(jobs)
        branch_and_bound_profit, _ = job_sequencing_branch_and_bound(jobs)
        
        # Create a DataFrame for analysis
        analysis_data = pd.DataFrame({
            'Algorithm': ['Knapsack', 'Dynamic Programming', 'Max Heap', 'Branch and Bound'],
            'Max Profit': [knapsack_profit, dp_profit, max_heap_profit, branch_and_bound_profit]
        })
        # Display the analysis data
        st.write(analysis_data)

if __name__ == "__main__":
    main()

