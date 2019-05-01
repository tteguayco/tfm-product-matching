
class NodeURL():

    def __init__(self, url, level=0, url2detail=False):
        self.url = url
        self.level = level
    
    def __str__(self):
        return "{" + str(self.level) + "}: " + self.url
