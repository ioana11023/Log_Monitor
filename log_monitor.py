import csv
from datetime import datetime, timedelta
from collections import defaultdict

LOG_FILE = 'logs.log'
REPORT_FILE = 'output_report.txt'
TIME_FORMAT = "%H:%M:%S"

jobs = defaultdict(dict)

with open(LOG_FILE, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        timestamp, status, job_name, pid = row
        pid = int(pid)
        time_obj = datetime.strptime(timestamp, TIME_FORMAT)
        jobs[pid][status] = time_obj

with open(REPORT_FILE, 'w') as report:
    for pid, times in jobs.items():
        if "START" in times and "END" in times:
            start_time = times["START"]
            end_time = times["END"]

            if end_time < start_time:
                end_time += timedelta(days=1)

            duration = (end_time - start_time).total_seconds() / 60

            line = f"Job PID {pid} took {duration:.2f} minutes."
            if duration > 10:
                report.write(f"[ERROR] {line}\n")
            elif duration > 5:
                report.write(f"[WARNING] {line}\n")
            else:
                report.write(f"[INFO] {line}\n")
        else:
            report.write(f"[INCOMPLETE] Job PID {pid} has missing START or END.\n")

print("Raport generated here: output_report.txt")
