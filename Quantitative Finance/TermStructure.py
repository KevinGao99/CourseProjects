import matplotlib.pylab as plt
import seaborn as sns

from bonds.bill import Bill
from bonds.bond import Bond
from bonds.read_bond_info import read_bills_from_file, read_bonds_from_file
from term_structure.term_structure import TermStructure


def main():
    # read bonds and bills

    #
    bills_data_file = "data/bills.txt"
    bonds_data_file = "data/bonds.txt"
    bonds = []

    # read bills from a file and instantiate bond objects
    bill_instruments = read_bills_from_file(bills_data_file)
    for bill_instrument in bill_instruments:
        bill = Bill(bill_instrument[0], bill_instrument[1], bill_instrument[2], bill_instrument[3])
        bill.set_price(float(bill_instrument[3]))
        bonds.append(bill)

    # read bonds from a file and instantiate bond objects
    bond_instruments = read_bonds_from_file(bonds_data_file)
    for bond_instrument in bond_instruments:
        bond = Bond(bond_instrument[0], bond_instrument[1], bond_instrument[2], bond_instrument[3],
                    bond_instrument[4])
        bond.set_price(float(bond_instrument[5]))
        bonds.append(bond)
    
    bonds2 = []
    for bill_instrument in bill_instruments:
        bill = Bill(bill_instrument[0], bill_instrument[1], bill_instrument[2], bill_instrument[3])
        bill.set_price(float(bill_instrument[3]))
        bonds2.append(bill)
    
    for bond_instrument in bond_instruments:
        bond = Bond(bond_instrument[0], bond_instrument[1], bond_instrument[2], bond_instrument[3],
                    4.0)
        bond.set_price(float(bond_instrument[5]))
        bonds2.append(bond)

    # compute yield-to-maturities for bonds
    #
    tenors_from_bonds, ytm_from_bonds = [], []
    for bond in bonds:
        tenors_from_bonds.append(bond.get_tenor_in_years())
        ytm_from_bonds.append(bond.compute_ytm())

    # print bonds
    #
    print(f'Name\tCoupon\tIssueDate\tMaturityDate\tPrice\t\tYTM')
    for bond in bonds:
        print(f'{bond.get_name()}\t{bond.get_coupon():10.4f}' +
              f'\t{bond.get_issue_date()}\t{bond.get_maturity_date()}' +
              f'\t{bond.get_price():10.4f}\t{bond.compute_ytm():10.4f}')
    
    for bond in bonds2:
        print(f'{bond.get_name()}\t{bond.get_coupon():10.4f}' +
              f'\t{bond.get_issue_date()}\t{bond.get_maturity_date()}' +
              f'\t{bond.get_price():10.4f}\t{bond.compute_ytm():10.4f}')

    # build the term strucure
    #
    forward_rate_tenors = {'6M': (60, 0.50, bonds), '3M': (120, 0.25, bonds2)}
    for forward_rate_tenor in forward_rate_tenors.keys():
        tenor_count = forward_rate_tenors[forward_rate_tenor][0]
        time_period = forward_rate_tenors[forward_rate_tenor][1]
        bonds_candidate = forward_rate_tenors[forward_rate_tenor][2]

        term_structure = TermStructure(tenor_count)
        term_structure.set_bonds(bonds_candidate)
        term_structure.compute_spot_rates()
        term_structure.compute_discount_factors()
        term_structure.compute_forward_rates()

        tenors = [(i + 1) * time_period for i in range(tenor_count)]
        spot_rates, forward_rates, discount_factors = [], [], []
        for i in range(tenor_count):
            spot_rates.append(term_structure.get_spot_rate(i))
            forward_rates.append(term_structure.get_forward_rate(i))
            discount_factors.append(term_structure.get_discount_factor(i))

        print(f'Tenor\tSpot Rate\tDiscount Factor\tForward {forward_rate_tenor} Rate')
        for i in range(tenor_count):
            tenor = (i + 1) * time_period
            print(f'{tenor:4.2f}y\t{term_structure.get_spot_rate(i):9.4f}' +
                  f'\t{term_structure.get_discount_factor(i):10.4f}' +
                  f'\t{term_structure.get_forward_rate(i):14.4f}')

        # plot spot and forward rates
        sns.set()
        fig, ax = plt.subplots()
        ax.plot(tenors, spot_rates, linewidth=2, label='Spot', color='blue')
        ax.plot(tenors[:-1], forward_rates[:-1], linewidth=2, label='Forward', color='orange')
        ax.xaxis.set_major_locator(plt.MaxNLocator(10))
        ax.set_xlabel('Tenor (yrs)')
        ax.set_ylabel('Rate')
        ax.set_title(f'Spot and Forward {forward_rate_tenor} Rates')
        ax.legend(loc='best', fontsize='x-small')
        plt.show()

        # plot discount factors
        fig, ax = plt.subplots()
        ax.plot(tenors, discount_factors, linewidth=2, label='Discount Factor', color='blue')
        ax.xaxis.set_major_locator(plt.MaxNLocator(10))
        ax.set_xlabel('Tenor (yrs)')
        ax.set_ylabel('Discount Factor')
        ax.set_title(f'Discount Factors')
        ax.legend(loc='best', fontsize='x-small')
        plt.show()




if __name__ == '__main__':
    main()
