from user.models import Badge


def check_for_badges(user):
    badges = {5: ("Initié", "Vous avez gagné 5 parties"),
              10: ("Joueur", "Vous avez gagné 10 parties"),
              20: ("Confirmé", "Vous avez gagné 20 parties"),
              40: ("Expert", "Vous avez gagné 40 parties"),
              50: ("Légendaire", "Vous avez gagné 60 parties")}
    for badge_key, badge_value in badges.items():
        if user.won_games == badge_key:
            try:
                Badge.objects.get(title=badge_value[0],
                                  description=badge_value[1],
                                  owner=user)
            except Badge.DoesNotExist:
                won_badge = Badge(title=badge_value[0],
                                  description=badge_value[1],
                                  owner=user)
                won_badge.save()
                return won_badge


def check_for_special_badges(user):
    special_badges = []
    if user.played_games == 50:
        try:
            Badge.objects.get(title="Tryharder",
                              description="Vous avez joué plus de 50 parties",
                              owner=user)
        except Badge.DoesNotExist:
            won_badge = Badge(title="Tryharder",
                              description="Vous avez joué plus de 50 parties",
                              owner=user)
            won_badge.save()
            special_badges.append(won_badge)

    if user.win_rate >= 70 and user.played_games >= 10:
        try:
            Badge.objects.get(title="Voltaire",
                              description="Vous avez obtenu un taux de victoires supérieur "
                                          "ou égal à 70% après 10 parties",
                              owner=user)
        except Badge.DoesNotExist:
            won_badge = Badge(title="Voltaire",
                              description="Vous avez obtenu un taux de victoires supérieur "
                                          "ou égal à 70% après 10 parties",
                              owner=user)
            won_badge.save()
            special_badges.append(won_badge)

    if user.streak >= 10:
        try:
            Badge.objects.get(title="Imbattable",
                              description="Vous avez réussi une série de 10 victoires!",
                              owner=user)
        except Badge.DoesNotExist:
            won_badge = Badge(title="Imbattable",
                              description="Vous avez réussi une série de 10 victoires!",
                              owner=user)
            won_badge.save()
            special_badges.append(won_badge)

    return special_badges
