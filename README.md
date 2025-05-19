# Log Monitor App
This app reads a CSV file with job logs, tracks the duration of each job from START to END, and creates a report with warnings and errors if a job runs longer than expected.

Features:
> Reads the CSV file called logs.log.

> Finds jobs using their PID and tracks their START and END times.

> Calculates how long each job runs in minutes.

> Writes a report to output_report.txt:
    > Marks [WARNING] if a job takes more than 5 minutes.
    > Marks [ERROR] if a job takes more than 10 minutes.

> Flags jobs that don’t have both START and END entries as incomplete.
