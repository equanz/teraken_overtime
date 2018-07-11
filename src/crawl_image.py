# import module
from urllib import request, error
import datetime
import os
import sys

def crawl_image():
    URI = "http://www.tsuyama-ct.ac.jp/image/web-image/webimage0.jpg"

    # try to request
    try:
        res = request.urlopen(URI).read()
    except error.URLError as e:
        return {
            "image": None,
            "err": e
        }
    finally:
        # response data
        return {
            "image": res,
            "err": None
        }

def save_data(dest_data, dir_path=os.getenv('HOME') + "/", file_path="image.jpg"):
    # create directory
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # save into ${dir_path}${file_path}
    with open(dir_path + file_path, mode='wb') as w:
        w.write(dest_data)

def main():
    # get image
    crawl_data = crawl_image()

    if crawl_data['err'] == None: # no error exist
        # destination directory
        DIR_PATH = os.getenv('HOME') + "/teraken_overtime_dump/"
        # create filepath string
        now_date = datetime.datetime.today()
        file_path = now_date.strftime("%Y%m%d%H%M") + ".jpg"

        # save image
        save_data(crawl_data['image'], dir_path=DIR_PATH, file_path=file_path)
        print('saved!')
    else: # error exist
        sys.stderr.write(crawl_data['err'])
        print('not saved!')

# run as main program
if __name__ == "__main__":
    main()

