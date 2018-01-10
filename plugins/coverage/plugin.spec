---
plugin_type: test
subparsers:
    coverage:
        description: Collection of overcloud configuration tasks
        include_groups: ["Ansible options", "Inventory", "Common options", "Answers file"]
        groups:
            - title: Activate
              options:
                  activate:
                      type: Bool
                      default: no
                      help: Install the coverage
                  dfg:
                      type: Value
                      help: Openstack components packages of code to be measured
                      default: all

            - title: Collect
              options:
                  collect:
                      type: Bool
                      default: no
                      help: Aggregate covereage and copy to the first controller

            - title: Report
              options:
                  report:
                      type: Bool
                      default: no
                      help: Generate reports
