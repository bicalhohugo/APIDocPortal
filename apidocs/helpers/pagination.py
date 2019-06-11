from math import ceil

from apidocs.helpers.utils import get_configurations


class Pagination(object):

    def __init__(self, total_count, actual_page):
        config = get_configurations()
        self.per_page = config["pagination"]["max_per_page"]
        self.total_count = total_count
        self.page = actual_page

    @property
    def actual_page(self):
        return self.page

    @property
    def pages(self):
        if not self.total_count or self.total_count == 0:
            return 1
        else:
            return int(ceil(self.total_count / float(self.per_page)))

    @property
    def pages_array(self):
        array = []

        for p in range(self.pages):
            array.append(p + 1)

        return array

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num