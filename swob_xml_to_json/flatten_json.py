from swob_xml_to_json.ungroup_elements import ungroup_elements


def flatten_json(data):
    """
    Flattens the json structure that is created by xmltodict to make
    it more suitable for displaying as tabular data
    """
    # 'results' and 'metadata' stored at different paths in the XML.
    # results & metadata are dictionaries
    results = ungroup_elements(
        data["om:ObservationCollection"]["om:member"]["om:Observation"]["om:result"][
            "elements"
        ]["element"]
    )

    metadata = ungroup_elements(
        data["om:ObservationCollection"]["om:member"]["om:Observation"]["om:metadata"][
            "set"
        ]["identification-elements"]["element"]
    )

    # samplingTime also recorded as date_tm?
    sampling_time = data["om:ObservationCollection"]["om:member"]["om:Observation"][
        "om:samplingTime"
    ]["gml:TimeInstant"]["gml:timePosition"]

    result_time = data["om:ObservationCollection"]["om:member"]["om:Observation"][
        "om:resultTime"
    ]["gml:TimeInstant"]["gml:timePosition"]

    # combine all of these
    record = {
        "sampling_time": sampling_time,
        "result_time": result_time,
        "metadata":metadata,
        "results":results,
    }

    return record