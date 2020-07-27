import socket
import os
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '192.168.1.11'
port = 8080
s.connect((host, port))
print("\nServer is currently running @", host)
print("Waiting for incoming connections")




while True:

    print("1: View cwd\n"
          "2: View custom Dir\n"
          "3: Download File \n"
          "4: Delete File \n"
          "5: Delete Dir  \n"
          "6: Create File \n"
          "7: Return ipconfig (TODO...) \n"
          "8: Execute custom CMD command \n"
          "9: Shut it down -MC Hammer \n"
          )
    print()
    command = input(str("command >> "))

    if command == "1":
        # Print Current Working Directory (CWD) 
        os.system("dir")  # send 1
        #files = conn.recv()  # get response
        #files = files.decode()  # decode response
        #print("Command output:", files)

    elif command == "2":
        # View custom directory
        conn.send(command.encode())
        userInput = input(str("Custom Dir: "))
        conn.send(userInput.encode())
        files = conn.recv().decode()
        print("Custom dir: ", files)

    elif command == "3":
        # Download a file 
         print("enter the url of the file you want to download")
         link = input()
         os.system("curl " + str(link))
         print("file downloaded")

    elif command == "4":
        # Delete file
        print("enter the full directory of the file to remove")
        file = input()
        os.system("del " + str(file))
        print("file removed")

    elif command == "5":
        # Delete dir
        print("enter the full directory to remove")
        dir = input()
        os.system("rmdir /S " +str(dir))

    elif command == "6":
        # make directory
        print("enter the new directory name")
        direct = input()
        print("enter the desired location")
        location = input()
        os.system("mkdir " + str(location) + '\\' + str(direct))
        print("directory made")



    elif command == "7":
        # Get ipconfig
        os.system("ipconfig -all")
    elif command == "8":
        # Run command in CMD (non-admin)
        print("enter the command to use")
        comm = input()
        os.system(str(comm))

    elif command == "9":
        # Shutdown target PC
        print("shutting down")
        os.system("shutdown /s")

    else:
        print("Invalid Command")
