from pydantic import ValidationError
from app.api.rest.pins.schemas import PinOut
import pytest
from app.postgresql.models import TagsOrm, PinsOrm, UsersOrm
from sqlalchemy import select


async def test_get_pins(authenticated_ac):
    response = await authenticated_ac.get("/pins/", params={"offset": 0, "limit": 10})
    
    assert response.status_code == 200
    
    response_data = response.json()

    assert isinstance(response_data, list)
    for pin in response_data:
        try:
            PinOut(**pin)  
        except ValidationError as e:
            pytest.fail(f"Response does not match PinOut schema: {e}")
    
    assert response_data == sorted(response_data, key=lambda x: x["id"], reverse=True)


@pytest.mark.parametrize(
    "title, description",
    [
        ("Test Pin 1", "This is a test pin 1"),
        ("Test Pin 2", "This is a test pin 2"),
        ("Test Pin 3", "This is a test pin 3"),
        ("Test Pin 4", "This is a test pin 4"),
        ("Test Pin 5", "This is a test pin 5"),
    ],
)
async def test_create_pin(title: str, description: str, authenticated_ac, db):
    response = await authenticated_ac.post(
        "/pins/",
        json={"title": title, "description": description}
    )

    assert response.status_code == 201

    response_data = response.json()

    assert "id" in response_data
    assert response_data["title"] == title
    assert response_data["description"] == description

    result = await db.execute(select(PinsOrm).filter_by(id=response_data["id"]))
    pin_in_db = result.scalar_one_or_none()

    assert pin_in_db is not None
    assert pin_in_db.title == title
    assert pin_in_db.description == description



async def test_user_delete_created_pin(authenticated_ac, db):
    response_post = await authenticated_ac.post(
        "/pins/",
        json={"title": "test title", "description": "test description"}
    )

    pin_data = response_post.json()
    
    response_delete = await authenticated_ac.delete(f"/pins/{pin_data['id']}")
    
    assert response_delete.status_code == 204

    result = await db.execute(select(PinsOrm).where(PinsOrm.id == pin_data['id']))
    deleted_pin = result.scalars().first()
    assert deleted_pin is None


async def test_user_delete_non_existent_pin(authenticated_ac):
    response = await authenticated_ac.delete("/pins/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "pin not found"}