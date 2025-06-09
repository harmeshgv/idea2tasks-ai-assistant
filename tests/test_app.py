import json

def test_roadmap_json_structure():
    with open("roadmap.json") as f:
        data = json.load(f)

    # Check main key
    assert "modules" in data
    assert isinstance(data["modules"], list)

    for module in data["modules"]:
        assert "module" in module
        assert "submodules" in module
        for sub in module["submodules"]:
            assert "submodule_name" in sub
            assert "tasks" in sub
            assert isinstance(sub["tasks"], list)
            assert "tools" in sub
