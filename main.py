from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing_extensions import Optional
from random import randrange

app = FastAPI()


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_post = [
    {'title': 'title_example', 'content': 'content_example', 'id': 3},
    {'title': 'title_example_2', 'content': 'content_example_2', 'id': 4}
]


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p


@app.get('/')
def root():
    return {'message': 'first api'}


@app.get('/get')
def get_request():
    return {'data': my_post}


@app.get('/get/{id}')
def get_one_post(id: int, response: Response):
    print(id)
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Id not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
    return {'data': post}


@app.post('/post', status_code=status.HTTP_201_CREATED)
def post_request(post_model: PostModel):
    post_dict = post_model.dict()
    post_dict['id'] = randrange(0, 10000)
    my_post.append(post_dict)
    return {'message': post_dict}
