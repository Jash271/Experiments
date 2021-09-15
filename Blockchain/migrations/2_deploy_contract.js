const p2p_lending = artifacts.require('./p2p_lending.sol');

module.exports = function(deployer) {
  deployer.deploy(p2p_lending);
};
