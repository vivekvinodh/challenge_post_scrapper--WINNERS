from threading import Thread
from bs4 import BeautifulSoup
from urllib import urlopen

#Url strings
url_front = "http://challengepost.com/software/search?page="
url_end = "&query=is%3Awinner"

def find_in_page(link, first_tag, second_tag):
    req = urlopen(link).read()
    soup = BeautifulSoup(req)
    return [x.text for x in soup.find_all(first_tag, second_tag)] 

def find_challenge_winners(link):
    req = urlopen(link).read()
    soup = BeautifulSoup(req)
    return  [x.get('href') for x in soup.find_all("a","block-wrapper-link fade link-to-software")]

def find_tags(link):
    req = urlopen(link).read()
    soup = BeautifulSoup(req)
    return [x.text.replace("'", "").encode('utf8') for x in soup.find_all("span", "cp-tag recognized-tag")] 

def find_create(link):
    req = urlopen(link).read()
    soup = BeautifulSoup(req)
    return [x.text.replace("'", "").encode('utf8') for x in soup.find_all("a","user-profile-link")] 

def find_hack(link):
    req = urlopen(link).read()
    soup = BeautifulSoup(req)
    return soup.find("div", "software-list-content").a.text.replace("'", "").encode('utf8')

def go_get_data(idx,range_start, range_end):
    with open("data" + str(idx) + ".sql", "a") as myfile:
        for i in xrange(range_start, range_end):
            page = url_front + str(i) + url_end
            for win in find_challenge_winners(page):
                sql = "INSERT INTO hackpoly VALUES ("
                sql += "'" + win.split('http://challengepost.com/software/')[1].encode('utf8')+ "', "
                sql += "'" + find_hack(win)  + "'"
                sql += "'" + win.encode('utf8')+ "', "
                sql += "{" + ",".join('"{0}"'.format(w) for w in filter(None,find_tags(win))) + "},"
                sql += "{" + ",".join('"{0}"'.format(w) for w in filter(None,find_create(win))) + "}"
                sql += ");"
                myfile.write(sql) 
                myfile.write("\n")
                myfile.flush()

t1 = Thread(target=go_get_data, args=(0, 0, 28))
t2 = Thread(target=go_get_data, args=(1, 29, 56))
t3 = Thread(target=go_get_data, args=(2, 57, 84))
t4 = Thread(target=go_get_data, args=(3, 85, 110))

t1.start()
t2.start()
t3.start()
t4.start()
