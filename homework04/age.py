import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    list_fr = get_friends(user_id, 'bdate')
    ages = []
    for friend in list_fr:
        user = User(**friend)
        try:
            bdate = str(user.bdate)
            if bdate.count('.') == 2:
                day, month, year = map(int, bdate.split('.'))
                today = str(dt.date.today())
                year_now, month_now, day_now = map(int, today.split('-'))
                if month_now > month or (month == month_now and day_now > day):
                    ages.append(year_now - year)
                else:
                    ages.append(year_now - year - 1)
        except:
            pass
    if ages:
        return median(ages)
