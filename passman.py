#!/usr/bin/env python

import subprocess
from Crypto.Cipher import AES
import os
import pickle
from datetime import datetime

class PassMan(object):

	def __init__(self, accounts=None):
		"""Initializes a PassMan object with a secret key. Account dict optional."""
		
		#Current task number
		self.task = ""

		#User password required length--must be 16, 24, or 32 bytes
		self.passwordlength = 16

		#Determines whether information is decrypted or still protected
		self.isplaintext = False
		
		#User's secret password
		self.key = ""

		#Name of the account dictionary
		self.accountsfile = "accountdict"

		if accounts is None:
			self.accounts = []
		else:
			assert(type(accounts) is str)
			self.accounts = pickle.load(open(accounts))
			#assert(type(self.accounts) is dict)

	def login(self):
		"""Takes in a key to decrypt passwords with"""
		print c("-----------------------------------------------------------------------------------------------------------------------\n							LOGIN")

		print c("Password length must be " + str(self.passwordlength))
		self.key = str((raw_input("Password: ")))

		while len(self.key) != self.passwordlength:
			print c("You entered a password of length "+str(len(self.key))+". Password length must be " + str(self.passwordlength))
			self.key = str(raw_input("Password: "))
		self.isplaintext = True

	def logout(self):
		"""Erases key to decrypt passwords with from memory"""
		print c("-----------------------------------------------------------------------------------------------------------------------\n							LOGOUT")
		sure = str(raw_input("Are you sure you want to logout? Enter [n] for no and just press ENTER for yes: "))

		if len(sure) == 0:
			open(self.accountsfile, "w").write(pickle.dumps(self.accounts))
			self.key = None
			self.isplaintext = False
			print c("Goodbye!\nMake sure you close this window so any passwords you accessed during this session remain private.")
		else:
			self.task = ""

	def storenew(self):
		"""Inserts a new account's information into database"""
		print c("-----------------------------------------------------------------------------------------------------------------------\n							NEW ACCOUNT")
		
		if self.isplaintext is False:
			raise ValueError("Have not logged in yet!")

		print c("(*) denotes a mandatory field. Hit ENTER to leave a field blank.")
		account = "" 
		while len(account) == 0:
			account = str(raw_input("Account name (*): "))
		username = str(raw_input("Username: "))
		email = str(raw_input("Email: "))
		password = "" 
		while len(password) == 0:
			password = str(raw_input("Password (*): "))
		
		newentry = {}
		newentry["account"] = account
		newentry["username"] = username	#e.g. "ecr
		newentry["email"] = email	#e.g. "ecr@ecr.ecr"
		newentry["time"] = str(datetime.now())

		diff16 = 16 - len(password) % 16
		
		cipherpswd = password + os.urandom(diff16 - 1) + chr(diff16)
		cipherpswd = AES.new(self.key).encrypt(cipherpswd)
		newentry["password"] = cipherpswd

		self.accounts.append(newentry)
		open(self.accountsfile, "w").write(pickle.dumps(self.accounts))

	def listaccounts(self):
		"""Lists every account with its email and username if filled in"""
		
		print c("-----------------------------------------------------------------------------------------------------------------------\n							LIST ACCOUNTS")

		if self.isplaintext is False:
			raise ValueError("Have not logged in yet!")
		if len(self.accounts) == 0:
			print c("No accounts to list.")

		for account in self.accounts:
			toprint = "Added " + account["time"]
			toprint +="\nAccount: " + account["account"]
			if len(account["username"]) > 0:
				toprint +="\nUsername: {}".format(account["username"])
			if len(account["email"]) > 0:
				toprint +="\nEmail: {}".format(account["email"])
			print c(toprint+"\n")
	
	def getaccount(self):
		"""Retrieves and prints one entry's complete information"""

		print c("-----------------------------------------------------------------------------------------------------------------------\n							GET ACCOUNT")

		assert(self.isplaintext is True)
		account = raw_input("Enter an account name to get password (case sensitive): ")

		tempdict = {}
		#gets only the first instance of this account name! *TODO
		found = False
		for entry in self.accounts:
			if entry["account"] == account:
				tempdict = entry
				found = True
				break
		if found is False:
			print c("The account name '" + account + "' was not found.")
			return

		passwordtoprint = AES.new(self.key).decrypt(tempdict["password"])
		padflag = ord(passwordtoprint[len(passwordtoprint) - 1])
		passwordtoprint = passwordtoprint[:len(passwordtoprint) - padflag]
		if len(passwordtoprint) == 0:
			afterword = "\nUnable to decipher. Try logging in again with a different key."
		else:
			afterword = "\nIf this does not look like your password, consider logging in again with a different key."

		toprint = "Added " + tempdict["time"]
		toprint +="\nAccount: " + tempdict["account"]
		if len(tempdict["username"]) > 0:
			toprint += "\nUsername: " + tempdict["username"]
		if len(tempdict["email"]) > 0:
			toprint += "\nEmail: " + tempdict["email"]
		toprint += "\nPassword: " + passwordtoprint
		print c(toprint + afterword)

	def getall(self):
		"""Gets all user passwords"""                                              
		print c("-----------------------------------------------------------------------------------------------------------------------\n          					 GET ALL PASSWORDS")
				
		if len(self.accounts) == 0:
			print c("No accounts to list.")
			return
		
		action = False
		while action is False:
			confirm = str(raw_input("Enter your PassMan passkey to confirm, or hit ENTER to cancel: "))
			if len(confirm) == 0:
				return
			elif confirm == self.key:
				for account in self.accounts:
					toprint = "Added " + account["time"]
					toprint +="\nAccount: " + account["account"]
					if len(account["username"]) > 0:
						toprint +="\nUsername: {}".format(account["username"])
					if len(account["email"]) > 0:
						toprint +="\nEmail: {}".format(account["email"])

					passwordtoprint = AES.new(self.key).decrypt(account["password"])
					padflag = ord(passwordtoprint[len(passwordtoprint) - 1])
					passwordtoprint = passwordtoprint[:len(passwordtoprint) - padflag]
					toprint +="\nPassword: {}".format(passwordtoprint)
					print c(toprint)
				return
			else:
				print c("Incorrect passkey.")

	
	def deleteaccount(self):
		"""Asks user for account to delete from dictionary"""
		print c("-----------------------------------------------------------------------------------------------------------------------\n							DELETE ACCOUNT")
		account = raw_input("Account name to delete (case sensitive): ")
		
		for entry in self.accounts:
			if entry["account"] == account:
				action = False
				while action is False:
					confirm = str(raw_input("Enter your PassMan passkey to confirm deletion, or hit ENTER to cancel: "))
					if confirm == self.key:
						del self.accounts[self.accounts.index(entry)]
						print c("The account '" + account + "' was successfully deleted.")
						open(self.accountsfile, "w").write(pickle.dumps(self.accounts))
						found = True
						return
					elif len(confirm) == 0:
						return
					else:
						print c("Incorrect passkey.")

		print c("The account name '" + account + "' was not found.")



