from user.models import Badge


def hide_word(word_to_hide, found_letters):
    for letter in word_to_hide:
        if letter not in found_letters:
            word_to_hide = word_to_hide.replace(letter, "_")
    return word_to_hide


def check_for_badges(user):
    if user.won_games == 5:
        try:
            badge = Badge.objects.get(title="Initié", description="Vous avez gagné 5 parties",
                                      owner=user)
        except Badge.DoesNotExist:
            badge = Badge(title="Initié", description="Vous avez gagné 5 parties", owner=user)
            badge.save()
            return badge
