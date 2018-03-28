from session import session
from img_set import img_set

def main():
    ppn_input = input("proefpersoon nummer: ")
    try:
        ppn = int(ppn_input)
    except ValueError:
        print("That's not an int!")
    img_files = img_set()
    cur_ses = session(ppn, img_files)
main()
