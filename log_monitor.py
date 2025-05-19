import csv # import csv module
from datetime import datetime, timedelta
from collections import defaultdict

LOG_FILE = 'logs.log' # define the input log file
REPORT_FILE = 'output_report.txt' # define the output log file
TIME_FORMAT = "%H:%M:%S"

# create a dictionary to store job times, each PID maps to another dict with START and END times
jobs = defaultdict(dict)

# open the log file for reading
with open(LOG_FILE, 'r') as file:
    reader = csv.reader(file) # read the CSV content row by row
    for row in reader: # each row contains: timestamp, status (START/END), job_name, and pid
        timestamp, status, job_name, pid = row
        pid = int(pid) # convert PID string to integer
        time_obj = datetime.strptime(timestamp, TIME_FORMAT) # convert timestamp string into a datetime object for easier time calculations
        jobs[pid][status] = time_obj # store the timestamp under the corresponding status (START or END) for that PID

# open the report file for writing results
with open(REPORT_FILE, 'w') as report: # loop over each job PID and its corresponding START and END times
    for pid, times in jobs.items():
        if "START" in times and "END" in times: # check if both START and END timestamps are present for the job
            start_time = times["START"] # get the job start time
            end_time = times["END"] # get the job end time

            if end_time < start_time: # handle cases where the job ends after midnight (end time < start time)
                end_time += timedelta(days=1) # add one day to the end time to correctly calculate duration

            duration = (end_time - start_time).total_seconds() / 60 # calculate the duration in minutes between END and START

            line = f"Job PID {pid} took {duration:.2f} minutes." # create the output line with job PID and duration rounded to 2 decimals
            if duration > 10: # duration > 10 minutes is an error
                report.write(f"[ERROR] {line}\n")
            elif duration > 5: # duration > 5 minutes is a warning
                report.write(f"[WARNING] {line}\n")
            else:
                report.write(f"[INFO] {line}\n") # otherwise info
        else:
            report.write(f"[INCOMPLETE] Job PID {pid} has missing START or END.\n") # if START or END missing, write incomplete job info

print("Raport generated here: output_report.txt") # inform user where the report was saved
