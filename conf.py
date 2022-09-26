global key , dir_hosts , dir_smtp

key = "key_1"
dir_hosts = "conf/hosts.json"
dir_smtp  = "conf/smtp.json"

def get_key():
	return key

def get_hosts():
	return dir_hosts

def get_smtp():
	return dir_smtp