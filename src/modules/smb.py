# SMB plugin

# Contains following functions:
# - plant(flag) : plant a flag on the server
# - check(flag) : check if a flag is still on the server

# Imports
from smb.SMBConnection import SMBConnection
import os
import urllib
from smb.SMBHandler import SMBHandler

def plant(flag, ip, port, username, password):
    # Plant a flag on the server
    # Return True if the flag was planted, False otherwise
    # Send the SMB command to delete the flag located at intel/intel in the SMB share general

    try:
        # Connect to the SMB server
        conn = SMBConnection(username, password, "client", "server", use_ntlm_v2=True)
        conn.connect(ip, port)

        # Define the path to the file
        file_path = os.path.join("intel/intel")

        # Write the flag to a temporary file
        f = open("tmp", "w")
        f.write(flag)
        f.close()
        f = open("tmp", "rb")
        conn.storeFile("general", file_path, f)

        return True
    except Exception as e:
        print("Error writing flag to SMB share: " + str(e))
        return False

def check(flag, ip, port, username, password):
    # Check if a flag is still on the server
    # Return True if the flag is still on the server, False otherwise
    # Send the SMB command to read the flag located at intel/intel in the SMB share general

    # Connect to the SMB server
    try:
        # Connect to the SMB server
        conn = SMBConnection(username, password, "client", "server", use_ntlm_v2=True)
        conn.connect(ip, port)

        # Open the flag file
        opener = urllib.request.build_opener(SMBHandler)
        f = opener.open("smb://" + username + ":" + password + "@" + ip + ":" + str(port) + "/general/intel/intel")
        data = f.read().decode("utf-8")
        f.close()

        # Check if the flag is still on the server
        if data == flag:
            return True
        else:
            #print("Found flag: " + data + " instead of " + flag)
            return False

    except Exception as e:
        print("Error reading flag from SMB share: " + str(e))
        return False


