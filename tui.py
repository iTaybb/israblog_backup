import os.path
import colorama
import sys
import time
import logging

import scrapper

colorama.init()
logging.basicConfig(level=logging.CRITICAL)

print(colorama.Back.GREEN + colorama.Fore.GREEN + colorama.Style.BRIGHT + '### Israblog Blog Backup v{0} ###'.format(scrapper.__VERSION__) + colorama.Style.RESET_ALL)
print(colorama.Back.YELLOW + colorama.Fore.YELLOW + colorama.Style.BRIGHT + 'Written by Itay Brandes\r\n' + colorama.Style.RESET_ALL)

if len(sys.argv) >= 2:
	print("Requested to backup blog {}.".format(sys.argv[1]))
	blogid = sys.argv[1]
	if not blogid.isdigit() or not 1 <= int(blogid) <= 900000:
		print(colorama.Fore.RED + colorama.Style.BRIGHT + "Input invalid." + colorama.Style.RESET_ALL)
		sys.exit(1)
	if not scrapper.is_blog_exists(blogid):
		print(colorama.Fore.RED + colorama.Style.BRIGHT + "Blog does not exist, or it's private." + colorama.Style.RESET_ALL + " If it's private, please set it to public beforehand.")
		sys.exit(1)
else:
	while True:
		blogid = input("Please enter the blog ID you want to backup: ")
		while not blogid or not blogid.isdigit() or not 1 <= int(blogid) <= 900000:
			print(colorama.Fore.RED + colorama.Style.BRIGHT + "Input invalid." + colorama.Style.RESET_ALL + " Please enter the blog ID you want to backup: ", end="")
			blogid = input()

		if not scrapper.is_blog_exists(blogid):
			print(colorama.Fore.RED + colorama.Style.BRIGHT + "Blog does not exist, or it's private." + colorama.Style.RESET_ALL + " If it's private, please set it to public beforehand.")
		else:
			break

start = time.time()
dl_path = os.path.join(scrapper.BACKUP_FOLDER, "blog{0}".format(blogid))
scrapper.main(blog_id=blogid, dl_path=dl_path)
end = time.time()
print("Took {:.2f} seconds.".format(end - start))

os.startfile(os.path.join(dl_path, 'landing.htm'))
