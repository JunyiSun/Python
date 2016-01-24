"""Assignment 1 - Grocery Store Models (Task 1)

This file should contain all of the classes necessary to model the entities
in a grocery store.
"""
# This module is used to read in the data from a json configuration file.
import json


class GroceryStore:
    """A grocery store.

    A grocery store should contain customers and checkout lines.

    === Private Attributes ===
    @type _capacity: int
        The the maximum number of customers allowed in each line.
        All lines have the same capacity.

    @type _line_list: list
        A list of lines for each checkout counter.
    """
    def __init__(self, filename):
        """Initialize a GroceryStore from a configuration file <filename>.

        @type filename: str
            The name of the file containing the configuration for the
            grocery store.
        @rtype: None
        """
        with open(filename, 'r') as file:
            config = json.load(file)
        # <config> is now a dictionary with the keys 'cashier_count',
        # 'express_count', 'self_serve_count', and 'line_capacity'.
        self._capacity = config['line_capacity']
        self._line_list = []

        cashier_num = config['cashier_count']
        express_num = config['express_count']
        self_serve_num = config['self_serve_count']
        total_num = cashier_num+express_num + self_serve_num

        for count_id in range(total_num):
            if count_id < cashier_num:
                count = Cashier()
                self._line_list.append(count)
            elif cashier_num <= count_id < cashier_num + express_num:
                count = Express()
                self._line_list.append(count)
            else:
                count = SelfServe()
                self._line_list.append(count)

    def line_is_empty(self, index):
        """Indicate if a line is empty by giving the index of the line.

        @type index: int
        @rtype: bool
            Return True if is empty.
        """
        return (len(self._line_list[index].customer_list)-1) == 0

    def join_line(self, name, num_items):
        """Choose an open line that the customer should join.
        Customers join the line that has fewest people.
        However, customers can only join the express line if he/she
        has less than 8 items. The number of customers in the line
        should not be more than line capacity.

        @type name: str
        @type num_items: int
        @rtype: int
            Return the index of the chosen line.
        """
        chosen_line_index = 0
        shortest_length = self._capacity
        for line_index in range(len(self._line_list)):
            if self._line_list[line_index].open:
                sublist = self._line_list[line_index].customer_list
                if num_items < 8:
                    if len(sublist) < shortest_length:
                        shortest_length = len(sublist)
                        chosen_line_index = line_index
                else:
                    if len(sublist) < shortest_length:
                        if not type(self._line_list[line_index]) == Express:
                            shortest_length = len(sublist)
                            chosen_line_index = line_index

        self._line_list[chosen_line_index].add_customer(name, num_items)
        return chosen_line_index

    def spend_time(self, name, num_items):
        """Get the time that a customer will spend during the checkout process.
        Time varies depending on which line the customer joins and the number
        of items the customer has.

        @type name: str
        @type num_items: int
        @rtype: int
            The spent time during checkout.
        """
        time = 0
        for i in range(len(self._line_list)):
            sub_list = self._line_list[i].customer_list
            for j in range(len(sub_list)):
                if name == sub_list[j].name:
                    time = self._line_list[i].checkout_time(num_items)
        return time

    def find_next_customer(self, name):
        """Determine whether there existing next customer in the line given the
        customer's name who is currently checking out. If there is no next
        customer, return a boolean false, otherwise return the Customer object.

        @type name: str
        @rtype: bool
           Return false the customer is the last customer in the line.
           Return true if there are more customers in the line.
        """
        for i in range(len(self._line_list)):
            sub_list = self._line_list[i].customer_list
            for j in range(len(sub_list)):
                if name == sub_list[j].name:
                    if j == len(sub_list) - 1:
                        return False
                    else:
                        return True

    def find_next_customer_name(self, name):
        """Find the name of the next customer given current customer name.

        @type name: str
        @rtype: str
        """
        for i in range(len(self._line_list)):
            sub_list = self._line_list[i].customer_list
            for j in range(len(sub_list)):
                if name == sub_list[j].name:
                    return self._line_list[i].customer_list[j+1].name

    def find_next_customer_items(self, name):
        """Find the number of items the next customer has
        given current customer name.

        @type name: str
        @rtype: int
        """
        for i in range(len(self._line_list)):
            sub_list = self._line_list[i].customer_list
            for j in range(len(sub_list)):
                if name == sub_list[j].name:
                    return self._line_list[i].customer_list[j+1].items

    def leave_store(self, line_index):
        """Remove the customer from list after the customer has checked out
        from a specific line.

        @type line_index: int
            The index of the line where the customer checked out
        @rtype: None
        """
        self._line_list[line_index].remove_customer(0)

    def close_line(self, line_index):
        """Close the line given its index.

        @type line_index: int
        @rtype: None
        """
        self._line_list[line_index].open = False

    def get_customer_list(self, line_index):
        """Get the list of customer line by its index.

        @type line_index: int
        @rtype: list

        """
        return self._line_list[line_index].customer_list

    def leave_line(self, name):
        """To remove a customer from a line after the line is closed

        @type name: str
        @rtype: None
        """
        for i in range(len(self._line_list)):
            sublist = self._line_list[i].customer_list
            for j in range(len(sublist)):
                if name == sublist[j].name:
                    self._line_list[i].remove_customer(j)


