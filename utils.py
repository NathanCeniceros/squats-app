def log_message(message):
    with open("squats_log.txt", "a") as log:
        log.write(f"{message}\n")
