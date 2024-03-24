import streamlit as st


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

def job_sequencing_knapsack(jobs, max_deadline):
    jobs.sort(key=lambda x: x[2] / x[1], reverse=True)
    dp = [0] * (max_deadline + 1)
    selected_jobs = []

    for job in jobs:
        deadline = job[1]
        for j in range(deadline, 0, -1):
            if dp[j] == 0:
                dp[j] = job[2]
                selected_jobs.append(job)
            else:
                dp[j] = max(dp[j], dp[j - 1] + job[2])

    return dp[max_deadline], selected_jobs

def job_sequencing_dynamic_programming(jobs):
    jobs.sort(key=lambda x: x[1])
    max_deadline = max(jobs, key=lambda x: x[1])[1]
    dp = [[0] * (max_deadline + 1) for _ in range(len(jobs) + 1)]
    selected_jobs = []

    for i in range(1, len(jobs) + 1):
        for j in range(1, max_deadline + 1):
            job_id, deadline, profit = jobs[i - 1]
            if j >= deadline:
                if dp[i - 1][j] >= dp[i - 1][j - deadline] + profit:
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = dp[i - 1][j - deadline] + profit
                    selected_jobs.append(jobs[i-1])
            else:
                dp[i][j] = dp[i - 1][j]

    max_profit = dp[len(jobs)][max_deadline]

    return max_profit, selected_jobs

def job_sequencing_ndf(jobs):
    jobs.sort(key=lambda x: x[1])
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
    jobs.sort(key=lambda x: x[2])
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

def visualize_sequence(sequence, profits):
    data = {'Job': sequence, 'Profit': profits}
    st.bar_chart(data)

def main():
    st.title("Job Sequencing Problem Solver")

    algorithm = st.radio("Select Algorithm", ("Knapsack", "Backtracking", "Dynamic Programming", "NDF", "SPT"))

    num_jobs = st.number_input("Enter number of jobs", min_value=1, step=1, value=1)

    jobs = []
    max_deadline = 0

    for i in range(num_jobs):
        job_id = st.text_input(f"Job {i+1} ID")
        deadline = st.number_input(f"Job {i+1} Deadline", min_value=1, step=1)
        profit = st.number_input(f"Job {i+1} Profit", min_value=0, step=1)
        jobs.append((job_id, deadline, profit))
        max_deadline = max(max_deadline, deadline)

    
    if st.button("Solve"):
        if algorithm == "Knapsack":
            total_profit, selected_jobs = job_sequencing_knapsack(jobs, max_deadline)
            st.write("Knapsack Algorithm:")
            st.write("Total Profit:", total_profit)
            st.write("Job Sequence:")
            for job in selected_jobs:
                st.write(f"Job ID: {job[0]}, Deadline: {job[1]}, Profit: {job[2]}")
        elif algorithm == "Dynamic Programming":
            total_profit, selected_jobs = job_sequencing_dynamic_programming(jobs)
            st.write("Dynamic Programming Algorithm:")
            st.write("Total Profit:", total_profit)
            st.write("Job Sequence:")
            for job in selected_jobs:
                st.write(f"Job ID: {job[0]}, Deadline: {job[1]}, Profit: {job[2]}")

        elif algorithm == "Backtracking":
            sequence, total_profit = job_sequencing_backtracking(jobs, [0] * max_deadline, 0, 0)
            st.write("Backtracking Algorithm:")
            st.write("Job Sequence:", sequence)
            st.write("Total Profit:", total_profit)

        elif algorithm == "NDF":
            sequence, total_profit = job_sequencing_ndf(jobs)
            st.write("Nearest Deadline First (NDF) Algorithm:")
            st.write("Job Sequence:", sequence)
            st.write("Total Profit:", total_profit)
        elif algorithm == "SPT":
            sequence, total_profit = job_sequencing_spt(jobs)
            st.write("Shortest Processing Time (SPT) Algorithm:")
            st.write("Job Sequence:", sequence)
            st.write("Total Profit:", total_profit)

        visualize_sequence([job[0] for job in selected_jobs], [job[2] for job in selected_jobs])

if __name__ == "__main__":
    main()

       


