from OTPViews import MainWindow
from AppStorage import OTPDatabase
from OTPControllers import Controller


if __name__ == "__main__":
    MainApp = Controller(MainWindow(), OTPDatabase())
    MainApp.run()
