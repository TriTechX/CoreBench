from . import utils, colours
import random, time

def show_loading_screen():
    """
    Displays a loading screen over the top of a background
    loading process. Waits for the global in utils to be
    set to true once necessary data is gathered.

    Void function
    """

    messages = ["So, you're back...", "Hello there!", "It's hot in here...", "400FPS", "Disabling frame generation...", 
                "RTX ON", "Removing nanites...", "Stealing your personal information...", "Pro tip: bench", 
                "Sussy Bucket", "No standard users allowed!", "We've got a website, did you hear? https://www.corebench.me",
                "Getting more ping...", "Optimizing...", "Initiating...", "WELCOME.", "Deleting main.py...", "Always remember to remove the French language pack!", "I use Arch btw",
                "I use Core btw", "Over 6GHz!", "Bringing out the Intel Pentium...", "Gathering texel fillrate...", "Collecting frames...", "No fake frames here!",
                "Changing boot order...", "Imagine if you were using this on Windows lol", "No longer held prisoner by Replit!", "It's dangerous to go alone.", 
                "All your bench are belong to us.", "GPU bench coming soon. Maybe.", "Unused RAM is useless RAM. Give some to me.",
                "ThinkPad is the only Pad", "Hoarding FPS...", "Super Accurate™!", "HEY THERE BUDDY PAL", "Jimmy smiles upon you.",
                "Remember to enable XMP...", "Ryzen 4070", "GPU test coming never!", "Glorp"]
    
    message = messages[random.randint(0,len(messages)-1)]

    while not utils.finished_loading:
        utils.clear()
        print(colours.cyan() + """░█████╗░░█████╗░██████╗░███████╗""")
        print("""██╔══██╗██╔══██╗██╔══██╗██╔════╝""")
        print("""██║░░╚═╝██║░░██║██████╔╝█████╗░░""")
        print("""██║░░██╗██║░░██║██╔══██╗██╔══╝░░""")
        print("""╚█████╔╝╚█████╔╝██║░░██║███████╗""")
        print("""░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝""")
        print()
        print(colours.magenta() + """██████╗░███████╗███╗░░██╗░█████╗░██╗░░██╗""")
        print("""██╔══██╗██╔════╝████╗░██║██╔══██╗██║░░██║""")
        print("""██████╦╝█████╗░░██╔██╗██║██║░░╚═╝███████║""")
        print("""██╔══██╗██╔══╝░░██║╚████║██║░░██╗██╔══██║""")
        print("""██████╦╝███████╗██║░╚███║╚█████╔╝██║░░██║""")
        print("""╚═════╝░╚══════╝╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝""")
        print(colours.reset())
        print(colours.grey() + "© TriTech 2026 - If you paid for this software, get a refund.\n" + colours.reset())
        print(message)
        time.sleep(0.3)
        utils.clear()
        print(colours.magenta() + """░█████╗░░█████╗░██████╗░███████╗""")
        print("""██╔══██╗██╔══██╗██╔══██╗██╔════╝""")
        print("""██║░░╚═╝██║░░██║██████╔╝█████╗░░""")
        print("""██║░░██╗██║░░██║██╔══██╗██╔══╝░░""")
        print("""╚█████╔╝╚█████╔╝██║░░██║███████╗""")
        print("""░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝""")
        print()
        print(colours.green() + """██████╗░███████╗███╗░░██╗░█████╗░██╗░░██╗""")
        print("""██╔══██╗██╔════╝████╗░██║██╔══██╗██║░░██║""")
        print("""██████╦╝█████╗░░██╔██╗██║██║░░╚═╝███████║""")
        print("""██╔══██╗██╔══╝░░██║╚████║██║░░██╗██╔══██║""")
        print("""██████╦╝███████╗██║░╚███║╚█████╔╝██║░░██║""")
        print("""╚═════╝░╚══════╝╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝""")
        print(colours.reset())
        print(colours.grey() + "© TriTech 2026 - If you paid for this software, get a refund.\n" + colours.reset())
        print(message)
        time.sleep(0.3)
        utils.clear()
        print(colours.green() + """░█████╗░░█████╗░██████╗░███████╗""")
        print("""██╔══██╗██╔══██╗██╔══██╗██╔════╝""")
        print("""██║░░╚═╝██║░░██║██████╔╝█████╗░░""")
        print("""██║░░██╗██║░░██║██╔══██╗██╔══╝░░""")
        print("""╚█████╔╝╚█████╔╝██║░░██║███████╗""")
        print("""░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝""")
        print()
        print(colours.cyan() + """██████╗░███████╗███╗░░██╗░█████╗░██╗░░██╗""")
        print("""██╔══██╗██╔════╝████╗░██║██╔══██╗██║░░██║""")
        print("""██████╦╝█████╗░░██╔██╗██║██║░░╚═╝███████║""")
        print("""██╔══██╗██╔══╝░░██║╚████║██║░░██╗██╔══██║""")
        print("""██████╦╝███████╗██║░╚███║╚█████╔╝██║░░██║""")
        print("""╚═════╝░╚══════╝╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝""")
        print(colours.reset())
        print(colours.grey() + "© TriTech 2026 - If you paid for this software, get a refund.\n" + colours.reset())
        print(message)
        time.sleep(0.3)
        utils.clear()

    utils.clear()