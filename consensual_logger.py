from datetime import datetime
import os

def get_log_path():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"consensual_log_{ts}.txt"
    return os.path.join(os.getcwd(), fname)

def main():
    print("=== Consent-based input logger ===")
    print("This program WILL NOT capture keystrokes stealthily.")
    print("It will ONLY log text you type into this terminal, after you explicitly consent.")
    consent = input("Do you consent to log your typed input to a local file? (yes/no): ").strip().lower()

    if consent not in ("yes", "y"):
        print("Consent not given. Exiting.")
        return

    log_path = get_log_path()
    print(f"Logging will be saved to: {log_path}")
    print("Type lines and press Enter. Type 'exit' on a line by itself to stop.")

    try:
        with open(log_path, "a", encoding="utf-8") as f:
            while True:
                line = input("> ")
                if line.strip().lower() == "exit":
                    print("Exiting. Log saved.")
                    break
                timestamp = datetime.now().isoformat()
                f.write(f"{timestamp}\t{line}\n")
                f.flush()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")

if __name__ == "__main__":
    main()
