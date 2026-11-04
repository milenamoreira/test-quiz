import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_choice_with_empty_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')

def test_create_choice_with_text_longer_than_100_characters():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a'*101)

def test_choices_receive_sequential_ids():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    assert choice1.id == 1
    assert choice2.id == 2

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')

    question.remove_choice_by_id(choice1.id)

    assert question.choices == [choice2]

def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(99)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert question.choices == []

def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')

    question.set_correct_choices([choice2.id])

    assert not choice1.is_correct
    assert choice2.is_correct

def test_correct_selected_choices_returns_only_correct_ones():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)

    result = question.correct_selected_choices([choice1.id, choice2.id])

    assert result == [choice1.id]

def test_select_more_choices_than_allowed():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', True)
    with pytest.raises(Exception):
        question.correct_selected_choices([choice1.id, choice2.id])


@pytest.fixture
def question_with_choices():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', False)
    question.add_choice('c', True)
    return question

def test_fixture_question_has_three_choices(question_with_choices):
    assert len(question_with_choices.choices) == 3

def test_correct_selected_choices_with_fixture(question_with_choices):
    result = question_with_choices.correct_selected_choices([1, 2])
    assert result == [1]

def test_new_choice_id_continues_after_existing_ones(question_with_choices):
    choice = question_with_choices.add_choice('d')
    assert choice.id == 4

def test_remove_choice_keeps_the_others(question_with_choices):
    question_with_choices.remove_choice_by_id(2)
    assert [choice.id for choice in question_with_choices.choices] == [1, 3]
