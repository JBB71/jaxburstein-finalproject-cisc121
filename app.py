import random
import gradio as gr



# This function chooses the pivot index based on the user's chosen method
def choose_pivot(arr, method):
    # If the array is empty, we can't choose a pivot
    if len(arr) == 0:
        raise ValueError("Array is empty, cannot choose pivot.")

    # Normalize the method string to lowercase for comparison
    method = method.lower()

    # Choose pivot based on the method
    if method == "first element":
        idx = 0
    elif method == "middle element":
        idx = len(arr) // 2
    elif method == "random element":
        idx = random.randrange(len(arr))
    else:
        # Fallback: default to the first element
        idx = 0

    # Return the pivot value and its index
    return arr[idx], idx


# This version of quicksort is only used to compute the final sorted answer
def quicksort_for_answer(arr, method):
    # Base case: arrays of size 0 or 1 are already sorted
    if len(arr) <= 1:
        return arr[:]

    # Choose pivot and separate the rest of the elements
    pivot, idx = choose_pivot(arr, method)
    rest = [v for i, v in enumerate(arr) if i != idx]

    # Partition the rest into left and right based on the pivot
    left = [x for x in rest if x < pivot]
    right = [x for x in rest if x >= pivot]

    # Recursively sort the left and right subarrays
    return quicksort_for_answer(left, method) + [pivot] + quicksort_for_answer(right, method)




# This function creates the starting state of a new game
def create_initial_state(pivot_method):
    # Generate a random unsorted list with 8 unique numbers between 1 and 49
    original = random.sample(range(1, 50), 8)

    # The state dictionary holds everything the game needs
    state = {
        "original": original,                       # The original random array
        "pivot_method": pivot_method,               # Pivot selection strategy
        "sorted_result": quicksort_for_answer(original, pivot_method),  # Fully sorted array (for the end)
        "stack": [original],                        # Stack of sub-arrays still to partition
        "current_segment": None,                    # Current sub-array being partitioned
        "pivot": None,                              # Current pivot value
        "remaining": [],                            # Elements still to classify in this partition
        "left": [],                                 # Left partition (values < pivot)
        "right": [],                                # Right partition (values >= pivot)
        "current_element": None,                    # Current element the user is classifying
        "questions_total": 0,                       # Total number of classification attempts
        "questions_correct": 0,                     # Number of correct classifications
        "game_over": False,                         # Has the quick sort finished?
    }

    # Prepare the first partition before returning the state
    state, _ = prepare_next_partition(state)
    return state


# This function sets up the next partition (next sub-array to work on)
def prepare_next_partition(state):
    # If the game is already over, just return the state
    if state["game_over"]:
        return state, "Game is already over."

    stack = state["stack"]

    # Skip any segments that are size 0 or 1 (already "sorted")
    while stack and len(stack[-1]) <= 1:
        stack.pop()

    # If there are no more segments, we are done
    if not stack:
        state["current_segment"] = None
        state["pivot"] = None
        state["remaining"] = []
        state["left"] = []
        state["right"] = []
        state["current_element"] = None
        state["game_over"] = True
        return state, "All partitions complete! Array fully sorted."

    # Take the next segment from the stack
    segment = stack.pop()

    # Choose a pivot in this segment and get all the other elements
    pivot, pivot_idx = choose_pivot(segment, state["pivot_method"])
    remaining = [v for i, v in enumerate(segment) if i != pivot_idx]

    # Update state to represent this new partition step
    state["current_segment"] = segment
    state["pivot"] = pivot
    state["remaining"] = remaining
    state["left"] = []
    state["right"] = []
    state["current_element"] = remaining[0] if remaining else None

    # Message for the UI
    return state, f"New partition: pivot = {pivot}, to classify: {remaining}"


# This helper builds a string for the score
def format_score(state):
    total = state["questions_total"]
    correct = state["questions_correct"]

    # If the user hasn't made any moves yet
    if total == 0:
        return "Score: 0 / 0"

    # Show number correct out of total attempts
    return f"Score: {correct} / {total}"


# This function converts the raw state into all the UI outputs
def build_outputs(state, msg):
    # If there is no message yet and the game isn't over, show the default
    if not msg and not state["game_over"]:
        msg = "Classify the element into LEFT or RIGHT."

    # Add a message when the game finishes
    if state["game_over"]:
        msg += "\n\nSorting complete."

    # Decide what to show as the "current element" message
    if state["game_over"]:
        current = "Game over."
    elif state["current_element"] is None:
        current = "Preparing next partition..."
    else:
        current = f"Place: {state['current_element']} (pivot = {state['pivot']})"

    # Return all Gradio outputs in the correct order
    return (
        msg,                                              # status text
        current,                                          # current element text
        str(state["left"]),                               # left partition display
        str(state["pivot"]) if state["pivot"] is not None else "",  # pivot display
        str(state["right"]),                              # right partition display
        str(state["original"]),                           # original list display
        str(state["sorted_result"]) if state["game_over"] else "Not finished.",  # sorted list display
        format_score(state),                              # score display
        state,                                            # internal state (gr.State)
    )



