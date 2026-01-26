from enum import Enum


class PostSorting(str, Enum):
    NEWEST = "newest"
    OLDEST = "oldest"
    MOST_LIKED = "most_liked"
    LEAST_LIKED = "least_liked"
