def ungroup_elements(elements):
    """
    Iterate through json version of <elements> tags convert JSON structure to key,value pairs

    <elements>
        <element group="wind" name="wind_speed" orig-name="011012" uom="m/s" value="0.0">
            <qualifier group="element" name="statistical_significance" uom="unitless" value="average" />
            <qualifier group="element" name="time_displacement" uom="min" value="-2" />
            <qualifier group="element" name="time_duration" uom="min" value="2" />
            <qualifier group="element" name="vertical_displacement" uom="m" value="10" />
        </element>
    </elements>

    """

    results = {}
    for element in elements:
        results[element["@name"]] = element["@value"]

        if "qualifier" in element:
            # needed b/c xmltodict could make 'qualifiers' an array
            # if > 1 elements otherwise a dictionary
            if not isinstance(element["qualifier"], list):
                qualifiers = [element["qualifier"]]

            # there can be multiple qualifiers
            for qualifier in qualifiers:
                results[f"{element['@name']}_{qualifier['@name']}"] = qualifier[
                    "@value"
                ]
    return results
