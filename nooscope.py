'''=======================================================
Nooscope: Version 1.0
Description: This program creates the class Nooscope 
to pull a Top Level Domain (TLD )report for a given 
domain/IP using tcpiputils.com & whoismind.com.

Input(via terminal): a single domain/IP or text file with 
line separated domain/IP values.

Output(via terminal): text display of TLD report
=========================================================='''


#handle import errors
#---------------------------------
import sys
import codecs

error_list = []
try:
	import requests
except ImportError:
	error_list.append('Error on import requests: Goto http://docs.python-requests.org/')
try:
	from bs4 import BeautifulSoup
except ImportError:
	error_list.append('Error on import BeautifulSoup: Goto https://www.crummy.com/software/BeautifulSoup/')
try:
	from tld import get_tld
except ImportError:
	error_list.append('Error on import get_tld: Goto https://pypi.python.org/pypi/tld')

if len(error_list) > 0:
	print '\n'.join(error_list)
	exit()
#---------------------------------

# class to pull DNS information from tcpiputils.com &
# Whois information from whoismind.com
# define class with a 'source' which can be a domain or ip address
class nooscope: 	

	def __init__(self, source, is_domain=True):
		self.source = source
		self.is_domain = is_domain
		self.datafields = []
		self.data = {}

	def __str__(self):
		str_return = []
		
		#print for domain
		if self.is_domain == True:
			for category in self.datafields:
				if category == 'DNS server (NS records)':
					str_return.append(category + ':')
					for server in self.data['domain'][category]:
						str_return.append('\t' + server)

				elif category == 'Mail server (MX records)':
					str_return.append(category + ':')
					for server in self.data['domain'][category]:
						str_return.append('\t' + server)

				elif category == 'IP address (IPv4)':
					str_return.append(category + ':')
					for address in self.data['domain'][category]:
						str_return.append('\t' + address)

				elif category == 'Domain in directory':
					str_return.append(category + ': ' + self.data['domain'][category][0])
					for path in self.data['domain'][category]:
						str_return.append('\t' + path)

				elif category == 'Network History':
					str_return.append(category + ':')
					str_return.append('\t' + 'Number of IP history records: ' + self.data['domain'][category]['Number of IP history records'])
					str_return.append('\t' + 'Number of DNS history records: ' + self.data['domain'][category]['Number of DNS history records'])
					str_return.append('\t' + 'Number of MX history records: ' + self.data['domain'][category]['Number of MX history records'])
					str_return.append('\t' + 'Number of SPF history records: ' + self.data['domain'][category]['Number of SPF history records'])

				elif category == 'Update information':
					str_return.append(category + ':')
					str_return.append('\t' + 'Alexa ranking: ' + self.data['domain'][category]['Alexa ranking'])
					str_return.append('\t' + 'AS number information: ' + self.data['domain'][category]['AS number information'])
					str_return.append('\t' + 'DMOZ open directory: ' + self.data['domain'][category]['DMOZ open directory'])
					str_return.append('\t' + 'Network information: ' + self.data['domain'][category]['Network information'])
					str_return.append('\t' + 'PageRank: ' + self.data['domain'][category]['PageRank'])
					str_return.append('\t' + 'WOT Reputation Scorecard: ' + self.data['domain'][category]['WOT Reputation Scorecard'])

				else:
					str_return.append(category + ': ' + self.data['domain'][category])
		
		#print for IP
		elif self.is_domain == False:
			for category in self.datafields:
				if category == 'DNS server (NS record)':
					str_return.append(category + ':')
					for server in self.data['ip'][category]:
						str_return.append('\t' + server)

				elif category == 'Hosting information':
					str_return.append(category + ':')
					str_return.append('\t' + 'Number of domains hosted: ' + self.data['ip'][category]['Number of domains hosted'])
					str_return.append('\t' + 'Number of mail servers hosted: ' + self.data['ip'][category]['Number of mail servers hosted'])
					str_return.append('\t' + 'Number of name servers hosted: ' + self.data['ip'][category]['Number of name servers hosted'])
				
				elif category == 'Hosting history':
					str_return.append(category + ':')
					str_return.append('\t' + 'Number of domains hosted: ' + self.data['ip'][category]['Number of domains hosted'])
					str_return.append('\t' + 'Number of mail servers hosted: ' + self.data['ip'][category]['Number of mail servers hosted'])
					str_return.append('\t' + 'Number of name servers hosted: ' + self.data['ip'][category]['Number of name servers hosted'])

				else:
					str_return.append(category + ': ' + self.data['ip'][category])

		else: 
			str_return.append('no data')

		return '\n'.join(str_return)


	def pull(self):
		#run domain pull
		if self.is_domain == True:
			categories = ['Domain name', 'Top-level domain (TLD)', 'Current ranking Alexa', 
			'Google PageRank', 'Trustworthiness', 'Child safety', 'DNS server (NS records)', 
			'Mail server (MX records)', 'IP address (IPv6)', 'ASN number', 'ASN name (ISP)', 
			'SPF']

			#scrape tcpiputils for DNS data
			url = "http://www.tcpiputils.com/browse/domain/" + self.source
			html = requests.get(url).text
			soup = BeautifulSoup(html, 'lxml')
			tds = soup.find_all('td')
			tables = [td.text.encode('utf-8') for td in tds]
			table_dict = {}

			for category in categories:
				try:
					table_dict[category] = tables[tables.index(category)+1]
				except ValueError:
					table_dict[category] = 'N/A'

			#set other fields
			table_dict['IP address (IPv4)'] = 'N/A'
			table_dict['IP-range/subnet'] = 'N/A'
			table_dict['Domain in directory'] = 'N/A'
			table_dict['Network History'] = {
			'Number of IP history records': 'N/A', 
			'Number of DNS history records': 'N/A',
			'Number of MX history records': 'N/A',
			'Number of SPF history records': 'N/A'
			}
			table_dict['Update information'] = {
			'Alexa ranking': 'N/A', 
			'AS number information': 'N/A',
			'DMOZ open directory': 'N/A',
			'Network information': 'N/A',
			'PageRank': 'N/A',
			'WOT Reputation Scorecard': 'N/A'
			}


			if table_dict['DNS server (NS records)'] != 'N/A':
				servers = table_dict['DNS server (NS records)'].replace(')', '), ', table_dict['DNS server (NS records)'].count(')')-1)
				table_dict['DNS server (NS records)'] = servers.split(', ')
			else:
				table_dict['DNS server (NS records)'] = ['N/A']

			if table_dict['Mail server (MX records)'] != 'N/A':
				servers = table_dict['Mail server (MX records)'].replace(')', '), ', table_dict['Mail server (MX records)'].count(')')-1)
				table_dict['Mail server (MX records)'] = servers.split(', ')
			else:
				table_dict['Mail server (MX records)'] = ['N/A']

			for j in range(len(tds)):
				if tds[j-1].text == 'IP address (IPv4)':
					for i in range(len(tds[j].find_all("br"))-1):
						tds[j].find_all("br")[0].replace_with(', ')
					table_dict['IP address (IPv4)'] = tds[j].text.split(', ')

				if tds[j-1].text == 'IP-range/subnet':
					tds[j].find_all("br")[0].replace_with(", ")
					table_dict['IP-range/subnet'] = tds[j].text

				if tds[j-1].text == 'Domain in directory':
					i = 0
					DinD = []
					while tds[j+i].text != 'Trustworthiness':
						DinD.append(tds[j+i].text)
						i += 1
					table_dict['Domain in directory'] = DinD

			categories.insert(8, 'IP address (IPv4)')
			categories.insert(13, 'IP-range/subnet')
			categories.insert(14, 'Domain in directory')

			try:
				table_dict['Network History']['Number of IP history records'] = tables[tables.index('Number of IP history records')+1]
				table_dict['Network History']['Number of DNS history records'] = tables[tables.index('Number of DNS history records')+1]
				table_dict['Network History']['Number of MX history records'] = tables[tables.index('Number of MX history records')+1]
				table_dict['Network History']['Number of SPF history records'] = tables[tables.index('Number of SPF history records')+1]
			except Exception:
				pass

			categories.insert(14, 'Network History')

			try:
				table_dict['SPF'] = soup.pre.text
			except AttributeError:
				table_dict['SPF'] = 'N/A'

			try:
				table_dict['Update information']['Alexa ranking'] = tables[tables.index('Alexa ranking')+1]
				table_dict['Update information']['AS number information'] = tables[tables.index('AS number information')+1]
				table_dict['Update information']['DMOZ open directory'] = tables[tables.index('DMOZ open directory')+1]
				table_dict['Update information']['Network information'] = tables[tables.index('Network information')+1]
				table_dict['Update information']['PageRank'] = tables[tables.index('PageRank')+1]
				table_dict['Update information']['WOT Reputation Scorecard'] = tables[tables.index('WOT Reputation Scorecard')+1]
			except Exception:
				pass

			categories.insert(18, 'Update information')
			#Whois
			user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8'
			headers = {'User-Agent': user_agent}
			url = "http://www.whoismind.com/whois/" + self.source + ".html"
			r = requests.get(url, headers=headers)
			soup = BeautifulSoup(r.text, 'lxml')
			whois = soup.findAll("div", { "class" : "raw_content" })
			if len(whois) == 1:
				if len(whois[0]) > 0:
					table_dict['Whois'] = whois[0].text[5:]
				else:
					table_dict['Whois'] = 'N/A'
			else:
				table_dict['Whois'] = 'N/A'

			categories.insert(18, 'Whois')

			self.datafields = categories
			self.data['domain'] = table_dict

		#run ip pull
		if self.is_domain == False:
			categories = ['IP address', 'Registry', 'Reverse DNS (PTR record)', 
			'DNS server (NS record)', 'ASN number', 'ASN name (ISP)']

			url = "http://www.tcpiputils.com/browse/ip-address/" + self.source
			html = requests.get(url).text
			soup = BeautifulSoup(html, 'lxml')
			tds = soup.find_all('td')
			tables = [td.text.encode('utf-8') for td in tds]
			table_dict = {}

			for category in categories:
				try:
					table_dict[category] = tables[tables.index(category)+1]
				except ValueError:
					table_dict[category] = 'N/A'

			# handle readability DNS server (NS record) -- ', ' after every entry except last
			if table_dict['DNS server (NS record)'] != 'N/A':
				servers = table_dict['DNS server (NS record)'].replace(')', '), ', table_dict['DNS server (NS record)'].count(')')-1)
				table_dict['DNS server (NS record)'] = servers.split(', ')
			else:
				table_dict['DNS server (NS record)'] = ['N/A']

			# insert and handle readability w/ IP-range/subnet -- add ', ' between
			dh = []
			mh = []
			nsh = []

			for j in range(len(tds)):
				if tds[j-1].text == 'IP-range/subnet':
					tds[j].find_all("br")[0].replace_with(", ")
					table_dict['IP-range/subnet'] = tds[j].text

				if tds[j-1].text == 'Number of domains hosted':
					dh.append(tds[j].text)

				if tds[j-1].text == 'Number of mail servers hosted':
					mh.append(tds[j].text)

				if tds[j-1].text == 'Number of name servers hosted':
					nsh.append(tds[j].text)

			categories.insert(7, 'IP-range/subnet')
			if 'IP-range/subnet' not in table_dict:
				table_dict['IP-range/subnet'] = 'N/A'

			if len(dh) == len(mh) == len(nsh) >= 1:
				table_dict['Hosting information'] = {
				'Number of domains hosted': dh[0], 
				'Number of mail servers hosted': mh[0],
				'Number of name servers hosted': nsh[0]}
			else:
				table_dict['Hosting information'] = {
				'Number of domains hosted': 'N/A', 
				'Number of mail servers hosted': 'N/A',
				'Number of name servers hosted': 'N/A'}

			if len(dh) == len(mh) == len(nsh) > 1:
				table_dict['Hosting history'] = {
				'Number of domains hosted': dh[1], 
				'Number of mail servers hosted': mh[1],
				'Number of name servers hosted': nsh[1]}
			else:
				table_dict['Hosting history'] = {
				'Number of domains hosted': 'N/A', 
				'Number of mail servers hosted': 'N/A',
				'Number of name servers hosted': 'N/A'}

			categories.insert(8, 'Hosting information')
			categories.insert(9, 'Hosting history')

			self.datafields = categories
			self.data['ip'] = table_dict

