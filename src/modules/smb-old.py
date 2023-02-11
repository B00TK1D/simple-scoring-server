# SMB plugin

# Contains following functions:
# - plant(flag) : plant a flag on the server
# - check(flag) : check if a flag is still on the server

# Imports
from smb.SMBConnection import SMBConnection


def plant(flag, ip, port, username, password):
    # Plant a flag on the server
    # Return True if the flag was planted, False otherwise
    # Send the SMB command to delete the flag located at intel/intel in the SMB share general

    # Connect to the SMB server
    try:
        conn = SMBConnection(username, password, "client", "server", use_ntlm_v2 = True)
        conn.connect(ip, port)
    except Exception as e:
        print("Error connecting to SMB server: " + str(e))
        return False
    
    # Write the flag to the file intel/intel
    try:
        conn.storeFile("general", "intel/intel", flag)
    except Exception as e:
        print("Error writing flag to SMB share: " + str(e))
        return False

    # Close the SMB connection
    conn.close()

    return True

def check(flag, ip, port, username, password):
    # Check if a flag is still on the server
    # Return True if the flag is still on the server, False otherwise
    # Send the SMB command to read the flag located at intel/intel in the SMB share general

    # Connect to the SMB server
    try:
        conn = SMBConnection(username, password, "client", "server", use_ntlm_v2 = True)
        conn.connect(ip, port)
    except Exception as e:
        print("Error connecting to SMB server: " + str(e))
        return False
    
    # Read the flag from the file intel/intel
    try:
        data = conn.retrieveFile("general", "intel/intel")
    except Exception as e:
        print("Error reading flag from SMB share: " + str(e))
        return False

    # Close the SMB connection
    conn.close()

    # Check if the flag is still on the server
    if data == flag:
        return True
    else:
        return False


