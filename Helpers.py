#tibors classes
import random


class bColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class ProgressBar:
    @staticmethod
    def draw(iterator, length, sizeOfBar,endc = '\r',color = bColors.OKBLUE, fchar ='█' , echar = '░'):
        percent = "{:.2f}".format((iterator/float(length))*100)+'%'
        full = sizeOfBar * iterator//length
        bar = fchar*full + echar *(sizeOfBar-full)
        
        print(f'\r[{color}{bar}'+bColors.ENDC+'] '+percent + ' [' +str(iterator) + '/' +str(length) + ']', end= endc)
        



class Proxy:
    @staticmethod
    def setProxyFF(FirefoxProfile, PROXY_HOST, PROXY_PORT):
        FirefoxProfile.set_preference("network.proxy.type", 1)
        FirefoxProfile.set_preference("network.proxy.http",PROXY_HOST)
        FirefoxProfile.set_preference("network.proxy.http_port",int(PROXY_PORT))
        FirefoxProfile.set_preference("general.useragent.override","whater_useragent")
        FirefoxProfile.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0")
        FirefoxProfile.set_preference("places.history.enabled", False)
        FirefoxProfile.set_preference("privacy.clearOnShutdown.offlineApps", True)
        FirefoxProfile.set_preference("privacy.clearOnShutdown.passwords", True)
        FirefoxProfile.set_preference("privacy.clearOnShutdown.siteSettings", True)
        FirefoxProfile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
        FirefoxProfile.update_preferences()
        return FirefoxProfile

    @staticmethod
    def GetRandomProxy(file_path):
        proxies = open(file_path).read().splitlines()
        PROXY = random.choice(proxies)
        PROXY.split(':')
        return PROXY[0], PROXY[1]


