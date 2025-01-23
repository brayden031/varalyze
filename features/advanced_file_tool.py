#imports
from shared_imports import *
from tool_options import file_tool
from scripts import virustotal_file_cli_tool
from features import history_cli_tool
import varalyze_cli

def folder_creation():
    investigation_path = os.path.join(os.getcwd(), "investigations")
    if not os.path.exists(investigation_path):
        os.makedirs(investigation_path)
        print(f"Investigation folder path has been created at: {investigation_path}")
    else:
        # This feature or case feature has already been used therefore folder path already created
        return
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
                pass 
            return report_path
        except Exception as e:
            print(f"Error: File creation failed with '{filename}', {e}")
            print("Please try again with a different filename.")

def main():
    print("\033[1m" + "\n►►► Welcome to the advanced file investigation tool ◄◄◄\n" + "\033[0m")
    print("- This feature allows you to pass a file to be analysed by VirusTotal.")
    print("- Once completed, the results are then processed by taking the connecting IP addresses/URLs and cross-referencing them through the varalyze scoring system used in the report generation feature.")
    print("- This helps to generate a comprehensive overview of the legitimacy of a file.")
    # Overall while loop for tool being run
    running_tool = True
    while running_tool:
        # Try to fetch API key environment variable, if fails displays error message but doesn't prevent program running
        try:
            VIRUSTOTAL_API_KEY = os.environ["VIRUSTOTAL_API_KEY"]
        except KeyError:
            os.system('cls')
            print("Error: VIRUSTOTAL_API_KEY environment variable is not set.")
            print("Returning back to the tool page...")
            file_tool.File_tools()
        # File path error handling
        intialize_investigation = folder_creation()
        intialize_file = file_creation(intialize_investigation)
        #print({intialize_file})
        #running_tool = False

        #vt_analysis_id = virustotal_file_cli_tool.virustotal(file_path, VIRUSTOTAL_API_KEY)
        #if vt_analysis_id:
            # Needs passing parameter to prevent processing url message as progress bar replaces this
            #response_json = virustotal_file_cli_tool.result_complete(vt_analysis_id, VIRUSTOTAL_API_KEY)
            # Progress bar update
            #if response_json:
                # Needs passing parameter to prevent processing url message as progress bar replaces this
                # Will need seperate function to write results to file
                #virustotal_file_cli_tool.file_results(response_json, file_path)
                # Progress bar update
                # Call to relationship api and collect results

if __name__ == "__main__":
    main()