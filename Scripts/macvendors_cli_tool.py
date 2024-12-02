#imports
from shared_imports import *
from tool_options import mac_tool
import varalyze_cli

# MAC vendor connection request 
def mac_vendor_request(MAC_address):
    url = f"https://api.macvendors.com/{MAC_address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    
    # if not successful 200 connection due to invalid MAC or other issue display error message
    else:
        print("An error has occured attempting to make the request: ", {response.status_code})
        return None
    
def main():
        print("\033[1m" + "\n►►► Welcome to the macvendors CLI tool ◄◄◄\n" + "\033[0m")
        # Overall while loop for tool being run
        running_tool = True
        while running_tool:
            MAC_address = input("Enter the MAC address: ")
            MAC_vendor_result = mac_vendor_request(MAC_address)
            print("\n▼ MAC Vendor result ▼\n")
            table.field_names = ["Field", "Result"]
            table.add_row(["MAC Vendors", Fore.GREEN + str(MAC_vendor_result) + Style.RESET_ALL])
            table.max_width["Result"] = 80
            print(table)
            table.clear_rows()
            
            # Second loop for determining if the user would like to check another
            invalid_re_run = True
            while invalid_re_run:
                re_run_tool = input("\nWould you like to check another ?\nEnter 'yes' or 'no'\n\nAnswer: ")
                if re_run_tool == 'yes':
                    running_tool = True
                    invalid_re_run = False
                
                # Exit loop to determine correct input and next user navigation
                elif re_run_tool == 'no':
                    running_tool = False
                    invalid_re_run = False
                    invalid_exit = True
                    while invalid_exit:
                        exit_tool = input("\nWould you like to return to the category page, home page or exit the program?\nEnter 'category' or 'home' 'exit'\n\nAnswer: ")
                        if exit_tool == "category":
                            invalid_exit = False
                            running_tool = False
                            os.system('cls')
                            mac_tool.MAC_tools()
                        elif exit_tool == "home":
                            invalid_exit = False
                            running_tool = False
                            os.system('cls')
                            varalyze_cli.main()
                        elif exit_tool == "exit":
                            invalid_exit = False
                            running_tool = False
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
    
if __name__ == "__main__":
    main()
    