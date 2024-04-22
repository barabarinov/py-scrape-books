import scrapy
from scrapy.http import Response


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response: Response, *args, **kwargs) -> None:
        book_urls = response.css(".product_pod h3 a::attr(href)").getall()
        for book_url in book_urls:
            yield response.follow(book_url, callback=self.parse_book)

        next_page = response.css(".next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def parse_book(response: Response) -> dict[str, str]:
        yield {
            "title": response.css("h1::text").get(),
            "price": response.css(".price_color::text").get(),
            "amount_in_stock": response.css(".instock.availability::text").re_first(r"\d+"),
            "rating": response.css(".star-rating::attr(class)").re_first(r"Two|Three|Four|Five|One"),
            "category": response.css(".breadcrumb li:nth-last-child(2) a::text").get(),
            "description": response.css("#product_description + p::text").get(),
            "upc": response.css('.table-striped th:contains("UPC") + td::text').get(),
        }
