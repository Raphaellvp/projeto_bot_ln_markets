from datetime import datetime
import sys

_last_message_length = 0

def log(message, replace_previous=False):
    global _last_message_length
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    if replace_previous:
        sys.stdout.write('\r' + ' ' * _last_message_length + '\r')
        sys.stdout.write(log_entry)
        sys.stdout.flush()
        _last_message_length = len(log_entry)
    else:
        print(log_entry)
        _last_message_length = 0
    
    # Salva em arquivo
    log_file = f"bot_log_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(log_entry + "\n")