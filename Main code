import random
from typing import List, Tuple, Dict, Any, Optional

import gradio as gr


def parse_numbers(numbers_str: str) -> List[int]:
    """
    Parse a string of numbers separated by spaces and/or commas into a list of ints.
    Example: "3 9 2, 8,5 1" -> [3, 9, 2, 8, 5, 1]
    """
    if not numbers_str.strip():
        raise ValueError("Please enter at least one number.")
    cleaned = numbers_str.replace(",", " ")
    tokens = [t for t in cleaned.split() if t.strip() != ""]
    try:
        return [int(t) for t in tokens]
    except ValueError:
        raise ValueError("All entries must be integers (use spaces and/or commas).")


def format_list(lst: List[int]) -> str:
    """Format a list as a human-readable string version, e.g. [1, 2, 3]."""
    return "[" + ", ".join(str(x) for x in lst) + "]" if lst else "[]"


def choose_pivot_index(lo: int, hi: int, method: str) -> int:
    """Choose pivot index based on selected method."""
    if method == "First element":
        return lo
    elif method == "Middle element":
        return (lo + hi) // 2
    elif method == "Random element":
        return random.randint(lo, hi)
    else:
        # Fallback
        return lo


def start_new_partition(
    array: List[int],
    stack: List[Tuple[int, int]],
    pivot_method: str,
) -> Tuple[Optional[Dict[str, Any]], str, str, str, str, str, str, bool]:
    """
    Pop segments from the stack until we find one that needs partitioning (size >= 2).
    Set up a new partition step for the user to interact with.

    Returns:
      current_partition (dict or None),
      left_text,
      pivot_text,
      right_text,
      question_text,
      feedback_text,
      final_array_text,
      game_over_flag
    """
    # Find the next non-trivial segment
    while stack:
        lo, hi = stack.pop()
        if lo < hi:
            # We have a real segment to partition
            pivot_idx = choose_pivot_index(lo, hi, pivot_method)
            pivot_val = array[pivot_idx]
            elements_to_classify = [i for i in range(lo, hi + 1) if i != pivot_idx]

            current_partition = {
                "lo": lo,
                "hi": hi,
                "pivot_index": pivot_idx,
                "pivot_value": pivot_val,
                "elements_to_classify": elements_to_classify,
                "current_pos": 0,
                "left": [],
                "right": [],
            }

            # First question
            first_elem_idx = elements_to_classify[0]
            first_val = array[first_elem_idx]
            question = f"Pivot = {pivot_val}. Where does {first_val} belong?"
            feedback = "Classify each element as LEFT (< pivot) or RIGHT (≥ pivot)."

            left_text = format_list(current_partition["left"])
            right_text = format_list(current_partition["right"])
            pivot_text = str(pivot_val)

            return (
                current_partition,
                left_text,
                pivot_text,
                right_text,
                question,
                feedback,
                "",
                False,
            )

    # If we get here, there are no more segments to sort → game over
    final_array_text = format_list(array)
    feedback = "All done! The array is fully sorted."
    question = "Game over. Press 'Start Game / Reset' to play again."

    return None, "", "", "", question, feedback, final_array_text, True


def start_game(
    numbers_str: str,
    pivot_method: str,
):
    """
    Initialize the game:
      - parse input numbers
      - set up the stack of segments for Quick Sort
      - start the first partition step
    """
    # Default outputs
    default_array: List[int] = []
    default_stack: List[Tuple[int, int]] = []
    default_partition = None
    score = 0
    total = 0

    # UI defaults
    left_text = ""
    pivot_text = ""
    right_text = ""
    question = "Enter numbers and click 'Start Game / Reset' to begin."
    feedback = ""
    score_text = "Score: 0/0"
    final_array_text = ""

    try:
        array = parse_numbers(numbers_str)
    except ValueError as e:
        feedback = f"Input error: {e}"
        # Return defaults with feedback
        return (
            default_array,
            default_stack,
            pivot_method,
            score,
            total,
            default_partition,
            left_text,
            pivot_text,
            right_text,
            question,
            feedback,
            score_text,
            final_array_text,
        )

    if len(array) <= 1:
        feedback = "Array has 0 or 1 element, so it is already sorted."
        final_array_text = format_list(array)
        question = "Nothing to do. Try entering more numbers."
        return (
            array,
            [],
            pivot_method,
            score,
            total,
            None,
            left_text,
            pivot_text,
            right_text,
            question,
            feedback,
            score_text,
            final_array_text,
        )

    # Initial stack has one segment containing the whole array
    stack: List[Tuple[int, int]] = [(0, len(array) - 1)]

    current_partition, left_text, pivot_text, right_text, question, feedback, final_array_text, game_over = \
        start_new_partition(array, stack, pivot_method)

    # Score is 0/0 at the start
    score_text = f"Score: {score}/{total}"

    return (
        array,
        stack,
        pivot_method,
        score,
        total,
        current_partition,
        left_text,
        pivot_text,
        right_text,
        question,
        feedback,
        score_text,
        final_array_text,
    )


