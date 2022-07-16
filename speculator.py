import yaml
from urllib import request
import json

results = {}


def versionYaml(task):
    x = request.urlopen(task["sourceVersion"])
    releases = yaml.load(x, Loader=yaml.FullLoader)
    version = list(
        map(
            lambda release: release[task["lookup"]["returnValueFromKey"]],
            filter(
                lambda release: release[task["lookup"]["key"]]
                == task["lookup"]["value"],
                releases,
            ),
        )
    )[0]
    return dict({task["label"]: version})


with open("speculator.yaml", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    list(
        map(
            lambda result: results.update(result),
            map(
                versionYaml,
                filter(lambda task: task["schemaType"] == "yaml", data),
            ),
        )
    )

with open("results.json", "w") as outfile:
    json.dump(results, outfile)
