import scrapy
from scrapy_splash import SplashRequest


class BitcoinSpider(scrapy.Spider):
    name = 'bitcoin'
    allowed_domains = ['finance.yahoo.com']
    script ='''
function main(splash, args)
  url = args.url
  assert(splash:go(args.url))
  assert(splash:wait(5))

  btn = assert(splash:select('#Col1-1-HistoricalDataTable-Proxy > section > div > div > div:nth-child(1) > div > div > div > span'))
  btn:mouse_click()
  assert(splash:wait(5))

  btn2 = assert(splash:select('#dropdown-menu > div > ul:nth-child(2) > li:nth-child(4) > button > span'))
  btn2:mouse_click()
  assert(splash:wait(15))

  btn3 = assert(splash:select('#Col1-1-HistoricalDataTable-Proxy > section > div > div > button > span'))
  btn3:mouse_click()
  assert(splash:wait(5))

  current_scroll = 0  

  scroll_to = splash:jsfunc("window.scrollTo")
  get_body_height = splash:jsfunc(
    "function() {return document.body.scrollHeight;}"
  )
  splash:wait(3)

  height = get_body_height()

  while current_scroll < height do
    scroll_to(0, get_body_height())
    splash:wait(5)
    current_scroll = height
    height = get_body_height()
  end 

  return {
    html = splash:html(),
  }
end'''
    
    def start_requests(self):
        yield SplashRequest(url='https://finance.yahoo.com/quote/BTC-USD/history/',callback=self.parse, endpoint="execute",args={
            'lua_source': self.script,'timeout': 3600
        })

    def parse(self, response):
        history = response.xpath('//tbody/tr[@class="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"]')
        for data in history:
            yield {
                'Date': data.xpath('(.//span)[1]/text()').get(),
                'Open': data.xpath('(.//span)[2]/text()').get(),
                'High': data.xpath('(.//span)[3]/text()').get(),
                'Low': data.xpath('(.//span)[4]/text()').get(),
                'Close': data.xpath('(.//span)[5]/text()').get(),
                'Adjusted Close': data.xpath('(.//span)[6]/text()').get(),
                'Volume': data.xpath('(.//span)[7]/text()').get()
            }
