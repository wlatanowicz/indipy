import datetime
import warnings

from indi.message import now


def test_now_is_naive_utc_without_deprecation():
    before = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", DeprecationWarning)
        stamp = now()
    after = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)

    assert "+" not in stamp
    assert not stamp.endswith("Z")

    parsed = datetime.datetime.fromisoformat(stamp)
    assert parsed.tzinfo is None
    assert before <= parsed <= after
    assert not any(issubclass(item.category, DeprecationWarning) for item in caught)
