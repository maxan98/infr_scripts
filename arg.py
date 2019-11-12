


def main():

	dst = ""
	toad = ""
	top = ""
	with open("2IP.txt") as f:
		toad = f.read()
	with open("toport.txt") as f:
		top = f.read()
	with open("dstport.txt") as f:
		dst = f.read()
	string = f"""
/ip/firewall/nat/add
=chain=dstnat
=protocol=tcp
=dst-port={dst}
=in-interface=ether1
=action=netmap
=to-addresses={toad}
=to-ports={top}




	"""
	print(string)

if __name__ == '__main__':
	main()