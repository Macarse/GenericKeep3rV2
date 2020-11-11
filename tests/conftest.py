import pytest
from brownie import config, Wei
from brownie import GenericKeep3rV2, ERC20Token, MockStrategy, MockKeep3r


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
def keep3r(deployer, keeper):
    yield deployer.deploy(MockKeep3r, keeper)


@pytest.fixture
def vault(deployer, token, pm):
    Vault = pm(config["dependencies"][-1]).Vault
    vault = deployer.deploy(Vault, token, deployer, deployer, "", "")
    token.approve(vault, Wei("100 ether"), {"from": deployer})
    vault.deposit({"from": deployer})
    yield vault


@pytest.fixture
def token(deployer):
    yield deployer.deploy(ERC20Token, "Token", "TKR", Wei("100 ether"))


@pytest.fixture
def strategy(deployer, vault, genericKeeper):
    strategy = deployer.deploy(MockStrategy, vault)
    strategy.setKeeper(genericKeeper)
    vault.addStrategy(strategy, Wei("100 ether"), 2 ** 256 - 1, 0, {"from": deployer})
    yield strategy


@pytest.fixture
def genericKeeper(deployer, keep3r):
    yield deployer.deploy(GenericKeep3rV2, keep3r)
