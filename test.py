import subprocess
cmdd = "echo test".split()
#cmdd.append(args["vmname"])
p = subprocess.Popen(cmdd, stdout=subprocess.PIPE)
with open("last-vm-info.txt","wt") as f:
    for line in p.stdout:
            f.write(line.decode("utf-8"))