from pymongo.database import Database
from pymongo.command_cursor import CommandCursor
from reportes.mongo_data import get_db


def get_reports(
    query: dict | None = None,
    db: Database = get_db(),
    collection: str = "reportes",
) -> CommandCursor:
    # reports = db[collection].find(filter=query, limit=100)

    pipeline = [
        {
            "$group": {
                "_id": {"E": "$disease", "B": "$barrio", "M": "$municipio"},
                "casos_E_por_lugar": {"$sum": 1},
            }
        },
        {
            "$project": {
                "disease": "$_id.E",
                "municipio": "$_id.M",
                "barrio": "$_id.B",
                "casos": "$casos_E_por_lugar",
            }
        },
        {"$sort": {"disease": 1, "casos": -1, "municipio": 1, "barrio": 1}},
    ]
    if query:
        pipeline = [{"$match": query}] + pipeline

    return db[collection].aggregate(pipeline)


def get_pipeline():
    pass


class Aggregate:
    def __init__(self) -> None:
        self.match: dict = None
        self.group: dict = None
        self.stage_n: list[dict] = []

    def setMatch(self, match_stage: dict):
        self.match = match_stage

    def setGroup(self, group_stage: dict):
        self.match = group_stage

    def setStage(self, stage: dict):
        self.stage_n.append(stage)


class QueryBuilder:
    def __init__(self) -> None:
        self.aggregate = Aggregate()

    def addMatch(self, stage: dict | None):
        if stage:
            self.aggregate.setMatch(stage)
        return self

    def addGroup(self, stage: dict | None):
        if stage:
            self.aggregate.setMatch(stage)
        return self

    def addStage(self, stage: dict | None):
        if stage:
            self.aggregate.setStage(stage)
        return self

    def build(self):
        result = []
        if self.aggregate:
            if self.aggregate.match:
                result.append(self.aggregate.match)
            if self.aggregate.group:
                result.append(self.aggregate.group)
            for stage in self.aggregate.stage_n:
                result.append(stage)
        return result
