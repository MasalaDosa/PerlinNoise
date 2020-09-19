from collections import OrderedDict


class PagedDataCache:
    MAX_NUM_PAGES = 9

    def __init__(self, get_function, page_x_size, page_y_size):
        self.get_function = get_function
        self.page_x_size = page_x_size
        self.page_y_size = page_y_size
        self.cache = OrderedDict()

    def get(self, x, y):
        px = int(x / self.page_x_size)
        py = int(y / self.page_y_size)
        ix = x % self.page_x_size
        iy = y % self.page_y_size
        return self._get_page_via_cache(px, py)[ix][iy]

    def _get_page_via_cache(self, px, py):
        key = (px, py)
        if key not in self.cache:
            self.cache[key] = self._get_page(px, py)
            if len(self.cache.keys()) > PagedDataCache.MAX_NUM_PAGES:
                self.cache.popitem(False)
        return self.cache[key]

    def _get_page(self, px, py):
        page_data = []
        sx = px * self.page_x_size
        sy = py * self.page_y_size
        for x in range(sx, sx + self.page_x_size):
            col = []
            page_data.append(col)
            for y in range(sy, sy + self.page_y_size):
                col.append(self.get_function(x, y))
        return page_data








