from result import Ok, Err
from protector.rules.rule import Rule


class RuleChecker(Rule):
    def __init__(self):
        # Todo: Make this configurable from config file
        self.max_duration = 20

    @staticmethod
    def description():
        return "Prevent lengthy queries"

    @staticmethod
    def reason():
        return ["Such queries can bring down the time series database",
                "usually performing long and inefficient scans or aggregations"]

    def check(self, query):
        """
        :param query OpenTSDBQuery
        """
        stats = query.get_stats()
        if stats:

            duration = int(stats.get('duration', 0))
            if self.max_duration <= duration:
                return Err("Query duration exceeded: {}s Limit: {}s".format(duration, self.max_duration))
        return Ok(True)