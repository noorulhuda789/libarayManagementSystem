import datetime


class Notifications:
    def __init__(self, message, isViewed=False, date=datetime.date.today()):
        self._message = message
        self._isViewed = isViewed
        self._date = date

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    @property
    def isViewed(self):
        return self._isViewed

    @isViewed.setter
    def isViewed(self, isViewed):
        self._isViewed = isViewed

    @property
    def date(self):
        return self._date

    def readNotification(self):
        self.isViewed = True

    def __str__(self) -> str:
        return f"Message: {self.message}\nDate: {self.date}\n"

    def writeToFile(self):
        return f"{self.message},{int(self.isViewed)},{self.date}"
