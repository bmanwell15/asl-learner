from HandRecognizer import HandRecognizer

def main():
    handRecognizer = HandRecognizer()
    print("Waiting for 'A' symbol...")
    handRecognizer.waitUntilHandSymbol("A")
    print("'A' symbol recognized!")
    while True:
        print(handRecognizer.getCurrentHandSymbol())


main()