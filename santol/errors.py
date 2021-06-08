class DatabaseError(Exception):

    def __init__(self, info, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.info = info


class DuplicateEntryError(Exception):

    def __init__(self, info, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.info = info


class DoesNotExistError(Exception):

    def __init__(self, info, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.info = info


class ForbiddenError(Exception):

    def __init__(self, info, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.info = info
