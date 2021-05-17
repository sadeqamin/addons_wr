Test Cases Sales Discount Approval
==================================

    1- Set user1 discount limit = 5
    2- Set user2 discount limit = 10
    3- user1 create order #1 without discount [Passed]
    4- user1 create order #2 with discount < 5 [Passed]
    4- user1 create order #3 with discount = 5 [Passed]
    5- user1 create order #4 with discount > 5 and <= 10 [Passed]
    6- user2 approve order #3 [passed]
    7- check email notification sent to you user2 [Passed]


