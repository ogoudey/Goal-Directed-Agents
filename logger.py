import os
from datetime import datetime

def log(message: str, log_name: str):
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Define log file path
    log_path = os.path.join("logs", f"{log_name}.log")
    
    # Timestamp the message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}\n"
    
    # Append the message to the log file
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(formatted_message)
