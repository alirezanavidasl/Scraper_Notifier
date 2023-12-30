from datetime import datetime,timedelta

class Logger:
    def __init__(self, log_file_name):
        self.log_file_path = f'log/log_{log_file_name}.txt'

        try:
            with open(self.log_file_path, "x"): 
                pass
        except FileExistsError:
            with open(self.log_file_path, "w"):
                pass

        


    def log_result(self, success, exception=None):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if success:
            log_message = f"{current_datetime} => Code works successfully"
        else:
            error_message = str(exception) if exception else "Unknown error"
            log_message = f"{current_datetime} => Error - {error_message}"

        with open(self.log_file_path, "a") as log_file:
            log_file.write(log_message + "\n")


    def log_cleaner(self):
            # Read all log lines from the log file
            with open(self.log_file_path, "r") as log_file:
                log_lines = log_file.readlines()



            # Calculate the time threshold for keeping logs (last three hours)
            three_hours_ago = datetime.now() - timedelta(hours=3)

            # Filter logs based on the time threshold
            filtered_logs = Logger.filter_logs_by_time(log_lines, three_hours_ago)

            # Write the filtered logs back to the log file
            with open(self.log_file_path, "w") as log_file:
                log_file.writelines(filtered_logs)

    @staticmethod
    def filter_logs_by_time(log_lines, time_threshold):
        filtered_logs = [log for log in log_lines if Logger.get_log_time(log) >= time_threshold]
        return filtered_logs
    
    @staticmethod
    def get_log_time(log_line):
        # Extract the timestamp from the log entry
        timestamp_str = log_line.split("=>")[0].strip()
        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
