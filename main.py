from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui import Ui_MainWindow
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # buttons
        self.ui.OK.accepted.connect(self.save_vote)
        self.ui.OK.rejected.connect(self.close)

        # checkboxes
        self.ui.cb_Repub.stateChanged.connect(self.limit_checkboxes)
        self.ui.cb_Demo.stateChanged.connect(self.limit_checkboxes)
        self.ui.cb_thrdprty.stateChanged.connect(self.limit_checkboxes)

    # makes only one political choice at a time
    def limit_checkboxes(self):
        all_cbs = [self.ui.cb_Repub, self.ui.cb_Demo, self.ui.cb_thrdprty]
        chosen = self.sender()
        for cb in all_cbs:
            if cb != chosen:
                cb.setChecked(False)

    # saves vote and updates summary
    def save_vote(self):
        voter_name = self.ui.name.text().strip()
        voter_phone = self.ui.phone.text().strip()
        vote_date = self.ui.dayvoted.dateTime().toString()

        # find candidate choice
        if self.ui.cb_Repub.isChecked():
            picked_candidate = "Republican"

        elif self.ui.cb_Demo.isChecked():
            picked_candidate = "Democrat"

        elif self.ui.cb_thrdprty.isChecked():
            third_name = self.ui.customcan.text().strip()
            if third_name == "":
                self.error_box("Please enter the 3rd Party candidate name.")
                return
            picked_candidate = "3rd Party - " + third_name
        else:
            self.error_box("Pick someone before submitting.")
            return

        # basic validation
        if voter_name == "":
            self.error_box("Name missing")
            return

        if voter_phone == "":
            self.error_box("Phone number missing")
            return

        # write the vote to the file
        try:
            vote_file = open("voteresults.txt", "a")
            vote_file.write("Name: " + voter_name + "\n")
            vote_file.write("Phone: " + voter_phone + "\n")
            vote_file.write("Candidate: " + picked_candidate + "\n")
            vote_file.write("Date: " + vote_date + "\n")
            vote_file.write("Next Vote\n")
            vote_file.close()
        except:
            self.error_box("Could not write to voteresults.txt")
            return

        # read file again to count votes
        try:
            read_file = open("voteresults.txt", "r")
            all_lines = read_file.readlines()
            read_file.close()
        except:
            self.error_box("Couldn't read voteresults.txt")
            return

        # count the votes
        vote_counts = {}
        for line in all_lines:
            if line.startswith("Candidate:"):
                found_cand = line.replace("Candidate:", "").strip()
                if found_cand in vote_counts:
                    vote_counts[found_cand] += 1
                else:
                    vote_counts[found_cand] = 1

        # remove old summary
        updated_lines = []
        skip_flag = False
        for line in all_lines:
            if line.startswith("Vote Summary"):
                skip_flag = True
                continue
            if skip_flag:
                continue
            updated_lines.append(line)

        # rewrite file with updated summary
        try:
            write_file = open("voteresults.txt", "w")
            for line in updated_lines:
                write_file.write(line)

            write_file.write("\nVote Summary\n")
            for cand, num in vote_counts.items():
                write_file.write(cand + ": " + str(num) + "\n")

            write_file.close()

        except:
            self.error_box("Failed to update summary.")
            return

        QMessageBox.information(self, "Vote Saved", "Your vote was saved!")

    def error_box(self, msg):
        QMessageBox.critical(self, "Error", msg)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
