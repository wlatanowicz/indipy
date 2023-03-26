import string
from itertools import chain, combinations
from random import choice, randint, random

import pytest

from indi import message
from indi.message import const, one_parts
from indi.transport import Buffer

NUM_RANDOM_TEST_CASES = 50
NUM_MESSAGES_IN_RANDOM_TEST_CASE = 100


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


noise_messages = [
    "<hbshjshjbsbjh />",
    "<asdF><aaaa/></asdF>",
    '<getProperties version="1.0">',
    "<asdf>",
]

raw_messages = [
    '<getProperties version="1.0" />',
    '<getProperties version="1.0" device="Camera" />',
    '<getProperties version="1.0" device="Camera" name="EXPOSURE" />',
    '<setTextVector device="CAMERA" name="EXPOSE" state="Alert"><oneText name="EXPOSE_TIME">2.0</oneText></setTextVector>',
]

indi_messages = [
    message.GetProperties(version="1.0"),
    message.GetProperties(version="1.0", device="Camera"),
    message.GetProperties(version="1.0", device="Camera", name="EXPOSURE"),
    message.SetTextVector(
        device="CAMERA",
        name="EXPOSE",
        state=const.State.ALERT,
        children=[one_parts.OneText(name="EXPOSE_TIME", value="2.0")],
    ),
]

manual_test_cases = [
    [
        (
            "junk",
            "junk2",
        ),
        (),
    ],
    [
        (
            "junk",
            raw_messages[0],
        ),
        (indi_messages[0],),
    ],
]


def random_test_case(size, with_noise=False):
    input_strings = []
    output_messages = []

    choices = list(range(min(len(raw_messages), len(indi_messages))))

    for _ in range(size):
        if with_noise and random() > 0.5:
            for _ in range(randint(1, 5)):
                input_strings.append(choice(noise_messages))

        idx = choice(choices)
        input_strings.append(raw_messages[idx])
        output_messages.append(indi_messages[idx])

        if with_noise and random() > 0.5:
            for _ in range(randint(1, 5)):
                input_strings.append(choice(noise_messages))

    return (
        tuple(input_strings),
        tuple(output_messages),
    )


def random_string(length):
    chars = string.ascii_letters + string.digits
    return "".join(choice(chars) for i in range(length))


def random_test_cases(count, size, with_noise=False):
    for _ in range(count):
        input_strings, output_messages = random_test_case(size, with_noise=with_noise)
        if with_noise:
            noise_to_append = random_string(1024)
            input_strings = input_strings + (noise_to_append,)
        yield input_strings, output_messages


@pytest.mark.parametrize(
    "input_strings,expected_output_messages",
    manual_test_cases
    + list(random_test_cases(NUM_RANDOM_TEST_CASES, NUM_MESSAGES_IN_RANDOM_TEST_CASE))
    + list(
        random_test_cases(
            NUM_RANDOM_TEST_CASES, NUM_MESSAGES_IN_RANDOM_TEST_CASE, with_noise=True
        )
    ),
)
def test_buffer_individual_messages(input_strings, expected_output_messages):
    output_messages = []

    buffer = Buffer()

    def callback(msg):
        output_messages.append(msg)

    for b in input_strings:
        buffer.append(b)
        buffer.process(callback)

    assert len(expected_output_messages) == len(output_messages)
    assert tuple(expected_output_messages) == tuple(output_messages)


@pytest.mark.parametrize(
    "input_strings,expected_output_messages",
    manual_test_cases
    + list(random_test_cases(NUM_RANDOM_TEST_CASES, NUM_MESSAGES_IN_RANDOM_TEST_CASE))
    + list(
        random_test_cases(
            NUM_RANDOM_TEST_CASES, NUM_MESSAGES_IN_RANDOM_TEST_CASE, with_noise=True
        )
    ),
)
def test_buffer_all_at_once(input_strings, expected_output_messages):
    output_messages = []

    buffer = Buffer()

    def callback(msg):
        output_messages.append(msg)

    complete_input = "".join(input_strings)
    buffer.append(complete_input)

    buffer.process(callback)

    assert len(expected_output_messages) == len(output_messages)
    assert tuple(expected_output_messages) == tuple(output_messages)


# @pytest.mark.skip()
@pytest.mark.parametrize(
    "input_strings,expected_output_messages",
    manual_test_cases
    + list(random_test_cases(NUM_RANDOM_TEST_CASES, NUM_MESSAGES_IN_RANDOM_TEST_CASE))
    + list(
        random_test_cases(
            NUM_RANDOM_TEST_CASES, NUM_MESSAGES_IN_RANDOM_TEST_CASE, with_noise=True
        )
    ),
)
def test_buffer_random_length_reads(input_strings, expected_output_messages):
    output_messages = []

    buffer = Buffer()

    def callback(msg):
        output_messages.append(msg)

    complete_input = "".join(input_strings)

    while complete_input:
        num_chars_to_append = randint(1, 1024)
        chars_to_append = complete_input[:num_chars_to_append]
        complete_input = complete_input[num_chars_to_append:]

        buffer.append(chars_to_append)
        buffer.process(callback)

    assert len(expected_output_messages) == len(output_messages)
    assert tuple(expected_output_messages) == tuple(output_messages)
