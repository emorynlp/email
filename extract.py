from enron.extracter import Extracter

if __name__ == '__main__':
    extracter = Extracter()

    print("Retrieving all emails into an array json.")
    extracter.get_all()
    print("Retrieving emails containing threads into an array json.")
    extracter.get_threads_only()
