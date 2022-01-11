
import pytest
from app import schemas


def test_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    print(res.json())

    def validate(post):
        return schemas.PostOut(**post)

    post_map = map(validate, res.json())
    post_list = list(post_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_get_single_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    res1 = res.json()

    assert res1['Post']['id'] == test_posts[0].id
    assert res.status_code == 200

@pytest.mark.parametrize("title,content,status_code",[
    ('123qwe',"rerwt",201),
    (None,'12312',422),
    ('asfa',None,422),
    (None,None,422)
])
def test_create_post(authorized_client,title,content,status_code):
    res = authorized_client.post('/posts/', json={'title':title,'content':content})

    assert res.status_code == status_code


def test_create_post_unauthorized(client):
    post_data = {
        "title": "123st title",
        "content": "1st con",
    }
    
    res = client.post('/posts/',json=post_data)
    post = res.json()
    assert res.status_code == 401
    assert post['detail'] == 'Not authenticated'


@pytest.mark.parametrize("title,content,status_code", [
    ('123qwe', "rerwt", 200),
    (None, '12312', 422),
    ('asfa', None, 422),
    (None, None, 422)])
def test_update_post(authorized_client,test_posts,title,content,status_code):
    res=authorized_client.put(f'/posts/{test_posts[0].id}',json={'title':title,'content':content})

    assert res.status_code ==status_code


def test_update_post(client, test_posts):
    res = client.put(
        f'/posts/{test_posts[0].id}', json={'title': 'title', 'content': 'content'})

    assert res.status_code == 401


def test_delete_post(authorized_client,test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[1].id}')

    assert res.status_code==204


def test_delete_post_unauthorized(authorized_client1,test_posts):
    res =authorized_client1.delete(f'/posts/{test_posts[1].id}')

    assert res.status_code == 403
