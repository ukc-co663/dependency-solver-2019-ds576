def list_flatten(input_list):
    """Flatten an N-dimensional list of lists into a single dimension."""

    # Convert atomic elements to single item lists then using a list
    # comprehension convert to a flattened equivalent.
    formatted_list = []
    for element in input_list:
        element = element if isinstance(element, list) else [element]
        formatted_list.append(element)
    output_list = [item for sublist in formatted_list for item in sublist]

    # If all elements are atomic return, else recursively call until flattened.
    if all(not isinstance(x, list) for x in output_list):
        return output_list
    else:
        return list_flatten(output_list)