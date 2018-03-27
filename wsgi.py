import json
from datetime import datetime, timezone
import markdown
from flask import Flask
from flask import request
from flask import Markup

application = Flask(__name__)
lastEchoParameters = []


@application.route("/")
def home():
    return 'GET or POST /apifeed?DemoSize={the total size you want}&PageSize={PageSize}&CurrentPage={CurrentPage}'


@application.route("/apifeed", methods=['GET', 'POST'])
def apifeed():
    parameters = {}
    if request.args is not None:
        parameters.update(request.args.to_dict())
    if request.json is not None:
        parameters.update(request.json)
    if request.form is not None:
        parameters.update(request.form.to_dict())

    print(parameters)
    # return json.dumps(parameters)

    page_size = int(parameters['PageSize'])
    current_page = int(parameters['CurrentPage'])
    total = int(parameters['DemoSize'])

    def create_allergy(name, result, note, date_recorded):
        return {"Allergen": name, "AllergyResult": result, "Note": note, "DateRecorded": date_recorded}

    # allergies = [create_allergy("Pollen", "Sneezes", "a note", "23/05/2016"),
    #              create_allergy("Penicillin", "Death", "a note", "21/05/2016"),
    #              create_allergy("Dust", "Immediate Death", "a note", "20/05/2016"),
    #              create_allergy("Cats", "Loss of limb", "a note", "24/05/2016")]

    first_idx = (current_page - 1) * page_size
    last_idx = first_idx + page_size
    if last_idx > total - 1: last_idx = total

    allergies = []
    for i in range(first_idx, last_idx):
        allergies.append(create_allergy('test, %d' % i, "Sneezes", "All API parameters: %s" % str(parameters), "23/05/2016"))

    v = {
        "Allergies": allergies,
        "RecordSetPageSize": page_size,
        "RecordSetCurrentPage": current_page,
        "RecordSetTotalResults": total
    }
    return json.dumps(v)


@application.route("/echo", methods=['GET', 'POST'])
def echo():
    parameters = {}
    if request.args is not None:
        parameters.update(request.args.to_dict())
    if request.json is not None:
        parameters.update(request.json)
    if request.form is not None:
        parameters.update(request.form.to_dict())

    print(parameters)

    if len(lastEchoParameters) > 20:
        del lastEchoParameters[0]
    lastEchoParameters.append([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), parameters])

    return json.dumps(parameters)


@application.route("/lastEcho")
def lastEcho():
    # return json.dumps(application.lastEchoParameters)
    content = """
#Last parameters used by /echo
___


    """
    if len(lastEchoParameters) > 0:
        content += """

|  ID  | Date             | Parameters              |
| ---- | ---------------- | ----------------------- |
"""
        for i, [dt, parameters] in enumerate(lastEchoParameters):
            content += "| %d. | %s | `%s` |\n" % (i, dt, json.dumps(parameters))
    else:
        content += '\n> no item found\n'

    content = Markup(markdown.markdown(content, extensions=['markdown.extensions.tables']))
    return content


if __name__ == "__main__":
    application.run()
