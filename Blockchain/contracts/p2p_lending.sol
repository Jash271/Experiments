pragma solidity ^0.5.16;

contract p2p_lending {
    uint256 listing_counter = 0;
    uint256 transaction_counter = 0;
    uint256 payments_counter = 0;
    uint256 collateral_payout_counter = 0;
    uint256 liquidated_payouts = 0;
    address payable bank;

    struct Listings {
        address payable borrower;
        string reason;
        uint256 amount;
        uint256 key;
        string reg_id;
        bool flag;
        uint256 Collateral;
        bool Transaction_processed;
    }
    struct Transaction {
        address payable borrower;
        address payable lender;
        bool Loan_Paid;
        string borrower_reg_id;
        string lender_reg_id;
        uint256 transaction_number;
        uint256 listing_id;
        uint256 collateral_deposit;
        uint256 pay_back_amt;
        uint256 amt_due;
        bool collateral_liquidated;
    }

    struct Payments {
        address sender;
        address receiver;
        uint256 amt;
        uint256 transaction_id;
        bool full_repayment;
        uint256 next_amt_due;
        uint256 payment_id;
    }
    struct collateral_payments {
        address sender;
        uint256 amt;
        uint256 c_p_id;
    }
    struct Liquidated_Payouts {
        address payable receiver;
        uint256 amt;
        bool to_lender;
        bool to_borrower;
        uint256 t_id;
        uint256 payouts_id;
    }
    mapping(uint256 => Listings) public Listed_Requirements;
    mapping(uint256 => Transaction) public Processed_Transactions;
    mapping(uint256 => Payments) public Payouts;
    mapping(uint256 => collateral_payments) public collateral_payouts;
    mapping(uint256 => Liquidated_Payouts) public wallet_payouts;

    function create_listing(
        string memory _reason,
        uint256 _amt,
        string memory _reg_id,
        uint256 _coll
    ) public returns (uint256, uint256) {
        bool flag = false;
        uint256 c_amt;

        for (uint256 i = 0; i <= transaction_counter; i++) {
            Transaction memory t = Processed_Transactions[i + 1];
            if (t.borrower == msg.sender && t.Loan_Paid == false) {
                flag = true;
                break;
            }
        }
        if (flag == false) {
            //create a new new Lisiting
            listing_counter += 1;

            Listed_Requirements[listing_counter] = Listings(
                msg.sender,
                _reason,
                _amt,
                listing_counter,
                _reg_id,
                true,
                _coll,
                false
            );
            return (200, listing_counter);
        }
        return (300, 0);
    }

    function fetch_listing(uint256 count)
        public
        view
        returns (
            address,
            string memory,
            uint256,
            uint256,
            string memory,
            bool,
            uint256
        )
    {
        return (
            Listed_Requirements[count].borrower,
            Listed_Requirements[count].reason,
            Listed_Requirements[count].amount,
            Listed_Requirements[count].key,
            Listed_Requirements[count].reg_id,
            Listed_Requirements[count].flag,
            Listed_Requirements[count].Collateral
        );
    }

    function transfer_coll(
        uint256 l_id,
        address payable a,
        uint256 _amt
    ) public payable returns (uint256) {
        a.transfer(msg.value);
        Listed_Requirements[l_id].Transaction_processed = true;
        collateral_payout_counter += 1;
        collateral_payouts[collateral_payout_counter] = collateral_payments(
            msg.sender,
            _amt,
            collateral_payout_counter
        );

        return 1;
    }

    function process_transaction(
        uint256 l_id,
        string memory borrower_reg_id,
        string memory lender_reg_id,
        uint256 c_d,
        uint256 pay_back_amt
    ) public payable returns (uint256, uint256) {
        address payable borrower = Listed_Requirements[l_id].borrower;

        // Increment Counter
        transaction_counter += 1;

        Processed_Transactions[transaction_counter] = Transaction(
            borrower,
            msg.sender,
            false,
            borrower_reg_id,
            lender_reg_id,
            transaction_counter,
            l_id,
            c_d,
            pay_back_amt,
            pay_back_amt,
            false
        );
        // Tranfer Funds from Lender to borrower

        borrower.transfer(msg.value);

        return (200, transaction_counter);
    }

    function view_transactions(uint256 _t_c) public returns (string memory) {
        return Processed_Transactions[_t_c].lender_reg_id;
    }

    function make_payouts(uint256 transaction_no, uint256 _amt)
        public
        payable
        returns (uint256, uint256)
    {
        bool flag = false;
        if (_amt == Processed_Transactions[transaction_no].amt_due) {
            flag = true;
            // liquidate collateral and payout to the borrower
            // case of borrower returning the loan amount with interest
        }
        //Tranfer Money into Lenderer's Account
        address payable l_acc = Processed_Transactions[transaction_no].lender;
        l_acc.transfer(msg.value);
        // IF Full Amount tranfered,change transaction state to Paid
        Processed_Transactions[transaction_no].Loan_Paid = flag;
        uint256 amt_left = Processed_Transactions[transaction_no].amt_due -
            _amt;
        Processed_Transactions[transaction_no].amt_due = amt_left;
        Processed_Transactions[transaction_no].collateral_liquidated = false;

        // Create a Payment Record
        payments_counter += 1;
        Payouts[payments_counter] = Payments(
            Processed_Transactions[transaction_no].borrower,
            Processed_Transactions[transaction_no].lender,
            msg.value,
            transaction_no,
            flag,
            amt_left,
            payments_counter
        );
        return (200, payments_counter);
    }

    function borrower_payout(uint256 t_id, uint256 amt)
        public
        payable
        returns (uint256, uint256)
    {
        // case where borrower returns the loan amount with interest
        address payable b_acc = Processed_Transactions[t_id].borrower;
        b_acc.transfer(msg.value);
        liquidated_payouts += 1;
        wallet_payouts[liquidated_payouts] = Liquidated_Payouts(
            b_acc,
            amt,
            false,
            true,
            t_id,
            liquidated_payouts
        );

        return (200, 1);
    }

    function liquidate_collateral(uint256 t_id, uint256 amt)
        public
        payable
        returns (uint256, uint256)
    {
        // Liquidate collateral and transfer the amount into the lenderer's account
        // Case where  borrower defaults
        address payable acc = Processed_Transactions[t_id].lender;
        Processed_Transactions[t_id].Loan_Paid = false;
        acc.transfer(msg.value);
        liquidated_payouts += 1;
        wallet_payouts[liquidated_payouts] = Liquidated_Payouts(
            acc,
            amt,
            false,
            true,
            t_id,
            liquidated_payouts
        );

        return (200, 1);
    }
}
