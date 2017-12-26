import urllib.request
import urllib.parse
import os
import re
import argparse
import sys
import logging
import time
from distutils.dir_util import copy_tree

from bs4 import BeautifulSoup
import colorama
import progressbar

### VARS ###
__VERSION__ = '2017.12.27'
ISRABLOG_HOSTNAME = 'http://israblog.nana10.co.il'
REFERER = "{}/blogread.asp?blog={}"  # formatted just before main()
USERAGENT = 'IsrablogScrapper {}'.format(__VERSION__)
WORKING_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))
INJECT_DIR = os.path.join(WORKING_DIR, 'inject')
BACKUP_FOLDER = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
LOGGING_LEVEL = logging.WARN
ENABLE_PROGRESSBAR = True

# only for chunks. not relevant for backuping the blog
CHUNKS_OUTPUT_PATH = r'd:\tmp'  
CHUNK_SIZE = 5000
MAX_BLOG_SCAN = 900000

# regexes
blog_page_regex = re.compile(r'\?blog=\d+&page=(\d+)')
blog_post_regex = re.compile(r'.*\?blog=\d+&blogcode=(\d+)')
blog_month_regex = re.compile(r'^\?blog=\d+&year=(\d+)&month=(\d+)(?:&.*pagenum=(\d+))?')
blog_readlist_regex = re.compile(r'^BlogReadLists\.asp\?blog=\d+&(?:.*)ListColumns=(\d+)&SideGroup=(\d+)')
drawmonthlink_regex = re.compile(r'drawMonthLinkNew')
commentlink_regex = re.compile(r'comments\.asp\?newcomment=&blog=(\d+)&user=\d+&commentuser=&origcommentuser=&posnew=(\d+)')
listframe_regex = re.compile(r'^ListFrame_\d$')


### FUNCS ###
def get_local_path(intent='main', year=None, month=None, postid=None, pagenum=1, relative=False, dl_path=None, sidebar_cols=None, sidebar_group=None):
	if intent == 'main':
		if not year and not month:
			path = 'index.htm'
		else:
			year = year if year else "1970"
			month = month if month else "0"
			path = '{}-{}-p{}.htm'.format(year, month, pagenum)
	elif intent == 'board_list':
		if not pagenum:
			path = 'board_list.htm'
		else:
			path = 'board_list-p{}.htm'.format(pagenum)
	elif intent == 'posts':
		path = 'post-{}.htm'.format(postid)
	elif intent == 'comments':
		if not pagenum:
			path = 'comments-{}.htm'.format(postid)
		else:
			path = 'comments-{}-p{}.htm'.format(postid, pagenum)
	elif intent == 'sidebar':
		path = 'sidebar-{}-{}.htm'.format(sidebar_cols, sidebar_group)

	if not relative:
		if not dl_path:
			raise Exception("dl_path is null")
		path = os.path.join(dl_path, path)

	return path


def get_url(blog_id, postid=None, intent='main', **kwargs):
	if intent == 'main':
		url = "{0}/blogread.asp?blog={1}".format(ISRABLOG_HOSTNAME, blog_id)
	elif intent == 'board_list':
		url = "{0}/board_list.asp?blog={1}".format(ISRABLOG_HOSTNAME, blog_id)
	elif intent == 'posts':
		url = "{0}/blogread.asp?blog={1}&blogcode={2}".format(ISRABLOG_HOSTNAME, blog_id, postid)
	elif intent == 'comments':
		url = "{0}/comments.asp?blog={1}&user={2}".format(ISRABLOG_HOSTNAME, postid, blog_id)
	elif intent == 'sidebar':
		url = "{0}/BlogReadLists.asp?blog={1}".format(ISRABLOG_HOSTNAME, blog_id)
	else:
		raise Exception("Not possible!")

	for k, v in kwargs.items():
		url += "&{}={}".format(k, v)

	return url


