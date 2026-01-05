from socialapi.models.comment import Comment, CommentIn

comment_table = {}


def add_comment(comment: CommentIn):
    data = comment.model_dump()
    id = len(comment_table)
    new_comment = {"id": id, **data}
    comment_table[id] = new_comment
    return new_comment


def find_comments_by_post_id(post_id: int):
    comments: list[Comment] = []
    for comment in comment_table.values():
        if comment["post_id"] == post_id:
            comments.append(comment)
    return comments