class Cashier:
    """A cashier count in the store.
    """

    # === Public Attributes ===
    # @type customer_list: list
    #     A list of customers for the cashier counter.
    #
    # @type open: bool
    #     Determine whether the counter is closed or open.

    def __init__(self):
        """Initialize the status of cashier count.

        @type self: Cashier
        @rtype: None
        """
        self.customer_list = []
        self.open = True

    @staticmethod
    def checkout_time(items):
        """Calculate the time a customer need to check out by a cashier count
        with certain number of items.

        @type items: int
        @rtype: int
            The time need during checkout.
        """
        time = items + 7
        return time

    def add_customer(self, name, items):
        """Add a customer in the line to cashier given the number of items
        and his/her name.

        @type name:  str
        @type items: int
        @rtype: None
        """
        new_customer = Customer(name, items)
        self.customer_list.append(new_customer)

    def remove_customer(self, index):
        """Remove a customer from the cashier line given the index of the line.

        @type index: int
            The index of the cashier line
        @rtype: None
        """
        self.customer_list.pop(index)


class Express:
    """A express count in the store.
    """

    # === Public Attributes ===
    # @type customer_list: list
    #     A list of customers for the express counter.
    #
    # @type open: bool
    #     Determine whether the counter is closed or open.

    def __init__(self):
        """Initialize the status of express count.

        @type self: Express
        @rtype: None
        """
        self.customer_list = []
        self.open = True

    @staticmethod
    def checkout_time(items):
        """Calculate the time a customer need to check out by an express count
        with certain number of items.

        @type items: int
        @rtype: int
            The time need during checkout.
        """
        time = items + 4
        return time

    def add_customer(self, name, items):
        """Add a customer in the line to express count given the number
        of items and his/her name.

        @type name:  str
        @type items: int
        @rtype: None
        """
        new_customer = Customer(name, items)
        self.customer_list.append(new_customer)

    def remove_customer(self, index):
        """Remove a customer from the express line given the index of the line.

        @type index: int
            The index of the express line
        @rtype: None
        """
        self.customer_list.pop(index)


class SelfServe:
    """A express count in the store.
    """

    # === Public Attributes ===
    # @type customer_list: list
    #     A list of customers for the self-serve counter.
    #
    # @type open: bool
    #     Determine whether the counter is closed or open.

    def __init__(self):
        """Initialize the status of self-serve count.

        @type self: SelfServe
        @rtype: None
        """
        self.customer_list = []
        self.open = True

    @staticmethod
    def checkout_time(items):
        """Calculate the time a customer need to check out by a self-serve
         count with certain number of items.

        @type items: int
        @rtype: int
            The time need during checkout.
        """
        time = 2 * items + 1
        return time

    def add_customer(self, name, items):
        """Add a customer in the line to self-serve count given the number
        of items and his/her name.

        @type name:  str
        @type items: int
        @rtype: None
        """
        new_customer = Customer(name, items)
        self.customer_list.append(new_customer)

    def remove_customer(self, index):
        """Remove a customer from the self-serve line given the
        index of the line.

        @type index: int
            The index of the self-serve line
        @rtype: None
        """
        self.customer_list.pop(index)


class Customer:
    """A Customer in the store.
    """
    # === Public Attributes ===
    # @type name: str
    #     The name of customers.
    #
    # @type items: int
    #     The number of items the customer has.

    def __init__(self, name, items):
        """Initialize the information of a customer with name and num of items.

        @type self: Customer
        @type name: str
        @type items: int
        @rtype: None
        """
        self.name = name
        self.items = items


if __name__ == '__main__':
    store = GroceryStore('config.json')
