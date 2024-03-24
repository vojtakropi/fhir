checkup_string = '''{
  "resourceType" : "Observation",
  "id" : "f005",
  "text" : {
    "string" : "%s"
  },
  "identifier" : [{
    "use" : "official",
    "system" : "http://www.bmc.nl/zorgportal/identifiers/observations",
    "value" : "6327"
  }],
  "status" : "%s",
  "code" : {
    "coding" : [{
      "system" : "http://loinc.org",
      "code" : "718-7",
      "display" : "Hemoglobin [Mass/volume] in Blood"
    }]
  },
  "subject" : {
    "reference" : "%s",
    "display" : "%s"
  },
  "effectiveDateTime" : "%s",
  "issued" : "%s",
  "performer" : [{
    "reference" : "%s",
    "display" : "%s"
  }],
  "valueQuantity" : {
    "value" : "%s",
    "unit" : "g/dl",
    "system" : "http://unitsofmeasure.org",
    "code" : "g/dL"
  },
  "interpretation" : [{
    "coding" : [{
      "system" : "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
      "code" : "%s",
      "display" : "%s"
    }]
  }],
  "referenceRange" : [{
    "low" : {
      "value" : "7.5",
      "unit" : "g/dl",
      "system" : "http://unitsofmeasure.org",
      "code" : "g/dL"
    },
    "high" : {
      "value" : "10",
      "unit" : "g/dl",
      "system" : "http://unitsofmeasure.org",
      "code" : "g/dL"
    }
  }]
}'''


def create_json(values):
    jsonstring = checkup_string % (values["text_field"], values["status"], values["subject_id"],
                                   values["subject_name"],
                                   values["efective_date"],
                                   values["issued_date"], values["performer_reference"],
                                   values["performer_display"], values["value"],
                                   values["interpretation_code"], values["interpretation_display"])

    return jsonstring
