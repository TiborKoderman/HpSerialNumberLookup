#tibors classes

class bColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class ProgressBar():
    @staticmethod
    def draw(iterator, length, sizeOfBar,endc = '\r',color = bColors.OKBLUE, fchar ='█' , echar = '░'):
        percent = "{:.2f}".format((iterator/float(length))*100)+'%'
        full = sizeOfBar * iterator//length
        bar = fchar*full + echar *(sizeOfBar-full)
        
        print(f'\r[{color}{bar}'+bColors.ENDC+'] '+percent + ' [' +str(iterator) + '/' +str(length) + ']', end= endc)
        

