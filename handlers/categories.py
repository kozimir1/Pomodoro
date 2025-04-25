from fastapi import APIRouter, status
from fixtures import categories as fixtures_categories
from schema.categories import Category

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/all",
            response_model=list[Category]
            )
async def get_categories():
    return fixtures_categories


@router.post("/",
             response_model=Category)
async def create_category(category: Category):
    fixtures_categories.append(category)
    return category


@router.patch("/{category_id}",

              response_model=Category)
async def update_category(category_id: int, name: str):
    for category in fixtures_categories:
        if category['id'] == category_id:
            category['name'] = name
            return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int):
    for idx, category in enumerate(fixtures_categories):
        if category['id'] == category_id:
            del fixtures_categories[idx]
            return {'status': 'success'}
        return {'status': 'fail'}