def handle_choice(
    choice: str,
    array: List[int],
    stack: List[Tuple[int, int]],
    pivot_method: str,
    score: int,
    total: int,
    current_partition: Optional[Dict[str, Any]],
):
    """
    Handle a user click: choice is "left" or "right".

    Returns same outputs as start_game:
      array, stack, pivot_method, score, total, current_partition,
      left_text, pivot_text, right_text,
      question, feedback, score_text, final_array_text
    """
    # Defaults for UI
    left_text = ""
    pivot_text = ""
    right_text = ""
    question = ""
    feedback = ""
    final_array_text = ""

    # If the game is over (no partition and no stack), just show message
    if current_partition is None and not stack:
        question = "Game over. Press 'Start Game / Reset' to play again."
        feedback = "No more moves."
        score_text = f"Score: {score}/{total}"
        return (
            array,
            stack,
            pivot_method,
            score,
            total,
            current_partition,
            left_text,
            pivot_text,
            right_text,
            question,
            feedback,
            score_text,
            final_array_text,
        )

    # If there is no active partition but there are segments left, start a new partition
    if current_partition is None:
        current_partition, left_text, pivot_text, right_text, question, feedback, final_array_text, game_over = \
            start_new_partition(array, stack, pivot_method)
        score_text = f"Score: {score}/{total}"
        return (
            array,
            stack,
            pivot_method,
            score,
            total,
            current_partition,
            left_text,
            pivot_text,
            right_text,
            question,
            feedback,
            score_text,
            final_array_text,
        )

    # We are in the middle of a partitioning step
    lo = current_partition["lo"]
    hi = current_partition["hi"]
    pivot_val = current_partition["pivot_value"]
    elements_to_classify = current_partition["elements_to_classify"]
    current_pos = current_partition["current_pos"]
    left_list = current_partition["left"]
    right_list = current_partition["right"]

    # Identify the current element to classify
    idx = elements_to_classify[current_pos]
    val = array[idx]

    # Determine the correct side
    correct_side = "left" if val < pivot_val else "right"

    # Update score
    total += 1
    if choice == correct_side:
        score += 1
        relation = "<" if val < pivot_val else "≥"
        feedback = f"Correct! {val} {relation} pivot ({pivot_val})."
    else:
        relation = "<" if val < pivot_val else "≥"
        feedback = (
            f"Not quite. {val} {relation} pivot ({pivot_val}), "
            f"so it should go to the {correct_side} partition."
        )

    # Place element into the chosen partition (for visualization),
    # but the correctness is judged separately (score).
    if choice == "left":
        left_list.append(val)
    else:
        right_list.append(val)

    current_partition["current_pos"] = current_pos + 1

    # Check if we have finished classifying all elements in this segment
    if current_partition["current_pos"] >= len(elements_to_classify):
        # Partitioning complete for this segment.
        # Build the new segment array: left + pivot + right.
        new_segment = left_list + [pivot_val] + right_list
        # Overwrite this part of the main array
        for offset, v in enumerate(new_segment):
            array[lo + offset] = v

        # Compute new pivot index in the global array
        new_pivot_index = lo + len(left_list)

        # Push right and left segments onto the stack for further sorting
        # (size >= 2 only, but we check that later when starting new partition)
        if new_pivot_index + 1 < hi:
            stack.append((new_pivot_index + 1, hi))
        if lo < new_pivot_index - 1:
            stack.append((lo, new_pivot_index - 1))

        # Clear current partition and move to the next
        current_partition = None

        # Start the next partition or end the game
        current_partition, left_text, pivot_text, right_text, next_question, next_feedback, final_array_text, game_over = \
            start_new_partition(array, stack, pivot_method)

        # If game_over is False, we want to show both current feedback and next_question
        # We can append feedback messages.
        if game_over:
            question = next_question
            feedback = feedback + " " + next_feedback
        else:
            question = next_question
            feedback = feedback + " " + next_feedback

    else:
        # We are still in the same partition; prepare next question.
        next_idx = elements_to_classify[current_partition["current_pos"]]
        next_val = array[next_idx]
        question = f"Pivot = {pivot_val}. Where does {next_val} belong?"

        left_text = format_list(left_list)
        right_text = format_list(right_list)
        pivot_text = str(pivot_val)

    score_text = f"Score: {score}/{total}"

    return (
        array,
        stack,
        pivot_method,
        score,
        total,
        current_partition,
        left_text,
        pivot_text,
        right_text,
        question,
        feedback,
        score_text,
        final_array_text,
    )


