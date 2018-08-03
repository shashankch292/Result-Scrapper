# Scrapes the result of all the students in a branch and stores in a file

import time, threading
from selenium import webdriver

print('Enter the Branch Code:')
code = raw_input()

data = []

def result(startNum, endNum):
	browser = webdriver.PhantomJS()
	browser.get('http://result.ietlucknow.ac.in/ODDSEM201718')

	for i in range(startNum, endNum):
		elem = browser.find_elements_by_tag_name('input')
		elem[0].clear()

		if i > 900:
			elem[0].send_keys('16052' + code + str(i))
		elif i < 10:
			elem[0].send_keys('15052' + code + '00' + str(i))
		else:
			elem[0].send_keys('15052' + code + '0' + str(i))
		elem[0].submit()

		time.sleep(0.6)

		try:
			table = browser.find_elements_by_tag_name('td')
			#print(table[5].text + ' -- ' +  table[1].text + ' -- ' + table[82].text)
			data.append((table[5].text, table[82].text, table[1].text))
			browser.back()
		except:
			continue

	browser.quit()


downloadThreads = []
for i in range(1, 61, 5):
	downloadThread = threading.Thread(target = result, args=(i, i+5))
	downloadThreads.append(downloadThread)
	downloadThread.start()

for i in range(901, 921, 5):
	downloadThread = threading.Thread(target = result, args=(i, i+5))
	downloadThreads.append(downloadThread)
	downloadThread.start()

# Wait for all threads to end.
for downloadThread in downloadThreads:
	downloadThread.join()

file = open('Branch Code=' + code + ' Result.txt', 'w')

Sno = 1
for (x,y,z) in reversed(sorted(data, key=lambda data: data[1])):
	file.write((str(Sno) + '.').ljust(3) + x.ljust(11) + y.ljust(9) + z + '\n')
	Sno += 1

file.close()

print('Done.')