def whattodo():
	"""Asks user what they would like to in PassMan"""
	print c("-----------------------------------------------------------------------------------------------------------------------\nWhat would you like to do? Enter the number of the task.\n0. Re-login\n00. Logout\n1. Store a new entry\n2. View your current entries\n3. Get an entry's password\n4. Get all entries' passwords\n5. Delete an entry from your stored entries")
	pm.task = str(raw_input("Task number: "))
	return pm.task

def executetask():
	"""Calls the relevant function"""
	print "-----------------------------------------------------------------------------------------------------------------------"
	if pm.task == "0":
		pm.login()
	elif pm.task == "00":
		pm.logout()
	elif pm.task == "1":
		pm.storenew()
	elif pm.task == "2":
		pm.listaccounts()
	elif pm.task == "3":
		pm.getaccount()
	elif pm.task == "4":
		pm.getall()
	elif pm.task == "5":
		pm.deleteaccount()
	else:
		print c("Invalid task number! Take a look at the options again.")
		whattodo()

def c(string='kek'):
	kek = subprocess.Popen(['lolcat', '-f'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	stdout, stderr = kek.communicate(input='{}'.format(string))
	return stdout.rstrip('\n')


banner = subprocess.Popen(["figlet","   																																					PassMan"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
print c(banner.communicate()[0])
print c("=========================================== Welcome to Pass(word)Man(ager)! ===========================================")
isfirsttime = ""
while len(isfirsttime) == 0:
	isfirsttime = str(raw_input("Is this your first time using PassMan? Enter [y] for yes and [n] for no: "))
if isfirsttime == "y":
	isfirsttime = True
else:
	isfirsttime = False

if isfirsttime:
	pm = PassMan()
	print c("Your first step is to set up a key by which all your passwords will be encrypted and decrypted.")
	pm.login()
	print c("Great! You can now start using PassMan.")
else:
	pm = PassMan('accountdict')
	pm.login()
	
while pm.task != "00":
	whattodo()
	executetask()
