from DL.BookDL import BookDL
from DL.UserDL import UserDL
from BL.member import Member
from DataStructures.PriorityQueue import PriorityQueue
import datetime

if __name__ == "__main__":
    BookDL.readDataFromFile()
    # # print("Before: ")
    # # BookDL.displayList()
    # # BookDL.readDataFromFile()
    UserDL.readDataFromFile()

    book = BookDL.searchBookByTitle("Hungary 56")
    user1 = UserDL.searchUserByUserName("q")
    user2 = UserDL.searchUserByUserName("s")

    book.reservedUsers.display()
    print()
    book.reserve(user1)
    book.reservedUsers.display()
    print()
    book.reserve(user2)
    book.reservedUsers.display()    
    

    # # book.issueBook(user)
    # # print(book.issueEvent)

    # # book.extendBook(7)
    # # print(book.issueEvent)
    # print(book.writeToFile())

    user = Member(1, "s", "s", "s", "s")
    print(user.notifications)
