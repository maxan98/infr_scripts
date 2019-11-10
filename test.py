    cmdd = "python hw.py".split()
    cmdd.append(args["vmname"])
    p = subprocess.Popen(cmdd, stdout=subprocess.PIPE)
    with open("last-vm-info.txt","wt") as f:
        f.write(p.stdout)