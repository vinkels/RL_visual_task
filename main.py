from window import session

def main():
    ppn_input = input("proefpersoon nummer: ")
    try:
        ppn = int(ppn_input)
    except ValueError:
        print("That's not an int!")
    cur_ses = session(ppn)
main()
