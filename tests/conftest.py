import pytest
from brownie import config, Wei


@pytest.fixture
def deployer(a):
    yield a[1]


@pytest.fixture
def keeper(a):
    yield a[2]


@pytest.fixture
def rando(a):
    yield a[3]


@pytest.fixture
def oracle(deployer, MockSlidingOracle):
    yield deployer.deploy(MockSlidingOracle)


@pytest.fixture
def mockKeep3rHelper(deployer, MockKeep3rHelper):
    yield deployer.deploy(MockKeep3rHelper)


@pytest.fixture
def keep3r(deployer, MockKeep3r, keeper, mockKeep3rHelper):
    yield deployer.deploy(MockKeep3r, keeper, mockKeep3rHelper)


@pytest.fixture
def vault(deployer, token, pm):
    Vault = pm(config["dependencies"][0]).Vault
    vault = deployer.deploy(Vault, token, deployer, deployer, "", "")
    token.approve(vault, Wei("100 ether"), {"from": deployer})
    vault.deposit({"from": deployer})
    yield vault


@pytest.fixture
def token(deployer, ERC20Token):
    yield deployer.deploy(ERC20Token, "Token", "TKR", Wei("100 ether"))


@pytest.fixture
def strategy(deployer, MockStrategy, vault, genericKeeper):
    strategy = deployer.deploy(MockStrategy, vault)
    strategy.setKeeper(genericKeeper)
    vault.addStrategy(strategy, Wei("100 ether"), 2 ** 256 - 1, 0, {"from": deployer})
    yield strategy


@pytest.fixture
def strategy2(deployer, MockStrategy2, vault, genericKeeper):
    strategy = deployer.deploy(MockStrategy2, vault)
    strategy.setKeeper(genericKeeper)
    vault.addStrategy(strategy, Wei("100 ether"), 2 ** 256 - 1, 0, {"from": deployer})
    yield strategy


@pytest.fixture
def genericKeeper(deployer, GenericKeep3rV2, keep3r, mockKeep3rHelper, oracle):
    yield deployer.deploy(GenericKeep3rV2, keep3r, mockKeep3rHelper, oracle)