# run from command line
def main():
	
	#check to see if source is ip address
	def ip_check(ip_arg):
		if len(ip_arg.split('.')) == 4:
			isnum = True
			for i in range(0, 4):
				isnum = isnum & unicode(ip_arg.split('.')[i]).isnumeric()
			if isnum == True:
				return True
			else:
				return False
	
	#handle http:// for tld check
	def tld_setup(domain_arg):
		http = domain_arg[0:7]
		https = domain_arg[0:8]

		if http == 'http://':
			tld_check = domain_arg
			domain = domain_arg[7:]
		elif https == 'https://':
			tld_check = domain_arg
			domain = domain_arg[8:]
		else:
			tld_check = "http://" + domain_arg
			domain = domain_arg

		return (tld_check, domain)
	
	# make sure domain argument gets passed 
	if len(sys.argv) >= 2:
		end = len(sys.argv[1])
		
		# handle 1 ip/domain on command line
		if sys.argv[1][end-4:end] != '.txt':
		
			#if argument is an ip address
			if ip_check(sys.argv[1]) == True:	
				try:
					site = nooscope(sys.argv[1], is_domain=False)
					site.pull()
					print site
				except Exception as e: print str(e)

			#if argument is a domain
			else:
				[tld_check, domain] = tld_setup(sys.argv[1])
				try:
					get_tld(tld_check)
					try: 
						site = nooscope(domain)
						site.pull()
						print site
					except Exception as e: print str(e)
				except Exception as e: print str(e)
		
		# handle .txt file with domains every new line
		else:
			with codecs.open(sys.argv[1], 'r', "utf-8") as f:
				f_out = f.read().split('\n')
			f.close()
			
			# test for proper TLDs
			for line in f_out:

				if ip_check(line) == True:
					try:
						site = nooscope(line, is_domain=False)
						site.pull()
						print site
						print "---------------"
					except Exception as e: print str(e)

				else:
					[tld_check, domain] = tld_setup(line)
					try: 
						get_tld(tld_check)
						
						# run nooscope for all domains with proper TLD
						try: 
							site = nooscope(domain)
							site.pull()
							print site
							print "---------------"
						except Exception as e: print str(e)

					except Exception:
						pass # if no TLD
				
	else:
		print "Please pass a single domain name or .txt file of domain names"

if __name__ == "__main__":
	main()