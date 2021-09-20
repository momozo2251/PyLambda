from selenium import webdriver
import boto3

def lambda_handler(event, context):
    options = webdriver.ChromeOptions()

    # のちほどダウンロードするバイナリを指定
    options.binary_location = "./bin/headless-chromium"

    # headlessで動かすために必要なオプション
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")

    # set driver and url
    driver = webdriver.Chrome(
        "./bin/chromedriver",
        chrome_options=options)
    url = 'https://www.google.com/search?q=%E8%AA%BF%E5%B8%83+%E5%A4%A9%E6%B0%97'
    driver.get(url)
    title = driver.title

    # get width and height of the page
    w = driver.execute_script("return document.body.scrollWidth;")
    #h = driver.execute_script("return document.body.scrollHeight;")
    # set window size
    driver.set_window_size(w,600)
    # Get Screen Shot
    weather_capture = driver.save_screenshot('/tmp/weather.png')
    driver.close()

    # s3
    s3 = boto3.client('s3')
    bucket = 'weather-capture'
    s3.upload_file(Filename="/tmp/weather.png",
                   Bucket=bucket,
                   Key="weather.png")

    return title
