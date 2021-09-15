const p2p_lending = artifacts.require('p2p_lending');

require('chai')
  .use(require('chai-as-promised'))
  .should();
contract('p2p_lending', ([borrower, lender, wallet]) => {
  before(async function() {
    this.contract = await p2p_lending.deployed();
  });
  describe('deployment', async function() {
    it('deploys successfully', async function() {
      const address = await this.contract.address;
      console.log(this.contract.address);
      assert.notEqual(address, 0x0);
      assert.notEqual(address, '');
      assert.notEqual(address, null);
      assert.notEqual(address, undefined);
    });
  });
  describe('listings', async function() {
    it('creates Listing', async function() {
      const result = await this.contract.create_listing(
        'MS in USA',
        5,
        '123',
        1,
        { from: borrower }
      );
    });
    it('fetches listings', async function() {
      const result = await this.contract.fetch_listing(1);
      assert.strictEqual(result['2']['words'][0], 5);
      assert.strictEqual(result['1'], 'MS in USA');
    });
  });
  describe('Lending Feature', async function() {
    it('Lends Money', async function() {
      const result = await this.contract.process_transaction(
        1,
        '123',
        '234',
        1,
        6,
        { from: lender, value: web3.utils.toWei('5', 'ether') }
      );
      console.log(result);
      const transaction = await this.contract.view_transactions(1);
      console.log('This is the last result', transaction);
    });
  });
});
