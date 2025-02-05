#imports
from shared_imports import *
import varalyze_cli

session_active = False
session_file = None

def folder_creation():
    investigation_path = os.path.join(os.getcwd(), "investigations")
    if not os.path.exists(investigation_path):
        os.makedirs(investigation_path)
        print(f"\n> Investigation folder path has been created at: {investigation_path}")
    else:
        print(f"> Investigation folder already exists at: {investigation_path}")
    return investigation_path

def file_creation(investigation_path):
    while True:
        filename = input("\nEnter a filename to use for the report: ").strip()
        if not filename.endswith(".txt"):
            filename += ".txt"
        report_path = os.path.join(investigation_path, filename)
        try:
            # Try creating the file to check for validity
            with open(report_path, "w") as file:
                file.write("=== VARALYZE CASE INVESTIGATION ===\n\n")
                file.write("Title: \n\n")
                file.write("Date: \n\n")
                file.write("Analyst: \n\n")
                file.write("=== Report details ===\n\n")
                file.write("Findings: \n\n")
                file.write("Conclusion: \n")
                file.write("=== Threat intel data ===")
            print("\n> File structures successfully setup...")
            return report_path
        except Exception as e:
            print(f"Error: File creation failed with '{filename}', {e}")
            print("Please try again with a different filename.")

def session_start():
    global session_active, session_file
    if not session_active:
        session_active = True
        print("\n> Session started. All activities will be recorded.")
    else:
        print("A session is already active.")

def session_end():
    global session_active
    if session_active:
        print("> Session ended.")
        session_active = False
    else:
        print("No active session to end.")

def log_activity(data):
    if session_active:
        if session_file:  
            with open(session_file, "a") as file:
                file.write(f"{data}\n")
        else:
            print(f"Activity recorded (no session file defined yet): {data}")
    else:
        print(f"Processing data without session: {data}")


def main():
    print("\033[1m" + "\n►►►►►►►►► Welcome to the case workflow tool ◄◄◄◄◄◄◄◄◄\n" + "\033[0m")
    print("- This feature allows you to initate a session which records all activity into a single file.")
    time.sleep(1)
    intialize_investigation = folder_creation()
    report_path = file_creation(intialize_investigation)
    session_start()
    global session_file
    session_file = report_path
    varalyze_cli.main()

if __name__ == "__main__":
    main()