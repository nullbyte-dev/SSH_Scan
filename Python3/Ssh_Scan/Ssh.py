import paramiko


def try_user1(ip):
    mask = '192.168.1.'
    increase = ((mask + '%s') % ip) # Merging input digit with ip mask
    client.connect(hostname=increase, username=user1, password=pw1, port=port) #Trying to connect to client
    stdin, stdout, stderr = client.exec_command('hostname') #command to execute, doesn't work with sudo... yet
    data = stdout.read() + stderr.read()
    hostdata = ('Ip: ' + (increase + ' ' + '\nHostname: ' + '%s') % data.decode("utf-8")) #formatting text output
    file.write(hostdata) #writing data to the file
    client.close()


def try_user2(ip):
    mask = '192.168.1.'
    increase = ((mask + '%s') % ip)
    client.connect(hostname=increase, username=user2, password=pw2, port=port)
    stdin, stdout, stderr = client.exec_command('hostname')
    data = stdout.read() + stderr.read()
    hostdata = ('Ip: ' + (increase + ' ' + '\nHostname: ' + '%s') % data.decode("utf-8"))
    file.write(hostdata)
    client.close()


file = open("ip.txt", "w") #writing data to %filename%, stored at ssh repository by default

user1 = 'user1' #username, yep
user2 = 'user2'
pw1 = 'password1' #password indeed
pw2 = 'password2'
port = 22 #use any free port
ldigit = 1 #digit, from which counter starts, if exception - add 1 to ip where exception happen
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

while ldigit <= 255:
    try:
        try_user1(ldigit)
        ldigit += 1
    except paramiko.ssh_exception.AuthenticationException: #Note: if you only have 1 user, remove line 41-43
        try_user2(ldigit)
        ldigit += 1
    except Exception as err:
        print(err) #prints error code to terminal, can be written to text file, by replacing line with file.write(err)
        ldigit += 1

file.close()
