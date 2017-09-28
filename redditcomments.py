import scrapy
#to do: empty posts/ get link text / posts with multiple paragraphs or whatever
class RedditSpider(scrapy.Spider):
    name = "reddit"

    start_urls = [
        'https://www.reddit.com/r/france/',
        'https://www.reddit.com/r/Quebec/',
        'https://www.reddit.com/r/etsmtl/',
        'https://www.reddit.com/r/PolyMTL/',
        'https://www.reddit.com/r/BiereQc/',  
        ]
    
    def traverse(self, currentComment, dialogue, dialogues, utterers):
        author = currentComment.xpath('@data-author').extract_first()
        if not author in utterers:
            utterers.append(author)
        dialogue += '\t\t<utt uid=' + str(utterers.index(author)) + '>'
        dialogue += currentComment.xpath('./div[contains(@class, "entry unvoted")]/form/div/div/p/text()').extract_first()    
        dialogue += '</utt>\n'
        childComments = currentComment.xpath('./div[contains(@class, "child")]/div/div[contains(@data-type, "comment")]')
        if len(childComments) == 0:
            dialogues.write(dialogue + '\t</s>\n')
            return
        self.traverse(childComments[0], dialogue, dialogues, utterers[:])

    def parse(self, response):
        for href in response.css('li.first a::attr(href)'):
            yield response.follow(href, self.parse_comments)

        for href in response.css('span.next-button a::attr(href)'):
            yield response.follow(href, self.parse)
    def parse_comments(self, response):
        dialogues = open('dialoguefile.xml', 'a')
        FirstComments = response.css('div.commentarea').xpath('//div[contains(@class, "sitetable nestedlisting")]/div[contains(@data-type, "comment")]')
        for FirstComment in FirstComments:
            if FirstComment.css('div.child').xpath('./node()').extract():
                currentComment = FirstComment
                dialogue = '\t<s>\n'
                self.traverse(currentComment, dialogue, dialogues, [])

        dialogues.close()
#gets all comments on a page (text value)   
#response.xpath('//div[@data-type=$val]/div[contains(@class, "entry unvoted")]/form/div/div/p/text()', val = 'comment').extract()
