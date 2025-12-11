# 12/10/2025 5:57 PM

I need to write a program that creates and manages index files, which will contain a b-tree. I can tell that I will have to implement the index file management and also think of a way to create b-trees in code. I do not have much experience with b-trees in code, so this will be an interesting challenge. There are six commands that will be used: create, insert, search, load, print, and extract. I will implement these one-by-one through the sessions. I will be using Python, as this is the language I am most comfortable with, meaning that I will be able to finish this project most efficiently. My first commit after this will be committing the file to the repo, so that I can have a canvas to start my ideas on.

# 12/10/2025 6:08 PM

SESSION START
In this session, I will be adding the index.py file, which I will add the functions onto after I make it. I will declare all of the functions I believe will be necessary, so that I can simply keep adding onto them later. I will write the parameters as well, so that I can know, from the start, what the inputs and outputs will be throughout the program

# 12/10/2025 7:00 PM

SESSION END
During this session, I was able to create the file itself and declare the functions I will be filling in later. I added docstrings to the functions themselves so that I can easily understand what to do when the time comes. I decided to go with an object-oriented approach, as this would be most appropriate for a structure with nodes. This will make it much easier to traverse the nodes and carry out the necessary actions. Next, I plan on implementing the functions one-by-one. I will decide which function to implement at the start of the next session.

# 12/10/2025 7:04 PM

SESSION START
For this session, I will implement the header class, as it seems to be the easiest to do, since I simply need to figure out the partitioning and make the read/write functions. I aim to complete this by the end of the session.

# 12/10/2025 7:20 PM

SESSION END
During this session, I was able to implement the header class. It was not as simple as I thought, as I had to consider the block of memory and where exactly I was placing which piece of information. However, once I understood it, I was able to implement the class effectively. I also added global constants so that these important values can be accessed whenever necessary, regardless of class instance. I will decide which portion to work on next in the next session.

# 12/10/2025 7:23 PM

SESSION START
In this session, I will implement the node class, so that I can start working on the b-tree node management system. I will finish the read and write functions necessary for the node. I will have to make sure that I accurately keep track of the block number and don't accidentally offset any pointer.

# 12/10/2025 7:44 PM

SESSION END
I implemented the node class successfully. The node class now is able to read and write a node from a block. While I have not fully tested this class yet, I will eventually test it through implementation. As of right now, the logic seems sound.

# 12/10/2025 7:47 PM

SESSION START
In this session, I will write all of teh code for the b-tree operations, which are the search_node, split_child, insert_nonfull, insert, and inorder functions. This will take some time, as it is a lot of code. However, implementing this will allow me to test my b-tree implementation with the node class.

# 12/10/2025 8:32 PM

SESSION END
For this session, I implemented the code for the b-tree operations, which was the aforementioned functions. While this did take a while, I am satisfied with what I wrote. Now, all I need to do is implement the way to get the commands from the command line and run the functions I have written. That is what I will be doing in the future sessions. This is a very interesting project so far, as I have had to implement things that we have learned in class, such as indexes and b-trees. While it is easy to learn, writing code truly tests your understanding of the subject.

# 12/10/2025 8:36 PM

SESSION START
During this session, I will implement the commands that the user will input into the command line. These are teh create, insert, search, print, extract, and load functions. Once I have this done, I will test this out in the main. Because all of the functions will have been created by this point, I will complete the project in this session by calling the necessary functions in main.

# 12/10/2025 9:15 PM

SESSION END
I have finally completed the project. I implemented the command line functions and wrote code in main that allows the program to run. I tested the code, and it worked for all inputs necessary. This part of the code was not very difficult to implement, as all of the necessary functions had already been written, and I simply needed to use them properly. I would say this portion was more of a higher-level view of the task at hand, as I was able to use pre-defined functions that complete the action. As for the menu, that was very simple as well, as it was a normal while loop with menu options, similar to the menus I have implemented in previous projects. Throughout this project, the most difficult part for me was figuring out which inputs lead to which outputs. Once I had the plan for what I wanted to do, filling in the functions was simply a task that I needed to complete. I learned that when doing a project, creating a plan is the most important part, as it dictates the ease by which the future steps can be completed. In this project, because I had my functions and classes defined at the start, I knew exactly how I wanted to write the code itself. This led to an easier time debugging, as I knew what my functions needed to send to each other. This was a very fun project, and I truly enjoyed implementing concepts that we learned from class into code.