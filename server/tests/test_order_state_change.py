from server.crud.orders import state_change


def test_SUBMITTED():
    assert state_change('SUBMITTED', 'CANCEL') == 'CANCELLED'
    assert state_change('SUBMITTED', 'REJECT') == 'REJECTED'
    assert state_change('SUBMITTED', 'APPROVE') == 'APPROVED'
    assert state_change('SUBMITTED', 'PREPARE') == 'SUBMITTED'
    assert state_change('SUBMITTED', 'SERVE') == 'SUBMITTED'
    assert state_change('SUBMITTED', 'DELIVER') == 'SUBMITTED'


def test_REJECTED():
    assert state_change('REJECTED', 'CANCEL') == 'REJECTED'
    assert state_change('REJECTED', 'REJECT') == 'REJECTED'
    assert state_change('REJECTED', 'APPROVE') == 'REJECTED'
    assert state_change('REJECTED', 'PREPARE') == 'REJECTED'
    assert state_change('REJECTED', 'SERVE') == 'REJECTED'
    assert state_change('REJECTED', 'DELIVER') == 'REJECTED'


def test_APPROVED():
    assert state_change('APPROVED', 'CANCEL') == 'CANCELLED'
    assert state_change('APPROVED', 'REJECT') == 'APPROVED'
    assert state_change('APPROVED', 'APPROVE') == 'APPROVED'
    assert state_change('APPROVED', 'PREPARE') == 'IN PREPARATION'
    assert state_change('APPROVED', 'SERVE') == 'APPROVED'
    assert state_change('APPROVED', 'DELIVER') == 'APPROVED'


def test_CANCELLED():
    assert state_change('CANCELLED', 'CANCEL') == 'CANCELLED'
    assert state_change('CANCELLED', 'REJECT') == 'CANCELLED'
    assert state_change('CANCELLED', 'APPROVE') == 'CANCELLED'
    assert state_change('CANCELLED', 'PREPARE') == 'CANCELLED'
    assert state_change('CANCELLED', 'SERVE') == 'CANCELLED'
    assert state_change('CANCELLED', 'DELIVER') == 'CANCELLED'


def test_IN_PREPARATION():
    assert state_change('IN PREPARATION', 'CANCEL') == 'IN PREPARATION'
    assert state_change('IN PREPARATION', 'REJECT') == 'IN PREPARATION'
    assert state_change('IN PREPARATION', 'APPROVE') == 'IN PREPARATION'
    assert state_change('IN PREPARATION', 'PREPARE') == 'IN PREPARATION'
    assert state_change('IN PREPARATION', 'SERVE') == 'IN DELIVERY'
    assert state_change('IN PREPARATION', 'DELIVER') == 'IN PREPARATION'


def test_IN_DELIVERY():
    assert state_change('IN DELIVERY', 'CANCEL') == 'IN DELIVERY'
    assert state_change('IN DELIVERY', 'REJECT') == 'IN DELIVERY'
    assert state_change('IN DELIVERY', 'APPROVE') == 'IN DELIVERY'
    assert state_change('IN DELIVERY', 'PREPARE') == 'IN DELIVERY'
    assert state_change('IN DELIVERY', 'SERVE') == 'IN DELIVERY'
    assert state_change('IN DELIVERY', 'DELIVER') == 'DELIVERED'


def test_DELIVERED():
    assert state_change('DELIVERED', 'CANCEL') == 'DELIVERED'
    assert state_change('DELIVERED', 'REJECT') == 'DELIVERED'
    assert state_change('DELIVERED', 'APPROVE') == 'DELIVERED'
    assert state_change('DELIVERED', 'PREPARE') == 'DELIVERED'
    assert state_change('DELIVERED', 'SERVE') == 'DELIVERED'
    assert state_change('DELIVERED', 'DELIVER') == 'DELIVERED'
