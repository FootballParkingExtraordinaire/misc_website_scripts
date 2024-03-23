""" Fetches all webpages and saves a screenshot of the map element """
error_text_mail = ""

try:
	import os
	from glob import iglob
	import traceback
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.chrome.service import Service as ChromeService
	from selenium.webdriver.common.by import By
	
	def save_screenshot(driver: webdriver.Chrome, path: str = '/tmp/screenshot.png') -> None:
		original_size = driver.get_window_size()
		required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
		required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
		driver.set_window_size(required_width, required_height)
		driver.find_element(By.ID,"map").screenshot(path)  # avoids scrollbar
		driver.set_window_size(original_size['width'], original_size['height'])

	from selenium.webdriver.chrome.service import Service

	service = Service(executable_path=r'/usr/bin/chromedriver')

	print('Starting headless Chromium browser...')
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--window-size=1366,768')
	driver = webdriver.Chrome(service=service,options=chrome_options)
	driver.command_executor.set_timeout(10)
	print('Chromium started!')
	
	directoryglob = 'public/**/ # Note the added asterisks
	datajsonlist = [f for f in iglob(directoryglob, recursive=False) if os.path.isfile(f)]
	for f in datajsonlist:
		url = os.path.basename(os.path.dirname(f))
		print("====== "+url+" ======") 
		try:
			driver.get("https://website.com/"+url+"/");
			save_screenshot(driver, 'public/'+url+'/map.png')
		except Exception: # Catch all exceptions so we can continue updating
			traceback.print_exc()
			error_text_mail=error_text_mail+'\n'+traceback.format_exc()
	driver.quit()
except Exception: # Catch all exceptions so we can continue updating
	traceback.print_exc()
	error_text_mail=error_text_mail+'\n'+traceback.format_exc()
