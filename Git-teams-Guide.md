# since we are working as a team we should use software engineering concepts to keep structure to our project:

(1) Only one person controls "Main" branch. 
    - Noone else will utilize this branch unless otherwise asked to.
    - this ensures that any mistakes were to happen, we could easily revert to previous versions
(2) Stay on your branch/ specified task:
(3) Save progress regurlarly (On your branch):
    - git push <my-branch-name> (Not Main!!)
        * See steps to save, below...
()

Steps to save changes/ Edits:
(1) check what your current branch is:
    git branch
        ( this will show an asterisk (*) and highlighted the text associated to your current working branch )
        OR -
        git status (will show detailed output of your branch)

(2) give short description of what you changed. This is very important! we will probably all make a bunch of mistakes the next few weeks so it is important we know what we were doing to "undo" the mistake:
    For example:
        `git commit -m "`Updated gameroom's html to connect client-side websocket. Need to handle real-time user signin through the ws.onmessage().`"`  
    *CMD*:
    `git commit -m "My First commit"`

(3) Send changes to Staging (Add)
    *CMD*:
    git add .
    git add <file_name1> <file_name2> 

(4) Save changes, send to remote repository on GitHub:
    git push -u origin <my_branch>


(5) Once you have successfully completed your task, we need to merge our changes to our *`remote-staging`* area on github. This step is extremely important and easy to create "merge conflicts" for eachother if not done correctly.  
*From your Branch*
git checkout remote-staging
# IMPORTANT! Do not make any changes here as you are no longer on your Branch.
git merge <my_branch>
* this will "Fast-Forward" our remote-staging branch to include your changes.
*Now, make sure to go BACK to your branch*
git checkout <my_branch>
# If you want to update your branch with the content of our 'remote-staging' which will contain compilation of ALL our updates, make sure to communicate to teamates you wish to do so. 

See [https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging] if you have further questions on branch, checkout, and merge.