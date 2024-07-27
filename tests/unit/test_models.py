def test_new_fan(new_fan):
    """
    GIVEN a Fan model
    WHEN a new Fan is created
    THEN check the name, swtch, and speed fields are defined correctly
    """
    assert new_fan.name == None
    assert new_fan.swtch == False
    assert new_fan.speed == 0
