def remove_duplicates(list_: list) -> list:
    index = 0
    already_defined = []
    while index < len(list_):
        if already_defined:
            if list_[index] in already_defined:
                del list_[index]
                continue
        already_defined.append(list_[index])
        index += 1
    return list_
