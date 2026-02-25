"""Governance module: policy, auditing and compliance helpers.
"""

class Governance:
    def __init__(self):
        self.policies = {}

    def register_policy(self, name, policy_callable):
        self.policies[name] = policy_callable

    def evaluate(self, name, context):
        policy = self.policies.get(name)
        if not policy:
            return True
        return policy(context)