def dl_file(src, dst, encoding='windows-1255', force=False):
	if not src.startswith('http'):
		src = src.strip('/.')
		src = "{}/{}".format(ISRABLOG_HOSTNAME, src.strip('/'))

	if os.path.exists(dst) and not force:
		logging.info("File {} already exists. No need to download.".format(dst))
		with open(dst, 'rb') as f:
			raw = f.read()
			if encoding:
				raw = raw.decode(encoding, 'surrogateescape')
	else:
		logging.info("Downloading {}".format(src))
		req = urllib.request.Request(src)
		req.add_header('Referer', REFERER)
		req.add_header('User-agent', USERAGENT)
		try:
			with urllib.request.urlopen(req) as f:
				raw = f.read()
				if encoding:
					raw = raw.decode(encoding, 'surrogateescape')
		except urllib.error.URLError as e:
			logging.error("URLError while fetching %s: %s", src, str(e))
			return ''
		except UnicodeEncodeError as e:
			logging.error("UnicodeEncodeError: %s", str(e))
			return ''

		logging.info("Saving {}".format(dst))
		if not os.path.exists(os.path.dirname(dst)):
			os.makedirs(os.path.dirname(dst))

		with open(dst, 'wb') as f:
			if encoding:
				f.write(raw.encode(encoding, 'surrogateescape'))
			else:
				f.write(raw)

	return raw


def dl_and_replace_external_resources(soup, dl_path, fast=False):
	'''
		Fast=True skips downloading avatars.
	'''
	for tag in soup.find_all('img'):
		if tag.has_attr('src'):
			if not fast or '/avatar/' not in tag['src'].lower():
				tag['src'] = dl_external_resource(tag['src'], dl_path)

	for tag in soup.find_all('link'):
		if tag.has_attr('href'):
			if not fast or '/avatar/' not in tag['href'].lower():
				tag['href'] = dl_external_resource(tag['href'], dl_path)

	for tag in soup.find_all('script'):
		if tag.has_attr('src'):
			if not fast or '/avatar/' not in tag['src'].lower():
				tag['src'] = dl_external_resource(tag['src'], dl_path)

	tag = soup.find('meta', property='og:image')
	if tag:
		tag['content'] = dl_external_resource(tag['content'], dl_path)

	return soup


def dl_external_resource(link, dl_path):
	parsed = urllib.parse.urlparse(link)
	local_path = os.path.join(dl_path, parsed.netloc, parsed.path.strip('./').replace('/', '\\'))
	try:
		dl_file(link, local_path, encoding=None)
	except Exception as e:
		logging.error('Could not download %s: %s', link, str(e))

	localpath = "{}/{}".format(parsed.netloc, parsed.path) if parsed.netloc else link.strip('/')
	return localpath


