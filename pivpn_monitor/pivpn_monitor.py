# -*- coding: utf-8 -*-
import time

import pivpn_monitor.configuration.config as cc


"""Main module."""
def main():
    config = cc.load_configuration("pivpn_monitor.cfg", ".env")
    monitors = config['monitors']
    actions = config['actions']

    while True:
        time.sleep(60)
        for monitor_name, monitor in monitors.items():
            print("checking monitor: {}".format(monitor_name))
            events = monitor.run()

            for event in events:
                print("found event: {}".format(event))

                for action_name, action in actions.items():
                    print("firing action {}".format(action_name))

                    action.act(event)


