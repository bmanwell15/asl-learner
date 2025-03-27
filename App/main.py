from HandRecognizer import HandRecognizer
import traceback

def main():
    handRecognizer = HandRecognizer()
    print("Waiting for 'A' symbol...")
    handRecognizer.waitUntilHandSymbol("A")
    print("'A' symbol recognized!")
    while True:
        print(handRecognizer.getCurrentHandSymbol())



try:
    main()
except Exception:
    traceback.print_exc()