def replace_internal_resources(soup, previous_month=None, next_month=None, saveTo=None, encoding="windows-1255"):
	for t in soup.find_all('a', href=blog_page_regex):
		t['href'] = get_local_path(intent='board_list', relative=True, pagenum=re.match(blog_page_regex, t['href']).group(1))

	for t in soup.find_all('a', href=blog_post_regex):
		t['href'] = get_local_path(intent='posts', relative=True, postid=re.match(blog_post_regex, t['href']).group(1))
	for t in soup.find_all('option', value=blog_post_regex):
		t['value'] = get_local_path(intent='posts', relative=True, postid=re.match(blog_post_regex, t['value']).group(1))

	for t in soup.find_all('a', href=blog_month_regex):
		m = re.match(blog_month_regex, t['href'])
		t['href'] = get_local_path(relative=True, year=m.group(1), month=m.group(2), pagenum=m.group(3) if m.group(3) else 1)

	#edit TDtitle link
	t = soup.find('a', class_='TDtitle')
	if t:
		t['href'] = get_local_path(relative=True)

	# board list
	t = soup.find('iframe', id='ifrmBoard')
	if t:
		t['src'] = get_local_path(intent='board_list', relative=True)

	# sidebar(s)
	for tag in soup.find_all('iframe', src=blog_readlist_regex):
		m = re.match(blog_readlist_regex, tag['src'])
		tag['src'] = get_local_path(intent='sidebar', relative=True, sidebar_cols=m.group(1), sidebar_group=m.group(2))

	# drawMonthLinkNew
	t = soup.find('script', text=drawmonthlink_regex)
	if t:
		new_tag = soup.new_tag('p')
		if previous_month:
			month, year = previous_month.split('/')
			elem = soup.new_tag('a', href=get_local_path(relative=True, year=year, month=month))
			elem.string = " החודש הקודם ({0})".format(previous_month)
			new_tag.insert(1, elem)

		if next_month:
			month, year = next_month.split('/')
			elem = soup.new_tag('a', href=get_local_path(relative=True, year=year, month=month))
			elem.string = "החודש הבא ({0})".format(next_month)
			new_tag.insert(1, elem)

		t.replace_with(new_tag)

	# replace comments.asp links
	for t in soup.find_all('a', href=commentlink_regex):
		m = re.match(commentlink_regex, t['href'])
		t['href'] = get_local_path(intent='comments', postid=m.group(1), pagenum=m.group(2), relative=True)

	# replace LoginMe and JoinIsrablog
	t = soup.find('div', id='LoginMe')
	if t:
		new_tag = soup.new_tag('p')
		new_tag.string = "ארכיון - גובה ע\"י ברנדס איתי"
		t.replace_with(new_tag)
	t = soup.find('div', id='JoinIsrablog')
	if t:
		t.string = ""

	# remove google recaptcha from comments
	if soup.find('table', class_='comment'):  # if it's comments page
		t = soup.find('script', src='www.google.com//recaptcha/api/challenge')
		if t:
			t.parent.parent.extract()

	# inject iframeResizer
	already_injected = False
	for tag in soup.find_all('iframe', id=listframe_regex):
		if not already_injected:
			tag.insert_after(BeautifulSoup("""<script type="text/javascript" src="iframeResizer.min.js"></script><script>iFrameResize({{log:false}}, '#{0}')</script>""".format(tag['id']), 'html.parser'))
			already_injected = True
		else:
			tag.insert_after(BeautifulSoup("""</script><script>iFrameResize({{log:false}}, '#{0}')</script>""".format(tag['id']), 'html.parser'))

	if saveTo:
		with open(saveTo, 'wb') as f:
			f.write(soup.prettify(encoding, formatter='html'))


def is_blog_exists(blog_id, encoding='windows-1255'):
	with urllib.request.urlopen(get_url(blog_id=blog_id)) as f:
		raw = f.read(100)
		if encoding:
			raw = raw.decode(encoding, 'surrogateescape')
		exists = 'noblog' not in raw
		public = 'private_login' not in raw

	return exists and public


def find_existing_blogs(from_=1, to=900000):
	blogs = []

	if ENABLE_PROGRESSBAR:
		bar = progressbar.ProgressBar(max_value=to-from_).start()
	for i in range(from_, to):
		if is_blog_exists(str(i)):
			blogs.append(i)
		bar.update(i-from_)
	if ENABLE_PROGRESSBAR:
		bar.finish()

	return blogs


def find_existing_blogs_chunks(chunk, chunksize=CHUNK_SIZE):
	# chunk is going from 0 to 159 (160 chunks)
	print("Processing Chunk {} (blogs {}-{} inclusive)".format(chunk, chunk*chunksize, (chunk+1)*chunksize-1))
	blogs = find_existing_blogs(chunk*chunksize, (chunk+1)*chunksize)

	dst = os.path.join(CHUNKS_OUTPUT_PATH, 'chunk_{:04d}.dat'.format(chunk))
	print("Saving to {}".format(dst))
	with open(dst, 'w') as f:
		for blog in blogs:
			f.write("{}\n".format(blog))


