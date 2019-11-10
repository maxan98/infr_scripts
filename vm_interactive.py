import subprocess
import time
counter = 0
def extract_descriptions(filename):
    data = open(filename, "rt").read().split("\n")
    data = "\n".join(data)
    data = data.split("\n\n")
    data = [i for i in data if "parser.add_argument(" in i]
    data = [" ".join(i.replace("\\\n", " ").split()) for i in data]

    descriptions = [i[i.find("help='")+6:-2] for i in data]
    names = [i[i.find("--")+2:i.find("',", i.find("--"))] for i in data]
    descriptions = dict(zip(names, descriptions))

    return descriptions

def run_with_args(name, args, argnames):
    cmd = ['python', name]
        global counter
    for i in argnames:
        if i not in args:
            continue

        if i == "no-ssl" or i == "disable_ssl_verification":
            if args[i] == "True":
                cmd.append("--" + i)
            continue

        if type(args[i]) == str:
            cmd.append("--" + i)
            cmd.append(args[i])
        elif args[i]:
            cmd.append("--" + i)

    print "Running", name, "with args:\n", cmd

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    for line in p.stdout:
        print line
    p.wait()
    if p.returncode:
        print name + " returned non-zero value.\n Terminating."
        print "Attempt" + str(counter)
        print "Waiting for Machine to awake 15s"
        if counter >= 20:
            exit(1)
        counter +=1
        time.sleep(15)
        run_with_args(name, args, argnames)
        exit(1)

if __name__ == "__main__":
    email = raw_input("Enter your email")

    with open("vm_interactive_last_user", "wt") as f:
        f.write(email)

    defaults = {"disable_ssl_verification": "True", "host": "192.168.88.238", "user":"administrator@dev.local", "password": "Dev0psi0t!", "vmname": "New_Test", "template" : "ubuntu18", "datastore-name": "HDD_DS", "no-ssl": "True", "vm-folder": "VMS"}

    descriptions = extract_descriptions("vsphere.py")
    vsphere_argnames = list(descriptions.keys())
    tmp = extract_descriptions("soft_reboot.py")
    tmp.update({"disable_ssl_verification": "Disable ssl verification (for execute program)"})
    executeprogramm_argnames = list(tmp.keys()) + ["host", "user", "port", "password"]
    descriptions.update(tmp)
    tmp = extract_descriptions("poweronvm.py")
    poweronvm_argnames = list(tmp.keys())

    args = {}

    for i in list(set(vsphere_argnames + executeprogramm_argnames)):
        tmp = "\n(default " + defaults[i] + ")" if i in defaults else ""
        inp =  raw_input(descriptions[i] + tmp + ":\n")

        if inp == "":
            if i in defaults:
                args[i] = defaults[i]
        else:
            args[i] = inp
    print args
    print vsphere_argnames
    print args
    print vsphere_argnames
    cmdd = "python getallvms.py -s 192.168.88.238 -u administrator@dev.local -p Dev0psi0t! -S -f".split()
    print args["vmname"]
    cmdd.append(args["vmname"])
    p = subprocess.Popen(cmdd, stdout=subprocess.PIPE)
    with open("last-vm-info.txt","wt") as f:
            f.write(p.stdout.read())
    p.wait()
    run_with_args("vsphere.py", args, vsphere_argnames)
    run_with_args("poweronvm.py", args, poweronvm_argnames)
    
    cmd = "python getallvms.py -s 192.168.88.238 -u administrator@dev.local -p Dev0psi0t! -S -f".split()
    cmd.append(args["vmname"])
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    uid = None

    for line in p.stdout:
        if "Bios" in line:
            args["uuid"]= line.split(",")[1][2:-3]

    p.wait()

    if p.returncode:
        print "getallvms.py returned non-zero value.\nTerminating." 
        exit(1)

    print "Got vm uuid as", args["uuid"] 
    try:
        run_with_args("soft_reboot.py", args, executeprogramm_argnames)
    except:
        print "Waiting for Machine to awake 10s First stage reboot. Applying network configuration..."
        #time.sleep(10)
        #run_with_args("execute_program_in_vm.py", args, executeprogramm_argnames)
    try:
        run_with_args("soft_reboot.py", args, executeprogramm_argnames)
    except:
        print "Waiting for Machine to awake 10s. Second stage reboot cleaning up old network leases, etc.."

    exit(0)

