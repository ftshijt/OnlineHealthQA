import re
import requests
import traceback

head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Cookie': 'guid=97b6b81de4b87637e6c1654ea99940dfa3693f17; __gads=ID=03d44f7efa080256:T=1507815730:S=ALNI_MaZ7t-7tcT_kM7h8S7UcOFkQ6s7sA; _igg=pW13We3a8ZDcGuLniRk1; sort_by=first_post; _medhelp_session=228981afa02e4c70d02c7a6541203ab3; _ga=GA1.2.1823142418.1507815730; _gid=GA1.2.1872544567.1508510082; s_cc=true; s_sq=%5B%5BB%5D%5D; __ybotb=c4f0; __ybotu=j8oijzc3fly5zxkfvw; __ybotv=1508517730027; __ybots=j904i9ykd5n5li2gh9.0.j904i9yjwc0ye2jk39.1; _igt=9dfbe19e-7df1-45d6-9d53-0c8b5a117aba; _ig=616321d2-b717-4313-a9de-4ee85ee3e3e5; __ybotc=http%3A//ads-adseast-vpc.yldbt.com/m/; __ybotn=1',
            'Host': 'www.medhelp.org'
            }

def extract_url(list):
    result = []
    for l in list:
        temp = (re.search("<div class='fonts_resizable_subject subject_title  hn_16b' >(.*?)</div>", l, re.S)).group(1)
        result.append('www.medhelp.org' + re.search('<a href="(.*?)"', temp, re.S).group(1))
    return result

def main():
    urlx = 'http://www.medhelp.org/forums/Depression/show/57?page'
    file = open("data.txt", "w+")
    fileing = open("error.txt", "w+")
    #file.write("yes\n")
    for i in range(1, 695):
        extract = []
        list = []
        try:
            url = urlx + "=%d"%i
            print(url)
            html = requests.get(url=url, headers=head)
            list = re.findall("<div class='new_subject_element float_fix'>(.*?)<span class='mh_timestamp'",html.text, re.S)
            extract = extract_url(list)
            print(extract)
        except:
            traceback.print_exc()
            fileing.write("%d\n" % i)
        for l in extract:
            file.write(l)
            file.write("\n")
            file.flush()
        print(list)




main()