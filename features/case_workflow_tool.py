#imports
from shared_imports import *
import varalyze_cli

# Global variables
session_active = False
session_file = None

# Investigations folder path creation
def folder_creation():
    investigation_path = os.path.join(os.getcwd(), "investigations")
    if not os.path.exists(investigation_path):
        os.makedirs(investigation_path)
        print(f"\n> Investigation folder path has been created at: {investigation_path}")
    else:
        print(f"\n> Investigation folder already exists at: {investigation_path}")
    return investigation_path

# File creation within investigations folder
def file_creation(investigation_path):
    while True:
        filename = input("\nEnter a filename to use for the report: ").strip()
        if not filename.endswith(".txt"):
            filename += ".txt"
        report_path = os.path.join(investigation_path, filename)
        if os.path.exists(report_path):
            print(f"A file named '{filename}' already exists. Please choose a different filename.")
            continue
        try:
            # Varalyze file template
            with open(report_path, "w") as file:
                file.write("=== VARALYZE CASE INVESTIGATION ===\n\n")
                file.write("Title: \n\n")
                file.write("Date: \n\n")
                file.write("Analyst: \n\n")
                file.write("=== Report details ===\n\n")
                file.write("Findings: \n\n")
                file.write("Conclusion: \n\n")
                file.write("=== Threat intel data ===\n")
            print("\n> File structures successfully setup...")
            return report_path
        except Exception as e:
            print(f"Error: File creation failed with '{filename}', {e}")
            print("Please try again with a different filename.")

# Session start function to notify program to save activity to users investigation file
def session_start():
    global session_active, session_file
    if not session_active:
        session_active = True
        print("> Session started. All activities will be recorded...\n")
    else:
        print("\nWarning: A session is already active.")

# Session end function to notify program to stop saving activity to users investigation file
def session_end():
    global session_active
    if session_active:
        print("> Session ended.\n")
        session_active = False
    else:
        print("No active session to end.")

# Function used to open investigation file and write tool collected data in
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
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                               Workflow feature                             ║
║                                                                            ║ 
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║          Welcome to the workflow tool. This feature can be used to         ║
║     initiate a session which will record all program activity into a file  ║
║                         for case management purposes.                      ║
║                                                                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║                                
║               ▼ Choose an option from the list below to begin ▼            ║
║                                                                            ║
║                    TOOLS                          OTHER                    ║
║                                                                            ║
║                    1. Initiate session            4. Home page             ║    
║                    2. End session                 5. Exit                  ║
║                    3. Restore session                                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
    awaiting_valid_tool_choice = True
    while awaiting_valid_tool_choice:
        user_option = input("Enter the number of the option you wish to select: ")
        if user_option == '1':
            if session_active:
                print("\nWarning: A session is already active please end this before attempting to start a new one.\n")
            else:
                intialize_investigation = folder_creation()
                report_path = file_creation(intialize_investigation)
                session_start()
                global session_file
                session_file = report_path
        elif user_option == '2':
            session_end()
        elif user_option == '3':
            if session_active:
                print("\nWarning: A session is already active please end it before re-initiating.\n")
            else:
                investigation_path = folder_creation()
                filename = input("\nEnter the filename to re-initiate session: ").strip()
                if not filename.endswith(".txt"):
                    filename += ".txt"
                report_path = os.path.join(investigation_path, filename)
                if os.path.exists(report_path):
                    session_start()
                    session_file = report_path
                else:
                    print(f"No file found with name '{filename}'. Please check the filename and try again.")   
        elif user_option == '4':
            os.system('cls')
            varalyze_cli.main()
            break
        elif user_option == '5':
            varalyze_cli.exit_program()
        else:
            print("\nError: Invalid choice. Please select from 1-4...\n")

if __name__ == "__main__":
    main()