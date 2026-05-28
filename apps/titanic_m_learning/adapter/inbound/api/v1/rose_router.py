from fastapi import APIRouter

from titanic.app.use_cases.titanic_query_impl import TitanicQueryImpl

router = APIRouter(prefix="/titanic", tags=["titanic"])


@router.get("/info")
def read_titanic_info():
    use_case = TitanicQueryImpl()
    return use_case.get_dataset_info()


@router.get("/tree")
def read_titanic_tree():
    use_case = TitanicQueryImpl()
    return {"tree": use_case.has_decision_tree_model()}


@router.get("/model")
def read_titanic_model():
    use_case = TitanicQueryImpl()
    return {"model": use_case.get_current_model_name()}
