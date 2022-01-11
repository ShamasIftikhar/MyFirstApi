import pytest


def test_voting(authorized_client, test_posts):
    res = authorized_client.post(
        f'/votes/', json={'post_id': 1})
    assert res.status_code == 201
    res = authorized_client.post(
        f'/votes/', json={'post_id': 1})
    assert res.status_code == 200


def test_voting_notfound(authorized_client, test_posts):
    res = authorized_client.post('/voting/',json={'post_id':4})

    assert res.status_code == 404

