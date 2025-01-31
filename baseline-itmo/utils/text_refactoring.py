import re
from typing import List, Optional


def extract_multiple_choice_answers(query: str) -> List[str]:
    """
    Extracts response options from a user query.
    It is assumed that the options are in the format:
        1. ...
        2. ...
        3. ...
        etc.
    Returns a list of variant strings.
    """
    lines = query.splitlines()

    # find lines starting with "<int>. "
    # TODO: fix pattern; in general it's morm but for some cases it doesn't work really good
    pattern = r"^(\d+)\.\s(.*)"
    choices = []
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            choices.append(line.strip())
    return choices


def detect_correct_choice_from_llm(llm_response: str, num_choices: int) -> Optional[int]:
    """
    An example of the simplest heuristic: it tries to find a mention of "Answer: N" in the text of the model
    and returns the number N if it is in the range from 1 to num_choices.
    Tbh, the logic can be complicated (but this is enough for now).
    """
    pattern = r"Ответ:\s?(\d+)"
    match = re.search(pattern, llm_response)
    if match:
        choice = int(match.group(1))
        if 1 <= choice <= num_choices:
            return choice

    # if not found explicitly
    return None
