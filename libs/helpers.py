import sys

def die(message):
    """Print status and exit."""
    print(message)
    exit(0)

def print_stats(stats_list):
    """Print statistics about image."""
    print("[*] Statistics: ")
    for i in range(len(stats_list)):
        print("[*] " + str(i) + " white pixels: " + str(round(stats_list[i] / sum(stats_list), 4)))

def update_progress(progress, message, longest_message, bar_length=10):
    """
    Updates progress on action.

    Args:
        progress (float): The current progress as a percentage.
        message (str): The message to display.
        bar_length (int, optional): The size of the progress bar 
                (chars, excluding brackets).
    Returns: 
        1 on completion, 0 otherwise
    """   
    status = ""
    if isinstance(bar_length, float):
        bar_length = int(bar_length)
    if not isinstance(bar_length, int):
        progress = 0
        status = "[!] Expected int for bar_length.\r\n"
        return 1
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "[!] Expected float for progress.\r\n"
        return 1
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
        return 1
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
        return 1

    block = int(round(bar_length*progress))
    text = "\r{0} {1}] {2}% {3}".format( message," "*(len(longest_message) - len(message)) + "[" + "#"*block + "-"*(bar_length-block), round(progress*100, 2), status )

    sys.stdout.write(text)
    sys.stdout.flush()
    
    return 0

def show_current_progress(current_progress, message, longest_message="[*] Longest message...", debug=False):
    """Show current progress"""
    if not debug:
        return True if update_progress(current_progress, message, longest_message=longest_message) == 0 else False

def out_success(message, longest_message, clock, td):
    """
    Print time on success.

    Args:
        message (str): The message to display.
        longest_message (str): The longest message displayed.
        clock (float): start time
        td (float): end time

    Returns:
        td (float) -- end time
    """
    if clock != -1:
        status = "{0}s    \r\n".format(round(td - clock, 4))
    else:
        status = "SUCCESS!    \r\n"

    block = 10
    text = "\r{0} {1}] {2}% {3}".format(message," "*(len(longest_message) - len(message)) + "[" + "#"*block + "-"*(10-block), 100, status)

    sys.stdout.write(text)
    sys.stdout.flush()

    if clock != -1: 
        return td