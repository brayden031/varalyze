# imports
import os
from shared_imports import *
from collections import Counter
import varalyze_cli

# Initializing variable for file
history_log = 'search_history.json'

# Function to check if the history file exists (has a tool been used)
def get_history():
    if os.path.exists(history_log):
        try:
            with open(history_log, 'r') as file:
                history = json.load(file)
                return history
        except json.JSONDecodeError:
            print("An error has occured trying to open the history log file..")
            return []
    else:
        return []
    
# Function that is called once a tool has ran successfully to store the search in the history file
def record_search(tool_name, category_name, search_term, comment, result):
    entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "tool": tool_name,
        "category": category_name,
        "search_term": search_term,
        "comment": comment,
        "result": result
    }
    
    history = get_history()
    history.append(entry)             
    with open(history_log, 'w') as file:
        json.dump(history, file, indent=4)
        
# Formatting the results retrieved into the command line
def display_entry_details(entry):
    print("\nDetails for selected entry:\n")
    table = PrettyTable()
    table.field_names = ["Field", "Value"]
    
    table.add_row(["Time", entry['timestamp']])
    table.add_row(["Tool", entry['tool']])
    table.add_row(["Category", entry['category']])
    table.add_row(["Search Term", entry['search_term']])
    table.add_row(["Comment", entry['comment']])
    
    for key, value in entry['result'].items():
        table.add_row([key, value])
        
    print(table.get_string())
    
    # First loop for determining if the user would like to check another
    invalid_re_run = True
    while invalid_re_run:
        re_run_tool = input("\nWould you like to check another ?\nEnter 'yes' or 'no'\n\nAnswer: ")
        if re_run_tool == 'yes':
            os.system('cls')
            main()
            invalid_re_run = False
        
        # Exit loop to determine correct input and next user navigation
        elif re_run_tool == 'no':
            invalid_re_run = False
            invalid_exit = True
            while invalid_exit:
                exit_tool = input("\nWould you like to return to the home page or exit the program?\nEnter 'home' or 'exit'\n\nAnswer: ")
                if exit_tool == "home":
                    invalid_exit = False
                    os.system('cls')
                    varalyze_cli.main()
                elif exit_tool == "exit":
                    invalid_exit = False
                    varalyze_cli.exit_program()    
                # Error statement for category selection
                else:
                    os.system('cls')
                    print("Invalid option, please try again")
                # Error statement for check again selection
            else:
                os.system('cls')
                print("Invalid option, please try again")
        else:
            os.system('cls')
            print("Invalid option, please try again")
            
# Function to allow user to inspect a past search by selecting the associated number (value)
def entry_select(selection, history):
    running_tool = True
    while running_tool:
        if selection == 0:
            print("Returning to home page..")
            time.sleep(2)
            os.system('cls')
            running_tool = False
            varalyze_cli.main()
        elif 1 <= selection <= len(history):
            selected_entry = history[selection - 1]
            display_entry_details(selected_entry)
        else:
            os.system('cls')
            print("Invalid selection. Please try again.")
            main()
            
# Function to check if the history file exists (has a scan been run) else not an accessible feature yet
def display_history():
    history = get_history()
    
    # Check if the history file exists (has a scan been run) else not an accessible feature yet
    if not history:
        print("ⓘ Note: History log does not exist, a history file will be initialized after running a tool for the first time. ⓘ\n")
        print("Returning to home page..")
        time.sleep(6)
        os.system('cls')
        varalyze_cli.main()
        
    # Sort historical searches by timestamp in a descending order
    history.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    
    # Formatting the results retrieved into the command line table
    log_table = PrettyTable()
    log_table.field_names = ["Index", "Time", "Category", "Tool", "Search Term", "Comment"]
    
    category_counter = Counter()
    tool_counter = Counter()

    for index, entry in enumerate(history):
        log_table.add_row([index + 1, Fore.GREEN + entry['timestamp'] + Style.RESET_ALL, Fore.GREEN + entry['category'] + Style.RESET_ALL, Fore.GREEN + entry['tool'] + Style.RESET_ALL, Fore.GREEN + entry['search_term'] + Style.RESET_ALL, Fore.BLUE + entry['comment'] + Style.RESET_ALL])
        category_counter[entry['category']] += 1
        tool_counter[entry['tool']] += 1
    
    print(log_table.get_string())

    most_common_category = category_counter.most_common(1)[0][0]
    most_common_tool = tool_counter.most_common(1)[0][0]
    
    print("\n▼ Stats ▼\n")
    print("Total lifetime searches ->", index + 1)
    print(f"Most used category -> {most_common_category}")
    print(f"Most used tool -> {most_common_tool}")
    
    return history

def main():
    print("\033[1m" + "\n►►►►►►►►► Welcome to the history page ◄◄◄◄◄◄◄◄◄\n" + "\033[0m")
    print("\n▼ Previous searches ▼\n")
    history = display_history()
    if history:  # Proceed only if history is not empty
        try:
            selection = int(input("\nEnter a number to view the associated results or type '0' to return to the home page: "))
            entry_select(selection, history)
        except ValueError:
            print("Invalid input. Please enter a number.")
            os.system('cls')
            main()  # Re-run main() to prompt again
            
if __name__ == "__main__":
    main()