def choose_left(
    array, stack, pivot_method, score, total, current_partition
):
    return handle_choice(
        "left",
        array,
        stack,
        pivot_method,
        score,
        total,
        current_partition,
    )


def choose_right(
    array, stack, pivot_method, score, total, current_partition
):
    return handle_choice(
        "right",
        array,
        stack,
        pivot_method,
        score,
        total,
        current_partition,
    )


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Quick Sort Partition Game

        **Goal:** Learn how Quick Sort partitioning works by classifying numbers
        into a left partition (less than pivot) or right partition (greater than or equal to pivot).
        """
    )

    with gr.Row():
        numbers_input = gr.Textbox(
            label="Enter an unsorted list of integers",
            placeholder="Example: 3 9 2 8 5 1",
        )
        pivot_method_input = gr.Radio(
            label="Pivot selection method",
            choices=["First element", "Random element", "Middle element"],
            value="First element",
        )

    start_button = gr.Button("Start Game / Reset")

    gr.Markdown("### Current Partition")

    with gr.Row():
        left_box = gr.Textbox(
            label="Left partition (values < pivot)", interactive=False
        )
        pivot_box = gr.Textbox(label="Pivot", interactive=False)
        right_box = gr.Textbox(
            label="Right partition (values ≥ pivot)", interactive=False
        )

    question_markdown = gr.Markdown("Question will appear here.")
    feedback_markdown = gr.Markdown("")
    score_markdown = gr.Markdown("Score: 0/0")

    final_array_box = gr.Textbox(
        label="Final sorted array (shown when game ends)",
        interactive=False,
    )

    with gr.Row():
        left_button = gr.Button("Send to LEFT partition")
        right_button = gr.Button("Send to RIGHT partition")

    # State variables to preserve game progress between clicks
    array_state = gr.State([])
    stack_state = gr.State([])
    pivot_state = gr.State("First element")
    score_state = gr.State(0)
    total_state = gr.State(0)
    partition_state = gr.State(None)

    # Wire up the start/reset button
    start_button.click(
        fn=start_game,
        inputs=[numbers_input, pivot_method_input],
        outputs=[
            array_state,
            stack_state,
            pivot_state,
            score_state,
            total_state,
            partition_state,
            left_box,
            pivot_box,
            right_box,
            question_markdown,
            feedback_markdown,
            score_markdown,
            final_array_box,
        ],
    )

    # Wire up the left/right partition buttons
    left_button.click(
        fn=choose_left,
        inputs=[
            array_state,
            stack_state,
            pivot_state,
            score_state,
            total_state,
            partition_state,
        ],
        outputs=[
            array_state,
            stack_state,
            pivot_state,
            score_state,
            total_state,
            partition_state,
            left_box,
            pivot_box,
            right_box,
            question_markdown,
            feedback_markdown,
            score_markdown,
            final_array_box,
        ],
    )

    right_button.click(
        fn=choose_right,
        inputs=[
            array_state,
            stack_state,
            pivot_state,
            score_state,
            total_state,
            partition_state,
        ],
        outputs=[
            array_state,
            stack_state,
            pivot_state,
            score_state,
            total_state,
            partition_state,
            left_box,
            pivot_box,
            right_box,
            question_markdown,
            feedback_markdown,
            score_markdown,
            final_array_box,
        ],
    )


if __name__ == "__main__":
    demo.launch()
