from titanic_m_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.molly_dto import MollyNotableSurvivorQuery


def _assistance_note(person: PersonORM) -> str:
    if person.parch != "0" and person.sib_sp != "0":
        return "가족 동반 생존·연대"
    if person.parch != "0":
        return "자녀 동반 생존"
    if person.sib_sp != "0":
        return "형제·배우자 동반 생존"
    return "단독 생존"


def person_booking_to_molly_query(person: PersonORM, booking: BookingORM) -> MollyNotableSurvivorQuery:
    return MollyNotableSurvivorQuery(
        passenger_id=person.passenger_id,
        name=person.name,
        pclass=booking.pclass,
        survived=person.survived,
        gender=person.gender,
        assistance_note=_assistance_note(person),
    )
