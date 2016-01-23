# PassMan, a Pass(word)Man(ager)

In the modern age of technology, vulnerabilities in privacy and security abound, with software becoming exploited as quickly as it is produced. Therefore, it is more important than ever that people protect themselves and their information--from social media accounts to email inboxes, passwords are of vital importance to keeping information safe.

However, the problem with practicing secure password-creating habits is that it soon becomes difficult to remember the different passwords to all of one's accounts. There are online password storage schemes that claim to store people's passwords securely on the cloud, but storing anything online makes it inherently riskier and more prone to hacking attacks than if it was stored locally (on people's computers).

That is where PassMan comes in. As a simple, storage-efficient, secure password manager, it operates entirely offline and keeps user information protected. It combines the power of AES encryption and salting to fortify privacy defenses. It is written entirely in Python, which allows it to run on almost every platform and operating system known to humankind. And lastly, it's easy on the eyes, if I do say so myself.

Watch [this video](https://www.youtube.com/watch?v=X40iDBUwBKU) to get a more in-depth understanding of how PassMan works.

### Installation and How to Run

To make everything look as [it should](https://raw.githubusercontent.com/echenran/PassMan/master/demo.png), you must have [lolcat](https://github.com/busyloop/lolcat/) and [figlet](http://www.figlet.org/) installed.

Once you have lolcat and figlet, you can open PassMan on command line by running
```Bash
$ python passman.py
```
or 
```Bash
$ ./passman.py
```
or removing the .py extension from the file and doing the good ol' double-click in your file manager.

### Other Notes

If you move the location of the PassMan program and you've already stored passwords on it, you must move the file "accountdict" (in the same folder) to the same location! Otherwise, PassMan will not know where to look for your stored passwords and will tell you there are no accounts to list when you want to see your entries.
