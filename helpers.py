def hide_word(word_to_hide, found_letters):
    for letter in word_to_hide:
        if letter not in found_letters:
            word_to_hide = word_to_hide.replace(letter, "_")
    return word_to_hide