### CODE ###
def main(blog_id, dl_path, fast=False):
	global REFERER
	REFERER = REFERER.format(ISRABLOG_HOSTNAME, blog_id)

	logging.info("WORKING_DIR is %s", WORKING_DIR)
	print("Starting download of blog {} to destination {} (fast={}).".format(blog_id, dl_path, fast))
	if not os.path.exists(dl_path):
		os.makedirs(dl_path)

	logging.info("Copying %s to %s", INJECT_DIR, dl_path)
	copy_tree(INJECT_DIR, dl_path)

	post_ids = []

	# Main Page
	print("Downloading main page...")
	raw = dl_file(get_url(blog_id=blog_id), get_local_path(dl_path=dl_path))
	main_soup = BeautifulSoup(raw, 'html.parser')
	main_soup = dl_and_replace_external_resources(main_soup, dl_path, fast=fast)

	# sidebar
	print("Downloading sidebar page(s)...")
	for tag in main_soup.find_all('iframe', src=blog_readlist_regex):
		m = re.match(blog_readlist_regex, tag['src'])

		raw = dl_file(get_url(blog_id=blog_id, intent='sidebar', ListColumns=m.group(1), SideGroup=m.group(2)), get_local_path(intent='sidebar', dl_path=dl_path, sidebar_cols=m.group(1), sidebar_group=m.group(2)))
		raw = raw.replace('</body>', '<script type="text/javascript" src="iframeResizer.contentWindow.min.js"></script></body>')  # adding iframeResizer
		soup = BeautifulSoup(raw, 'html.parser')
		dl_and_replace_external_resources(soup, dl_path, fast=fast)
		replace_internal_resources(soup, saveTo=get_local_path(intent='sidebar', dl_path=dl_path, sidebar_cols=m.group(1), sidebar_group=m.group(2)))

	# Board List
	print("Downloading board list...")
	pagenum = 1
	while True:
		raw = dl_file(get_url(blog_id=blog_id, intent='board_list', page=pagenum), get_local_path(intent='board_list', pagenum=pagenum, dl_path=dl_path))
		soup = BeautifulSoup(raw, 'html.parser')
		if soup.find('a', href='?blog={}&page=2'.format(blog_id, pagenum + 1)):
			replace_internal_resources(soup, saveTo=get_local_path(intent='board_list', pagenum=pagenum, dl_path=dl_path))
			pagenum += 1
		else:
			replace_internal_resources(soup, saveTo=get_local_path(intent='board_list', pagenum=pagenum, dl_path=dl_path))
			pagenum += 1
			raw = dl_file(get_url(blog_id=blog_id, intent='board_list', page=pagenum), get_local_path(intent='board_list', pagenum=pagenum, dl_path=dl_path))
			soup = BeautifulSoup(raw, 'html.parser')
			replace_internal_resources(soup, saveTo=get_local_path(intent='board_list', pagenum=pagenum, dl_path=dl_path))
			break

	# Archive Dates
	archive_dates = [x.get('value') for x in main_soup.find('select', id="PeriodsForUser").find_all('option')]
	archive_dates.sort(key=lambda x: x.split('/')[1] + "{:02d}".format(int(x.split('/')[0])), reverse=True)
	print("Downloading archive pages...")
	if ENABLE_PROGRESSBAR:
		bar = progressbar.ProgressBar(max_value=len(archive_dates)).start()
	for i, date in enumerate(archive_dates):
		pagenum = 1
		pages_count = 1
		next_month = archive_dates[i - 1] if i > 0 else None
		previous_month = archive_dates[i + 1] if i < len(archive_dates) - 1 else None

		while pagenum <= pages_count:
			month, year = date.split('/')
			raw = dl_file(get_url(blog_id=blog_id, month=month, year=year, pagenum=pagenum), get_local_path(year=year, month=month, pagenum=pagenum, dl_path=dl_path))

			soup = BeautifulSoup(raw, 'html.parser')
			for tag in soup.find_all('a', href=re.compile('javascript:showCommentsHere')):
				post_ids.append(tag['href'].split('(')[1].split(',')[0])

			t = soup.find('script', text=re.compile('navigateCount'))
			pages_count = int(t.text.strip().split('=')[1].strip(';')) if t else 1
			logging.info("Pages count for {}/{}: {}".format(year, month, pages_count))

			dl_and_replace_external_resources(soup, dl_path, fast=fast)
			replace_internal_resources(soup, next_month=next_month, previous_month=previous_month, saveTo=get_local_path(year=year, month=month, pagenum=pagenum, dl_path=dl_path))

			pagenum += 1

		if ENABLE_PROGRESSBAR:
			bar.update(i)
	if ENABLE_PROGRESSBAR:
		bar.finish()

	# Save Main Page
	replace_internal_resources(main_soup, previous_month=archive_dates[1] if len(archive_dates) > 1 else None, saveTo=get_local_path(dl_path=dl_path))

	# Posts
	print("Downloading posts...")
	if ENABLE_PROGRESSBAR:
		bar = progressbar.ProgressBar(max_value=len(post_ids)).start()
	for i, postid in enumerate(post_ids):
		raw = dl_file(get_url(blog_id=blog_id, intent='posts', postid=postid), get_local_path(intent='posts', postid=postid, dl_path=dl_path))
		soup = BeautifulSoup(raw, 'html.parser')
		dl_and_replace_external_resources(soup, dl_path, fast=fast)
		replace_internal_resources(soup, saveTo=get_local_path(intent='posts', postid=postid, dl_path=dl_path))

		if ENABLE_PROGRESSBAR:
			bar.update(i)
	if ENABLE_PROGRESSBAR:
		bar.finish()

	# Comments
	print("Downloading comment pages...")
	if ENABLE_PROGRESSBAR:
		bar = progressbar.ProgressBar(max_value=len(post_ids)).start()
	for i, postid in enumerate(post_ids):
		pagenum = 1

		raw = dl_file(get_url(blog_id=blog_id, intent='comments', postid=postid), get_local_path(intent='comments', postid=postid, dl_path=dl_path))
		soup = BeautifulSoup(raw, 'html.parser')
		t = soup.find('table', id="Table3")
		pages_count = int(t.td.text.strip().split(' ')[-2]) if t else 1
		logging.info("Comment Pages count for {}: {}".format(postid, pages_count))
		dl_and_replace_external_resources(soup, dl_path, fast=fast)
		replace_internal_resources(soup, saveTo=get_local_path(intent='comments', postid=postid, dl_path=dl_path))

		pagenum += 1
		while pagenum <= pages_count:
			raw = dl_file(get_url(blog_id=blog_id, intent='comments', postid=postid, posnew=pagenum), get_local_path(intent='comments', postid=postid, pagenum=pagenum, dl_path=dl_path))
			soup = BeautifulSoup(raw, 'html.parser')
			dl_and_replace_external_resources(soup, dl_path, fast=fast)
			replace_internal_resources(soup, saveTo=get_local_path(intent='comments', postid=postid, pagenum=pagenum, dl_path=dl_path))
			pagenum += 1

		if ENABLE_PROGRESSBAR:
			bar.update(i)
	if ENABLE_PROGRESSBAR:
		bar.finish()

	print(colorama.Fore.GREEN + "Done!" + colorama.Style.RESET_ALL)


if __name__=='__main__':
	logging.basicConfig(level=LOGGING_LEVEL)
	colorama.init()

	parser = argparse.ArgumentParser(description='Backup israblog.')

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--backup', type=str, dest='blog_id', help='Backup this blog')
	group.add_argument('--scan', type=int, dest='chunk', help='Scan this chunk (0-{:.0f})'.format(MAX_BLOG_SCAN/CHUNK_SIZE))
	parser.add_argument('--fast', action='store_true', help='Backup faster (no avatars)')
	args = parser.parse_args()

	start = time.time()

	if args.blog_id:
		main(blog_id=args.blog_id, dl_path=os.path.join(BACKUP_FOLDER, args.blog_id), fast=args.fast)
	else:
		find_existing_blogs_chunks(args.chunk)

	end = time.time()
	print("Took {:.2f} seconds.".format(end - start))
