from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess


def test_null_io():
    p = AtlasProcess(name="test", typeName="Process", qualified_name="test",
                     inputs=None, outputs=None
                     )

    assert(p.attributes["inputs"] is None)
    assert(p.attributes["outputs"] is None)

    d = p.to_json()
    assert(d["attributes"]["inputs"] is None)
    assert(d["attributes"]["outputs"] is None)


def test_setting_mixed():
    e1 = AtlasEntity(name="e1", typeName="DataSet",
                     qualified_name="e1", guid=-1)
    e2 = AtlasEntity(name="e2", typeName="DataSet",
                     qualified_name="e2", guid=-2)
    p = AtlasProcess(name="test", typeName="Process", qualified_name="test",
                     inputs=[e1], outputs=[e2.to_json(minimum=True)]
                     )

    assert(len(p.attributes["inputs"]) == 1)
    assert(len(p.attributes["outputs"]) == 1)

    assert(isinstance(p.attributes["inputs"][0], dict))
    assert(isinstance(p.attributes["outputs"][0], dict))
    # Should only have the minimum attributes necessary (3)
    assert(all (len(v) ==3 for v in p.attributes["inputs"]))
    assert(all (len(v) ==3 for v in p.attributes["outputs"]))

def test_adding_later():
    e1 = AtlasEntity(name="e1", typeName="DataSet",
                     qualified_name="e1", guid=-1)
    e2 = AtlasEntity(name="e2", typeName="DataSet",
                     qualified_name="e2", guid=-2)
    e3 = AtlasEntity(name="e3", typeName="DataSet",
                     qualified_name="e3", guid=-2)
    p = AtlasProcess(name="test", typeName="Process", qualified_name="test",
                    inputs=[], outputs=[]
                    )
    p.addInput(e1)
    p.addOutput(e2, e3.to_json(minimum=True))

    assert(len(p.inputs) == 1)
    assert(isinstance(p.attributes["inputs"][0], dict))
    assert(len(p.inputs) == 1)
    assert(all( [isinstance(e, dict) for e in p.attributes["inputs"]]))
    # Should only have the minimum attributes necessary (3)
    assert(all (len(v) ==3 for v in p.attributes["inputs"]))
    assert(all (len(v) ==3 for v in p.attributes["outputs"]))

def test_process_from_json():
    input_proc = {
      "typeName": "Process",
      "attributes": {
        "owner": None,
        "replicatedTo": None,
        "replicatedFrom": None,
        "qualifiedName": "testEntity",
        "name": "testEntity",
        "description": None,
        "inputs":[{"guid":"123"}],
        "outputs":[{"guid":"456"}]
      },
      "guid": "f3a2390d-f300-487e-8756-b27767e540f0",
      "status": "ACTIVE",
      "relationshipAttributes": {
        "schema": [],
        "inputToProcesses": [],
        "children": [],
        "attachedSchema": [],
        "meanings": [],
        "outputFromProcesses": []
      }
    }
    ap = AtlasProcess.from_json(input_proc)

    assert(ap.qualifiedName == input_proc["attributes"]["qualifiedName"])
    assert(ap.name == input_proc["attributes"]["name"])
    assert(ap.typeName == input_proc["typeName"])
    assert(ap.inputs == input_proc["attributes"]["inputs"])
    assert(ap.outputs == input_proc["attributes"]["outputs"])
