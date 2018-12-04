#basic web scraping

import requests, bs4
import urllib.request
from PIL import Image
import os

#make directory

def ensure_dir(path):
	directory = 'C:/Users/VicFel/Documents/Programming/merlinsvoyage/{}'.format(path)
	if not os.path.exists(directory):
		os.makedirs(directory)


def web_scrapper(month_num, year):
	#dictionary of months
	month_dict = {
	1: 'January',
	2: 'February',
	3: 'March',
	4: 'April',
	5: 'May',
	6: 'June',
	7: 'July',
	8: 'August',
	9: 'September',
	10: 'October',
	11: 'November',
	12: 'December'
	}

	#setup
	post_counter = 0
	month = month_dict[month_num]
	print('Year: {}, Month: {}'.format(year, month))

	#ensure_dir('{}/'.format(month_num))
	url_o = 'http://www.merlinsvoyage.net/merlin-log/month/{}-{}'.format(month, year)

	res_o = requests.get(url_o)
	res_o.raise_for_status()
	soup_o = bs4.BeautifulSoup(res_o.text, features='html.parser')

	#number of pages
	num_pages = 1
	pagination_html = soup_o.select('.paginationPageNumber')
	if (len(pagination_html) > 1):
		num_pages = len(pagination_html)
		
	for page in range(1, num_pages+1):
		url = 'http://www.merlinsvoyage.net/merlin-log/month/{}-{}?currentPage={}'.format(month, year, page)

		res = requests.get(url)
		res.raise_for_status()
		soup = bs4.BeautifulSoup(res.text, features='html.parser')
		print ('page: {}'.format(page))


		entry_list = soup.select('.journal-entry-text')
		post_num = len(entry_list)

		#number of pages
		num_pages = (post_num / 5) + 1

		for post in range(0, post_num):
			#increase conters
			post_counter += 1

			img_counter = 0
			
			#a folder to store the info in
			direrctory_post = '{}/{}/{}/'.format(year, month_num, post_counter)
			ensure_dir(direrctory_post)

			#get file
			file = open('{}/blog.txt'.format(direrctory_post), 'w')

			
			entry = entry_list[post]
			
			#title
			title = entry.select('.title')[0].getText()
			file.write(('Title: |{}|\n').format(title.encode('utf-8')))
			#print ('title is: {}'.format(title))

			#date
			journal_tag = entry.select('.journal-entry-tag-post-title')
			post_date = journal_tag[0].select('.posted-on')[0].getText()
			file.write(('Date: |{}|\n').format(post_date.encode('utf-8')))
			#print ('date is: {}'.format(post_date))

			#body
			content = entry.select('.body')[0]
			paragraphs_list = content.select('p')
			paragraphs_len = len(paragraphs_list)

			#getting info from each paragraph
			for para in range(0, paragraphs_len):
				body_i = paragraphs_list[para]

				#if there's an image
				if (int(len(body_i.select('span img')) > 0)):

					img_counter += 1
					file.write(('Image: |{}|\n').format(img_counter))
					#print(("Yay it's the {} image of the post").format(img_counter))
					#print ('Image url:')

					#get image details
					image = body_i.select('span img')[0]
					file_name = '{}/{}.jpg'.format(direrctory_post, img_counter)
					img_url = 'http://www.merlinsvoyage.net{}'.format(image['src'])
					#print (img_url)

					#download image
					img_inst = Image.open(requests.get(img_url, stream = True).raw)
					img_inst.save(file_name)




				#otherwise just get text
				else:
					file.write(('Paragraph:|\n{}\n|').format(body_i.getText().encode('utf-8')))
				#print('text: \n {}'.format(body_i.getText()))

			file.close()
			print ('Done')
	print('Finished {}, {}'.format(month, year))
		#for images, get src then add www.merlinsvoyage.net/
