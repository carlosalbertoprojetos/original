import environ

class OlhoVivo:
    """
    """
    _search_url="https://api.mercadolibre.com/sites/"\
              "{country_id}/search?q={keyword}"\
              "&category={category_id}&offset={offset}&limit={page_size}"
    _str_date="%d-%m-%YT%H:%M"

    def __init__(self, keyword, country_id, category_id, **kwargs):
        """
        ML page size default is 50
        """
        client_id = os.environ.get('CLIENT_ID_MERCADOLIVRE')
        client_secret = os.environ.get('CLIENT_SECRET_MERCADOLIVRE')

        self.page_count=0
        self.item_count=0
        self.keyword=keyword
        self.country_id=country_id
        self.category_id=category_id
        self.user_profile=kwargs.get("user_profile", True)
        self.description=kwargs.get("description", True)
        self.categories=kwargs.get("categories", True)
        self.questions=kwargs.get("questions", True)
        self.no_token=kwargs.get("no_token", True)
        self.offset=kwargs.get("offset",0)
        self.limit=kwargs.get("limit", 0)
        self.page_size=kwargs.get("page_size", 50)
        self.tags=kwargs.get("tags",{})
        self.session=requests.Session()
        self.session.headers={
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "User-Agent":"pyMerli"
        }
        self.metadata={
            "request":{
                "country_id":self.country_id,
                "category_id":self.category_id,
                "keyword":self.keyword
            }
        }

    def __del__(self):
        """
        """
        self.session.close()
