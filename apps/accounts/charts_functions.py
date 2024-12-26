import calendar

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, F
from django.db.models.functions import Coalesce, ExtractMonth, TruncMonth
from django.utils import timezone

from .models import Profile

# from datetime import datetime


User = get_user_model()

###############################################################################


def get_total_users():
    return User.objects.filter(is_active=True).count()


###############################################################################


def get_total_admins():
    return User.objects.filter(is_active=True).filter(is_superuser=True).count()


###############################################################################


def get_total_managers():
    return User.objects.filter(is_active=True).filter(profile__is_admin=True).count()


###############################################################################


def get_older_user():
    return User.objects.order_by("date_joined").filter(is_active=True).first()


###############################################################################


def get_newer_user():
    return User.objects.order_by("-date_joined").filter(is_active=True).first()


###############################################################################


# def get_user_distribuition_gender_pie():
#     all_genders = dict(constants.GENDER)
#     gender_distribution = (Profile.objects.values(
#         'gender').annotate(count=Coalesce(Count('gender'), 0)))

#     gender_count_dict = {gender[0]: 0 for gender in constants.GENDER}
#     gender_count_dict.update(
#         {entry['gender']: entry['count'] for entry in gender_distribution})

#     labels = list(gender_count_dict.keys())
#     data = list(gender_count_dict.values())

#     return {"labels": labels, "data": data}

###############################################################################


def get_user_distribution_area_pie():
    # Calcula a contagem de usuários por área, substituindo NULL por 0
    user_distribution = (
        User.objects
        # Assume que a relação com Profile foi definida como related_name="profile"
        .values("profile__area__name").annotate(count=Coalesce(Count("profile__area"), 0))
    )

    labels = [entry["profile__area__name"] for entry in user_distribution]
    data = [entry["count"] for entry in user_distribution]
    return {"labels": labels, "data": data}


###############################################################################


def get_user_increase_time_line():
    # Calcula a contagem de funcionários por mês
    profile_evolution = (
        Profile.objects.annotate(month=TruncMonth("hiring_date")).values("month").annotate(count=Count("id"))
    )

    if profile_evolution:
        # Prepara os dados para serem passados para o template
        # labels = [entry['month'].strftime('%B %Y') for entry in profile_evolution]
        # data = [entry['count'] for entry in profile_evolution]
        # else:
        labels = data = []

    return {"labels": labels, "data": data}


###############################################################################


def get_user_by_manager_bar():
    # Calcula a contagem de funcionários por gerente
    profiles_per_manager = (
        Profile.objects.filter(is_admin=True)  # Apenas gerentes
        .values("created_by__id")  # Use 'id' para agrupar os gerentes
        .annotate(manager_name=Count("created_by__id", distinct=True), count=Count("id"))
    )

    managers = [entry["created_by__id"] for entry in profiles_per_manager]
    users = User.objects.filter(is_active=True)
    i = 0
    labels = []
    for user in users:
        if user.id == int(managers[i]):
            labels.append(user.get_full_name())

    data = [entry["count"] for entry in profiles_per_manager]
    return {"labels": labels, "data": data}


###############################################################################


def get_user_birthday_by_month_bar():
    # Calcula a contagem de funcionários por mês de aniversário
    birthday_distribution = (
        Profile.objects
        # Exclui funcionários sem data de nascimento
        .exclude(birthday__isnull=True)
        .values("birthday")
        .annotate(month=ExtractMonth("birthday"))
        .annotate(count=Count("id"))
    )
    # Prepara os dados para serem passados para o template
    labels = [calendar.month_name[entry["month"]] for entry in birthday_distribution]
    data = [entry["count"] for entry in birthday_distribution]
    return {"labels": labels, "data": data}


def get_average_tenure():
    # Calcula a diferença entre a data atual e a data de início para cada funcionário
    current_date = timezone.now()
    tenure_data = (
        Profile.objects
        # Exclui funcionários sem data de início
        .filter(hiring_date__isnull=False).annotate(tenure=current_date - F("hiring_date"))
    )

    # Calcula a média das diferenças
    average_tenure = tenure_data.aggregate(Avg("tenure"))["tenure__avg"]

    return average_tenure
