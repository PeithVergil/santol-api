class DatabaseError(Exception):

    def __init__(self, info, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.info = info
    
    @property
    def detail(self):
        if self.info['code'] == 1062:
            return 'Duplicate entry'

        return 'Something went wrong with the database.'


class ForbiddenError(Exception):

    def __init__(self, info, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.info = info