# This function starts a new game when the user clicks "Start New Game"
def start_game(pivot_method):
    # Build a brand new state with the chosen pivot method
    state = create_initial_state(pivot_method)

    # Status message showing the random list and pivot method
    msg = (
        "New game started!\n"
        f"Random list: {state['original']}\n"
        f"Pivot method: {pivot_method}"
    )

    # Return all the UI outputs for the first screen
    return build_outputs(state, msg)


# This function handles clicking LEFT or RIGHT for the current element
def handle_choice(choice, state):
    # If somehow state is None, create a default game
    if state is None:
        state = create_initial_state("First Element")

    # If the game is finished, just show that info
    if state["game_over"]:
        return build_outputs(state, "Game already finished.")

    current = state["current_element"]
    pivot = state["pivot"]

    # If there is no current element, move on to the next partition
    if current is None:
        state, msg = prepare_next_partition(state)
        return build_outputs(state, msg)

    # Decide the correct side based on the pivot
    correct_side = "left" if current < pivot else "right"

    # Update total number of questions asked
    state["questions_total"] += 1

    # Check if user was correct or not and update score + feedback
    if choice == correct_side:
        state["questions_correct"] += 1
        feedback = f"Correct! {current} {'<' if current < pivot else '>='} {pivot}"
    else:
        feedback = (
            f"Incorrect. {current} "
            f"{'<' if current < pivot else '>='} {pivot} → goes to {correct_side}"
        )

    # Actually place the element in the correct partition
    if correct_side == "left":
        state["left"].append(current)
    else:
        state["right"].append(current)

    # Remove the element we just classified from the remaining list
    remaining = state["remaining"][1:]
    state["remaining"] = remaining

    # If there are still elements to classify in this partition
    if remaining:
        state["current_element"] = remaining[0]
        msg = feedback
        return build_outputs(state, msg)
    else:
        # Partition is done: push right and left subarrays to the stack (if big enough)
        if len(state["right"]) > 1:
            state["stack"].append(state["right"])
        if len(state["left"]) > 1:
            state["stack"].append(state["left"])

        # No more current element in this partition
        state["current_element"] = None

        # Prepare the next partition or finish the game
        state, msg2 = prepare_next_partition(state)
        return build_outputs(state, feedback + "\n\nPartition complete!\n" + msg2)


# Helper wrapper when user clicks the LEFT button
def send_left(state):
    return handle_choice("left", state)


# Helper wrapper when user clicks the RIGHT button
def send_right(state):
    return handle_choice("right", state)




# This builds the full Gradio interface (layout + components)
with gr.Blocks(title="Quick Sort Partition Game") as demo:
    # Title of the app
    gr.Markdown("# Quick Sort Partition Game")

    # Row for pivot method selection + start button
    with gr.Row():
        pivot_method = gr.Radio(
            ["First Element", "Random Element", "Middle Element"],
            value="First Element",
            label="Pivot Method",
        )
        start_btn = gr.Button("Start New Game")

    # Row showing the original list and the final sorted list
    with gr.Row():
        original_box = gr.Textbox(label="Original List", interactive=False)
        sorted_box = gr.Textbox(label="Final Sorted", interactive=False)

    # Status message + current element
    status = gr.Markdown()
    current_elem = gr.Textbox(label="Current Element", interactive=False)

    # Row with left partition, pivot, and right partition
    with gr.Row():
        left_box = gr.Textbox(label="Left Partition", interactive=False)
        pivot_box = gr.Textbox(label="Pivot", interactive=False)
        right_box = gr.Textbox(label="Right Partition", interactive=False)

    # Score display
    score_box = gr.Textbox(label="Score", interactive=False)

    # Buttons the user clicks to classify elements
    with gr.Row():
        left_btn = gr.Button("LEFT partition")
        right_btn = gr.Button("RIGHT partition")

    # Hidden state object that Gradio passes between callbacks
    state = gr.State()

    ## Connect the "Start New Game" button to start_game()
    start_btn.click(
        start_game,
        inputs=[pivot_method],
        outputs=[
            status,
            current_elem,
            left_box,
            pivot_box,
            right_box,
            original_box,
            sorted_box,
            score_box,
            state,
        ],
    )

    # Connect LEFT button to send_left(), which calls handle_choice("left", state)
    left_btn.click(
        send_left,
        inputs=[state],
        outputs=[
            status,
            current_elem,
            left_box,
            pivot_box,
            right_box,
            original_box,
            sorted_box,
            score_box,
            state,
        ],
    )

    # Connect RIGHT button to send_right(), which calls handle_choice("right", state)
    right_btn.click(
        send_right,
        inputs=[state],
        outputs=[
            status,
            current_elem,
            left_box,
            pivot_box,
            right_box,
            original_box,
            sorted_box,
            score_box,
            state,
        ],
    )

# This line actually runs the app (locally or on Hugging Face)
demo.launch()
