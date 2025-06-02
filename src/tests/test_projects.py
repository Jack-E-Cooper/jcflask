import pytest


@pytest.mark.parametrize(
    "project_id,expected_title",
    [
        ("flaskwebapp", "Personal Website"),
        # Add more projects here as needed
    ],
)
def test_project_page_content(client, project_id, expected_title):
    response = client.get(f"/project/{project_id}")
    assert response.status_code == 200
    assert expected_title.encode() in response.data
    assert b"Description" in response.data
    assert b"Technologies Used" in response.data
