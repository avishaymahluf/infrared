---
plugin_type: test
subparsers:
    coverage:
        description: Collection of overcloud configuration tasks
        include_groups: ["Ansible options", "Inventory", "Common options", "Answers file"]
        groups:
            - title: Tasks Control
              options:
                  activate:
                      type: Bool
                      default: no
                      help: Install the coverage

                  collect:
                      type: Bool
                      default: no
                      help: Aggregate covereage and copy to the first controller

                  report:
                      type: Bool
                      default: no
                      help: Generate reports
