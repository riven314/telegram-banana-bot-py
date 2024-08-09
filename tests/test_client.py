import pytest
import requests_mock

from banana_bot_client.client import BananaBotClient
from banana_bot_client.constants import (
    BANANA_LIST_API,
    CLAIM_QUEST_API,
    DO_CLICK_API,
    DO_LOTTERY_API,
    LOTTERY_INFO_API,
    QUEST_LIST_API,
    USER_INFO_API,
)
from banana_bot_client.models import (
    BananaListModel,
    ClaimQuestModel,
    ClickRewardModel,
    DoLotteryModel,
    LotteryInfoModel,
    QuestListModel,
    UserInfoModel,
)

from .data import (
    sample_claim_quest_response,
    sample_click_response,
    sample_do_lottery_response,
    sample_get_banana_list_response,
    sample_get_lottery_info_response,
    sample_get_quest_list_response,
    sample_get_user_info_response,
)


# Use requests_mock to mock HTTP requests
@pytest.fixture
def client():
    return BananaBotClient(token="test-token")


def test_get_lottery_info(client, requests_mock):
    requests_mock.get(
        LOTTERY_INFO_API,
        json={"code": 0, "msg": "Success", "data": sample_get_lottery_info_response},
    )
    response = client.get_lottery_info()
    assert isinstance(response, LotteryInfoModel)
    assert response.remain_lottery_count == 1


def test_do_lottery(client, requests_mock):
    requests_mock.post(
        DO_LOTTERY_API,
        json={"code": 0, "msg": "Success", "data": sample_do_lottery_response},
    )
    response = client.do_lottery()
    assert isinstance(response, DoLotteryModel)
    assert response.banana_id == 26
    assert response.name == "Nonana"


def test_get_quest_list(client, requests_mock):
    requests_mock.get(
        QUEST_LIST_API,
        json={"code": 0, "msg": "Success", "data": sample_get_quest_list_response},
    )
    response = client.get_quest_list()
    assert isinstance(response, QuestListModel)
    assert len(response.quest_list) == 1
    assert response.quest_list[0].quest_id == 30


def test_claim_quest(client, requests_mock):
    requests_mock.post(
        CLAIM_QUEST_API,
        json={"code": 0, "msg": "Success", "data": sample_claim_quest_response},
    )
    response = client.claim_quest(quest_id=30)
    assert isinstance(response, ClaimQuestModel)
    assert response.peel == 100
    assert response.banana_reward.banana_id == 83


def test_click(client, requests_mock):
    requests_mock.post(
        DO_CLICK_API, json={"code": 0, "msg": "Success", "data": sample_click_response}
    )
    response = client.click(click_count=1)
    assert isinstance(response, ClickRewardModel)
    assert response.peel == 1


def test_get_user_info(client, requests_mock):
    requests_mock.get(
        USER_INFO_API,
        json={"code": 0, "msg": "Success", "data": sample_get_user_info_response},
    )
    response = client.get_user_info()
    assert isinstance(response, UserInfoModel)
    assert response.user_id == 2104747954
    assert response.username == "whatdoesmycatsay"
    assert response.equip_banana.banana_id == 35


def test_get_banana_list(client, requests_mock):
    requests_mock.get(
        BANANA_LIST_API,
        json={"code": 0, "msg": "Success", "data": sample_get_banana_list_response},
    )

    response = client.get_banana_list()

    assert isinstance(response, BananaListModel)
    assert len(response.banana_list) == 2
    assert response.banana_list[0].banana_id == 83
    assert response.banana_list[1].name == "XRaynana"
