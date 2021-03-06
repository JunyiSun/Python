"""Assignment 1 - Grocery Store Simulation (Task 3)

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from container import PriorityQueue
from store import GroceryStore
from event import create_event_list, JoinLine, FinishCheckOut


class GroceryStoreSimulation:
    """A Grocery Store simulation.

    This is the class which is responsible for setting up and running a
    simulation.
    The API is given to you: your main task is to implement the two methods
    according to their docstrings.

    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.

    This is the entry point into your program, and in particular is used for
    auto testing purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    """
    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    # @type _store: GroceryStore
    #     The grocery store associated with the simulation.

    def __init__(self, store_file):
        """Initialize a GroceryStoreSimulation from a file.

        @type store_file: str
            A file containing the configuration of the grocery store.
        @rtype: None
        """
        self._events = PriorityQueue()
        self._store = GroceryStore(store_file)

    def run(self, event_file):
        """Run the simulation on the events stored in <event_file>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.

        @type self: GroceryStoreSimulation
        @type event_file: str
            A filename referring to a raw list of events.
            Precondition: the event file is a valid list of events.
        @rtype: dict[str, int]
        """
        # Initialize statistics
        stats = {
            'num_customers': 0,
            'total_time': 0,
            'max_wait': -1
        }

        initial_events = create_event_list(event_file)

        for i in range(len(initial_events)):
            self._events.add(initial_events[i])
            if type(initial_events[i]) == JoinLine:
                stats['num_customers'] += 1

                # THE FOLLOWING CODE MAY SHOW SOME WARNINGS.
                # (IF NOT, PLEASE IGNORE THIS COMMENT)
                # PROFESSOR LIU TOLD ME THAT THESE WARNINGS ARE PROBLEMS
                # WITH PyCharm ITSELF. SINCE WE ARE NOT ALLOWED TO CHANGE
                # THE INTERFACE, PROF SAID WE CAN JUST IGNORE THEM. THANK YOU.

        while not self._events.is_empty():
            event = self._events.remove()
            spawned_events = event.do(self._store)
            stats['total_time'] = event.timestamp
            # Calculate max_wait
            if type(event) == FinishCheckOut:
                end_time = event.timestamp
                customer_name = event.name
                for u in range(len(initial_events)):
                    if type(initial_events[u]) == JoinLine:
                        temp = initial_events[u]
                        if customer_name == temp.name:
                            start_time = temp.timestamp
                            waited_time = end_time - start_time
                            if waited_time > stats['max_wait']:
                                stats['max_wait'] = waited_time

            if spawned_events is not None:
                for j in range(len(spawned_events)):
                    self._events.add(spawned_events[j])
        return stats


if __name__ == '__main__':
    sim = GroceryStoreSimulation('config1.json')
    final_stats = sim.run('events1.txt')
    print(final_stats)
